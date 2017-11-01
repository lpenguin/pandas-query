import pandas as pd
from sys import stderr

from pandas_query.operator import Operator, apply_op, apply_op_dict, apply_op_list
from pandas.core.indexing import _LocIndexer
_patched = False


def patch_method(pandas_object, method_name):
    def wrapper(func):
        orig_method = None
        if hasattr(pandas_object, method_name):
            orig_method = getattr(pandas_object, method_name)
        def new_method(instance, *args, **kwargs):
            return func(orig_method, instance, *args, **kwargs)
        setattr(pandas_object, method_name, new_method)
    return wrapper


def patch_pandas():
    global _patched
    if _patched:
        stderr.write('Pandas already patched\n')
        return

    @patch_method(pd.DataFrame, '__call__')
    def df_call(orig_method, instance, op):
        return op._func(instance)

    @patch_method(pd.DataFrame, '__getitem__')
    def df_getitem(orig_method, instance, op):
        return orig_method(instance, apply_op(instance, op))

    @patch_method(pd.DataFrame, '__setitem__')
    def df_set_item(orig_method, instance, name, op):
        value = apply_op(instance, op)
        return orig_method(instance, name, value)

    @patch_method(_LocIndexer, '__getitem__')
    def loc_indexer_getitem(orig_method, instance, key):
        df = instance.obj
        if isinstance(key, tuple):
            k1, k2 = key
            key = (apply_op(df, k1), apply_op(df, k2))
        else:
            key = apply_op(df, key)
        return orig_method(instance, key)

    @patch_method(pd.DataFrame, 'assign')
    def df_assign(orig_method, instance, **kwargs):
        kwargs = apply_op_dict(instance, kwargs)
        return orig_method(instance, **kwargs)

    @patch_method(pd.DataFrame, 'set_index')
    def df_set_index(orig_method, instance, keys, *args, **kwargs):
        if isinstance(keys, list):
            keys = apply_op_list(instance, keys)
        else:
            keys = apply_op(instance, keys)

        return orig_method(instance, keys, *args, **kwargs)

    @patch_method(pd.DataFrame, 'apply')
    def df_apply(orig_method, instance, func_op, *args, **kwargs):
        def wrapper(target):
            return apply_op(target, func_op)

        return orig_method(instance, wrapper, *args, **kwargs)

    _patched = True

patch_pandas()
