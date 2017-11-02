from functools import partial
import operator


def get_item1(name, target):
    return target[name]


def apply_op(instance, op):
    if isinstance(op, Operator):
        return op._func(instance)
    return op


def apply_op_dict(instance, op_dict):
    return {
        key: apply_op(instance, value)
        for key, value in op_dict.items()
    }


def apply_op_list(instance, op_list):
    return [
        apply_op(instance, op)
        for op in op_list
    ]


def partial_op(op, function, *args, **kwargs):
    def wrapper(target):
        return function(apply_op(target, op), *args, **kwargs)
    return wrapper


def partial_op2(op1, op2, function):
    def wrapper(target):
        return function(apply_op(target, op1), apply_op(target, op2))
    return wrapper


def identity(x):
    return x


class Operator(object):
    def __init__(self, func, _str_rep='unknown sig'):
        self._func = func
        self._str_rep = _str_rep

    def __str__(self):
        return self._str_rep

    def __getitem__(self, item):
        return Operator(partial(get_item1, item), '%s[%s]' % (self, item))

    def __add__(self, other):
        return Operator(partial_op2(self, other, operator.add), '(%s + %s)' % (self, other))

    def __sub__(self, other):
        return Operator(partial_op2(self, other, operator.sub), '(%s - %s)' % (self, other))

    def __mul__(self, other):
        return Operator(partial_op2(self, other, operator.mul), '%s * %s' % (self, other))

    def __abs__(self):
        return Operator(partial_op(self, operator._abs), 'abs(%s)' % self)

    def __pow__(self, power, modulo=None):
        return Operator(partial_op2(self, power, operator.pow), '%s ** %s' % (self, power))

    def __neg__(self):
        return Operator(partial_op(self, operator.neg), '-%s' % (self))

    def __invert__(self):
        return Operator(partial_op(self, operator.inv))

    def __floordiv__(self, other):
        return Operator(partial_op2(self, other, operator.floordiv), '%s // %s' % (self, other))

    def __truediv__(self, other):
        return Operator(partial_op2(self, other, operator.truediv), '%s / %s' % (self, other))

    def __mod__(self, other):
        return Operator(partial_op2(self, other, operator.mod))

    def __or__(self, other):
        return Operator(partial_op2(self, other, operator.or_))

    def __and__(self, other):
        return Operator(partial_op2(self, other, operator.and_))

    def __ne__(self, other):
        return Operator(partial_op2(self, other, operator.ne))

    def __eq__(self, other):
        return Operator(partial_op2(self, other, operator.eq))

    def __gt__(self, other):
        return Operator(partial_op2(self, other, operator.gt))

    def __lt__(self, other):
        return Operator(partial_op2(self, other, operator.lt))

    def __ge__(self, other):
        return Operator(partial_op2(self, other, operator.ge))

    def __le__(self, other):
        return Operator(partial_op2(self, other, operator.le))

    def __call__(self, *args, **kwargs):
        return Operator(lambda t: self._func(t).__call__(*args, **kwargs), '%s(%s)' % (self, (args, kwargs)))

    def __getattr__(self, item):
        def ga(target, item):
            return getattr(target, item)
        return Operator(partial_op(self, ga, item), '%s.%s' % (self, item))


def F(func, *args, **kwargs):
    def wrapper(target):
        loc_args = apply_op_list(target, args)
        loc_kwargs = apply_op_dict(target, kwargs)
        return func(*loc_args, **loc_kwargs)
    return Operator(wrapper, '<func>(%s, %s)' % (', '.join(map(str, args,)), '**kwargs'))

Op = Operator
_ = Operator(identity, '_')