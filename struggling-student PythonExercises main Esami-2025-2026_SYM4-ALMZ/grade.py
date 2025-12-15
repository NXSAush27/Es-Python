# -*- coding: utf-8 -*-
import testlib
import isrecursive
import os
import sys
from math import floor

import nary_tree, tree
from testlib import my_print, COL, check_expected

############ check that you have renamed the file as program.py   ###########
if not os.path.isfile('program.py'):
    print('WARNING: Save program.empty.py as program.py\n'
          'ATTENZIONE: salvare program.vuoto.py con nome program.py')
    sys.exit(0)
#############################################################################

import program

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

def test_personal_data_entry(run=True):
    assert program.nome != 'NOME', f"{COL['YELLOW']}ERRORE: Indica il tuo NOME in program.py{COL['RST']}"
    assert program.cognome != 'COGNOME', f"{COL['YELLOW']}ERRORE: Indica il tuo COGNOME in program.py{COL['RST']}"
    assert program.matricola != 'MATRICOLA', f"{COL['YELLOW']}ERRORE: Indica il tuo NUMERO DI MATRICOLA in program.py{COL['RST']}"
    print(f'{COL["GREEN"]}Informazioni studente: {program.nome} {program.cognome} {program.matricola}{COL["RST"]}')
    return 1e-9

# ----------------------------------- EX. 1----------------------------------- #


def do_ex1_test(N, P, Q, expected):
    # # Calcola il valore atteso per la data combinazione P e Q
    # expected = _calculate_lucas_U(N, P, Q)
    print(expected)

    if not DEBUG:
        try:
            isrecursive.decorate_module(program)
            program.ex1(N, P, Q)
        except isrecursive.RecursionDetectedError:
            pass
        else:
            raise Exception(
                "The program does not employ recursion / Il programma non adotta un approccio ricorsivo")
        finally:
            isrecursive.undecorate_module(program)

    res = program.ex1(N, P, Q)

    if res != expected:
        my_print(
            f'''{'*' * 50}\n[ERROR]Il valore ritornato non è corretto per U({P},{Q})!\nN={N}\nReturned={res}, expected={expected}''')
        return 0
    return 6/4


def test_ex1_1(run=True):
    N, P, Q = 6, 1, -1
    expected = 8
    return do_ex1_test(N, P, Q, expected)


def test_ex1_2(run=True):
    N, P, Q = 5, 2, -1
    expected = 29
    return do_ex1_test(N, P, Q, expected)


def test_ex1_3(run=True):
    N, P, Q = 10, 3, 2
    expected = 1023
    return do_ex1_test(N, P, Q, expected)


def test_ex1_4(run=True):
    N, P, Q = 12, 4, 3
    expected = 265720
    return do_ex1_test(N, P, Q, expected)

# ----------------------------------- EX. 2----------------------------------- #
def do_ex2_test(root, expected):
    if not DEBUG:
        try:
            isrecursive.decorate_module(program)
            program.ex2(root)
        except isrecursive.RecursionDetectedError:
            pass
        else:
            raise Exception(
                "The program does not employ recursion / Il programma non adotta un approccio ricorsivo")
        finally:
            isrecursive.undecorate_module(program)

    res = program.ex2(root)
    if res != expected:
        my_print(
            f'''{'*' * 50}\n[ERROR]Il valore ritornato non è corretto! / The returned value is incorrect!!\nReturned={res}, expected={expected}''')
        return 0
    return 8 / 3


def test_ex2_1(run=True):
    '''
    ______5______
   |             |
   8__           __2___
      |      |       |
      3      9       1
    Min Diff: 0 (da nodi foglia)
    '''
    root = tree.BinaryTree.fromList(
        [5, [8, None, [3, None, None]], [2, [9, None, None], [1, None, None]]])
    expected = 8
    return do_ex2_test(root, expected)


def test_ex2_2(run=True):
    '''
        ______2______
       |             |
    __ 7__           ___5___
   |      |        |      |
  _4_     3_       _0_     _5_
 |   |      |     |   |    |   |
 2   -1     1     8   3    2   9
    Min Diff: 0 (da nodi foglia)
    '''
    root = tree.BinaryTree.fromList([2,
                                     [7, [4, [2, None, None], [-1, None, None]],
                                      [3, None, [1, None, None]]],
                                     [5, [0, [8, None, None], [3, None, None]],
                                      [5, [2, None, None], [9, None, None]]]])
    expected = 16
    return do_ex2_test(root, expected)


def test_ex2_3(run=True):
    '''
    A complex tree, Min Diff: 0
    '''
    root = tree.BinaryTree.fromList([-2, [5, [13, [-7, [2, [26, [27, [10,
                                                                      [0, None,
                                                                       [24,
                                                                        None,
                                                                        None]],
                                                                      [14, None,
                                                                       None]],
                                                                 [13, [30,
                                                                       [2, None,
                                                                        None],
                                                                       None],
                                                                  [-3, None,
                                                                   [-1, None,
                                                                    None]]]],
                                                            [10,
                                                             [28, None, None],
                                                             [-1, [-3,
                                                                   [30, None,
                                                                    None],
                                                                   [-9, None,
                                                                    None]],
                                                              [19, None,
                                                               None]]]], None],
                                                   [8, [11,
                                                        [-2, [4, None, None],
                                                         [5, None, None]],
                                                        [6, [24, None, None],
                                                         [19, None, None]]],
                                                    [9, None, [1, [18, None,
                                                                   [-3, None,
                                                                    None]],
                                                               [22, None, [-10,
                                                                           [5,
                                                                            None,
                                                                            None],
                                                                           None]]]]]],
                                              [17, [12, [26, [10, [21, None,
                                                                   [1, None,
                                                                    None]],
                                                              [26, None,
                                                               [30, None,
                                                                None]]], [-3,
                                                                          [-2,
                                                                           [-3,
                                                                            None,
                                                                            [-2,
                                                                             [
                                                                                 28,
                                                                                 None,
                                                                                 None],
                                                                             [
                                                                                 21,
                                                                                 None,
                                                                                 None]]],
                                                                           [7,
                                                                            [-4,
                                                                             None,
                                                                             None],
                                                                            None]],
                                                                          [-1,
                                                                           [2,
                                                                            [18,
                                                                             None,
                                                                             None],
                                                                            [-2,
                                                                             None,
                                                                             None]],
                                                                           [24,
                                                                            [4,
                                                                             None,
                                                                             None],
                                                                            [30,
                                                                             [
                                                                                 -4,
                                                                                 None,
                                                                                 None],
                                                                             None]]]]],
                                                    [-2, [16, None, [9, [17,
                                                                         [23,
                                                                          None,
                                                                          None],
                                                                         None],
                                                                     [21, None,
                                                                      None]]],
                                                     [-8, [2, None,
                                                           [-10, None, None]],
                                                      [20, [21, [7, None, None],
                                                            [-5,
                                                             [20, None, None],
                                                             None]], [0, None,
                                                                      [-4, None,
                                                                       None]]]]]],
                                               [-1, None, [6, [30,
                                                               [22, None, None],
                                                               None], [28, [-4,
                                                                            None,
                                                                            None],
                                                                       [-10,
                                                                        None,
                                                                        None]]]]]],
                                          [-5, [13, [20, None, [17, [17, [25,
                                                                          [4,
                                                                           [5,
                                                                            [-4,
                                                                             [
                                                                                 21,
                                                                                 None,
                                                                                 None],
                                                                             None],
                                                                            None],
                                                                           [-3,
                                                                            [21,
                                                                             None,
                                                                             None],
                                                                            None]],
                                                                          None],
                                                                     [14, [-10,
                                                                           [5,
                                                                            None,
                                                                            [28,
                                                                             [
                                                                                 15,
                                                                                 [
                                                                                     7,
                                                                                     None,
                                                                                     [
                                                                                         12,
                                                                                         None,
                                                                                         None]],
                                                                                 [
                                                                                     7,
                                                                                     None,
                                                                                     None]],
                                                                             [
                                                                                 24,
                                                                                 None,
                                                                                 [
                                                                                     -2,
                                                                                     None,
                                                                                     None]]]],
                                                                           [-4,
                                                                            [2,
                                                                             None,
                                                                             None],
                                                                            [14,
                                                                             None,
                                                                             None]]],
                                                                      [10, None,
                                                                       [7, [12,
                                                                            None,
                                                                            None],
                                                                        [19, [0,
                                                                              None,
                                                                              None],
                                                                         None]]]]],
                                                                None]], [5, [2,
                                                                             [
                                                                                 14,
                                                                                 [
                                                                                     3,
                                                                                     None,
                                                                                     None],
                                                                                 [
                                                                                     0,
                                                                                     None,
                                                                                     None]],
                                                                             [5,
                                                                              [
                                                                                  15,
                                                                                  None,
                                                                                  [
                                                                                      15,
                                                                                      None,
                                                                                      None]],
                                                                              [
                                                                                  22,
                                                                                  [
                                                                                      15,
                                                                                      None,
                                                                                      None],
                                                                                  [
                                                                                      6,
                                                                                      None,
                                                                                      None]]]],
                                                                         None]],
                                           [-7, [-7, [14, [5, [24, None, [3, [4,
                                                                              [
                                                                                  10,
                                                                                  None,
                                                                                  None],
                                                                              None],
                                                                          [27,
                                                                           None,
                                                                           None]]],
                                                           [-5,
                                                            [30, None, None],
                                                            [24, None, None]]],
                                                      [-8, [4, [-10, [10,
                                                                      [27, None,
                                                                       None],
                                                                      [5, None,
                                                                       [14,
                                                                        None,
                                                                        None]]],
                                                                [10, [27, None,
                                                                      None],
                                                                 [16, None,
                                                                  None]]], [15,
                                                                            [20,
                                                                             None,
                                                                             None],
                                                                            [28,
                                                                             None,
                                                                             [
                                                                                 -7,
                                                                                 [
                                                                                     -5,
                                                                                     None,
                                                                                     None],
                                                                                 [
                                                                                     10,
                                                                                     None,
                                                                                     None]]]]],
                                                       [25, [17, [7, [19, None,
                                                                      None],
                                                                  [-4, [3, None,
                                                                        None],
                                                                   [12, None,
                                                                    None]]],
                                                             [12,
                                                              [23, None, None],
                                                              [2, None, None]]],
                                                        [20, [4, None, None],
                                                         [22, [22, None, None],
                                                          [21, [27, None, None],
                                                           None]]]]]], [9, [12,
                                                                            [6,
                                                                             [
                                                                                 -4,
                                                                                 [
                                                                                     -2,
                                                                                     None,
                                                                                     None],
                                                                                 [
                                                                                     11,
                                                                                     None,
                                                                                     [
                                                                                         18,
                                                                                         None,
                                                                                         None]]],
                                                                             [
                                                                                 25,
                                                                                 [
                                                                                     11,
                                                                                     None,
                                                                                     None],
                                                                                 [
                                                                                     25,
                                                                                     None,
                                                                                     None]]],
                                                                            [7,
                                                                             [
                                                                                 10,
                                                                                 [
                                                                                     6,
                                                                                     [
                                                                                         18,
                                                                                         None,
                                                                                         None],
                                                                                     [
                                                                                         18,
                                                                                         None,
                                                                                         [
                                                                                             0,
                                                                                             None,
                                                                                             None]]],
                                                                                 [
                                                                                     30,
                                                                                     [
                                                                                         5,
                                                                                         None,
                                                                                         None],
                                                                                     None]],
                                                                             [8,
                                                                              None,
                                                                              [
                                                                                  25,
                                                                                  [
                                                                                      2,
                                                                                      None,
                                                                                      [
                                                                                          -4,
                                                                                          None,
                                                                                          None]],
                                                                                  [
                                                                                      -2,
                                                                                      [
                                                                                          27,
                                                                                          None,
                                                                                          None],
                                                                                      [
                                                                                          -4,
                                                                                          None,
                                                                                          None]]]]]],
                                                                        [1, [-9,
                                                                             [
                                                                                 -10,
                                                                                 [
                                                                                     26,
                                                                                     [
                                                                                         17,
                                                                                         None,
                                                                                         None],
                                                                                     None],
                                                                                 [
                                                                                     28,
                                                                                     [
                                                                                         -2,
                                                                                         [
                                                                                             22,
                                                                                             None,
                                                                                             None],
                                                                                         None],
                                                                                     [
                                                                                         -6,
                                                                                         None,
                                                                                         [
                                                                                             30,
                                                                                             None,
                                                                                             None]]]],
                                                                             [
                                                                                 28,
                                                                                 [
                                                                                     19,
                                                                                     [
                                                                                         -3,
                                                                                         None,
                                                                                         [
                                                                                             25,
                                                                                             None,
                                                                                             [
                                                                                                 10,
                                                                                                 None,
                                                                                                 None]]],
                                                                                     [
                                                                                         8,
                                                                                         None,
                                                                                         [
                                                                                             4,
                                                                                             None,
                                                                                             None]]],
                                                                                 [
                                                                                     11,
                                                                                     [
                                                                                         8,
                                                                                         None,
                                                                                         None],
                                                                                     [
                                                                                         24,
                                                                                         None,
                                                                                         [
                                                                                             -10,
                                                                                             None,
                                                                                             None]]]]],
                                                                         [26,
                                                                          [29,
                                                                           [-10,
                                                                            None,
                                                                            None],
                                                                           [-6,
                                                                            None,
                                                                            None]],
                                                                          None]]]],
                                            [-2, [20, [-10, [2, None, [28, [-9,
                                                                            [11,
                                                                             None,
                                                                             None],
                                                                            None],
                                                                       [1, None,
                                                                        None]]],
                                                       [13, [10, None, None],
                                                        [-2, None, None]]], [-4,
                                                                             [
                                                                                 19,
                                                                                 [
                                                                                     -9,
                                                                                     None,
                                                                                     [
                                                                                         -1,
                                                                                         None,
                                                                                         None]],
                                                                                 [
                                                                                     -8,
                                                                                     [
                                                                                         12,
                                                                                         [
                                                                                             21,
                                                                                             None,
                                                                                             None],
                                                                                         [
                                                                                             8,
                                                                                             None,
                                                                                             None]],
                                                                                     [
                                                                                         3,
                                                                                         [
                                                                                             7,
                                                                                             None,
                                                                                             [
                                                                                                 17,
                                                                                                 None,
                                                                                                 None]],
                                                                                         [
                                                                                             23,
                                                                                             None,
                                                                                             None]]]],
                                                                             [
                                                                                 25,
                                                                                 [
                                                                                     3,
                                                                                     [
                                                                                         19,
                                                                                         None,
                                                                                         [
                                                                                             -4,
                                                                                             [
                                                                                                 25,
                                                                                                 None,
                                                                                                 None],
                                                                                             None]],
                                                                                     [
                                                                                         -10,
                                                                                         None,
                                                                                         None]],
                                                                                 [
                                                                                     12,
                                                                                     [
                                                                                         4,
                                                                                         [
                                                                                             -10,
                                                                                             None,
                                                                                             None],
                                                                                         None],
                                                                                     [
                                                                                         18,
                                                                                         [
                                                                                             15,
                                                                                             [
                                                                                                 27,
                                                                                                 None,
                                                                                                 None],
                                                                                             [
                                                                                                 -2,
                                                                                                 None,
                                                                                                 None]],
                                                                                         [
                                                                                             13,
                                                                                             None,
                                                                                             None]]]]]],
                                             [-6, [29, [17, [-4, None,
                                                             [-5, None, None]],
                                                        [-2, [-3, None,
                                                              [-8, None, None]],
                                                         [-7, None, None]]], [8,
                                                                              [
                                                                                  11,
                                                                                  [
                                                                                      21,
                                                                                      [
                                                                                          -3,
                                                                                          None,
                                                                                          [
                                                                                              2,
                                                                                              None,
                                                                                              None]],
                                                                                      [
                                                                                          2,
                                                                                          None,
                                                                                          None]],
                                                                                  [
                                                                                      -6,
                                                                                      None,
                                                                                      None]],
                                                                              None]],
                                              [-9, [29, [23, None,
                                                         [25, [20, None, None],
                                                          None]], [30, [24, [6,
                                                                             [
                                                                                 25,
                                                                                 None,
                                                                                 None],
                                                                             [
                                                                                 24,
                                                                                 None,
                                                                                 None]],
                                                                        [2, [25,
                                                                             None,
                                                                             None],
                                                                         [-9,
                                                                          [3,
                                                                           None,
                                                                           None],
                                                                          None]]],
                                                                   [16,
                                                                    [0, None,
                                                                     [-1, None,
                                                                      None]],
                                                                    [30, None,
                                                                     None]]]],
                                               [28, [25, [5, [3, None, None],
                                                          [9, [4, None, None],
                                                           None]], [-8, None,
                                                                    [21, None,
                                                                     None]]],
                                                [23, [16, [-7, [7, None, None],
                                                           [12, None, None]],
                                                      [16, None,
                                                       [16, None, None]]], [-8,
                                                                            [24,
                                                                             None,
                                                                             [5,
                                                                              None,
                                                                              None]],
                                                                            [2,
                                                                             [
                                                                                 23,
                                                                                 None,
                                                                                 None],
                                                                             [
                                                                                 14,
                                                                                 None,
                                                                                 None]]]]]]]]]]],
                                     [20, [20, [19, [-2, [-1, [3, [24,
                                                                   [12, None,
                                                                    None],
                                                                   None],
                                                               [5, None, None]],
                                                          [10, None, None]],
                                                     [27, [29, [24, None, None],
                                                           None], [30, [-9, [4,
                                                                             None,
                                                                             None],
                                                                        None],
                                                                   None]]],
                                                [-10, [21,
                                                       [26, [24, None, None],
                                                        None], [5, None,
                                                                [18, None,
                                                                 None]]],
                                                 [-4, [1, None, None],
                                                  [1, None, None]]]], [23, [2,
                                                                            [4,
                                                                             [
                                                                                 21,
                                                                                 None,
                                                                                 [
                                                                                     30,
                                                                                     None,
                                                                                     None]],
                                                                             None],
                                                                            [16,
                                                                             [
                                                                                 -8,
                                                                                 None,
                                                                                 None],
                                                                             [6,
                                                                              None,
                                                                              None]]],
                                                                       [14, [12,
                                                                             None,
                                                                             [
                                                                                 27,
                                                                                 [
                                                                                     -5,
                                                                                     None,
                                                                                     None],
                                                                                 [
                                                                                     10,
                                                                                     None,
                                                                                     None]]],
                                                                        [6, [18,
                                                                             None,
                                                                             None],
                                                                         [3,
                                                                          None,
                                                                          None]]]]],
                                      None]])

    expected = 2568
    return do_ex2_test(root, expected)


# ----------------------------------- EX.3 ----------------------------------- #

def do_ex3_test(directory, K, extensions, expected):
    if not DEBUG:
        try:
            isrecursive.decorate_module(program)
            program.ex3(directory, K, extensions)
        except isrecursive.RecursionDetectedError:
            pass
        else:
            raise Exception("The program does not employ recursion / Il programma non adotta un approccio ricorsivo")
        finally:
            isrecursive.undecorate_module(program)

    res = program.ex3(directory, K, extensions)

    if res is None:
        my_print(f'''{'*' * 50}\n[ERROR]La funzione ex3 ha ritornato None.''')
        return 0

    # Ordina le chiavi per un confronto stabile
    res_keys_sorted = sorted(res.keys())
    expected_keys_sorted = sorted(expected.keys())

    # 1. Confronta le chiavi (i path delle directory)
    if res_keys_sorted != expected_keys_sorted:
        my_print(
            f'''{'*' * 50}\n[ERROR]Le directory ritornate non sono corrette! (K={K}, ext={extensions})\nReturned keys={res_keys_sorted}\nExpected keys={expected_keys_sorted}''')
        my_print(f'''Full Returned={res}\nFull Expected={expected}''')
        return 0

    # 2. Se le chiavi sono le stesse, confronta i valori (i conteggi)
    for k in expected_keys_sorted:
        if k not in res or res[k] != expected[k]:
            my_print(
                f'''{'*' * 50}\n[ERROR]Il valore per la directory {k} non è corretto! (K={K}, ext={extensions})''')
            my_print(f'''Returned value={res.get(k)}, expected value={expected[k]}''')
            my_print(f'''Full Returned={res}\nFull Expected={expected}''')
            return 0

    # Se tutto è corretto
    return 8 / 3


def test_ex3_1(run=True):
    directory = 'ex3'
    K = 20
    extensions = ['txt']
    expected = {
        'ex3/B': 21,
        'ex3/C': 38,
        'ex3': 68
    }
    return do_ex3_test(directory, K, extensions, expected)


def test_ex3_2(run=True):
    directory = 'ex3/C'
    K = 2
    extensions = ['pdf', 'png', 'gif']
    expected = {
        'ex3/C/C/9n5': 4,
        'ex3/C/C': 7,
        'ex3/C': 9
    }
    return do_ex3_test(directory, K, extensions, expected)


def test_ex3_3(run=True):
    directory = 'ex3'
    K = 10
    extensions = ['txt', 'pdf', 'png']
    expected = {
        'ex3/A': 12,
        'ex3/B/DBvt2h4': 11,
        'ex3/B': 21,
        'ex3/C/A': 16,
        'ex3/C': 44,
        'ex3': 77
    }
    return do_ex3_test(directory, K, extensions, expected)

# ----------------------------------- EX. 4----------------------------------- #
def do_ex4_test(root, expected):
    if not DEBUG:
        try:
            isrecursive.decorate_module(program)
            res = program.ex4(root)
        except isrecursive.RecursionDetectedError:
            pass
        else:
            raise Exception(
                "The program does not employ recursion / Il programma non adotta un approccio ricorsivo")
        finally:
            isrecursive.undecorate_module(program)

    res = program.ex4(root)
    if res != expected:
        my_print(
            f'''{'*' * 50}\n[ERROR]Il valore ritornato non è corretto! / The returned value is incorrect!!\nReturned={res}, expected={expected}''')
        return 0
    return 8/3


def test_ex4_1(run=True):
    '''
    ______5______
   |             |
   8__        ___2___
      |      |       |
      3      9       1
    '''
    root = tree.BinaryTree.fromList(
        [5, [8, None, [3, None, None]], [2, [9, None, None], [1, None, None]]])
    expected = [5, 10, 13]
    return do_ex4_test(root, expected)


def test_ex4_2(run=True):
    '''
        ______2______
       |             |
    __ 7__        ___5___
   |      |      |       |
  _4_     3_    _0_     _5_
 |   |      |  |   |   |   |
 2   -1     1  8   3   2   9
    '''
    root = tree.BinaryTree.fromList([2,
                                     [7, [4, [2, None, None], [-1, None, None]],
                                      [3, None, [1, None, None]]],
                                     [5, [0, [8, None, None], [3, None, None]],
                                      [5, [2, None, None], [9, None, None]]]])
    expected = [2, 12, 12, 24]
    return do_ex4_test(root, expected)


def test_ex4_3(run=True):
    '''
    A big tree
    '''
    root = tree.BinaryTree.fromList([-2, [5, [13, [-7, [2, [26, [27, [10,
                                                                      [0, None,
                                                                       [24,
                                                                        None,
                                                                        None]],
                                                                      [14, None,
                                                                       None]],
                                                                 [13, [30,
                                                                       [2, None,
                                                                        None],
                                                                       None],
                                                                  [-3, None,
                                                                   [-1, None,
                                                                    None]]]],
                                                            [10,
                                                             [28, None, None],
                                                             [-1, [-3,
                                                                   [30, None,
                                                                    None],
                                                                   [-9, None,
                                                                    None]],
                                                              [19, None,
                                                               None]]]], None],
                                                   [8, [11,
                                                        [-2, [4, None, None],
                                                         [5, None, None]],
                                                        [6, [24, None, None],
                                                         [19, None, None]]],
                                                    [9, None, [1, [18, None,
                                                                   [-3, None,
                                                                    None]],
                                                               [22, None, [-10,
                                                                           [5,
                                                                            None,
                                                                            None],
                                                                           None]]]]]],
                                              [17, [12, [26, [10, [21, None,
                                                                   [1, None,
                                                                    None]],
                                                              [26, None,
                                                               [30, None,
                                                                None]]], [-3,
                                                                          [-2,
                                                                           [-3,
                                                                            None,
                                                                            [-2,
                                                                             [
                                                                                 28,
                                                                                 None,
                                                                                 None],
                                                                             [
                                                                                 21,
                                                                                 None,
                                                                                 None]]],
                                                                           [7,
                                                                            [-4,
                                                                             None,
                                                                             None],
                                                                            None]],
                                                                          [-1,
                                                                           [2,
                                                                            [18,
                                                                             None,
                                                                             None],
                                                                            [-2,
                                                                             None,
                                                                             None]],
                                                                           [24,
                                                                            [4,
                                                                             None,
                                                                             None],
                                                                            [30,
                                                                             [
                                                                                 -4,
                                                                                 None,
                                                                                 None],
                                                                             None]]]]],
                                                    [-2, [16, None, [9, [17,
                                                                         [23,
                                                                          None,
                                                                          None],
                                                                         None],
                                                                     [21, None,
                                                                      None]]],
                                                     [-8, [2, None,
                                                           [-10, None, None]],
                                                      [20, [21, [7, None, None],
                                                            [-5,
                                                             [20, None, None],
                                                             None]], [0, None,
                                                                      [-4, None,
                                                                       None]]]]]],
                                               [-1, None, [6, [30,
                                                               [22, None, None],
                                                               None], [28, [-4,
                                                                            None,
                                                                            None],
                                                                       [-10,
                                                                        None,
                                                                        None]]]]]],
                                          [-5, [13, [20, None, [17, [17, [25,
                                                                          [4,
                                                                           [5,
                                                                            [-4,
                                                                             [
                                                                                 21,
                                                                                 None,
                                                                                 None],
                                                                             None],
                                                                            None],
                                                                           [-3,
                                                                            [21,
                                                                             None,
                                                                             None],
                                                                            None]],
                                                                          None],
                                                                     [14, [-10,
                                                                           [5,
                                                                            None,
                                                                            [28,
                                                                             [
                                                                                 15,
                                                                                 [
                                                                                     7,
                                                                                     None,
                                                                                     [
                                                                                         12,
                                                                                         None,
                                                                                         None]],
                                                                                 [
                                                                                     7,
                                                                                     None,
                                                                                     None]],
                                                                             [
                                                                                 24,
                                                                                 None,
                                                                                 [
                                                                                     -2,
                                                                                     None,
                                                                                     None]]]],
                                                                           [-4,
                                                                            [2,
                                                                             None,
                                                                             None],
                                                                            [14,
                                                                             None,
                                                                             None]]],
                                                                      [10, None,
                                                                       [7, [12,
                                                                            None,
                                                                            None],
                                                                        [19, [0,
                                                                              None,
                                                                              None],
                                                                         None]]]]],
                                                                None]], [5, [2,
                                                                             [
                                                                                 14,
                                                                                 [
                                                                                     3,
                                                                                     None,
                                                                                     None],
                                                                                 [
                                                                                     0,
                                                                                     None,
                                                                                     None]],
                                                                             [5,
                                                                              [
                                                                                  15,
                                                                                  None,
                                                                                  [
                                                                                      15,
                                                                                      None,
                                                                                      None]],
                                                                              [
                                                                                  22,
                                                                                  [
                                                                                      15,
                                                                                      None,
                                                                                      None],
                                                                                  [
                                                                                      6,
                                                                                      None,
                                                                                      None]]]],
                                                                         None]],
                                           [-7, [-7, [14, [5, [24, None, [3, [4,
                                                                              [
                                                                                  10,
                                                                                  None,
                                                                                  None],
                                                                              None],
                                                                          [27,
                                                                           None,
                                                                           None]]],
                                                           [-5,
                                                            [30, None, None],
                                                            [24, None, None]]],
                                                      [-8, [4, [-10, [10,
                                                                      [27, None,
                                                                       None],
                                                                      [5, None,
                                                                       [14,
                                                                        None,
                                                                        None]]],
                                                                [10, [27, None,
                                                                      None],
                                                                 [16, None,
                                                                  None]]], [15,
                                                                            [20,
                                                                             None,
                                                                             None],
                                                                            [28,
                                                                             None,
                                                                             [
                                                                                 -7,
                                                                                 [
                                                                                     -5,
                                                                                     None,
                                                                                     None],
                                                                                 [
                                                                                     10,
                                                                                     None,
                                                                                     None]]]]],
                                                       [25, [17, [7, [19, None,
                                                                      None],
                                                                  [-4, [3, None,
                                                                        None],
                                                                   [12, None,
                                                                    None]]],
                                                             [12,
                                                              [23, None, None],
                                                              [2, None, None]]],
                                                        [20, [4, None, None],
                                                         [22, [22, None, None],
                                                          [21, [27, None, None],
                                                           None]]]]]], [9, [12,
                                                                            [6,
                                                                             [
                                                                                 -4,
                                                                                 [
                                                                                     -2,
                                                                                     None,
                                                                                     None],
                                                                                 [
                                                                                     11,
                                                                                     None,
                                                                                     [
                                                                                         18,
                                                                                         None,
                                                                                         None]]],
                                                                             [
                                                                                 25,
                                                                                 [
                                                                                     11,
                                                                                     None,
                                                                                     None],
                                                                                 [
                                                                                     25,
                                                                                     None,
                                                                                     None]]],
                                                                            [7,
                                                                             [
                                                                                 10,
                                                                                 [
                                                                                     6,
                                                                                     [
                                                                                         18,
                                                                                         None,
                                                                                         None],
                                                                                     [
                                                                                         18,
                                                                                         None,
                                                                                         [
                                                                                             0,
                                                                                             None,
                                                                                             None]]],
                                                                                 [
                                                                                     30,
                                                                                     [
                                                                                         5,
                                                                                         None,
                                                                                         None],
                                                                                     None]],
                                                                             [8,
                                                                              None,
                                                                              [
                                                                                  25,
                                                                                  [
                                                                                      2,
                                                                                      None,
                                                                                      [
                                                                                          -4,
                                                                                          None,
                                                                                          None]],
                                                                                  [
                                                                                      -2,
                                                                                      [
                                                                                          27,
                                                                                          None,
                                                                                          None],
                                                                                      [
                                                                                          -4,
                                                                                          None,
                                                                                          None]]]]]],
                                                                        [1, [-9,
                                                                             [
                                                                                 -10,
                                                                                 [
                                                                                     26,
                                                                                     [
                                                                                         17,
                                                                                         None,
                                                                                         None],
                                                                                     None],
                                                                                 [
                                                                                     28,
                                                                                     [
                                                                                         -2,
                                                                                         [
                                                                                             22,
                                                                                             None,
                                                                                             None],
                                                                                         None],
                                                                                     [
                                                                                         -6,
                                                                                         None,
                                                                                         [
                                                                                             30,
                                                                                             None,
                                                                                             None]]]],
                                                                             [
                                                                                 28,
                                                                                 [
                                                                                     19,
                                                                                     [
                                                                                         -3,
                                                                                         None,
                                                                                         [
                                                                                             25,
                                                                                             None,
                                                                                             [
                                                                                                 10,
                                                                                                 None,
                                                                                                 None]]],
                                                                                     [
                                                                                         8,
                                                                                         None,
                                                                                         [
                                                                                             4,
                                                                                             None,
                                                                                             None]]],
                                                                                 [
                                                                                     11,
                                                                                     [
                                                                                         8,
                                                                                         None,
                                                                                         None],
                                                                                     [
                                                                                         24,
                                                                                         None,
                                                                                         [
                                                                                             -10,
                                                                                             None,
                                                                                             None]]]]],
                                                                         [26,
                                                                          [29,
                                                                           [-10,
                                                                            None,
                                                                            None],
                                                                           [-6,
                                                                            None,
                                                                            None]],
                                                                          None]]]],
                                            [-2, [20, [-10, [2, None, [28, [-9,
                                                                            [11,
                                                                             None,
                                                                             None],
                                                                            None],
                                                                       [1, None,
                                                                        None]]],
                                                       [13, [10, None, None],
                                                        [-2, None, None]]], [-4,
                                                                             [
                                                                                 19,
                                                                                 [
                                                                                     -9,
                                                                                     None,
                                                                                     [
                                                                                         -1,
                                                                                         None,
                                                                                         None]],
                                                                                 [
                                                                                     -8,
                                                                                     [
                                                                                         12,
                                                                                         [
                                                                                             21,
                                                                                             None,
                                                                                             None],
                                                                                         [
                                                                                             8,
                                                                                             None,
                                                                                             None]],
                                                                                     [
                                                                                         3,
                                                                                         [
                                                                                             7,
                                                                                             None,
                                                                                             [
                                                                                                 17,
                                                                                                 None,
                                                                                                 None]],
                                                                                         [
                                                                                             23,
                                                                                             None,
                                                                                             None]]]],
                                                                             [
                                                                                 25,
                                                                                 [
                                                                                     3,
                                                                                     [
                                                                                         19,
                                                                                         None,
                                                                                         [
                                                                                             -4,
                                                                                             [
                                                                                                 25,
                                                                                                 None,
                                                                                                 None],
                                                                                             None]],
                                                                                     [
                                                                                         -10,
                                                                                         None,
                                                                                         None]],
                                                                                 [
                                                                                     12,
                                                                                     [
                                                                                         4,
                                                                                         [
                                                                                             -10,
                                                                                             None,
                                                                                             None],
                                                                                         None],
                                                                                     [
                                                                                         18,
                                                                                         [
                                                                                             15,
                                                                                             [
                                                                                                 27,
                                                                                                 None,
                                                                                                 None],
                                                                                             [
                                                                                                 -2,
                                                                                                 None,
                                                                                                 None]],
                                                                                         [
                                                                                             13,
                                                                                             None,
                                                                                             None]]]]]],
                                             [-6, [29, [17, [-4, None,
                                                             [-5, None, None]],
                                                        [-2, [-3, None,
                                                              [-8, None, None]],
                                                         [-7, None, None]]], [8,
                                                                              [
                                                                                  11,
                                                                                  [
                                                                                      21,
                                                                                      [
                                                                                          -3,
                                                                                          None,
                                                                                          [
                                                                                              2,
                                                                                              None,
                                                                                              None]],
                                                                                      [
                                                                                          2,
                                                                                          None,
                                                                                          None]],
                                                                                  [
                                                                                      -6,
                                                                                      None,
                                                                                      None]],
                                                                              None]],
                                              [-9, [29, [23, None,
                                                         [25, [20, None, None],
                                                          None]], [30, [24, [6,
                                                                             [
                                                                                 25,
                                                                                 None,
                                                                                 None],
                                                                             [
                                                                                 24,
                                                                                 None,
                                                                                 None]],
                                                                        [2, [25,
                                                                             None,
                                                                             None],
                                                                         [-9,
                                                                          [3,
                                                                           None,
                                                                           None],
                                                                          None]]],
                                                                   [16,
                                                                    [0, None,
                                                                     [-1, None,
                                                                      None]],
                                                                    [30, None,
                                                                     None]]]],
                                               [28, [25, [5, [3, None, None],
                                                          [9, [4, None, None],
                                                           None]], [-8, None,
                                                                    [21, None,
                                                                     None]]],
                                                [23, [16, [-7, [7, None, None],
                                                           [12, None, None]],
                                                      [16, None,
                                                       [16, None, None]]], [-8,
                                                                            [24,
                                                                             None,
                                                                             [5,
                                                                              None,
                                                                              None]],
                                                                            [2,
                                                                             [
                                                                                 23,
                                                                                 None,
                                                                                 None],
                                                                             [
                                                                                 14,
                                                                                 None,
                                                                                 None]]]]]]]]]]],
                                     [20, [20, [19, [-2, [-1, [3, [24,
                                                                   [12, None,
                                                                    None],
                                                                   None],
                                                               [5, None, None]],
                                                          [10, None, None]],
                                                     [27, [29, [24, None, None],
                                                           None], [30, [-9, [4,
                                                                             None,
                                                                             None],
                                                                        None],
                                                                   None]]],
                                                [-10, [21,
                                                       [26, [24, None, None],
                                                        None], [5, None,
                                                                [18, None,
                                                                 None]]],
                                                 [-4, [1, None, None],
                                                  [1, None, None]]]], [23, [2,
                                                                            [4,
                                                                             [
                                                                                 21,
                                                                                 None,
                                                                                 [
                                                                                     30,
                                                                                     None,
                                                                                     None]],
                                                                             None],
                                                                            [16,
                                                                             [
                                                                                 -8,
                                                                                 None,
                                                                                 None],
                                                                             [6,
                                                                              None,
                                                                              None]]],
                                                                       [14, [12,
                                                                             None,
                                                                             [
                                                                                 27,
                                                                                 [
                                                                                     -5,
                                                                                     None,
                                                                                     None],
                                                                                 [
                                                                                     10,
                                                                                     None,
                                                                                     None]]],
                                                                        [6, [18,
                                                                             None,
                                                                             None],
                                                                         [3,
                                                                          None,
                                                                          None]]]]],
                                      None]])
    expected = [-2, 25, 28, 58, 41, 213, 339, 644, 535, 551, 624, 425, 25, 12]
    return do_ex4_test(root, expected)


################################################################################

tests = [
    # TO RUN ONLY SOME OF THE TESTS, comment any of the following entries
    # PER DISATTIVARE ALCUNI TEST, commentare gli elementi seguenti

    test_ex1_1, test_ex1_2, test_ex1_3, test_ex1_4,  # 6 / 4
    test_ex2_1, test_ex2_2, test_ex2_3,  # 8 / 3
    test_ex3_1, test_ex3_2, test_ex3_3,  # 8 / 3
    test_ex4_1, test_ex4_2, test_ex4_3,  # 8 / 3
    test_personal_data_entry,
]

if __name__ == '__main__':
    if test_personal_data_entry() < 0:
        print(
            f"{COL['RED']}PERSONAL INFO MISSING. PLEASE FILL THE INITIAL VARS WITH YOUR NAME SURNAME AND STUDENT_ID{COL['RST']}")
        sys.exit()

    testlib.runtests(tests,
                     verbose=True,
                     logfile='grade.csv',
                     stack_trace=DEBUG)
    if 'matricola' in program.__dict__:
        print(
            f"{COL['GREEN']}Nome: {program.nome}\nCognome: {program.cognome}\nMatricola: {program.matricola}{COL['RST']}")
    elif 'student_id' in program.__dict__:
        print(
            f"{COL['GREEN']}Name: {program.name}\nSurname: {program.surname}\nStudentID: {program.student_id}{COL['RST']}")
    else:
        print('we should not arrive here the  matricola/student ID variable is not present in program.py')
################################################################################
