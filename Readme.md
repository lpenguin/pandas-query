# Pandas-query module
```python
import pandas as pd

really_long_name_dataframe = pd.DataFrame({'ints': range(10)})
really_long_name_dataframe['mul10'] = really_long_name_dataframe['ints'] * 10
really_long_name_dataframe['squares'] = really_long_name_dataframe['ints'] ** 2

really_long_name_dataframe
```
```
   ints  mul10  squares
0     0      0        0
1     1     10        1
2     2     20        4
3     3     30        9
4     4     40       16
5     5     50       25
6     6     60       36
7     7     70       49
8     8     80       64
9     9     90       81
```

```python
from pandas_query import _

really_long_name_dataframe[
    _['ints'].between(3, 6) & 
    (_['mul10'] != 40)
]
```
```
   ints  mul10  squares
3     3     30        9
5     5     50       25
6     6     60       36

```

```python
really_long_name_dataframe['cubes'] = really_long_name_dataframe(_['squares'] * _['ints'])
really_long_name_dataframe
```

```
 ints  mul10  squares  cubes
0     0      0        0      0
1     1     10        1      1
2     2     20        4      8
3     3     30        9     27
4     4     40       16     64
5     5     50       25    125
6     6     60       36    216
7     7     70       49    343
8     8     80       64    512
9     9     90       81    729
```

See [Example](./example.ipynb)