# TOPOAML — MASTER PROMPT FOR COMPLETE RESEARCH IMPLEMENTATION AND JOURNAL MANUSCRIPT

## 0. PROJECT IDENTITY AND NON-NEGOTIABLE INSTRUCTIONS

You are acting as a multidisciplinary research implementation team with expertise in:

- Bitcoin transaction forensics and anti-money laundering.
- Algebraic topology, Betti numbers and persistent homology.
- Directed graph theory and temporal financial networks.
- Graph neural networks and topological deep learning.
- Scientific Python, PyTorch Geometric and large-scale data processing.
- Experimental methodology, statistical validation and reproducibility.
- Original research manuscript preparation for high-quality Scopus-indexed journals.

**Authoritative project document:** `TopoAML_Complete_Research_Proposal.docx`

Read the entire attached proposal before doing any development.

Treat it as the primary research specification. Preserve its title, six hypotheses (H1–H6), dataset plan, seven experiments (E1–E7), mathematical requirements and publication ethics.

Do not substitute the earlier BettiGraph proposal.

**Research title:**

"TopoAML: Persistent Homology-Guided Graph Learning for Leakage-Free Bitcoin Anti-Money Laundering"

**Existing repository:**

https://github.com/sagarkorde/BettiGraphs

**Initial publication target:**

https://www.sciencedirect.com/journal/nexus

**Development machine:**

- Windows 11
- Intel Core i9, 13th Generation
- 64 GB RAM
- NVIDIA RTX 4060, 8 GB VRAM

**Research status:** Pre-experimental. No results should be assumed.

Your assignment is not merely to explain the research. You must implement executable code, obtain and validate permissible data, execute experiments, analyze actual outputs, and prepare an evidence-based manuscript.

Never fabricate experiments, benchmark results, references, DOI numbers, execution logs or statistical significance.

Do not proceed from one major phase to the next without recording its completion status and unresolved blockers. However, continue autonomously whenever the next step can be completed without user input.

---

# PHASE 1 — READ, AUDIT AND LOCK THE RESEARCH SPECIFICATION

1. Read the complete TopoAML proposal.
2. Extract all requirements, hypotheses, equations, datasets, experiments and expected outputs.
3. Create `docs/research_specification.md`.
4. Create `docs/requirements_traceability.csv`, mapping every requirement to implementation files, experiment outputs and eventual manuscript sections.
5. Identify ambiguities, mathematical risks and infeasible assumptions.
6. Resolve technically justified ambiguities while retaining a change log.

Do not silently change the research questions or convert hypothesis statements into claims of demonstrated results.

## Journal suitability gate

Investigate whether the supplied Nexus URL represents the intended journal.

Verify its exact title, ISSN, publisher, aims and scope, submission requirements, indexing, current journal category and APC.

In particular, distinguish Energy Nexus from any differently named publication.

Determine whether a standalone Bitcoin AML paper is genuinely within scope.

If not, record a journal-scope mismatch and maintain a journal-neutral original research manuscript. Recommend academically suitable alternative Q1/Q2 Scopus outlets without falsely claiming that the requested journal accepts financial forensic research.

Do not change the research subject to energy applications merely to force journal compatibility.

For the eventual selected journal, verify current requirements rather than assuming an abstract limit, manuscript word count, figure count or reference count.

---

# PHASE 2 — NOVELTY AUDIT AND VERIFIED BIBLIOGRAPHY

Use the proposal's 40 references as **unverified working DOI leads**, not accepted bibliographic facts.

For each reference:

1. Resolve its DOI through an authoritative source.
2. Verify title, authors, journal, year, volume and page/article identifier.
3. Confirm journal-indexing information where accessible.
4. Identify whether it genuinely supports the proposed claim.
5. Record corrections, unsupported metadata or dead DOI links.
6. Exclude unreliable citations from the manuscript.

Extend the review through October 2026 using reputable literature sources.

Investigate specifically:

- Persistent homology for financial networks.
- Blockchain illicit-transaction detection.
- Elliptic and Elliptic++ benchmarks.
- Elliptic2 subgraph classification.
- Topological deep learning.
- Directed path homology.
- Leakage-free graph machine learning.
- Structural confounding in graph classification.
- GraphSAGE, GAT and topology-feature fusion.

Pay particular attention to prior persistent-homology-enhanced GAT methods, grounded persistent path homology and recent AML-specific graph learning methods.

Produce:

- `literature/verified_references.bib`
- `literature/doi_audit.csv`
- `literature/novelty_matrix.xlsx`
- `literature/research_gap.md`

Distinguish methodological novelty from a novel application and from improved evaluation discipline.

**Novelty gate:** Do not assume that adding β₀ and β₁ to a graph classifier constitutes a publishable mathematical contribution. Identify and test the actual contribution experimentally.

---

# PHASE 3 — RESEARCH QUESTIONS AND PRE-REGISTERED HYPOTHESES

Implement and evaluate the proposal's six hypotheses.

**H1 — Topological separation**

Licit and illicit network neighborhoods exhibit different topological signatures after adjusting for graph size and density.

**H2 — Static topology contribution**

Static Betti descriptors improve prediction compared with matched non-topological models.

**H3 — Persistence contribution**

Persistent homology features provide incremental predictive information beyond static Betti features.

**H4 — Temporal generalization**

Topological features retain useful predictive value on strictly future time periods.

**H5 — Independent subgraph evaluation**

Topological representations demonstrate measurable utility on the separate Elliptic2 subgraph-classification task.

**H6 — Robustness and interpretability**

Observed improvements are robust to reasonable graph-construction and filtration choices, computationally practical, and interpretable through validated case-level analysis.

For each hypothesis, specify:

- Null hypothesis.
- Comparison groups.
- Independent evaluation unit.
- Metric.
- Statistical test.
- Effect size.
- Confidence interval.
- Acceptance or rejection interpretation.
- Limitations.

Pre-register the primary comparison, split and metric before examining test performance.

Do not revise hypotheses to match favorable results.

---

# PHASE 4 — DATASET ACQUISITION AND INTEGRITY

## Dataset A — Elliptic / Elliptic++

Primary benchmark:

https://github.com/juicy-candy/Elliptic

Tasks:

1. Verify the authoritative dataset source and available versions.
2. Download the permitted data.
3. Preserve immutable raw files.
4. Examine transaction IDs, edges, direction, feature matrices, labels and time steps.
5. Validate original counts and version-specific schema.
6. Retain unknown-label nodes distinctly from licit nodes.
7. Document overlap between original Elliptic and Elliptic++.
8. Create reproducible graph-construction scripts.

Do not treat Elliptic and Elliptic++ as mutually independent datasets if records overlap.

## Dataset B — Elliptic2

Independent benchmark:

https://github.com/MITIBMxGraph/Elliptic2

Implement its subgraph-level task as specified by its official release and associated documentation.

Important:

- Elliptic2 predicts labels for subgraphs, not necessarily for the same units as Elliptic transaction-node classification.
- Do not directly compare node classification and subgraph classification as identical tasks.
- Avoid assuming that features or labels transfer without modification.
- Implement independent benchmark baselines.
- Validate source-specific train/test protocols.

Do not describe Elliptic2 results as identical-task replication.

## Dataset C — BitcoinHeist (optional)

Use only if independently sourced, temporally aligned graph edges support topological construction.

Do not calculate persistent homology from an imagined graph reconstructed solely from unrelated feature-table rows.

If graph data are unavailable, document the limitation and omit this dataset from topology experiments.

## Dataset manifest

Generate:

`data/manifests/dataset_manifest.json`

Include:

- Dataset identity and version.
- Source URL.
- Download date.
- License.
- File checksum.
- Number of samples.
- Node and edge counts.
- Label distribution.
- Missing data.
- Temporal coverage.
- Processing rules.
- Known limitations.

Validate all datasets before model development.

---

# PHASE 5 — STRICT LEAKAGE-FREE TEMPORAL PROTOCOL

For Elliptic++ use the proposal's initial candidate split:

- Training: time steps 1–30.
- Validation: time steps 31–39.
- Testing: time steps 40–49.

This is the research proposal's specified protocol, not an official benchmark claim.

Verify that the selected dataset contains compatible time steps and document any necessary change before training.

Freeze explicit sample-ID lists.

Implement historical graph reconstruction at observation time t:

G_t = (V_t, E_t, X_t)

Only nodes, attributes and edges observable at the decision time may contribute to a prediction.

Prevent:

- Future-edge leakage.
- Future-neighbor aggregation.
- Held-out label propagation.
- Test-informed feature selection.
- Test-informed normalization.
- Test-informed threshold tuning.
- Test-informed class resampling.
- Uncontrolled overlap between train and test subgraphs.
- Cross-period embedding leakage.

Clearly distinguish strict historical inductive evaluation from transductive evaluation.

The primary reported protocol must be strict and time-respecting.

Create automated leakage-audit tests and produce `results/leakage_audit.json`.

Every input feature should be traceable to the earliest time at which it was observable.

---

# PHASE 6 — MATHEMATICAL TOPOLOGY IMPLEMENTATION

## 6.1 Graph representations

Construct and compare:

A. Directed transaction-dependency graph.

B. Undirected projection of the directed graph.

C. Time-respecting local neighborhoods.

D. Weighted neighborhood complexes.

E. Optional directed path-homology representation.

Recognize that Bitcoin transaction-dependency graphs are generally directed acyclic even when undirected projections contain cycles.

**Never describe an undirected cycle as proof of circular financial transfers or money laundering.**

## 6.2 Neighborhood extraction

For each eligible target transaction, extract neighborhoods with:

k ∈ {1, 2, 3}

Record:

- Node count.
- Edge count.
- Connected components.
- Density.
- Degree statistics.
- Triangle count.
- Clustering coefficient.
- Component size.
- Cycle rank.

Select neighborhood scale using training/validation data only.

Use bounded neighborhoods and caching to avoid memory exhaustion.

## 6.3 Static Betti computation

For an undirected one-dimensional graph complex, compute:

β₀ = C

β₁ = E − V + C

β₂ = 0

where C is the number of connected components.

Validate this against independently computed graph invariants.

Recognize that β₁ is algebraically determined by node count, edge count and component count.

Therefore, simple predictive improvements from β₁ alone do not establish additional information beyond these structural quantities.

Structural confounder controls are mandatory.

## 6.4 Simplicial construction

Implement clearly distinguished topological representations:

- One-dimensional graph complex.
- Flag/clique complex.
- Filtration-induced complex.
- Optional directed path-homology construction.

Demonstrate why a triangular cycle in a graph and a filled triangle in a flag complex can have different H₁.

Compute H₂ only for a complex that can support two-dimensional homology.

Never invent or force nonzero higher-dimensional topology.

## 6.5 Persistent homology

Implement valid nested filtrations:

K(a₁) ⊆ K(a₂) ⊆ ... ⊆ K(aₘ)

Evaluate:

1. Structural-distance filtration.
2. Edge-weight filtration.
3. Historical temporal filtration.
4. Optional directed path-homology filtration.

For every filtration:

- Define filtration values mathematically.
- Explain financial interpretation.
- Prove or programmatically validate nestedness.
- Respect causal time constraints.
- Prevent post-event information exposure.
- Declare edge-direction treatment.
- Specify treatment of essential/infinite bars.

Use GUDHI and other suitable verified libraries.

Extract:

- Persistence intervals.
- Lifetime statistics.
- Betti curves.
- Persistence entropy.
- Persistence images.
- Persistence landscapes where practical.
- Counts of persistent components/cycles.

Record zero and empty-diagram cases without introducing artificial features.

---

# PHASE 7 — MATHEMATICAL UNIT TESTS

Before applying topology to real Bitcoin graphs, implement known-topology tests.

Required test cases:

1. Empty graph.
2. Single isolated vertex.
3. Multiple isolated vertices.
4. Path graph.
5. Tree.
6. Single unfilled cycle.
7. Two disconnected cycles.
8. Triangle graph without a filling face.
9. Filled triangle.
10. Hollow tetrahedral boundary.
11. Filled tetrahedron.
12. Weighted graph with known persistence intervals.
13. Directed acyclic graph whose undirected projection contains a cycle.

Validate expected Betti numbers in the appropriate complex.

Check boundary-operator consistency and filtration-face compatibility where applicable.

Produce:

`tests/test_topology.py`

`results/mathematical_validation_report.md`

Do not proceed with empirical topological analysis if foundational mathematical tests fail.

---

# PHASE 8 — FEATURE REPRESENTATIONS

Construct the following feature groups.

**X — Original transaction features**

Dataset-provided attributes available before prediction time.

**S — Conventional structural controls**

Node degree, density, edge count, component size, clustering, triangles, degree statistics and cycle rank.

**B — Static Betti features**

β₀, β₁ and meaningful normalized variants.

**P — Persistent topology features**

Persistence entropy, lifetime statistics, persistence diagrams transformed into vectors, Betti curves and persistence-image embeddings.

**H — Learned graph embeddings**

GraphSAGE or GAT representations constructed under the prescribed graph-observation protocol.

Create an explicit feature registry and audit every feature for redundancy and temporal validity.

Standardize using training-only fitted transforms.

Keep feature provenance and extraction times.

---

# PHASE 9 — MODELS AND TOPOAML ARCHITECTURE

## 9.1 Conventional models

Implement:

- Logistic Regression.
- Random Forest.
- XGBoost.

## 9.2 Graph learning models

Implement:

- GraphSAGE.
- Graph Attention Network (GAT).

## 9.3 Static topology baselines

Implement:

- XGBoost + static Betti features.
- GAT + static Betti features.

## 9.4 Persistent topology baselines

Implement:

- XGBoost + persistence features.
- GAT + persistence features.

## 9.5 Naive fusion model

Use a clearly documented representation:

zᵥ = [xᵥ || sᵥ || Tᵥ || hᵥ]

where:

xᵥ = original transaction attributes.

sᵥ = structural features.

Tᵥ = topological features.

hᵥ = learned graph embedding.

Train a suitable MLP classifier.

## 9.6 Advanced TopoAML gated fusion

After simpler topology baselines have been evaluated, implement:

- A learnable topological encoder.
- Separate projection of graph embeddings.
- Gated fusion.
- Classification head.

Use a mathematically explicit architecture such as:

uᵥ = Enc_topo(Tᵥ)

qᵥ = Enc_graph([xᵥ || sᵥ || hᵥ])

gᵥ = sigmoid(W_g[qᵥ || uᵥ] + b_g)

fᵥ = gᵥ ⊙ qᵥ + (1 − gᵥ) ⊙ uᵥ

pᵥ = sigmoid(MLP(fᵥ))

Ensure qᵥ and uᵥ have matched dimensions.

Treat this as a candidate implementation, not an already-validated methodological contribution.

Compare gated fusion against concatenation under matched budgets.

Do not assume gating improves results.

---

# PHASE 10 — SEVEN MANDATORY EXPERIMENTS

## E1 — Topological Profiling

Objective: Determine whether licit and illicit labels show distinct topological distributions.

Control for graph size, edge count and density.

Produce:

- Class-wise distributions.
- Persistence diagrams.
- Effect sizes.
- Dependency-aware statistical comparisons.
- Structural confounding analyses.

Report whether any apparent separation persists after adjustment.

## E2 — Matched Model Comparison

Compare the model families specified above, including the advanced model when feasible.

Use the same temporal partitions and comparable model-selection procedures.

Primary metric:

Illicit-class PR-AUC.

Secondary metrics:

- ROC-AUC.
- Precision.
- Recall.
- F1.
- Balanced accuracy.
- Recall at fixed false-positive rate.
- Precision@K.
- Calibration.

Produce comparison tables, confidence intervals and saved prediction files.

## E3 — Topological Ablation

Remove or replace:

- Static Betti features.
- Persistent descriptors.
- Learned topology encoder.
- Gated fusion.

Also compare against structurally matched controls.

Quantify incremental contributions with paired uncertainty intervals.

## E4 — Temporal Generalization

Use locked future-period test data.

Measure degradation across time.

Evaluate class prevalence, representation drift and model calibration.

Never tune on the locked test periods.

Produce temporal trend figures.

## E5 — Elliptic2 External Task

Implement the separate Elliptic2 subgraph-classification protocol.

Run compatible task-specific baselines.

Evaluate whether topological features provide value on this independent financial benchmark.

Do not report this as direct node-level replication of Elliptic++.

## E6 — Sensitivity and Robustness

Vary:

- k-hop radius.
- Filtration choice.
- Weight threshold.
- Graph perturbations.
- Subgraph size.
- Random initialization.
- Feature normalization.
- Class imbalance handling.

Perform at least five random-seed runs where meaningful and feasible.

Quantify robustness rather than relying on a single favorable configuration.

## E7 — Computational Efficiency

Measure:

- Data preparation runtime.
- Neighborhood-extraction runtime.
- Betti computation time.
- Persistent homology computation time.
- Training and inference latency.
- Peak RAM.
- GPU memory.
- Throughput.
- Model parameters.
- Scaling with graph size.

Report actual hardware, software versions and execution environment.

Do not claim large-scale deployment readiness without measured evidence.

---

# PHASE 11 — STATISTICS AND SCIENTIFIC VALIDATION

Primary outcome:

PR-AUC for the illicit class.

Perform comparisons using the correctly matched evaluation units.

Use suitable approaches such as:

- Paired bootstrap.
- Temporal block bootstrap.
- Repeated seeded experiments.
- Appropriate hypothesis tests.
- Confidence intervals.
- Effect-size estimation.
- Multiple-comparison corrections.

Account for dependence created by overlapping graph neighborhoods and temporally related samples.

Distinguish uncertainty across test populations from training-seed variability.

Do not claim superiority solely from numerical ranking.

If TopoAML fails to improve on degree, density, edge count and cycle-rank controls, report that result and explain its implications.

Do not selectively remove unfavorable experiments.

---

# PHASE 12 — HARDWARE-AWARE IMPLEMENTATION

Target the local workstation:

Core i9 / 64 GB RAM / RTX 4060 8 GB / Windows 11.

Use an appropriate compatible Python and PyTorch environment.

Suggested libraries:

- PyTorch.
- PyTorch Geometric.
- GUDHI.
- NetworkX.
- scikit-learn.
- XGBoost.
- NumPy.
- Pandas / PyArrow / Polars.
- Optuna.
- Matplotlib.
- SciPy.

Validate all installations.

Use:

- Memory-mapped or Parquet datasets.
- Bounded subgraph extraction.
- CPU-based persistent homology when appropriate.
- GPU-based graph training where supported.
- Incremental result writing.
- Resume-safe checkpoints.
- Deterministic seeds where feasible.
- GPU memory monitoring.
- Resource-aware batch selection.

Make CPU worker count, RAM budget, GPU memory limit and graph-complexity bounds configurable.

Do not assume that an 8 GB GPU can accommodate full Elliptic2 processing.

Provide Windows setup instructions and WSL2 alternatives if technically required.

---

# PHASE 13 — REPOSITORY IMPLEMENTATION

Use the existing repository:

https://github.com/sagarkorde/BettiGraphs

First inspect the current repository.

Do not overwrite existing work, delete experiments or force-push.

Create a dedicated TopoAML work area or branch.

Suggested structure:

BettiGraphs/
  TopoAML/
    configs/
    data/
      download.py
      checksums.json
      manifests/
      raw/
      processed/
    docs/
    literature/
    src/
      preprocessing/
      graph_construction/
      topology/
      features/
      models/
      evaluation/
      statistics/
      visualization/
    experiments/
      E1/
      E2/
      E3/
      E4/
      E5/
      E6/
      E7/
    tests/
    results/
      raw/
      tables/
      figures/
      audits/
    manuscript/
    supplementary/
    scripts/
    environment.yml
    README.md
    CITATION.cff

Include scripts for:

1. Dataset acquisition and validation.
2. Temporal split generation.
3. Graph construction.
4. Topological feature computation.
5. Baseline training.
6. TopoAML training.
7. Statistical evaluation.
8. Ablation and robustness.
9. Figure generation.
10. Manuscript result-table export.

Create an end-to-end execution script.

Make every experiment resumable.

If repository permissions are unavailable, prepare local commits or patches without claiming the remote repository was updated.

---

# PHASE 14 — REPRODUCIBILITY VERIFICATION

Every manuscript result must be reproducible from recorded inputs.

Save:

- Git commit hash.
- Dataset checksums.
- Split IDs.
- Package versions.
- Hyperparameters.
- Seeds.
- Training logs.
- Model checkpoints.
- Evaluation predictions.
- Statistical outputs.
- Figure scripts.

Implement a fresh-environment smoke test.

Provide exact commands that regenerate manuscript tables and figures.

Create:

`results/reproducibility_audit.md`

Maintain a result traceability table linking each manuscript claim to its originating experiment and output file.

---

# PHASE 15 — PUBLICATION-QUALITY FIGURES

Prepare a concise main-text figure set, adjusted to verified journal requirements.

Proposed figures:

**Figure 1:** TopoAML end-to-end methodology, including historical graph reconstruction, topology extraction and gated graph fusion.

**Figure 2:** Illustrative directed Bitcoin subgraphs, undirected projections and mathematically correct topological interpretations.

**Figure 3:** Betti curves, persistence diagrams and class-conditioned topology with structural confounding controls.

**Figure 4:** Baseline versus TopoAML PR-AUC and other performance metrics with confidence intervals.

**Figure 5:** Ablation, temporal robustness and computational efficiency.

Produce additional detailed plots as supplementary material.

Use actual experiment results.

Export:

- Editable SVG.
- Vector PDF.
- 600 DPI PNG/TIFF where supported.

Ensure readable typography, captions, legends, statistical uncertainty and accessible contrast.

Do not generate empirical figures from assumed performance values.

---

# PHASE 16 — COMPLETE ORIGINAL RESEARCH MANUSCRIPT

Write a manuscript suitable for the verified target journal.

Keep the title:

"TopoAML: Persistent Homology-Guided Graph Learning for Leakage-Free Bitcoin Anti-Money Laundering"

Use the following structure unless the actual journal requirements specify otherwise.

## Abstract

Include actual motivation, methodology, datasets, evaluation protocol, measured findings and supported conclusion.

No predicted or invented percentage improvements.

## 1. Introduction

Explain AML challenges, Bitcoin graph properties, limitations of conventional GNNs, mathematical motivation for persistent homology, research gap and contributions.

## 2. Related Work

Cover recent AML benchmarks, graph learning, persistent homology, directed topology and leakage-controlled evaluation.

Provide a critical novelty comparison.

## 3. Mathematical Preliminaries

Introduce graph representations, one-dimensional homology, Betti numbers, simplicial complexes, persistent homology and filtrations.

Clarify undirected projection and causal interpretation.

## 4. TopoAML Framework

Describe historical graph extraction, topology construction, feature representation, encoders, gated fusion and complexity.

Include equations and pseudocode.

## 5. Datasets and Experimental Methodology

Document Elliptic/Elliptic++, Elliptic2, temporal splits, leakage audits, baselines, hyperparameters, evaluation measures and hardware.

## 6. Experimental Results

Organize real results around E1–E7.

Present uncertainty, structural controls, negative results and external-task limitations.

## 7. Discussion

Explain whether topology adds new predictive information beyond ordinary graph statistics.

Discuss when persistence is useful, why results may vary by graph construction, forensic interpretation and computational tradeoffs.

## 8. Threats to Validity

Include leakage, label quality, graph representation, overlapping neighborhoods, dataset overlap, task mismatch, hyperparameter bias, resource limits and external validity.

## 9. Conclusion

Summarize only contributions supported by measured evidence.

## Declarations

Prepare accurate author-contribution, funding, competing-interest, data/code availability and AI-use statements.

## References

Use verified bibliography entries only.

---

# PHASE 17 — JOURNAL SUBMISSION PACKAGE

Once the target journal is confirmed, prepare:

1. Editable manuscript DOCX.
2. LaTeX source if useful.
3. Submission-ready PDF.
4. Separate high-resolution figures.
5. Supplementary methodology.
6. Dataset provenance and leakage report.
7. Reproducibility package.
8. Graphical abstract, if required or accepted.
9. Highlights, if required.
10. Cover letter.
11. Declarations and compliance checklist.
12. Verified reference library.

Do not invent affiliations, author contributions, funding or ethics approvals.

Confirm actual submission requirements immediately before final formatting.

---

# PHASE 18 — INDEPENDENT CRITICAL REVIEW

Simulate three critical reviewers.

### Reviewer 1 — Mathematical Topology

Audit:

- Betti definitions.
- Complex construction.
- Filtration validity.
- Persistence correctness.
- Directed/undirected assumptions.
- Novelty beyond known topology.

### Reviewer 2 — Bitcoin AML

Audit:

- Benchmark validity.
- Labels.
- Temporal leakage.
- Graph interpretation.
- Cross-dataset claims.
- Baseline relevance.
- Practical forensic significance.

### Reviewer 3 — Machine Learning and Statistics

Audit:

- Fair training budgets.
- Hyperparameter selection.
- Dependency-aware inference.
- Uncertainty.
- Reproducibility.
- Ablations.
- Complexity.

Generate a reviewer report and response matrix.

Correct identifiable problems.

Explicitly disclose unresolved methodological limitations.

Do not guarantee acceptance or indexing.

---

# PHASE 19 — REQUIRED FINAL DELIVERABLES

The completed research package should include:

- Verified literature and DOI audit.
- Research specification traceability.
- Dataset manifests.
- Immutable temporal partitions.
- Validated topology library.
- Executable TopoAML implementation.
- Conventional and GNN baselines.
- Seven completed experiments, or clearly documented blockers.
- Raw experiment predictions.
- Statistical reports.
- High-quality publication figures.
- Complete research manuscript.
- Supplementary materials.
- Reproducibility instructions.
- Journal-compliance assessment.
- Reviewer-style audit.
- Final project completion report.

No fictional files or execution outcomes.

---

# PHASE 20 — EXECUTION STRATEGY

Use the following order:

**Milestone 1 — Benchmark reproduction**

Acquire and validate Elliptic++, freeze temporal partitions, implement basic non-topological models.

**Milestone 2 — Topological correctness**

Implement graph complexes, Betti numbers, filtrations, persistent homology and mathematical unit tests.

**Milestone 3 — Scientific characterization**

Run E1, compare topological distributions and evaluate structural confounding.

**Milestone 4 — Predictive modeling**

Implement static topology, persistent topology, GraphSAGE/GAT and gated TopoAML.

**Milestone 5 — Validation**

Run E2–E7, including temporal evaluation, Elliptic2, ablation, robustness and efficiency.

**Milestone 6 — Publication preparation**

Freeze experiments, regenerate evidence, verify bibliography, draft manuscript, review, and prepare the submission package.

At the end of each milestone:

1. Report files created.
2. Report tests executed.
3. Report measured outcomes.
4. Record failures and corrections.
5. Update the completion checklist.
6. Commit validated code when repository access is authorized.
7. Continue to the next feasible step.

Do not stop after writing pseudocode, architecture diagrams or empty source files.

Do not ask routine permission for decisions already specified in the proposal.

Never claim an experiment has succeeded merely because its code exists.

**FINAL SUCCESS CONDITION**

Deliver an independently reproducible, mathematically sound and temporally leakage-controlled TopoAML study evaluating whether persistent homology offers statistically and operationally meaningful incremental value for Bitcoin AML detection.

The final manuscript must accurately reflect all empirical findings, including negative results.

**BEGIN NOW:** Read `TopoAML_Complete_Research_Proposal.docx`, inspect the existing BettiGraphs repository, verify the intended journal, audit the references, and begin Milestone 1 with executable code and dataset validation.