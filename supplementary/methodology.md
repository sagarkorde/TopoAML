# Supplementary reproducibility notes

The main protocol is frozen in `configs/preregistered.json`. All paths below are repository-relative.

1. `scripts/acquire.py`: pin upstream commit, stream immutable CSVs, verify Git-LFS SHA256.
2. `scripts/prepare.py`: validate schema, counts, missingness, time coverage, edge references and DAG; freeze ID/time/class partitions.
3. `scripts/extract.py`: bounded historical radius-2 neighborhoods, structural/Betti/Rips features and per-target runtimes; cache atomic chunks.
4. `scripts/train_tabular.py`: fixed model settings, training-only imputation/scaling, validation-only thresholds, five seeds, saved predictions/checkpoints.
5. `scripts/train_graph.py`: reciprocal historical ego graphs, two message layers, original transaction fields plus target structural context, separate topology projection and fusion; validation AP selects the checkpoint.
6. `scripts/characterize.py`: training-only residual profiling, three radii/filtrations and edge-deletion sensitivity; measured extraction timing.
7. `scripts/elliptic2.py`: provider labeled-subgraph files, actual upstream file-order split, whole-subgraph S/P features and task-specific tabular baselines.
8. `scripts/cases.py`: first ten future target IDs, fixed edge deletion and genuine XGBoost contribution values; no outcome-driven case selection.
9. `scripts/analyze.py`: actual metric tables, seed summaries, primary paired step bootstrap and editable figures.

Missingness indicators are appended by the imputer; retained feature names are saved by the pipeline. Targets use class 1 as positive, class 2 as negative, class 3 as unknown on Elliptic++. Elliptic2 uses suspicious as positive and licit as negative. Scores cannot establish criminal conduct.

All label use is retrospective supervision. Dates at which investigators assigned the labels are unavailable. No online operational deployment claim follows from the experiment.
