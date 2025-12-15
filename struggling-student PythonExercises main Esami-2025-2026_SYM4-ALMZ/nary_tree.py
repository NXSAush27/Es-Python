
import copy
import random

class NaryTree:
    def __init__(self, V, children=None):
        self.value = V
        self.children = [] if children is None else children

################### THE FOLLOWING METHODS ARE USED IN TESTS, AND ARE FORBIDDEN #####################

    @classmethod
    def fromList(cls, lista):
        """
        Costruisce l'albero da una lista [value, figlio1, figlio2, ...]
        In cui figlio1, figlio2, ... sono altrettanti alberi oppure il value None
        :param lista:
        :return:
        """
        value, *children = lista
        children = [ cls.fromList(son) for son in children ]
        return cls(value, children)

    def toList(self):
        """
        Converte l'albero in lista di liste [value, figlio1, figlio2, ...]
        :return:
        """
        children = [son.toList() for son in self.children]
        return [self.value, *children]

    def __eq__(self, other):
        """
        Confronta due alberi
        :param other:
        :return:
        """
        return other != None and \
            type(self) == type(other) and \
            self.value == other.value and \
            self.children  == other.children

    def __repr__(self, livello=0):
        """
        Stampa un albero con livello di indentazione dato
        :param livello: indentazione
        :return:
        """
        indent = "|   "*(livello+1)
        res = f'{self.value}'
        for son in self.children:
            res += f"\n{indent} {son.__repr__(livello+1)}"
        return res

    @classmethod
    def randomTree(cls, level):
        """
        Genera un albero casuale di al più level livelli
        :param level:
        :return:
        """
        V = random.randint(-100, 100)
        if level >= 0:
            children = [cls.randomTree(level - random.randint(1,3))
                        for _ in range(random.randint(0,3))]
        else:
            children = []
        return cls(V, children)

if __name__ == '__main__':
    pass
    root = NaryTree.randomTree(10)
    print(root)
    print(root.toList())
