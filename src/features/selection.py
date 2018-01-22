import os
import pandas as pd
from pandas import Series, DataFrame

def find_important_variables(X=DataFrame(), y=Series(), verbose=True):
    """
    """
    try:
        if verbose: 
            print "Importing Libraries..."
        from sklearn.preprocessing import StandardScaler
        from sklearn.feature_selection import SelectKBest, f_classif
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.tree import ExtraTreeClassifier
        from sklearn.svm import LinearSVC
        from sklearn.linear_model import LogisticRegression

        if verbose: 
            print "There are {} variables.".format(X.shape[1])

        zv = \
        (X
         .std()
         .where(lambda sd: sd==0)
         .dropna()
         .index
         .tolist())
        X.drop(zv, axis=1, inplace=True)
        if verbose: 
            print "There are {} Zero Variance Predictors. Ignoring these...".format(len(zv))

        missings = \
        (X
         .isnull()
          .mean()
          .where(lambda x: x > 0.9)
          .dropna()
          .index
          .tolist())
        if verbose: 
            print "There are {} Variables with over 90% missing data. Ignoring these...".format(len(missings))
        X.drop(missings, axis=1, inplace=True)

        if verbose: 
            print "Now there are {} variables.".format(X.shape[1])
        if verbose: 
            print "Scaling Data (filling missings with Zeros.)..."
        scale = StandardScaler()
        X.fillna(0, inplace=True)

        scale.fit(X)
        X_scaled = scale.transform(X)
        
        print "Finished."
        
        if verbose: 
            print "Calculating % difference in means..."
        importance = \
        DataFrame(
            DataFrame(X_scaled)
            .groupby(y)
            .mean()
            .apply(lambda c: 0 if c.loc[1] == 0 else (c.loc[0] - c.loc[1])/float(c.loc[1]))
        )

        print "Finished."
        
        importance.index = X.columns
        importance.columns = ['per_diff_means']
        all_cols = importance.index.tolist()

        if verbose: 
            print "Calculating f-scores and p-values..."
        fvals = \
        Series(SelectKBest(k='all', score_func=f_classif).fit(X_scaled, y).scores_, 
               index=all_cols,
               name='f_values')

        pvals = \
        Series(SelectKBest(k='all', score_func=f_classif).fit(X_scaled, y).pvalues_, 
               index=all_cols,
               name='p_values')

        if verbose: 
            print "Fitting default regression-based models and calculating standardized coefficients..."
        log_coefs = \
        Series(LogisticRegression().fit(X_scaled, y).coef_[0],
               index=all_cols,
               name='std_betas')

        svc_coefs = \
        Series(LinearSVC().fit(X_scaled, y).coef_[0],
               index=all_cols,
               name='svc_coefs')

        if verbose: 
            print "Fitting default tree-based models and finding feature importances..."
        extr_fis = \
        Series(ExtraTreeClassifier().fit(X_scaled, y).feature_importances_,
               index=all_cols,
               name='rafo_imps')

        rafo_fis = \
        Series(RandomForestClassifier().fit(X_scaled, y).feature_importances_,
               index=all_cols,
               name='xtree_imps')

        if verbose: 
            print "Putting them all together..."
        var_imps = \
        (pd.concat([fvals, 
                    pvals, 
                    log_coefs, 
                     svc_coefs, 
                     extr_fis, 
                     rafo_fis], axis=1)
         .assign(avg_rank = lambda df: df.apply(lambda c: c.rank()).mean(axis=1)))

        if verbose: 
            print "{} variables have a p-value under 0.05".format(var_imps.query("p_values < 0.05").shape[0])
            print "Returning variable importance ranks in a DataFrame..."
            print "\nNote that a higher Average Rank of Variables is better.\n"
            print "Here are the first few variables..."
            print var_imps.sort_values("avg_rank", ascending=False).loc[:, 'avg_rank'].iloc[:5].round(1)
        return var_imps
    except:
        print "Oops! Something went wrong. Try again."
        pass