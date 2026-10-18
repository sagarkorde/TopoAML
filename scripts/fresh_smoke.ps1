$ErrorActionPreference = 'Stop'
python -m venv .venv-smoke
if ($LASTEXITCODE -ne 0) { throw 'Cannot create isolated smoke environment' }
& .\.venv-smoke\Scripts\python.exe -m pip install -r requirements-core.txt
if ($LASTEXITCODE -ne 0) { throw 'Cannot install core dependencies' }
& .\.venv-smoke\Scripts\python.exe -m pytest tests/test_topology.py tests/test_temporal.py tests/test_evaluation.py tests/test_provenance.py --junitxml=results/fresh_core_tests.xml -q
if ($LASTEXITCODE -ne 0) { throw 'Fresh core smoke failed' }
