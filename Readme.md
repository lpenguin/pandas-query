# Pandas-query module
```python
import pandas as pd
from pandas_query import _

really_long_name_dataframe = pd.DataFrame({'ints': range(10)})
```

## Assigning new columns
```python
# Instead of 
really_long_name_dataframe['mul10'] = really_long_name_dataframe['ints'] * 10
really_long_name_dataframe['squares'] = really_long_name_dataframe['ints'] ** 2

# Write shorter
really_long_name_dataframe['mul10'] = _['ints'] * 10
really_long_name_dataframe['squares'] = _['ints'] ** 2
```

## Indexing

```python
# Instead of
subset = really_long_name_dataframe[
    really_long_name_dataframe[['ints'].between(3, 6) 
    & (really_long_name_dataframe[['mul10'] != 40)
]

# Write shorter
subset = really_long_name_dataframe[
    _['ints'].between(3, 6) 
    & (_['mul10'] != 40)
]

```
## Evaluating expressions
```python
# Instead of
cubes = (
    really_long_name_dataframe['ints'] * really_long_name_dataframe['squares'] 
)

# Write shorter
cubes = (
    really_long_name_dataframe(_['ints'] * _['squares']) 
)
```
