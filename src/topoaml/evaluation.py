import numpy as np
from sklearn.metrics import average_precision_score, roc_auc_score, precision_recall_curve, f1_score, precision_score, recall_score, balanced_accuracy_score, brier_score_loss, roc_curve


def choose_threshold(y,p):
    precision,recall,thresholds=precision_recall_curve(y,p)
    f1=2*precision[:-1]*recall[:-1]/np.maximum(precision[:-1]+recall[:-1],1e-12)
    return float(thresholds[np.argmax(f1)])


def metrics(y,p,threshold=.5):
    y=np.asarray(y); p=np.asarray(p); pred=p>=threshold
    fpr,tpr,_=roc_curve(y,p)
    bins=np.minimum((p*10).astype(int),9)
    ece=sum(np.mean(bins==i)*abs(y[bins==i].mean()-p[bins==i].mean()) for i in range(10) if np.any(bins==i))
    return {'average_precision':float(average_precision_score(y,p)), 'roc_auc':float(roc_auc_score(y,p)),
            'precision':float(precision_score(y,pred,zero_division=0)), 'recall':float(recall_score(y,pred,zero_division=0)),
            'f1':float(f1_score(y,pred)), 'balanced_accuracy':float(balanced_accuracy_score(y,pred)),
            'recall_at_fpr_01':float(max(tpr[fpr<=.01],default=0)),
            'precision_at_100':float(y[np.argsort(-p,kind='stable')[:100]].mean()),
            'brier':float(brier_score_loss(y,p)), 'ece_10':float(ece)}


def block_bootstrap(y,a,b,blocks,seed=2026,repetitions=2000):
    """Paired test-time uncertainty conditional on fitted models; no seed CI."""
    rng=np.random.default_rng(seed); blocks=np.asarray(blocks); unique=np.unique(blocks)
    indices={u:np.flatnonzero(blocks==u) for u in unique}; differences=[]
    y,a,b=map(np.asarray,(y,a,b))
    for _ in range(repetitions):
        idx=np.concatenate([indices[u] for u in rng.choice(unique,len(unique),replace=True)])
        if len(np.unique(y[idx]))<2:continue
        differences.append(average_precision_score(y[idx],a[idx])-average_precision_score(y[idx],b[idx]))
    return {'delta':float(average_precision_score(y,a)-average_precision_score(y,b)),
            'ci95':np.quantile(differences,[.025,.975]).tolist(), 'blocks':len(unique),
            'replicates':len(differences),'scope':'conditional on fitted models; temporal blocks do not eliminate all graph dependence'}
