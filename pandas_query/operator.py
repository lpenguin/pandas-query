from functools import partial
import operator


def get_item1(name, target):
    return target[name]


def partial_op2(op1, op2, function):
    def wrapper(target):
        if isinstance(op1, Operator):
            r1 = op1.apply_op(target)
        else:
            r1 = op1
        if isinstance(op2, Operator):
            r2 = op2.apply_op(target)
        else:
            r2 = op2
        return function(r1, r2)
    return wrapper


def identity(x):
    return x


class Operator(object):
    def __init__(self, func):
        self.func = func

    def apply_op(self, target):
        return self.func(target)

    def __getitem__(self, item):
        return Operator(partial(get_item1, item))

    def __add__(self, other):
        return Operator(partial_op2(self, other, operator.add))

    def __sub__(self, other):
        return Operator(partial_op2(self, other, operator.sub))

    def __mul__(self, other):
        return Operator(partial_op2(self, other, operator.mul))

    def __abs__(self):
        return Operator(partial(operator._abs))

    def __neg__(self):
        return Operator(partial(operator.neg))

    def __truediv__(self, other):
        return Operator(partial_op2(self, other, operator.truediv))

    def __divmod__(self, other):
        return Operator(partial_op2(self, other, operator.floordiv))

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

_ = Operator(identity)