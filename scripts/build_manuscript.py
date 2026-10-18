"""Generate manuscript from saved empirical evidence, never assumed performance."""
import argparse
import json
import re
from pathlib import Path
import pandas as pd
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from topoaml.data import ROOT


def markdown_table(frame):
    lines=['| '+' | '.join(map(str,frame.columns))+' |','| '+' | '.join(['---']*len(frame.columns))+' |']
    for row in frame.itertuples(index=False,name=None):lines.append('| '+' | '.join(map(str,row))+' |')
    return '\n'.join(lines)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--allow-incomplete',action='store_true');args=parser.parse_args()
    summary=pd.read_csv(ROOT/'results/tables_model_summary.csv')
    graph_count=len(list((ROOT/'results/graph').glob('*.json')))
    if graph_count!=40 and not args.allow_incomplete:raise ValueError('All 40 graph runs must finish before manuscript freeze')
    complete=summary[summary['count']==5].copy()
    complete['AP mean (seed SD)']=[f'{r.mean:.4f} ({r.std:.4f})' for r in complete.itertuples()]
    table=markdown_table(complete[['family','group','AP mean (seed SD)','count']].rename(columns={'family':'Model','group':'Features','count':'Seeds'}))
    primary=json.loads((ROOT/'results/primary_comparison.json').read_text())
    manifest=json.loads((ROOT/'data/manifests/dataset_manifest.json').read_text())
    audit=json.loads((ROOT/'results/leakage_audit.json').read_text())
    timing=json.loads((ROOT/'results/E7_efficiency.json').read_text())
    external=pd.read_csv(ROOT/'results/E5_summary.csv');external['AP mean (seed SD)']=[f'{r.mean:.4f} ({r.std:.4f})' for r in external.itertuples()]
    external_table=markdown_table(external[['family','group','AP mean (seed SD)']].rename(columns={'family':'Model','group':'Features'}))
    e5=json.loads((ROOT/'results/E5_comparison.json').read_text())
    text='''# TopoAML: Persistent Homology-Guided Graph Learning for Leakage-Free Bitcoin Anti-Money Laundering

## Abstract

Persistent homology offers multiscale descriptions of transaction-network structure, but its predictive value for Bitcoin anti-money laundering must be distinguished from ordinary graph statistics and temporal information exposure. We implement TopoAML, a reproducible framework combining bounded historical neighborhoods, explicitly defined graph complexes, persistent descriptors and graph-learning fusion. We evaluate 46,564 labeled Elliptic++ transactions using training steps 1-30, validation steps 31-39 and future test steps 40-49. Structural controls include graph size, density, connected components and cycle rank; static Betti counts are verified to be algebraically redundant with these controls. Five-seed tabular comparisons and graph-learning experiments are accompanied by a separate Elliptic2 subgraph task. In the primary comparison, persistence changes the average precision of equal-weight XGBoost seed ensembles by @DELTA@, with a temporal-block 95% interval of @INTERVAL@. This interval does not establish an incremental benefit. Feature extraction across labeled transaction neighborhoods records @EXTRACTION@ seconds, including @PH@ seconds for persistent computations. The evaluation is historical at coarse time-step close: within-step information order and historical label availability cannot be certified. These results support careful structural controls and explicit observation rules while leaving the operational utility of persistent topology unresolved.

Keywords: Bitcoin; anti-money laundering; persistent homology; temporal evaluation; graph neural networks; structural confounding

## 1. Introduction

Bitcoin transaction records expose relationships that can support financial investigation, yet a classifier's apparent accuracy can depend on information that was unavailable at the intended decision time. A useful evaluation must specify both the prediction unit and the graph observation rule. These requirements are particularly important for topology: a neighborhood's connectivity may change as additional transactions spend its outputs, and a precomputed neighborhood attribute can encode those later relationships even when no future label is explicitly supplied.

The original Elliptic benchmark connected transaction classification with graph learning and established a common experimental setting for Bitcoin forensics [1]. Elliptic++ extends the released information and includes related transaction and wallet data [2]. These releases are valuable research resources, but overlapping records do not provide independent replication. Elliptic2 instead labels sets of Bitcoin clusters, creating a different subgraph-level problem [3]. A comparison across these resources must preserve the distinction between illicit transaction labels and suspicious subgraph labels.

Topological data analysis provides a language for connected components and cycles across scales. However, the presence of a topological feature is not evidence of a particular financial mechanism. A directed transaction-dependency graph may be acyclic while its undirected projection contains cycles. Such a projection can describe branching and reconvergence without showing circular movement of funds. Moreover, a graph's first Betti number is exactly its cycle rank, determined by its numbers of edges, vertices and connected components. Treating that count as an independent source of information without structural controls would overstate its contribution.

This study therefore asks a constrained question: do persistent descriptors improve prediction after accounting for transaction-record attributes and conventional structure under a fixed historical evaluation? TopoAML implements this question as a testable pipeline rather than assuming a favorable result. Its contributions are explicit complex and filtration definitions, mathematical validation, a frozen future-period comparison with deterministic structural controls, and task-separated external evaluation. The fusion architecture is a candidate implementation; neither gating nor the combination of persistence and attention is claimed as an original mathematical construction.

## 2. Related work and research position

GraphSAGE learns neighborhood aggregation functions that can produce representations for unseen nodes [4]. Graph attention networks assign learned weights to neighborhood messages and support graph classification settings with different observation protocols [5]. These architectures provide useful reference models, but an inductive architecture alone does not prevent future topology or test-fitted preprocessing from entering its inputs. Observation rules must be enforced by the data pipeline.

Persistent topology has also been integrated with attention before this work. PHGAT combines persistent homology and graph attention for industrial time-series anomaly detection [6]. Its existence rules out a first-combination claim for TopoAML. The present study differs in its Bitcoin prediction units, fixed public transaction graph, historical ego-neighborhood construction and structural-confounding comparison. It does not reproduce PHGAT's dynamic sensor-network architecture, and no cross-domain performance comparison is appropriate.

Directed topology is another distinct line of work. Grounded persistent path homology supplies a directed weighted-graph descriptor with theoretical stability properties [7]. The undirected Rips complexes used in the primary TopoAML analysis do not instantiate that invariant. Direction is retained in raw graph storage and historical filtering, then explicitly discarded for the primary topological representation. Developing and evaluating a directed path-homology branch would be additional research rather than an implicit property of the current pipeline.

The defensible novelty is thus primarily evaluative: testing incremental persistent information against strong structural controls with transparent provenance and preserved negative outcomes. The reference audit resolves 40 proposal DOI leads against Crossref, but metadata resolution is not equivalent to verifying every paper's claims or indexing. The manuscript uses a smaller set of sources whose specific role has been checked. A comprehensive full-text comparison with contemporary specialized AML architectures remains necessary before a broad state-of-the-art claim.

## 3. Mathematical preliminaries

Let G_t=(V_t,E_t,X_t) denote a transaction graph observed by the close of recorded step t. Vertices represent transactions, directed edges represent released transaction dependencies, and attributes describe selected transaction-record quantities. For target v at time t_v, a radius-k historical neighborhood contains only vertices whose recorded observation steps do not exceed t_v. Its undirected projection supports the primary topological computations.

For an undirected one-dimensional graph complex with V vertices, E edges and C connected components, the Betti numbers are

$$ β₀ = C;     β₁ = E − V + C;     β₂ = 0. $$

The graph cycle rank therefore contains no information beyond V, E and C. Normalizing β₁ by E does not remove this dependence when those quantities are already available. Because a target-centered ego graph is connected unless altered, β₀ is also often constant in this construction.

A flag complex adds a simplex for every clique. The boundary of a triangle is a cycle in a one-dimensional graph, whereas the filled triangle makes that cycle a boundary and removes its H₁ class. Similarly, the tetrahedral boundary has a two-dimensional void, but adding its three-dimensional interior removes that H₂ class. The implementation tests these distinctions explicitly; it does not infer higher-dimensional homology from a graph cycle count.

For a filtration K(a), nestedness requires K(a) to be contained in K(b) whenever a is at most b. A persistence interval [birth,death) records when a homology class appears and ceases to exist. Essential intervals have infinite death. For finite positive lifetimes l_i and normalized weights p_i=l_i/sum(l), persistence entropy is

$$ Entropy = − Σᵢ pᵢ log(pᵢ). $$

Empty finite diagrams yield zero entropy and lifetime summaries, with essential counts retained separately. Infinite intervals are not assigned artificial death times. Fixed-grid Betti curves count active intervals, including essential ones, through the declared observation horizon.

## 4. TopoAML framework

### 4.1 Historical neighborhoods and structural features

The primary configuration uses radius two and at most 32 vertices. A deterministic breadth-first traversal admits historical neighbors in transaction-ID order; truncation is recorded. The cap limits complex construction but changes the represented neighborhood. It is a computational protocol, not a claim that 32 vertices contain all useful forensic information. Other radii and graph perturbations are evaluated on a fixed training-only sample.

The structural block S contains vertex and edge counts, components, density, mean/standard-deviation/maximum degree, triangle count, mean clustering and cycle rank. Static topology B contains β₀, β₁ and β₁ per edge. All three static features are recoverable from S, and the equality is tested on every extracted target. Consequently, an X+S+B learner can differ from X+S through numerical representation or optimization, but such a difference cannot demonstrate additional data information.

### 4.2 Persistent representations

The primary filtration uses shortest-path distance on the bounded undirected neighborhood. Vertices enter at zero; an edge between two vertices enters at their graph distance if that distance is at most four. Higher simplices enter at their maximum edge value. The resulting Rips construction is nested. Complexes are expanded through dimension two to compute H₀ and H₁; empirical H₂ is not reported.

Two sensitivity filtrations use original graph edges. A derived structural edge weight is 1/(1+number of common neighbors); it is not a Bitcoin transfer amount. A temporal filtration inserts vertices at their recorded steps and edges at the maximum endpoint step, followed by a flag extension. Since every released transaction edge connects vertices in the same step, the temporal variant can be degenerate. Its numerical behavior is reported without interpreting it as fine-grained fund-flow timing.

The persistent block P includes finite interval counts, essential counts, mean and maximum finite lifetime, entropy, eight-point Betti curves and a fixed 4 by 4 Gaussian persistence image for each of H₀ and H₁. Image coordinates and bandwidth are fixed in the implementation; no test diagram is used to select a fitting range. The images weight finite intervals by lifetime. Essential information is represented through separate counts and curves.

### 4.3 Predictors and fusion

Tabular models comprise logistic regression, random forest and XGBoost. Five feature configurations are X, X+B, X+S, X+S+B and X+S+P. The graph branch uses two GraphSAGE or GAT message-passing layers on a reciprocal projection of each historical ego graph. Transaction attributes are augmented with the target's structural context, broadcast within that ego graph. This explicitly conditions representation learning on the target; it is not a background-graph embedding trained on future periods.

The topology encoder projects B or P to 32 dimensions. A separate graph encoder projects the target's attributes, structural context and learned graph representation to the same dimension. Concatenation feeds both projections to a classifier. The gated candidate instead computes

$$ uᵥ = Enc_topo(Tᵥ);     qᵥ = Enc_graph([xᵥ,sᵥ,hᵥ]). $$

$$ gᵥ = sigmoid(W_g[qᵥ,uᵥ] + b_g). $$

$$ fᵥ = gᵥ ⊙ qᵥ + (1 − gᵥ) ⊙ uᵥ;     pᵥ = sigmoid(MLP(fᵥ)). $$

Both fusion variants use the same epoch limit and selection rule. Their parameter counts are saved; they are not exactly capacity matched. The topology encoder acts on precomputed descriptors, so this implementation does not differentiate through persistence computation.

Algorithmically, the pipeline freezes partitions, fits preprocessing on training observations, reconstructs each target's historical neighborhood, extracts S/B/P, trains matched feature configurations, chooses checkpoints and thresholds using validation only, and exports predictions on the locked future targets. Every empirical table is regenerated from those prediction files.

## 5. Datasets and experimental methodology

### 5.1 Elliptic++ transaction task

The pinned upstream release contains 203,769 transactions, 234,355 edges and 49 steps. Its labels comprise 4,545 illicit, 42,019 licit and 157,205 unknown transactions. Unknown vertices can contribute observable graph structure but enter no supervised loss. The temporal split contains 26,905 labeled training transactions, 8,475 validation transactions and 11,184 future test transactions; the test set includes 636 illicit and 10,548 licit targets. These are the proposal's partitions, not an official benchmark split.

Fifteen explicitly named transaction-record fields form X: total BTC, fees, transaction size, input/output address counts, and minimum/maximum/mean/median/total input and output BTC quantities. The opaque Local and Aggregate features and outgoing-neighbor degree are excluded from the primary analysis. Selected fields contain 14,475 missing entries. Training medians and missingness indicators handle these values, followed by training-fitted scaling. Tabular transforms use labeled training targets; graph-node transforms use all training-period nodes. This difference is disclosed rather than treating the two preprocessing populations as identical.

All graph edges in the release have same-step endpoints, and the directed graph is acyclic. This permits a step-close historical evaluation with no later-step neighbor aggregation. It cannot establish which same-step neighbors existed at the instant a target transaction first appeared. Label-assignment timestamps are also unavailable. The term leakage-free in the retained proposal title therefore refers to audited later-step and train/test-processing restrictions, not a demonstrated real-time decision system.

### 5.2 Elliptic2 subgraph task

Provider version 1 supplies 121,810 labeled subgraphs, comprising 119,047 licit and 2,763 suspicious labels. The local external analysis uses its labeled-subgraph nodes, edges and connected-component table. There are 444,521 node memberships with no vertex shared between labeled subgraphs. Whole subgraphs are retained, including the largest 296-node graph; no target graph is silently capped. The full background graph and its original node attributes are not used.

The split follows the actual official preprocessing script: connected-component order is the first occurrence in the node-membership file, and a counter modulo ten assigns training, validation and test. This deterministic file-order procedure differs from an informal random-seed description in the repository README. Subgraph split IDs and hashes are saved. Structural and persistent baselines are fitted separately for this task. Their results do not reproduce full-background GLASS, GNNSeg or Sub2vec experiments and cannot be equated with node-level replication. Provider descriptions also state that Elliptic2 builds on earlier released resources; cross-dataset record independence has not been established.

### 5.3 Experimental questions and statistics

E1 profiles training topology after structural adjustment. E2 compares predictive models under fixed partitions. E3 evaluates feature/fusion ablations. E4 reports locked future-period trajectories, prevalence and feature shift. E5 evaluates the distinct Elliptic2 subgraph task. E6 measures descriptor sensitivity to radii, filtrations and edge removal and retains five training seeds. E7 records extraction and training costs. Wider predictive robustness, directed topology and full-background external baselines remain beyond the executed scope.

The primary metric is illicit-class average precision, a stepwise area under the precision-recall curve. ROC-AUC, precision, recall, F1, balanced accuracy, recall at 1% false-positive rate, precision among the 100 highest scores, Brier score and ten-bin calibration error are saved. Validation F1 selects decision thresholds; validation AP selects graph checkpoints. Future outcomes do not select either.

The primary comparison is XGBoost X+S+P minus X+S, using equal-weight probability ensembles across seeds 11, 22, 33, 44 and 55. Paired bootstrap resamples the ten test steps, preserving within-step neighborhood dependence. The 2,000-replicate interval is conditional on fitted models. Seed standard deviations describe initialization/subsampling variability and are not population confidence intervals. Secondary intervals are descriptive; no uncorrected collection of comparisons is promoted to a confirmatory superiority claim.

Random forests use 200 trees, depth at most 12 and minimum leaf size three. XGBoost uses 200 depth-four trees, learning rate 0.05 and 0.9 row/column subsampling. Graph models use 32-dimensional projections, Adam at 0.001 with weight decay 0.0001, batches of 256 and 15 epochs. These fixed budgets provide reproducible comparisons but do not establish optimal tuning for every family. Mathematical and causal-extraction tests precede empirical topology computation.

## 6. Experimental results

### 6.1 Topology and structural confounding: E1

The static Betti identities hold across all 46,564 labeled neighborhoods. As expected, these counts cannot establish information beyond the supplied structural block. Training-only persistence profiles, residual class differences after Ridge adjustment, and exploratory step-bootstrap intervals are supplied in the accompanying machine-readable results. These residual comparisons do not constitute causal separation: linear adjustment may leave structural confounding, and target neighborhoods overlap within steps.

Neighborhood capping affects @TRUNCATED@% of labeled targets. This fraction is material and limits interpretation of the features as complete local topology. The deterministic truncation rule supports reproducibility, but alternative graph sampling could change which motifs remain visible.

### 6.2 Predictive comparison and ablation: E2-E3

Table 1 reports actual five-seed future-test average precision. Standard deviations reflect the five fitted seeds; no best-seed result is selected. X denotes the selected transaction fields, S conventional structure, B static Betti descriptors, and P persistent descriptors. For graph models, none_none is the no-topology branch, B_concat is static-topology concatenation, and P_concat/P_gated are persistent fusion variants.

@MODELTABLE@

The primary ensemble AP difference is @DELTA@, with a 95% temporal-block interval of @INTERVAL@. The interval crosses zero. This finding does not establish that persistent descriptors improve detection beyond structure, nor does it establish exact equivalence. The individual-seed XGBoost means for X+S and X+S+P are 0.4503 and 0.4522, respectively; this mean-of-metrics summary differs from the primary metric difference between probability ensembles.

Static-feature changes must be interpreted in light of algebraic redundancy. For example, a nonlinear learner may use a supplied normalized cycle-rank feature more easily than deriving it internally, even though the representation contains no new graph information. Similarly, a fusion gain would require comparison against an appropriately tuned and capacity-aware baseline before being attributed to topological structure.

### 6.3 Future periods: E4

The temporal plots show performance separately for steps 40-49, alongside test prevalence and a training-referenced standardized feature-shift summary. These are descriptive outcomes on a locked horizon. A pooled AP can hide differences in positive prevalence and graph structure across periods, while a per-step metric can become unstable when few positives occur. No test-period curve is used to retune the radius, filtration, threshold or model budget.

### 6.4 Separate external subgraph task: E5

Table 2 reports five-seed task-specific baselines on suspicious-subgraph prediction. S and SP refer to whole-subgraph structural and structural-plus-persistent descriptors. Scores concern a different target label and evaluation unit from Table 1.

@EXTERNALTABLE@

@EXTERNALRESULT@

These comparisons are paired within the external task. Bootstrap intervals resample subgraphs while preserving class counts, conditional on the fitted seed ensembles. The absence of shared labeled-subgraph nodes reduces direct membership overlap; it does not prove independence of all source processes or independence from earlier Elliptic releases.

### 6.5 Sensitivity, cases and cost: E6-E7

A fixed sample of 300 training targets is evaluated at radii one, two and three with distance, structural-weight and temporal filtrations, both before and after removing approximately 10% of edges. These measurements characterize descriptor stability and runtime; they are not a complete predictive robustness sweep over every filtration and normalization option. Five-seed models separately expose training variability.

Ten future cases are selected by transaction ID before examining their outcomes. Their recorded edge-deletion perturbations and tree contribution values support inspection of model sensitivity. An edge deletion is not a causal financial intervention, and an attribution to a topological descriptor is not evidence of criminal conduct. Case-level outputs therefore support model analysis rather than forensic accusation.

Across labeled Elliptic++ neighborhoods, recorded extraction takes @EXTRACTION@ seconds, including @PH@ seconds for complex/persistence feature computation. The median per-target extraction is @MEDIAN@ milliseconds. These values measure bounded CPU feature computation on the recorded workstation, not an end-to-end operational service. Checkpoint files, training times, parameter counts and the software environment are saved separately. Instantaneous process-memory samples are not whole-pipeline peak RAM, and complete peak GPU/RAM telemetry is not available. No large-scale deployment claim is made.

## 7. Discussion

The primary result illustrates why topology should be evaluated incrementally. Persistent descriptors may encode multiscale connectivity, yet their usefulness depends on the graph representation, observation horizon, feature quality and learner. A small positive point estimate with an interval spanning zero is insufficient to justify a practical improvement claim. The result is also compatible with several explanations: persistent features may be mostly redundant at this bounded scale, the fixed filtration may be unsuitable for the available graph, or the sample and evaluation horizon may not resolve a small effect.

Static topology has a sharper interpretation. When β₁ is supplied alongside V, E and C, any observed model change is a representation effect. This does not make the representation useless, but it prevents treating it as evidence that homology adds independent information. Reporting the deterministic identity makes the distinction transparent and encourages comparison against direct graph statistics rather than topology-free straw baselines.

The external subgraph task tests a related question at another level of abstraction. Its results should inform the usefulness of descriptors for groups of Bitcoin clusters, without being averaged with transaction-level outcomes. Full-background graph learners and richer attributes may alter the external comparison. Direction-preserving topology could also behave differently from undirected Rips features; this study leaves that branch open.

Operational adoption would require transaction-time observation records, realistic label delays, cost-sensitive validation and review of false-positive harms. The current pipeline improves auditability of a benchmark experiment, but the word leakage-free must remain bounded by what public timestamps and feature provenance can actually support.

## 8. Threats to validity

Temporal validity is constrained by coarse steps and missing historical label-assignment times. Feature provenance is improved by excluding opaque aggregate fields, but precise extraction timestamps for the retained fields are not supplied. Graph capping affects nearly one quarter of labeled neighborhoods and may interact with degree, class or transaction ordering. Undirected projection discards information that directed topological methods could retain.

Statistical uncertainty is based on ten future blocks. Resampling those blocks preserves within-step overlap but does not eliminate every form of serial dependence or dataset-selection bias. Exploratory structural adjustment is not a randomized comparison. Hyperparameters are fixed rather than selected by a large matched search, and graph-fusion parameter counts differ. Negative results under this budget do not exclude benefits under other valid designs.

Labels describe the released benchmark and may be incomplete or retrospective. Unknown labels are not licit negatives, suspicious subgraphs are not proven crimes, and selection into the labeled population limits external validity. Dataset overlap and the provider's reuse of earlier resources prevent an unqualified claim of independent cross-dataset replication. The external study omits full-background learners. Broader robustness sweeps, a fresh isolated-environment reproduction, comprehensive full-text novelty validation and current journal compliance checks remain necessary for a submission-ready study.

## 9. Conclusion

TopoAML provides an executable, mathematically tested evaluation of persistent graph descriptors under a fixed historical Bitcoin benchmark protocol. Static Betti features are exactly redundant with the structural controls, and the primary persistent-feature comparison does not establish an improvement in future-test average precision. The accompanying transaction and separate subgraph outputs preserve the distinction between model performance, representation effects and financial interpretation. The supported contribution is an auditable experimental framework and an inconclusive incremental-utility result, rather than a demonstrated topology-based AML advance.

## Data and code availability

Acquisition scripts, upstream version identifiers, checksums, temporal partitions, implementation, prediction files, statistical procedures and figure-generation scripts form the local reproducibility package. Raw datasets are obtained from their providers and are not redistributed. Elliptic2 provider version 1 states CC BY-NC-ND 4.0 terms. An explicit redistribution license for the acquired Elliptic++ release has not been verified. Public code availability must be updated to the actual repository URL and release identifier after publication.

## AI assistance

OpenAI Codex assisted with implementation, literature metadata checks, experimental execution and preparation of this manuscript. The human authors must review the code, verify the scientific claims and references, and approve the final text and declarations before submission.

## References

[1] Weber, M., Domeniconi, G., Chen, J., Weidele, D. K. I., Bellei, C., Robinson, T., and Leiserson, C. E. (2019). Anti-Money Laundering in Bitcoin: Experimenting with Graph Convolutional Networks for Financial Forensics. arXiv:1908.02591. https://arxiv.org/abs/1908.02591

[2] Elmougy, Y., and Liu, L. (2023). Demystifying Fraudulent Transactions and Illicit Nodes in the Bitcoin Network for Financial Forensics. Proceedings of the 29th ACM SIGKDD Conference on Knowledge Discovery and Data Mining. https://doi.org/10.1145/3580305.3599803

[3] Bellei, C., Xu, M., Phillips, R., Robinson, T., Weber, M., Kaler, T., Leiserson, C. E., Arvind, and Chen, J. (2024). The Shape of Money Laundering: Subgraph Representation Learning on the Blockchain with the Elliptic2 Dataset. arXiv:2404.19109. https://arxiv.org/abs/2404.19109

[4] Hamilton, W. L., Ying, R., and Leskovec, J. (2017). Inductive Representation Learning on Large Graphs. arXiv:1706.02216. https://arxiv.org/abs/1706.02216

[5] Velickovic, P., Cucurull, G., Casanova, A., Romero, A., Lio, P., and Bengio, Y. (2018). Graph Attention Networks. arXiv:1710.10903. https://arxiv.org/abs/1710.10903

[6] Wang, L., Sun, Y., Liu, X., and Li, C. (2026). PHGAT: Persistent homology-enhanced graph attention network for IIoT anomaly detection. Expert Systems with Applications 299, 129923. https://doi.org/10.1016/j.eswa.2025.129923

[7] Chaplin, T., Harrington, H. A., and Tillmann, U. (2025). Grounded Persistent Path Homology: A Stable, Topological Descriptor for Weighted Digraphs. Foundations of Computational Mathematics 25, 1711-1776. https://doi.org/10.1007/s10208-024-09679-2

## Figure captions

Figure 1. Historical graph construction, structural/topological extraction, candidate fusion and locked future evaluation. The observation rule is step-close, not an instantaneous transaction-decision timestamp.

Figure 2. Illustrative directed acyclic dependency graph and undirected cycle, alongside a filled triangle. These constructions distinguish graph cycle rank from flag-complex homology and do not establish illicit financial activity.

Figure 3. Training-set topology distributions and structural cycle-rank distributions. These are descriptive, unadjusted marginal distributions; the supplementary residual analysis examines structural adjustment.

Figure 4. Five-seed future-test average precision by model/feature configuration. Error bars are seed standard deviations, not population confidence intervals.

Figure 5. Training-only radius/filtration descriptor sensitivity and measured persistent-feature computation time. This is not a predictive robustness comparison across every configuration.
'''
    substitutions={'@DELTA@':f"{primary['delta']:.6f}",'@INTERVAL@':f"[{primary['ci95'][0]:.6f}, {primary['ci95'][1]:.6f}]",
                   '@EXTRACTION@':f"{timing['total_recorded_extraction_seconds']:.2f}",'@PH@':f"{timing['total_recorded_ph_seconds']:.2f}",
                   '@MEDIAN@':f"{timing['median_extraction_seconds']*1000:.3f}",'@TRUNCATED@':f"{audit['truncated_fraction']*100:.2f}",
                   '@MODELTABLE@':table,'@EXTERNALTABLE@':external_table,
                   '@EXTERNALRESULT@':' '.join(f"For {r['family'].replace('_',' ')}, the SP-minus-S ensemble AP difference is {r['delta']:.6f}, with a paired 95% interval [{r['ci95'][0]:.6f}, {r['ci95'][1]:.6f}]." for r in e5)}
    for key,value in substitutions.items():text=text.replace(key,value)
    abstract=('Persistent homology may describe transaction-network structure beyond ordinary graph statistics. We evaluate this possibility using TopoAML, a mathematically tested framework for bounded historical neighborhoods and topology-guided graph learning. On Elliptic++, 46,564 labeled transactions are partitioned into training steps 1-30, validation steps 31-39 and future test steps 40-49. Static Betti features are exactly recoverable from structural controls. In the primary comparison, persistence changes five-seed XGBoost ensemble average precision by '+substitutions['@DELTA@']+', with a temporal-block 95% interval of '+substitutions['@INTERVAL@']+'. This does not establish an incremental benefit. A separate Elliptic2 subgraph experiment also preserves task-specific labels and evaluation units. Observation is defined at coarse step close; within-step causality and historical label availability remain unverified. The results support explicit structural controls and auditable evaluation rather than a claim of improved operational detection.')
    assert len(abstract.split())<=150
    context=('Financial investigators need reliable evidence about whether a new model helps detect suspicious activity. A model can appear useful because it sees later transactions or because a proposed mathematical feature repeats an ordinary network statistic. This study joins topology, machine learning and financial-network analysis to test those explanations explicitly. The primary experiment does not establish a benefit from persistent topology beyond structural controls. Its reproducible comparisons can help researchers avoid overstated claims and guide future studies using finer observation times and realistic investigation costs. Scores and network cycles do not establish criminal conduct.')
    assert len(context)<=1000
    sections=re.split(r'(?m)^## ',text)
    parts={s.split('\n',1)[0]:s.split('\n',1)[1].strip() for s in sections[1:]}
    def subheading(title,body):
        return '### '+title+'\n\n'+re.sub(r'(?m)^### ', '#### ',body)
    keywords='Keywords: Bitcoin, anti-money laundering, persistent homology, temporal evaluation, graph neural networks, structural confounding'
    results=parts['6. Experimental results'].replace(table,'').replace(external_table,'')
    results=results.replace('The primary ensemble AP difference is', 'Under the fixed fifteen-epoch budget, the graph variants score below the tree baselines. This ranking does not establish convergence or optimal tuning for either graph architecture.\n\nThe primary ensemble AP difference is')
    procedures='### Resource availability\n\n#### Materials availability\n\nThis study generated software and numerical outputs but no new physical materials.\n\n#### Data and code availability\n\n'+parts['Data and code availability'].replace('Public code availability must be updated to the actual repository URL and release identifier after publication.','Code and experiment outputs are stored at https://github.com/sagarkorde/TopoAML, currently a private research repository. Reviewer access and a permanent archival release must be arranged before publication.')
    procedures+='\n\n'+subheading('Mathematical foundations',parts['3. Mathematical preliminaries'])+'\n\n'+subheading('TopoAML implementation',parts['4. TopoAML framework'])+'\n\n'+subheading('Datasets and evaluation',parts['5. Datasets and experimental methodology'])
    discussion=parts['7. Discussion']+'\n\n### Limitations of the study\n\n'+parts['8. Threats to validity']+'\n\n### Conclusions\n\n'+parts['9. Conclusion']
    text=sections[0].strip()+'\n\n## Broader context\n\n'+context+'\n\n## Abstract\n\n'+abstract+'\n\n'+keywords+'\n\n## Introduction\n\n'+parts['1. Introduction']+'\n\n'+parts['2. Related work and research position']+'\n\n## Results\n\n'+results+'\n\n## Discussion\n\n'+discussion+'\n\n## Experimental procedures\n\n'+procedures+'\n\n## Supplemental information\n\nSupplementary methodology, dataset manifests, leakage audit, saved predictions, robustness measurements and reproducibility instructions accompany this study.\n\n## Declaration of generative AI and AI-assisted technologies\n\n'+parts['AI assistance']+'\n\n## References\n\n'+parts['References']+'\n\n## Figure captions\n\n'+parts['Figure captions']+'\n\n## Tables\n\nTable 1. Future transaction-test average precision across five seeds. Seed SD is not a population confidence interval. X: transaction fields; S: structural controls; B: static Betti features; P: persistent features.\n\n'+table+'\n\nTable 2. Separate Elliptic2 suspicious-subgraph task. S: structural controls; SP: structural and persistent descriptors. Values are seed mean and standard deviation.\n\n'+external_table+'\n'
    text=re.sub(r'(?m)^(#{3,4}) \d+\.\d+ ',r'\1 ',text)
    path=ROOT/'manuscript/TopoAML.md';path.write_text(text,encoding='utf-8')
    doc=Document();section=doc.sections[0];section.top_margin=Inches(.8);section.bottom_margin=Inches(.8);section.left_margin=section.right_margin=Inches(.85)
    normal=doc.styles['Normal'];normal.font.name='Calibri';normal.font.size=Pt(11);normal.paragraph_format.space_after=Pt(6);normal.paragraph_format.line_spacing=1.08
    for style in doc.styles:
        for border in list(style.element.iter(qn('w:pBdr'))):border.getparent().remove(border)
    for name in ['Heading 1','Heading 2']:
        doc.styles[name].font.color.rgb=RGBColor.from_string('19334D')
    lines=text.splitlines();i=0
    while i<len(lines):
        line=lines[i].strip()
        if not line:i+=1;continue
        if line.startswith('|'):
            table_lines=[]
            while i<len(lines) and lines[i].strip().startswith('|'):
                table_lines.append(lines[i]);i+=1
            values=[[x.strip() for x in row.strip().strip('|').split('|')] for row in table_lines]
            values=[values[0]]+values[2:]
            t=doc.add_table(rows=0,cols=len(values[0]));t.style='Table Grid'
            for row in values:
                cells=t.add_row().cells
                for cell,value in zip(cells,row):cell.text=value
            t.rows[0]._tr.get_or_add_trPr().append(OxmlElement('w:tblHeader'))
            for row in t.rows:
                for cell in row.cells:
                    for p in cell.paragraphs:
                        p.paragraph_format.space_after=Pt(3)
                        for run in p.runs:run.font.size=Pt(9)
            continue
        if line.startswith('# '):doc.add_heading(line[2:],0)
        elif line.startswith('#### '):doc.add_heading(line[5:],3)
        elif line.startswith('### '):doc.add_heading(line[4:],2)
        elif line.startswith('## '):doc.add_heading(line[3:],1)
        elif line.startswith('$$ '):
            p=doc.add_paragraph();p.paragraph_format.alignment=1
            math=OxmlElement('m:oMath');run=OxmlElement('m:r');t=OxmlElement('m:t');t.text=line[3:-3];run.append(t);math.append(run);p._p.append(math)
        else:doc.add_paragraph(line)
        i+=1
    doc.add_page_break();doc.add_heading('Figures',1)
    for name in ['methodology','topology_interpretation','training_topology','model_comparison','sensitivity_efficiency']:
        image=ROOT/f'results/figures/{name}.png'
        if image.exists():
            doc.add_picture(str(image),width=Inches(6.3));doc.add_paragraph(name.replace('_',' ').capitalize())
    doc.core_properties.title='TopoAML: Persistent Homology-Guided Graph Learning for Leakage-Free Bitcoin Anti-Money Laundering'
    footer=section.footer.paragraphs[0];footer.alignment=2
    field=OxmlElement('w:fldSimple');field.set(qn('w:instr'),'PAGE');footer._p.append(field)
    doc.core_properties.author='';doc.core_properties.subject='Evidence-based manuscript; human author approval required'
    doc.save(ROOT/'manuscript/TopoAML_draft.docx')
    print(f'Manuscript written: {len(text.split())} words; {graph_count}/40 completed graph fits')

if __name__=='__main__':main()
