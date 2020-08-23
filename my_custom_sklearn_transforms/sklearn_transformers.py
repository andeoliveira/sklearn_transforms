from sklearn.base import BaseEstimator, TransformerMixin


# All sklearn Transforms must have the `transform` and `fit` methods
class DropColumns(BaseEstimator, TransformerMixin):
    def __init__(self, columns):
        self.columns = columns

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        # Primeiro realizamos a cópia do dataframe 'X' de entrada
        data = X.copy()
        # Retornamos um novo dataframe sem as colunas indesejadas
        return data.drop(labels=self.columns, axis='columns')

# Classe AlterValueColumn altera o valor de uma ou mais colunas
class AlterValueColumn (BaseEstimator, TransformerMixin):
    def __init__(self, columns, valuesearch, trendmeasure=None, groupcolumn=None, valueupdate=None):
        self.columns = columns
        self.valuesearch = valuesearch
        self.trendmeasure = trendmeasure if trendmeasure is not None else None
        self.groupcolumn = groupcolumn if groupcolumn is not None else None
        self.valueupdate = valueupdate if valueupdate is not None else None
        
            
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        # Cópia do DF
        data = X.copy()
        for feature_df in self.columns :
            if self.groupcolumn is None:
                data.loc[data[feature_df] >= self.valuesearch, feature_df] = self.valueupdate
            else :
                data.loc[data[feature_df] == self.valuesearch, feature_df] = data.groupby(self.groupcolumn)[feature_df].transform(self.trendmeasure)
        # Retorna um novo dataframe sem as colunas alteradas
        return data

# Classe FillMeasureByColumn completa uma coluna ou mais, com a média dos valor agrupados em uma característica
class FillMeasureByColumn (BaseEstimator, TransformerMixin):
    def __init__(self, columns, groupcolumn, trendmeasure):
        self.columns = columns
        self.groupcolumn = groupcolumn
        self.trendmeasure = trendmeasure

    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        # Cópia do DF 
        data = X.copy()
        for feature_df in self.columns :
            data[feature_df] = data.groupby(self.groupcolumn)[feature_df].transform(lambda x: x.fillna(x.mean()) if self.trendmeasure == 'mean' else x.fillna(x.mode()[0]))
        # Retorna um novo data frame com a coluna preenchida
        return data