'''
This filter redacts passwords and IP addresses
'''

import re

class Replacer:
    '''
    Wrap re.sub
    '''
    def __init__(self, pattern_string, repl):
        self.pattern = re.compile(pattern_string)
        self.repl = repl

    def __call__(self, string):
        return self.pattern.sub(self.repl, string)


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
        raise NotImplementedError


class LineRedactor(LineFilter):
    '''
    This filter redacts each line
    '''
    replace_ip = Replacer(
            # With an abundance of caution,
            # the word delimiter "\b" which might normally
            # delimit a regex for an IP address, is omitted here.
            pattern_string=(
                    r'('
                    r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)'
                    r'('
                    r'\.'
                    r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)'
                    r'){3}'
                    r')'),
            repl=lambda match: ''.join(
                    '.' if c == '.' else 'X' for c in match.group(1)))
    replace_password = Replacer(
            pattern_string=r'(?i)("password": )"(.*?)"',
            repl=r'\1"REDACTED"')

    def filter(self, line):
        '''
        return filtered `line`
        '''
        return self.replace_ip(self.replace_password(line))


if __name__ == '__main__':
    import sys
    LineRedactor(sys.stdin, sys.stdout)()
