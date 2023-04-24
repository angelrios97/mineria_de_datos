# -*- coding: cp1252 -*-
import heapq
from collections import defaultdict
class TopK:
    '''This class implements an iterator for getting the first K closed sets'''
    def __init__(self, nameFile,K=2):
        '''Initialize the attributes
        - transactions: a list of all transactions in the
        dataset (a transaction is a set of items),
        - items: a list of all items,
        - l: the number of transactions
        - l_items: the number of items
        '''
        self.K=K
        self.transactions=[] #all transactions as a list of sets of items
        d=defaultdict(lambda:0) # all items with their frequencies
        for tran in open(nameFile):
            tran_items=set(tran.strip().split())
            self.transactions.append(tran_items)
            for item in tran_items:
                d[item]+=1
        self.items=[x for x,y in sorted(list(d.items()),key=lambda x: x[1],reverse=True)] #all the items in descdending oreder of support
        self.l=len(self.transactions) # number of transactions
        self.l_items=len(self.items) #number of items


    def __iter__(self):
        '''
        This method is necessary to initialize the
        iterator.
        '''
        self.q=[]
        heapq.heapify(self.q)
        self.generatedK=0
        element=self.closure(self.transactions)
        heapq.heappush(self.q,(0,(element,self.transactions,0)))
        return self

    def jth_prefix(self,itemset,j):
        '''
        This method returns the jth prefix of an itemset
        (Assume the alphabet is indexed from 1 to n)
        '''
        result = set.intersection(set(self.items[:j]), itemset)  # j primeros elementos
        return result

    def extract_trans(self,it,trans_list):
        '''
        This method receives as parameters an item it
        and a list of transactions (each being a set of items)
        and filters the list of transactions, returning only
        those that contain the item it
        '''
        result = []  # Inicialización de result.
        for _ in trans_list:  # Recorremos los conjuntos de la transacción.
            if it in _:  # Si it está en la transacción,
                result.append(_)  # añadimos la transacción.
        return result

    def closure(self,trans_list):
        '''
        This method returns the set of items that are included
        in all transactions in trans_list. If trans_list is empty,
        it returns the set of all items
        '''
        if trans_list == []:
            return set(self.items)
        result = set(self.items)  # Inicialización de result.
        for _ in trans_list:
            result.intersection_update(_) # Intersección de result con _
        return result


    def __next__(self):
        '''
        This method is the main function of the class. It throws
        StopIteration if more elements than necessary are generated
        or if there is no other closed set in the priority queue.

        '''
        if self.generatedK>self.K or not self.q:
            raise StopIteration

        Ysupp, (Yitems, Ytrans_list, Ycore) = heapq.heappop(self.q)
        for j in range(Ycore, self.l_items):  # Empieza en la posición Ycore de la lista, es decir, en a_{Ycore+1} como queremos.
            if self.items[j] not in Yitems:  # Si a_{j+1} no está en Yitems
                next_trans_list = self.extract_trans(self.items[j], Ytrans_list)  # Xtranslist
                next_items = self.closure(next_trans_list)  # Xitems
                if self.jth_prefix(next_items, j) == self.jth_prefix(Yitems, j):  # Si X(j) == Y(j)  (porque estamos en a_{j+1})
                    next_core = j + 1  # Xcore = j+1
                    next_supp = len(next_trans_list)  # Xsupp = len(Xtranslist)
                    heapq.heappush(self.q, (self.l - next_supp, (next_items, next_trans_list, next_core)))
        self.generatedK=self.generatedK+1
        return Yitems

if __name__=='__main__':
    a=TopK('data.txt',13)
    solucion=['[]']
    solucion.append('[\'Female\']')
    solucion.append('[\'DoNotOwnHome\']')
    solucion.append('[\'Homeowner\']')
    solucion.append('[\'Male\']')
    solucion.append('[\'cannedveg\']')
    solucion.append('[\'frozenmeal\']')
    solucion.append('[\'fruitveg\']')
    solucion.append('[\'beer\']')
    solucion.append('[\'fish\']')
    solucion.append('[\'wine\']')
    solucion.append('[\'confectionery\']')
    solucion.append('[\'Female\', \'Homeowner\']')
    solucion.append('[\'DoNotOwnHome\', \'Female\']')
    solucion.append('[\'DoNotOwnHome\', \'Male\']')
    solucion.append('[\'Homeowner\', \'Male\']')
    solucion.append('[\'Male\', \'frozenmeal\']')
    solucion.append('[\'cannedmeat\']')
    solucion.append('[\'Male\', \'cannedveg\']')
    solucion.append('[\'DoNotOwnHome\', \'fish\']')
    solucion.append('[\'Male\', \'beer\']')
    for num,e in enumerate(a):
        print("Solucion:",solucion[num]," Valor del programa:",sorted(e))