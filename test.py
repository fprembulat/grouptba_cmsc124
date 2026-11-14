from SyntaxAnalyzer import syntax

tests = [
    # 1. Valid switch with OMG
    ['START', 'WTF', 'OMG', 'NUM', 'PRINT', 'YARN', 'OIC', 'END'],

    # 2. Valid switch with OMGWTF
    ['START', 'WTF', 'OMG', 'NUM', 'OMGWTF', 'PRINT', 'YARN', 'OIC', 'END'],

    # 3. Missing OMG
    ['START', 'WTF', 'OMGWTF', 'OIC', 'END'],

    # 4. OMG without a value
    ['START', 'WTF', 'OMG', 'NEWLINE', 'OIC', 'END'],

    # 5. Duplicate OMGWTF
    ['START', 'WTF', 'OMG', 'NUM', 'OMGWTF', 'OMGWTF', 'OIC', 'END'],

    # 6. OMG after OMGWTF
    ['START', 'WTF', 'OMG', 'NUM', 'OMGWTF', 'OMG', 'NUM', 'OIC', 'END'],

    # 7. Missing OIC
    ['START', 'WTF', 'OMG', 'NUM', 'END'],

    # 8. Invalid statement inside WTF
    ['START', 'WTF', 'OMG', 'NUM', 'GIMMEH', 'END'],

    # 9. Valid assignment inside OMG
    ['START', 'WTF', 'OMG', 'NUM', 'VAR', 'R', 'NUM', 'OIC', 'END'],

    # 10. Valid GTFO inside OMG
    ['START', 'WTF', 'OMG', 'NUM', 'GTFO', 'OIC', 'END']
]

for number, test in enumerate(tests, 1):
    try:
        syntax(test)
        print("Test", number, ": Accepted")
    except SyntaxError as e:
        print("Test", number, ": Rejected -", e)