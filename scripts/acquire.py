"""Acquire upstream transaction release using a pinned Git commit and LFS hashes."""
import hashlib
import json
from pathlib import Path
import requests

ROOT = Path(__file__).resolve().parents[1]
REPO = "git-disl/EllipticPlusPlus"

def main():
    raw = ROOT / "data/raw/ellipticpp"
    raw.mkdir(parents=True, exist_ok=True)
    manifest_path = ROOT / "data/manifests/acquisition.json"
    prior = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    commit = prior.get("commit")
    if not commit:
        r = requests.get(f"https://api.github.com/repos/{REPO}/commits/main", timeout=60)
        r.raise_for_status()
        commit = r.json()["sha"]
    manifest = {"source": f"https://github.com/{REPO}", "commit": commit,
                "license": "No explicit dataset license verified; do not redistribute raw data",
                "files": []}
    for name in ["txs_classes.csv", "txs_edgelist.csv", "txs_features.csv"]:
        pointer = requests.get(f"https://raw.githubusercontent.com/{REPO}/{commit}/Transactions%20Dataset/{name}", timeout=60)
        pointer.raise_for_status()
        text = pointer.text
        expected = text.split("oid sha256:")[1].split()[0] if "oid sha256:" in text else None
        url = f"https://media.githubusercontent.com/media/{REPO}/{commit}/Transactions%20Dataset/{name}"
        path = raw / name
        if not path.exists():
            print(f"Downloading {name}", flush=True)
            with requests.get(url, stream=True, timeout=(30, 120)) as response:
                response.raise_for_status()
                with path.with_suffix(".part").open("wb") as out:
                    for block in response.iter_content(1024 * 1024):
                        out.write(block)
            path.with_suffix(".part").replace(path)
        digest = hashlib.file_digest(path.open("rb"), "sha256").hexdigest()
        if expected and digest != expected:
            raise ValueError(f"Checksum mismatch: {name}")
        from datetime import datetime, timezone
        manifest["files"].append({"name": name, "sha256": digest, "bytes": path.stat().st_size,
                                   "url": url, "download_date": datetime.now(timezone.utc).isoformat()})
        manifest_path.write_text(json.dumps(manifest, indent=2))
        print(name, path.stat().st_size, digest, flush=True)

if __name__ == "__main__":
    main()
