import pandas as pd

from pandas_query.operator import Operator
from pandas.core.indexing import _LocIndexer
_patched = False


def patch_pandas():
    global _patched
    if _patched:
        print('Pandas already patched')
        return
    pd.DataFrame.__call__ = lambda self, op: op.apply_op(self)

    last_get_item = pd.DataFrame.__getitem__

    def apply_if_op(df, op):
        if isinstance(op, Operator):
            return op.apply_op(df)
        return op

    def op_get_item(self, op):
        return last_get_item(self, apply_if_op(self, op))

    pd.DataFrame.__getitem__ = op_get_item


    last_indexer_get_item = _LocIndexer.__getitem__

    def op_log_indexer_get_item(self, key):
        df = self.obj
        if isinstance(key, tuple):
            k1, k2 = key
            k1 = apply_if_op(df, k1)
            k2 = apply_if_op(df, k2)
            return last_indexer_get_item(self, (k1, k2))
        else:
            key = apply_if_op(df, key)
            return last_indexer_get_item(self, key)

    _LocIndexer.__getitem__ = op_log_indexer_get_item
    _patched = True

patch_pandas()