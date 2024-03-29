'''
classes to redact files

>>> redaction = Redaction(
            replacer1=Replacer(pattern_string=, repl=), ...)
>>> LineRedactor(infile, outfile, redaction)()
'''

# pylint: disable=too-few-public-methods

import re

class Replacer:
    '''
    Wrap re.sub
    >>> replacer = Replacer(pattern_string, repl)
    >>> result_string = replacer(input_string)
    '''
    def __init__(self, pattern_string, repl):
        self.pattern = re.compile(pattern_string)
        self.repl = repl

    def __call__(self, string):
        return self.pattern.sub(self.repl, string)


class Redaction(dict):
    '''
    A dict of Replacer that reduces a given line by them
    when called.
    '''
    def __call__(self, line):
        '''
        return filtered `line`
        Reduce `line` by all the replacers.
        '''
        for replacer in self.values():
            line = replacer(line)
        return line

    def __setitem__(self, key, value):
        assert isinstance(value, Replacer)
        super().__setitem__(key, value)


class LineFilter:
    '''
    Filter infile a line at a time, write filtered line to outfile.
    '''
    def __init__(self, infile, outfile):
        self.infile = infile
        self.outfile = outfile

    def __call__(self):
        for line in self.infile:
            self.outfile.write(self.filter(line))

    def filter(self, line):
        '''
        return filtered `line`
        '''
        raise NotImplementedError   # pragma: no cover


class LineRedactor(LineFilter):
    '''
    This filter redacts each line
    '''
    def __init__(self, infile, outfile, redaction: Redaction):
        super().__init__(infile, outfile)
        self.redaction = redaction

    def filter(self, line):
        '''
        return redacted `line`
        '''
        return self.redaction(line)
