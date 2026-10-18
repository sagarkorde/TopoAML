# Research specification

The authoritative specification is the original proposal, preserved as `TopoAML_Complete_Research_Proposal.docx`, and the complete user brief in `docs/master_prompt.md`. The proposal is fully extracted in `docs/proposal_extracted.txt`; both remain available to audit this implementation. The title and H1-H6 are preserved. `docs/hypotheses.md` defines nulls, units, comparisons, effects and interpretation. E1-E7 remain distinct obligations.

Primary question: does persistence add useful information beyond transaction attributes and structural graph controls under a locked temporal protocol? Primary metric: illicit average precision. Primary comparison: XGBoost X+S+P minus X+S; five fixed seeds. Partitions: 1-30 training, 31-39 validation, 40-49 test. Unknown labels are never negative examples.

For a graph complex beta0=C, beta1=E-V+C and beta2=0. Flag complexes may fill graph cycles. Higher homology is only computed when cells support it. Filtrations are nested by maximum edge/face values. Essential intervals have no fabricated death. The main graph learner sees bounded historical ego neighborhoods, not a global future graph. Within-step order and historical label availability cannot be certified from this release.

X: 15 explicitly named transaction-record fields. S: size, edges, components, density, degree moments, triangles, clustering and cycle rank. B: static Betti counts and normalized cycle rank. P: finite persistence lifetime statistics/entropy, essential counts, fixed Betti curves and fixed Gaussian images. H: two-layer GraphSAGE or GAT representations. The gated candidate uses q=Enc_graph([x,s,h]), u=Enc_topo(T), g=sigmoid(W[q,u]+b), f=g*q+(1-g)*u. q and u share dimension 32. No new topology theorem or first-ever PH/GAT claim is made.

All deviations and unresolved ambiguities are recorded in `docs/change_log.md`. The traceability CSV indexes numbered/bulleted obligations by source line and implementation area; it is an inventory, not proof of satisfaction. The unabridged master prompt supplies prose obligations not separately tokenized in that inventory.

Completion requires real E1-E7 evidence or an explicit blocker, verified claim-level references, independent review, journal instructions, author declarations and verified manuscript rendering. A runnable implementation alone does not satisfy these gates.
