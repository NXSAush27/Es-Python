# -*- coding: utf-8 -*-
from isort import check_file

import testlib
import isrecursive2
import os
import sys

import nary_tree, tree
from testlib import my_print, COL, check_expected

#############################################################################
#### Mettete DEBUG=True per disattivare i test di ricorsione  e
#### fare debug delle funzioni più facilmente attivando stack trace
DEBUG = True
#DEBUG = False
#############################################################################

################################################################################
# --- IL CODICE SORGENTE DI SEGUITO È ESCLUSIVAMENTE PER EFFETTUARE I TEST --- #
# ------- L'uso delle funzioni seguenti nel vostro programma è vietato --------#
################################################################################

############ check that you have renamed the file as program.py   ###########
if not os.path.isfile('program.py'):
    print(  'WARNING: Save program.empty.py as program.py\n'
            'ATTENZIONE: salvare program.vuoto.py con nome program.py')
    sys.exit(0)
#############################################################################
if DEBUG:
    # import classico senza decorazioni
    import program
else:
    # import del file decorato in modo che possa accorgersi della ricorsione
    modulename = 'program'
    decorated_code = isrecursive2.decorate_file(f"{modulename}.py")
    program = isrecursive2.import_from_string(modulename, decorated_code)

################################################################################

def test_personal_data_entry(run=True):
    assert program.nome      != 'NOME', f"{COL['YELLOW']}ERRORE: Indica il tuo NOME in program.py{COL['RST']}"
    assert program.cognome   != 'COGNOME', f"{COL['YELLOW']}ERRORE: Indica il tuo COGNOME in program.py{COL['RST']}"
    assert program.matricola != 'MATRICOLA', f"{COL['YELLOW']}ERRORE: Indica il tuo NUMERO DI MATRICOLA in program.py{COL['RST']}"
    print(f'{COL["GREEN"]}Informazioni studente: {program.nome} {program.cognome} {program.matricola}{COL["RST"]}')
    return 1e-9

###############################################################################
# ----------------------------------- EX. 2----------------------------------- #

def do_ex2_test(directory, extensions, expected):
    if not DEBUG:
        isrecursive2.DETECT = True
        try:
            program.ex2(directory, extensions)
        except isrecursive2.RecursionDetectedError:
            pass
        else:
            raise Exception(
                "The program does not employ recursion / Il programma non adotta un approccio ricorsivo")
        finally:
            isrecursive2.DETECT = False

    res = program.ex2(directory, extensions)
    testlib.check_dict(res, expected)
    return 2

def test_ex2_1(run=True):
    directory  = 'ex2/A'
    extensions = ["txt", "pdf", "png", "gif"]
    expected   = {'txt': {'ex2/A/C', 'ex2/A', 'ex2/A/B'}, 'pdf': {'ex2/A/C', 'ex2/A'}, 'png': {'ex2/A/C'}, 'gif': {'ex2/A/C'}}
    return do_ex2_test(directory, extensions, expected)

def test_ex2_2(run=True):
    directory  = 'ex2'
    extensions = ["png", "gif", "tqq"]
    expected   = {'png': {'ex2/C/C', 'ex2/A/C', 'ex2/C/B/p3zt345614/17nt', 'ex2/C/C/9n5'}, 
                  'gif': {'ex2/A/C', 'ex2/C/C/9n5/22zi524j', 'ex2/C/C/9n5', 'ex2/C/C'}, 'tqq': {'ex2/B/hfc44ba'}}
    return do_ex2_test(directory, extensions, expected)

def test_ex2_3(run=True):
    directory  = 'ex2/C'
    extensions = ["pdf", "png", "txt", "ne3"]
    expected   = {'pdf': {'ex2/C/C', 'ex2/C/C/9n5', 'ex2/C/B/p3zt345614/17nt'}, 
                  'png': {'ex2/C/C', 'ex2/C/C/9n5', 'ex2/C/B/p3zt345614/17nt'}, 
                  'txt': {'ex2/C/A/a9fa5r54ol/9dlnpni', 'ex2/C/A', 'ex2/C', 'ex2/C/A/a9fa5r54ol', 'ex2/C/B', 'ex2/C/A/r5g/d501/tew8', 
                          'ex2/C/C/9n5/22zi524j', 'ex2/C/A/r5g', 'ex2/C/A/a9fa5r54ol/9dlnpni/1bqeb8', 'ex2/C/C/9n5/22zi524j/1iha5', 
                          'ex2/C/B/p3zt345614/17nt', 'ex2/C/A/r5g/d501', 'ex2/C/B/p3zt345614/ei9ej73p', 'ex2/C/C/9n5/22zi524j/u2g', 
                          'ex2/C/439/53d23yd', 'ex2/C/A/a9fa5r54ol/9dlnpni/p2q8', 'ex2/C/4q5ni', 'ex2/C/B/p3zt345614/7j30i'}, 
                  'ne3': {'ex2/C/A/r5g'}}
    return do_ex2_test(directory, extensions, expected)

################################################################################

tests = [
    # TO RUN ONLY SOME OF THE TESTS, comment any of the following entries
    # PER DISATTIVARE ALCUNI TEST, commentare gli elementi seguenti
    test_ex2_1,    test_ex2_2,   test_ex2_3,                    # 6   / 3
    test_personal_data_entry,
]


if __name__ == '__main__':
    check_expected()
    testlib.runtests(   tests,
                        verbose=True,
                        logfile='grade.csv',
                        stack_trace=DEBUG)
    import program
    if 'matricola' in program.__dict__:
        print(f"{COL['GREEN']}Nome: {program.nome}\nCognome: {program.cognome}\nMatricola: {program.matricola}{COL['RST']}")
    elif 'student_id' in program.__dict__:
        print(f"{COL['GREEN']}Name: {program.name}\nSurname: {program.surname}\nStudentID: {program.student_id}{COL['RST']}")
    else:
        print('we should not arrive here the  matricola/student ID variable is not present in program.py')
################################################################################