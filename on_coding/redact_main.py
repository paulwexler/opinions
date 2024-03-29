'''
This filter redacts passwords and IP addresses
'''
import redact

'''
Replace the password first because it may contain an IP.
'''
REDACTION = redact.Redaction(
        replace_password=redact.Replacer(
                pattern_string=r'(?i)("password": ?)"(.*?)"',
                repl=r'\1"REDACTED"'),
        replace_ip=redact.Replacer(
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
                        '.' if c == '.' else 'X'
                                for c in match.group(1))))

if __name__ == '__main__':  # pragma: no cover
    import sys

    redact.LineRedactor(sys.stdin, sys.stdout, REDACTION)()
