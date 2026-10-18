$ErrorActionPreference = 'Stop'
$steps = @('scripts/acquire.py','scripts/prepare.py','scripts/extract.py','scripts/train_tabular.py','scripts/train_graph.py','scripts/characterize.py','scripts/elliptic2.py','scripts/cases.py','scripts/method_figures.py','scripts/analyze.py','scripts/extended_analysis.py','scripts/build_research_docs.py','scripts/build_manuscript.py')
python -m pytest -q
if ($LASTEXITCODE -ne 0) { throw 'Mathematical/model checks failed' }
foreach ($step in $steps) {
    python $step
    if ($LASTEXITCODE -ne 0) { throw "Pipeline stopped at $step" }
}
