import io

import redact

def test_no_change():
    intext = '''
            This string has
            nothing in it to substitute.'''
    expect = intext
    infile = io.StringIO(intext)
    outfile = io.StringIO()
    redact.LineRedactor(infile, outfile)()
    outtext = outfile.getvalue()
    assert expect == outtext, f'{expect} != {outtext}'
    
def test_changes():
    intext = '''
            This line has a password: "foo": "doo", "passworD": "PW"
            This line has one IP: 0.0.0.12 n0t.12.34.56 123'''
    expect = intext.replace('PW', 'REDACTED').replace('0.0.0.12', 'X.X.X.XX')
    infile = io.StringIO(intext)
    outfile = io.StringIO()
    redact.LineRedactor(infile, outfile)()
    outtext = outfile.getvalue()
    assert expect == outtext, f'{expect} != {outtext}'
