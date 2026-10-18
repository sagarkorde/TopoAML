"""Preserve source requirements and produce a conservative evidence ledger."""
import csv
import json
import re
from pathlib import Path
from topoaml.data import ROOT, SAFE_FIELDS


def main():
    source=(ROOT/'docs/master_prompt.md').read_text(encoding='utf-8')
    phase='0';rows=[]
    mapping={1:'docs/research_specification.md',2:'literature/doi_audit.csv',3:'docs/hypotheses.md',
             4:'scripts/acquire.py;src/topoaml/data.py',5:'src/topoaml/temporal.py;tests/test_temporal.py',
             6:'src/topoaml/topology.py',7:'tests/test_topology.py',8:'scripts/extract.py',
             9:'src/topoaml/models.py;scripts/train_tabular.py;scripts/train_graph.py',
             10:'scripts/characterize.py;scripts/analyze.py',11:'src/topoaml/evaluation.py',
             12:'configs/preregistered.json',13:'README.md',14:'results/reproducibility_audit.md',
             15:'scripts/analyze.py',16:'manuscript/TopoAML.md',17:'docs/journal_assessment.md',
             18:'docs/reviewer_report.md',19:'docs/project_status.md',20:'scripts/run_all.ps1'}
    for number,line in enumerate(source.splitlines(),1):
        m=re.match(r'# PHASE (\d+)',line)
        if m:phase=m.group(1)
        if line.strip() and (re.match(r'^\d+\.',line) or line.startswith('- ') or line.startswith('**H') or line.startswith('## E')):
            rows.append({'id':f'R{len(rows)+1:03}','source_line':number,'phase':phase,'requirement':line.strip(),
                         'implementation':mapping.get(int(phase),'docs/change_log.md'),
                         'evidence':'See phase ledger; mapping does not assert completion',
                         'manuscript_section':'Methods/Results/Limitations as applicable','status':'requires item-level review'})
    with (ROOT/'docs/requirements_traceability.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
    text='''# Research specification

The authoritative specification is the original proposal, preserved as `TopoAML_Complete_Research_Proposal.docx`, and the complete user brief in `docs/master_prompt.md`. The proposal is fully extracted in `docs/proposal_extracted.txt`; both remain available to audit this implementation. The title and H1-H6 are preserved. `docs/hypotheses.md` defines nulls, units, comparisons, effects and interpretation. E1-E7 remain distinct obligations.

Primary question: does persistence add useful information beyond transaction attributes and structural graph controls under a locked temporal protocol? Primary metric: illicit average precision. Primary comparison: XGBoost X+S+P minus X+S; five fixed seeds. Partitions: 1-30 training, 31-39 validation, 40-49 test. Unknown labels are never negative examples.

For a graph complex beta0=C, beta1=E-V+C and beta2=0. Flag complexes may fill graph cycles. Higher homology is only computed when cells support it. Filtrations are nested by maximum edge/face values. Essential intervals have no fabricated death. The main graph learner sees bounded historical ego neighborhoods, not a global future graph. Within-step order and historical label availability cannot be certified from this release.

X: 15 explicitly named transaction-record fields. S: size, edges, components, density, degree moments, triangles, clustering and cycle rank. B: static Betti counts and normalized cycle rank. P: finite persistence lifetime statistics/entropy, essential counts, fixed Betti curves and fixed Gaussian images. H: two-layer GraphSAGE or GAT representations. The gated candidate uses q=Enc_graph([x,s,h]), u=Enc_topo(T), g=sigmoid(W[q,u]+b), f=g*q+(1-g)*u. q and u share dimension 32. No new topology theorem or first-ever PH/GAT claim is made.

All deviations and unresolved ambiguities are recorded in `docs/change_log.md`. The traceability CSV indexes numbered/bulleted obligations by source line and implementation area; it is an inventory, not proof of satisfaction. The unabridged master prompt supplies prose obligations not separately tokenized in that inventory.

Completion requires real E1-E7 evidence or an explicit blocker, verified claim-level references, independent review, journal instructions, author declarations and verified manuscript rendering. A runnable implementation alone does not satisfy these gates.
'''
    (ROOT/'docs/research_specification.md').write_text(text,encoding='utf-8')
    registry=[]
    for name in SAFE_FIELDS:
        registry.append({'feature':name,'group':'X','earliest_observation':'transaction record at step close (assumption)','transform':'training median + standardization','limitation':'exact source extraction timestamps unavailable'})
    for group,names in [('S',['nodes','edges','components','density','degree_mean','degree_std','degree_max','triangles','clustering','cycle_rank']),('B',['beta0','beta1','beta1_per_edge']),('P',['finite_count','essential_count','lifetime_mean','lifetime_max','entropy','betti_curve','persistence_image'])]:
        for name in names:registry.append({'feature':name,'group':group,'earliest_observation':'historical neighborhood at target step close','transform':'training standardization','limitation':'B is algebraically redundant with S' if group=='B' else 'bounded undirected projection; graph-construction dependence'})
    with (ROOT/'docs/feature_registry.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=registry[0]);w.writeheader();w.writerows(registry)
    # Approve only sources whose specific use has been checked, not all DOI leads.
    resolved=(ROOT/'literature/resolved_metadata.bib').read_text(encoding='utf-8')
    entries=re.split(r'\n\n(?=@article)',resolved)
    approved=[entry for entry in entries if entry.startswith(('@article{lead26,','@article{lead36,'))]
    approved.extend([
      '@inproceedings{elmougy2023, title={Demystifying Fraudulent Transactions and Illicit Nodes in the Bitcoin Network for Financial Forensics}, author={Elmougy, Youssef and Liu, Ling}, booktitle={Proceedings of the 29th ACM SIGKDD Conference on Knowledge Discovery and Data Mining}, year={2023}, doi={10.1145/3580305.3599803}}',
      '@misc{bellei2024, title={The Shape of Money Laundering: Subgraph Representation Learning on the Blockchain with the Elliptic2 Dataset}, author={Bellei, Claudio and Xu, Muhua and Phillips, Ross and Robinson, Tom and Weber, Mark and Kaler, Tim and Leiserson, Charles E. and Arvind and Chen, Jie}, year={2024}, eprint={2404.19109}, archivePrefix={arXiv}, url={https://arxiv.org/abs/2404.19109}}',
      '@misc{hamilton2017, title={Inductive Representation Learning on Large Graphs}, author={Hamilton, William L. and Ying, Rex and Leskovec, Jure}, year={2017}, eprint={1706.02216}, archivePrefix={arXiv}, url={https://arxiv.org/abs/1706.02216}}',
      '@misc{velickovic2018, title={Graph Attention Networks}, author={Velickovic, Petar and Cucurull, Guillem and Casanova, Arantxa and Romero, Adriana and Lio, Pietro and Bengio, Yoshua}, year={2018}, eprint={1710.10903}, archivePrefix={arXiv}, url={https://arxiv.org/abs/1710.10903}}',
      '@misc{weber2019, title={Anti-Money Laundering in Bitcoin: Experimenting with Graph Convolutional Networks for Financial Forensics}, author={Weber, Mark and Domeniconi, Giacomo and Chen, Jie and Weidele, Daniel Karl I. and Bellei, Claudio and Robinson, Tom and Leiserson, Charles E.}, year={2019}, eprint={1908.02591}, archivePrefix={arXiv}, url={https://arxiv.org/abs/1908.02591}}'
    ])
    (ROOT/'literature/verified_references.bib').write_text('\n\n'.join(approved),encoding='utf-8')
    novelty=[['Work','Domain/task','Topology contribution','Temporal protocol relevance','TopoAML implication','Source'],
      ['PHGAT (2026)','IIoT anomaly detection','Persistent homology with GAT','Different dynamic sensor task','PH + GAT is prior art','https://doi.org/10.1016/j.eswa.2025.129923'],
      ['Grounded PPH (2025)','Weighted directed graphs','New directed invariant and stability','Not Bitcoin-specific','Undirected Rips is not grounded PPH','https://doi.org/10.1007/s10208-024-09679-2'],
      ['Elliptic++ (2023)','Transaction and wallet AML','Graph benchmark','49 coarse steps','Overlap with original Elliptic','https://doi.org/10.1145/3580305.3599803'],
      ['Elliptic2 (2024)','Subgraph AML','Subgraph representation benchmark','Separate official split required','External task, not node replication','https://arxiv.org/abs/2404.19109'],
      ['GraphSAGE (2017)','Node representation','Inductive aggregation','Supports unseen-node representations','Baseline, not new component','https://arxiv.org/abs/1706.02216'],
      ['GAT (2018)','Node classification','Neighborhood attention','Inductive/transductive settings','Baseline, not new component','https://arxiv.org/abs/1710.10903'],
      ['TopoAML (current)','Bitcoin transaction AML','Fixed persistence + structural controls','Step-close future holdout','Application/evaluation contribution only','Local specification and measured outputs']]
    (ROOT/'literature/novelty_matrix.json').write_text(json.dumps(novelty,indent=2),encoding='utf-8')
    print(f'{len(rows)} requirement inventory entries; feature registry and approved bibliography written')

if __name__=='__main__':main()
