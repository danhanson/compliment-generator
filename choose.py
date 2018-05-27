from functools import reduce
from operator import mul

def count(item):
    if isinstance(item, str):
        return 1
    elif isinstance(item, (tuple, list)):
        return reduce(mul, (count(elem) for elem in item), 1)
    elif isinstance(item, Choose):
        return len(item)
    else:
        raise ValueError('invalid element found in semantic tree: {}'.format(repr(item)))

def get_choice(choice, i):
    if i < 0:
        raise IndexError
    if isinstance(choice, str):
        if i == 0:
            return choice
        else:
            raise IndexError
    elif isinstance(choice, (list,tuple)):
        if len(choice) == 0:
            if i == 0:
                return ''
            else:
                raise IndexError
        base = count(choice[1:])
        digit = i // base
        remainder = i - digit * base
        return '{}{}'.format(get_choice(choice[0], digit), get_choice(choice[1:], remainder))
    elif isinstance(choice, Choose):
        return choice[i]
    else:
        raise ValueError('invalid element found in semantic tree: {}'.format(repr(choice)))

class Choose(object):

    def __init__(self, *arguments):
        if len(arguments) == 1:
            if isinstance(arguments[0], str):
                self.choices = (arguments[0],'')
            else:
                self.choices = tuple(arguments[0])
        else:
            self.choices = tuple(arguments)
        self._len = sum(count(choice) for choice in self.choices)

    def __len__(self):
        return self._len

    def __repr__(self):
        return 'Choose({})'.format(len(self))

    def __getitem__(self, index):
        i = 0
        for choice in self.choices:
            choice_size = count(choice)
            if choice_size > index - i:
                return get_choice(choice, index - i)
            i += choice_size
        raise IndexError

