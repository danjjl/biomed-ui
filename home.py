#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui

from users import users
from graph import graph

"""Ecran d'accueil
Gère les deux widget qui sont présents sur l'écran d'acceuil : graph et users
"""
class home(QtGui.QWidget):
    def __init__(self):
        super(home, self).__init__()

        self.graphs = graph() #Initialisation (commence caché)
        self.userCards = users() # (commence affiché)

        self.layout = QtGui.QVBoxLayout(self) #Layout pour que leur resize soit dynamique
        self.layout.addWidget(self.userCards)
        self.layout.addWidget(self.graphs)

        """Lie les actions d'un widget à l'autre"""
        self.userCards.callGraph.connect(self._graphCaller) #Appel d'un nouveau graph
        self.graphs.hideCall.connect(self._chooseUser) #Retour choix utilisateurs

    """index: id de l'utilisateur, mesure : type de la mesure (string présent dans la db)'"""
    def _graphCaller(self, index, mesure):
        self.userCards.hide()
        self.graphs.redraw(index, mesure)

    def _chooseUser(self):
        self.graphs.hide()
        self.userCards.show()
