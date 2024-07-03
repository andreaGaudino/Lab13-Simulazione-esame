import copy

import networkx as nx

from database.DAO import DAO
import flet as ft
from geopy.distance import geodesic


class Model:
    def __init__(self):
        self.grafo = nx.Graph()
        self.idMap = {}

    def buildGraph(self, forma, anno):
        self.grafo.clear()
        self.idMap = {}
        nodi = DAO.getNodi()
        for n in nodi:
            self.grafo.add_node(n)
            self.idMap[n.id] = n
        archi1= DAO.getArchi1()
        pesi = DAO.getArchi2(forma, anno)
        for a in archi1:
            self.grafo.add_edge(self.idMap[a[0]], self.idMap[a[1]], weight = 0)
        for a in list(self.grafo.edges):
            somma = 0
            if a[0].id in pesi:
                somma+=pesi[a[0].id]
            if a[1].id in pesi:
                somma+=pesi[a[1].id]
            self.grafo.add_edge(a[0],a[1], weight=somma)

    def graphDetails(self):
        return len(self.grafo.nodes), len(self.grafo.edges)

    def getPesi(self):
        result = {}
        for n in list(self.grafo.nodes):
            somma = 0
            for v in list(self.grafo.neighbors(n)):
                somma += self.grafo[n][v]["weight"]
            result[n] = somma
        return result

    def getPercorso(self):
        self.solBest = []
        self.distanzaMax = 0
        for n in list(self.grafo.nodes):
            parziale = []
            parziale.append(n)
            self.ricorsione(parziale)
        print(self.distanzaMax, len(self.solBest))
        return self.distanzaMax, self.solBest


    def ricorsione(self, parziale):
        vicini = list(self.grafo.neighbors(parziale[-1]))
        viciniAmmissibili = self.getAmmissibili(parziale,vicini)
        if len(viciniAmmissibili) == 0:
            tot = 0
            for i in range(len(parziale)-1):
                tot += self.calcolaDistanza((parziale[i], parziale[i+1]))
            if tot > self.distanzaMax:
                self.distanzaMax=tot
                self.solBest = copy.deepcopy(parziale)
        else:
            for v in viciniAmmissibili:
                parziale.append(v)
                self.ricorsione(parziale)
                parziale.pop()
    def calcolaDistanza(self, arco):
        distanza = geodesic((arco[0].Lat, arco[0].Lng), (arco[1].Lat, arco[1].Lng)).km
        return distanza

    def getAmmissibili(self, parziale, vicini):
        ammissibili = []
        if len(parziale) == 1:
            ammissibili = copy.deepcopy(vicini)
            return ammissibili
        for v in vicini:
            boolean = False
            if self.grafo[parziale[-1]][v]["weight"] > self.grafo[parziale[-1]][parziale[-2]]["weight"]:
                for i in range(len(parziale)-1):
                    if {parziale[-1], v} == {parziale[i], parziale[i+1]}:
                        boolean = True
                if not boolean:
                    ammissibili.append(v)
        return ammissibili


    def fillDDAnno(self):
        anni = DAO.getAnni()
        return anni

    def fillDDForme(self, anno):
        forme = DAO.getForme(anno)
        return forme