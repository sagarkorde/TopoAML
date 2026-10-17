"""Resolve proposal DOI leads against Crossref; metadata match is not claim verification."""
import csv
import json
import re
from pathlib import Path
import requests

ROOT = Path(__file__).resolve().parents[1]

def main():
    text = (ROOT / "docs/proposal_extracted.txt").read_text(encoding="utf-8")
    dois = list(dict.fromkeys(re.findall(r"10\.\d{4,9}/[^\s]+", text)))
    cache = ROOT / "literature/crossref"
    cache.mkdir(exist_ok=True)
    rows, bib = [], []
    for i, doi in enumerate(dois, 1):
        doi = doi.rstrip(".,;")
        path = cache / f"{i:02}.json"
        row = {"id": i, "doi": doi, "status": "unresolved", "title": "", "authors": "", "venue": "", "year": "", "volume": "", "pages": "", "claim_support": "not assessed", "scopus_status": "not independently verified"}
        try:
            if path.exists():
                m = json.loads(path.read_text(encoding="utf-8"))
            else:
                r = requests.get(f"https://api.crossref.org/works/{doi}", timeout=30)
                r.raise_for_status()
                m = r.json()["message"]
                path.write_text(json.dumps(m, indent=2), encoding="utf-8")
            row.update(status="Crossref metadata resolved; lead comparison pending", title=m.get("title", [""])[0],
                       authors="; ".join(a.get("given", "") + " " + a.get("family", "") for a in m.get("author", [])),
                       venue=m.get("container-title", [""])[0], year=m.get("published", {}).get("date-parts", [[None]])[0][0],
                       volume=m.get("volume", ""), pages=m.get("page", m.get("article-number", "")))
            bib.append("@article{lead%d,\n  title={%s},\n  author={%s},\n  journal={%s},\n  year={%s},\n  doi={%s}\n}" % (i, row["title"], row["authors"].replace("; ", " and "), row["venue"], row["year"], doi))
        except Exception as e:
            row["status"] = str(e)
        rows.append(row)
        print(i, row["status"], flush=True)
    with (ROOT / "literature/doi_audit.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=rows[0]); w.writeheader(); w.writerows(rows)
    (ROOT / "literature/resolved_metadata.bib").write_text("\n\n".join(bib), encoding="utf-8")

if __name__ == "__main__":
    main()
