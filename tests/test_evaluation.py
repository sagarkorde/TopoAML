import numpy as np
from topoaml.evaluation import choose_threshold,metrics,block_bootstrap


def test_perfect_prediction_and_threshold():
    y=np.array([0,0,1,1]);p=np.array([.1,.2,.8,.9])
    threshold=choose_threshold(y,p)
    assert metrics(y,p,threshold)['f1']==1
    assert metrics(y,p,threshold)['average_precision']==1


def test_paired_bootstrap_identity():
    y=np.tile([0,1],10);p=np.tile([.1,.8],10);blocks=np.repeat(np.arange(10),2)
    out=block_bootstrap(y,p,p,blocks,repetitions=100)
    assert out['delta']==0 and out['ci95']==[0.,0.]
