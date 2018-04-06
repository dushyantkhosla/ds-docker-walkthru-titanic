from pandas import DataFrame, Series
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.metrics import accuracy_score, recall_score, precision_score, roc_auc_score, f1_score
from sklearn.model_selection import cross_val_score, cross_val_predict



def run_classifier(X=DataFrame(), y=Series(), UNCORR=[], TEST_SIZE=0.2, CLF='', GRID={}, SCORING='roc_auc'):
    """
    Input:
        Data, List of Important+Uncorrelated variables
        Pipeline
        Grid
        Performance Metric

    How it works:
        Splits the data into Train and Test
        Runs GridSearchCV over the Train set to find the best model automatically (across folds of the train set)
        Calculates OOS scores (over the test set) using this best model

    Returns:
        The best model
        Scores
        Predicted Labels, Probabilities
    """
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=TEST_SIZE)

    X_tr = DataFrame(X_tr, columns=X_tr.columns).loc[:, UNCORR].fillna(0)
    X_te = DataFrame(X_te, columns=X_te.columns).loc[:, UNCORR].fillna(0)

    gscv = \
    GridSearchCV(
        estimator=CLF,
        param_grid=GRID,
        scoring=SCORING,
        verbose=False,
        cv=5)

    gscv.fit(X_tr, y_tr)
    y_pred = gscv.predict(X_te)
    y_prob = DataFrame(gscv.predict_proba(X_te)).loc[:, 1]

    return {
        'model': gscv,
        'train_score': gscv.best_score_,
        'test_score__accuracy': accuracy_score(y_te, y_pred),
        'test_score__recall': recall_score(y_te, y_pred),
        'test_score__precision': precision_score(y_te, y_pred),
        'test_score__roc_auc': roc_auc_score(y_te, y_pred),
        'test_score__f1': f1_score(y_te, y_pred),
        'y_prob': y_prob,
        'y_te': y_te
    }