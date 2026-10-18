# Mathematical validation

The test log in `results/tests.xml` records actual pytest results. Tests cover empty/isolated/disconnected graphs, paths and trees, unfilled cycles, filled triangles, hollow/filled tetrahedra, known weighted persistence, DAGs with undirected cycles, boundary-squared-zero mod 2, filtration face compatibility, empty/essential descriptors, future-edge invariance, bounded neighborhoods, training-only transforms, graph-model forward/backward passes and paired evaluation identity.

GUDHI computes persistence over the default field in tests and F2 in the empirical extraction; all listed example Betti numbers are field-independent. Static graph Betti counts are independently compared with NetworkX cycle bases. Tests passing validate the implemented cases, not every possible large complex or the empirical novelty of TopoAML.
