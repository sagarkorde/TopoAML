# TopoAML

**Persistent Homology-Guided Graph Learning for Leakage-Free Bitcoin Anti-Money Laundering**

Executable research implementation based on the supplied proposal. Results are empirical only where backed by files under `results/`. The protocol is historical **step-close** observation; coarse public timestamps do not establish transaction-time causality or historical label availability. No laundering inference follows from a graph cycle.

## Windows setup and execution

Python 3.10+; tested locally with the environment recorded in `results/environment.json`. CUDA is optional; PyTorch and PyG require compatible builds. Use a dedicated virtual environment for replication.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
python -m pytest -q
python scripts/acquire.py
python scripts/prepare.py
python scripts/extract.py
python scripts/train_tabular.py
python scripts/train_graph.py --epochs 15
python scripts/characterize.py
python scripts/elliptic2.py
python scripts/cases.py
python scripts/method_figures.py
python scripts/analyze.py
python scripts/extended_analysis.py
python scripts/build_manuscript.py
python scripts/submission_extras.py
```

Acquisition downloads approximately 702 MB and verifies upstream Git-LFS SHA256 values. Raw data, processed features and binary model checkpoints are excluded from Git. Acquisition and completed model runs are resume-safe; delete no inputs to restart. Interrupted graph runs currently restart from the beginning of that model, preserving its saved best checkpoint.

The source supports logistic regression, random forest, XGBoost, GraphSAGE, GAT, static Betti fusion, persistent feature concatenation and gated fusion. Standardization/imputation uses training data only, and thresholds/checkpoint selection use validation data only. The locked split is 1-30 / 31-39 / 40-49. Unknown labels stay distinct from licit labels and enter no supervised loss.

For sensitivity extraction: `python scripts/extract.py --radius 3 --max-nodes 32 --filtration weight`. These produce separate caches. `characterize.py` runs training-only descriptor sensitivity; it does not constitute predictive robustness under every configuration.

Review `docs/journal_assessment.md`, `docs/change_log.md`, `docs/hypotheses.md`, `docs/project_status.md` and `docs/requirements_traceability.csv` for scope, evidence and blockers. A submission-ready paper must not be claimed while experimental or publication gates remain unresolved. `scripts/fresh_smoke.ps1` recreates an isolated core environment; it passed 22 topology/temporal/evaluation tests. The primary environment passed all 28 tests, including graph forward/backward checks. This is not a full independent GPU experiment reproduction.

## GitHub publication

The private repository was created at https://github.com/sagarkorde/TopoAML through the existing signed-in browser. Git's existing credential manager permits pushes even though GitHub CLI is signed out. To push later validated changes:

```powershell
git push origin main
```

Do not publish raw dataset files. Elliptic2 has provider CC BY-NC-ND 4.0 terms; explicit redistribution permission for the Elliptic++ release has not been verified.

## Research integrity

Original prose and verified attribution are required. No promise is made about Turnitin similarity or AI classification, and no detector-evasion workflow is used. AI assistance must be accurately disclosed. Author names, affiliations, funding and conflicts must be supplied/confirmed by the authors before submission.
