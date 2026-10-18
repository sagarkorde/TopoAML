import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import networkx as nx
from topoaml.data import ROOT


def export(fig,name):
    out=ROOT/'results/figures';out.mkdir(exist_ok=True)
    for extension in ['svg','pdf','png']:
        fig.savefig(out/f'{name}.{extension}',bbox_inches='tight',dpi=600)
    plt.close(fig)


def main():
    fig,ax=plt.subplots(figsize=(10,3));ax.axis('off')
    boxes=[('Historical inputs\nStep-close observation',.01),('Bounded ego graph\nStructural controls + PH',.27),('Matched predictors\nConcatenation / gate',.53),('Frozen future test\nPaired uncertainty',.79)]
    for text,x in boxes:
        ax.text(x,.55,text,transform=ax.transAxes,ha='left',va='center',fontsize=10,
                bbox=dict(boxstyle='round,pad=.6',facecolor='#e8eef5',edgecolor='#24476a'))
    for x in [.225,.485,.745]:
        ax.annotate('',xy=(x+.035,.55),xytext=(x,.55),xycoords='axes fraction',arrowprops=dict(arrowstyle='->',color='#24476a',lw=1.5))
    ax.text(.02,.12,'Train 1-30  |  Validate 31-39  |  Test 40-49\nTraining-only transforms; unknown labels excluded from supervised loss',transform=ax.transAxes,fontsize=10)
    export(fig,'methodology')
    fig,axes=plt.subplots(1,3,figsize=(10,3))
    g=nx.DiGraph([(0,1),(0,2),(1,3),(2,3)]);pos={0:(0,0),1:(1,1),2:(1,-1),3:(2,0)}
    nx.draw(g,pos,ax=axes[0],with_labels=True,node_color='#8fb2d5',arrows=True,node_size=550)
    nx.draw(g.to_undirected(),pos,ax=axes[1],with_labels=True,node_color='#8fb2d5',node_size=550)
    triangle=nx.complete_graph(3);tpos={0:(0,0),1:(1,0),2:(.5,.9)}
    axes[2].fill([0,1,.5],[0,0,.9],color='#c7d8e9');nx.draw(triangle,tpos,ax=axes[2],node_color='#8fb2d5',with_labels=True,node_size=550)
    axes[0].set_title('Directed acyclic dependency');axes[1].set_title('Undirected graph: beta1 = 1');axes[2].set_title('Filled triangle: beta1 = 0')
    fig.text(.5,-.02,'Illustrative mathematics: an undirected cycle does not establish circular transfers or illicit conduct.',ha='center',fontsize=10)
    export(fig,'topology_interpretation')

if __name__=='__main__':main()
