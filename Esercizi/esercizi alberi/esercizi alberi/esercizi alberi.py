# Ignorare le righe fino alla 31
from typing import Any, Callable, List, Tuple, Dict, Union
import sys
from unittest import result
import json
import math


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# Esegue un test e controlla il risultato
def check_test(func: Callable, expected: Any, *args: List[Any]):
    func_str = func.__name__
    args_str = ', '.join(repr(arg) for arg in args)
    try:
        result = func(*args)
        result_str = repr(result)
        expected_str = repr(expected)
        test_outcome = "succeeded" if (result == expected) else "failed"
        color = bcolors.OKGREEN if (result == expected) else bcolors.FAIL
        print(f'{color}Test on {func_str} on input {args_str} {test_outcome}. Output: {result_str} Expected: {expected_str}')
    except BaseException as error:
        error_str = repr(error)
        print(f'{bcolors.FAIL}ERROR: {func_str}({args_str}) => {error_str}')


# Helper functions
def load_json(filename):
    with open(filename) as f:
        return json.load(f)


# Helper functions
def save_json(filename, js):
    with open(filename, 'w') as f:
        json.dump(js, f, indent=2)


# Helper functions
def from_json1(filename):
    def convert(d):
        return Node(tag=d['tag'] if 'tag' in d else '', nodes=[convert(n) for n in d['nodes']] if 'nodes' in d else [])
    return convert(load_json(filename))


# Helper functions
def from_json2(filename):
    def convert(d):
        return Internal(nodes=[convert(n) for n in d['nodes']]) if 'nodes' in d else Leaf(tag=d['tag'])
    return convert(load_json(filename))

# Questo esercizio differisce dai precedenti perchè implementeremo sia funzione
# che classi. Ci focalizzeremo su due modi diversi di implemetare gli alberi.
# Nel resto di questo esercizio, chiameremo nodi interni i nodi che contengono
# altri nodi, mentre useremo il nome foglie per i nodi che non contengono altri
# nodi.
# In questo esercizio, il codice da scrivere è molto poco, ma richiede di capire
# bene come rappresentare gli alberi.


# Implementare la classe Node che rappresenta un nodo di un albero.
# Ogni nodo contiene due variabili: una stringa chiamata tag e una lista di
# nodi chiamati nodes. Il construttore prende come parametri opzionali tag e nodes.
# Si ricorda che nodes va copiato per evitare problemi.
# Implementare __repr__ e __eq__
class Node:
    tag: str
    nodes: List['Node']
    def __init__(self, tag: str = '', nodes: List['Node'] = None):
        self.tag = tag
        self.nodes = nodes.copy() if nodes is not None else []
    def __repr__(self):
        return f'Node(tag={repr(self.tag)}, nodes={repr(self.nodes)})'
    def __eq__(self, other):
        return isinstance(other, Node) and self.tag == other.tag and self.nodes == other.nodes


# Implementare una funzione ricorsiva che conta il numero di nodi di un albero.
def num_nodes(node: Node) -> int:
    count = 1 #conta il nodo corrente
    for child in node.nodes:
        count += num_nodes(child)
    return count


# Implementare una funzione ricorsiva che conta il numero di foglie di un albero.
def num_leaves(node: Node) -> int:
    count = 0
    if len (node.nodes) == 0:
        return 1
    for child in node.nodes:
        count += num_leaves(child)
    return count


# Implementare una funzione ricorsiva che ritorna una stringa ottenuta
# concatenando le stringhe tag di tutti i nodi.
def get_alltags(node: Node) -> str:
    result = node.tag
    for child in node.nodes:
        result += get_alltags(child)
    return result



# Implementare una funzione che converte un dizionario che rappresenta un albero, le cui chiavi
# sono i parametri del construttore. Vedere il file tree01.json per avere un'idea di come il dizionario
# definisce ricorsivamente l'albero.
def from_dict(d: dict) -> Node:
    node = Node(tag=d['tag'] if 'tag' in d else '', nodes=[from_dict(n) for n in d['nodes']] if 'nodes' in d else [])
    return node


# Implementare una funzione che converte un node in un dizionario ricorsivo.
def to_dict(node: Node) -> dict:
    return {'tag': node.tag, 'nodes': [to_dict(child) for child in node.nodes]}


# Nella seconda parte di questo esercizio implementeremo le stesse funzionalità
# su un albero eterogeneo. In questo albero, i nodi interni sono di classe
# Internal e contengono solo altri nodi, mentre i nodi foglia sono di classe
# Leaf e contengono solo tag. Internal e Leaf derivano da una classe Tree.

# In questa seconda implemetazione, le funzionalità descritte prima vanno
# implementate come metodi sulle classi. Avremo quindi metodi num_nodes(),
# num_leaves(), get_alltags() e to_dict(). Per from_dict() definiamo un
# metodo di classe in Tree.

# Implementare __eq__ e __repr__ in Internal e Leaf

class Tree:
    @classmethod
    def from_dict(cls, d: dict) -> 'Tree':
        if 'tag' in d:
            return Leaf(tag=d['tag'])
        else:
            return Internal(nodes=[cls.from_dict(n) for n in d['nodes']])



class Internal(Tree):
    nodes: List[Tree]
    def __init__(self, nodes: List['Tree'] = None):
        self.nodes = nodes.copy() if nodes is not None else []
    def __repr__(self):
        return f'Internal(nodes={repr(self.nodes)})'
    def __eq__(self, other):
        return isinstance(other, Internal) and self.nodes == other.nodes
    def num_nodes(self) -> int:
        count = 1 #conta il nodo corrente
        for child in self.nodes:
            count += child.num_nodes()
        return count
    def num_leaves(self) -> int:
        count = 0
        for child in self.nodes:
            count += child.num_leaves()
        return count
    def get_alltags(self) -> str:
        result = ''
        for child in self.nodes:
            result += child.get_alltags()
        return result
    def to_dict(self) -> dict:
        return {'nodes': [child.to_dict() for child in self.nodes]}



class Leaf(Tree):
    tag: str
    def __init__(self, tag: str = ''):
        self.tag = tag
    def __repr__(self):
        return f'Leaf(tag={repr(self.tag)})'
    def __eq__(self, other):
        return isinstance(other, Leaf) and self.tag == other.tag
    def num_nodes(self) -> int:
        return 1
    def num_leaves(self) -> int:
        return 1
    def get_alltags(self) -> str:
        return self.tag
    def to_dict(self) -> dict:
        return {'tag': self.tag}


# Test funzioni
check_test(num_nodes, 5, from_json1('Esercizi/esercizi alberi/esercizi alberi/tree01.json'))
check_test(num_leaves, 3, from_json1('Esercizi/esercizi alberi/esercizi alberi/tree01.json'))
check_test(get_alltags, 'Rickard Stark, padre di Eddard Stark (padre di Robb e Arya ) e Benjen Stark', from_json1('Esercizi/esercizi alberi/esercizi alberi/tree01.json'))
check_test(to_dict, {'tag': 'Rickard Stark, padre di ', 'nodes': [{'tag': 'Eddard Stark (padre di ', 'nodes': [{'tag': 'Robb e ', 'nodes': []}, 
                    {'tag': 'Arya ', 'nodes': []}]}, {'tag': ') e Benjen Stark', 'nodes': []}]}, from_json1('Esercizi/esercizi alberi/esercizi alberi/tree01.json'))
check_test(from_dict, from_json1('Esercizi/esercizi alberi/esercizi alberi/tree01.json'), load_json('Esercizi/esercizi alberi/esercizi alberi/tree01.json'))
check_test(lambda node: node.num_nodes(), 5, from_json2('Esercizi/esercizi alberi/esercizi alberi/tree02.json'))
check_test(lambda node: node.num_leaves(), 3, from_json2('Esercizi/esercizi alberi/esercizi alberi/tree02.json'))
check_test(lambda node: node.get_alltags(),
           'Robb e Arya ) e Benjen Stark', from_json2('Esercizi/esercizi alberi/esercizi alberi/tree02.json'))
check_test(lambda node: node.to_dict(), {'nodes': [{'nodes': [{'tag': 'Robb e '}, {'tag': 'Arya '}]}, {'tag': ') e Benjen Stark'}]}, from_json2('Esercizi/esercizi alberi/esercizi alberi/tree02.json'))
check_test(Tree.from_dict, from_json2('Esercizi/esercizi alberi/esercizi alberi/tree02.json'), load_json('Esercizi/esercizi alberi/esercizi alberi/tree02.json'))
