import pandas as pd
import numpy as np
from pandas_query import _

some_dataframe = pd.DataFrame({'ints': np.random.randint(1, 10, 200)})
some_dataframe['squares'] = _['ints'] ** 2  # Column assignment, .__setitem__() function

print(
    some_dataframe
    .groupby('squares')
    .count()
    .assign(sqrt=_.index.map(np.sqrt).astype(int))  # .assign() function
    .set_index(_.sqrt.map(str) + ' - ' + _.ints.map(str))  # .set_index() function
    [_['ints'].between(1, 20)]  # Selecting data, .__getitem__() function
    (_['sqrt'].map(np.log10) * _['ints'])  # Evaluating expressions, .__call__() function
)
