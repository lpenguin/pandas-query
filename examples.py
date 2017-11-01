import pandas as pd
import numpy as np
from pandas_query import _, F

df = pd.DataFrame({'ints': np.random.randint(0, 10, 20)})
df['squares'] = _['ints'] ** 2

t = (
    df
    .groupby('squares')
    .count()
    .assign(sqrt=_.index.map(np.sqrt).astype(int))
    .set_index(_.sqrt.map(str) + ' - ' + _.ints.map(str))
    [_['ints'].isin({1, 2 ,3})]
)
print(t)

print(
    df
    .assign(a=_.apply(F('{:02}: {:02}'.format, _['ints'], _['squares']), axis=1))
)
