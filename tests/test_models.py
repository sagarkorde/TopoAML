import pytest
import torch
from torch_geometric.data import Data, Batch
from topoaml.models import TopoGraph


@pytest.mark.parametrize('backbone',['gat','sage'])
@pytest.mark.parametrize('fusion',['none','concat','gated'])
def test_forward_backward(backbone,fusion):
    graphs=[Data(x=torch.randn(3,5),edge_index=torch.tensor([[0,1],[1,2]]),topology=torch.randn(1,4)) for _ in range(2)]
    model=TopoGraph(5,4,backbone=backbone,fusion=fusion)
    out=model(Batch.from_data_list(graphs))
    assert out.shape==(2,)
    loss=torch.nn.functional.binary_cross_entropy_with_logits(out,torch.tensor([0.,1.]))
    loss.backward()
    assert torch.isfinite(loss)
