"""GraphSAGE/GAT, concatenation and candidate gated topology fusion."""
import torch
from torch import nn
from torch_geometric.nn import SAGEConv, GATConv


class TopoGraph(nn.Module):
    def __init__(self,input_dim,topology_dim=0,hidden=32,backbone='gat',fusion='none'):
        super().__init__()
        if fusion not in ('none','concat','gated'):raise ValueError(fusion)
        self.fusion=fusion
        conv=SAGEConv if backbone=='sage' else GATConv
        self.conv1=conv(input_dim,hidden); self.conv2=conv(hidden,hidden)
        self.graph_encoder=nn.Sequential(nn.Linear(hidden+input_dim,hidden),nn.ReLU())
        if fusion!='none':
            if topology_dim<1:raise ValueError('Fusion requires topology')
            self.topology_encoder=nn.Sequential(nn.Linear(topology_dim,hidden),nn.ReLU(),nn.Linear(hidden,hidden))
            self.gate=nn.Linear(2*hidden,hidden)
        self.head=nn.Sequential(nn.Linear(hidden*(2 if fusion=='concat' else 1),hidden),nn.ReLU(),nn.Linear(hidden,1))

    def forward(self,data):
        h=torch.relu(self.conv1(data.x,data.edge_index))
        h=torch.relu(self.conv2(h,data.edge_index))
        # Every graph in a batch is a target-centered historical neighborhood.
        center=data.ptr[:-1] if hasattr(data,'ptr') else torch.zeros(1,dtype=torch.long,device=h.device)
        q=self.graph_encoder(torch.cat([data.x[center],h[center]],dim=-1))
        if self.fusion!='none':
            u=self.topology_encoder(data.topology)
            if self.fusion=='gated':
                gate=torch.sigmoid(self.gate(torch.cat([q,u],dim=-1)))
                q=gate*q+(1-gate)*u
            else:q=torch.cat([q,u],dim=-1)
        return self.head(q).flatten()
