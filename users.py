#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtCore, QtGui, QtSql

"""Redéfini une nouvelle classe de bouton qui connait son id, permet d'émettre sur click en envoyant l'id du bouton"""
class buttonId(QtGui.QPushButton):
    clikedId = QtCore.pyqtSignal(int, str, str)

    def __init__(self, label, index, mesure, name):
        super(buttonId, self).__init__(label)
        self.index = index #Id de l'utilisateur
        self.mesure = mesure #Type de mesure (str d'un champs de la db sauf BMI)
        self.name = name

        self.clicked.connect(self._clicked) #Redéfini le signal clicked pour passer l'id en paramètre
    def _clicked(self):
        self.clikedId.emit(self.index, self.mesure, self.name)

"""Ecran d'accueil"""
class users(QtGui.QWidget):
    callGraph = QtCore.pyqtSignal(int, str, str)

    def __init__(self):
        super(users, self).__init__()

        """On rangera les boutons dans ce layout"""
        self.layout = QtGui.QGridLayout(self) # Chaque fiche d'utilisateur sera rangé ds un grid layout en 2 collones
        self.x = 0 #Utilisé pour ranger les boutons proprement en 2 colonnes
        self.y = 0


        """Requete SQL"""
        self.utilisateurs = QtSql.QSqlQuery() #Requete : des utilisateurs (pas self car peut être détruit après le constructeur)
        self.mesures = QtSql.QSqlQuery() #Requete : des mesures

        self.update() #Update construit la grille

        self.show()

    def _graphCaller(self, index, mesure, name):
        self.callGraph.emit(index, mesure, name)

    """Genre de %2 pour parcourir le grid de bas en haut"""
    def _negMod(self):
        self.x += -1
        if self.x < 0:
            self.x = 1
            self.y += -1

    def _emptyGrid(self):
        self._negMod() #x est 1 trop loin
        while self.y >=0:
            self.layout.itemAtPosition(self.x, self.y).widget().hide()
            self.layout.removeItem(self.layout.itemAtPosition(self.x, self.y)) #Pourrait faire 'mieux' en vidant le QFormLayout
            self._negMod()

    def update(self):

        self._emptyGrid()

        """Coordonnée du layout"""
        self.x = 0 #Utilisé pour ranger les boutons proprement en 2 colonnes
        self.y = 0

        """Récupère les données et les affiche dans un bouton"""
        self.utilisateurs.exec_("SELECT id, nom, prenom FROM utilisateurs")

        """On parcours tous les utilisateurs"""
        while self.utilisateurs.next():
            """Récupère les identifiant des utilisateurs"""
            curId = self.utilisateurs.value(0).toInt()[0] #Id utilisateur
            lastName = self.utilisateurs.value(1).toString() #Nom
            firstName = self.utilisateurs.value(2).toString() #Prénom

            self.mesures.exec_("SELECT poids, taille, temperature, frequence FROM mesures WHERE utilisateur="+str(curId)+" ORDER BY time DESC LIMIT 1")
            #Si ils ont une mesure associé on récupère la dernière
            if self.mesures.first():
                """Récupère la dernière mesure"""
                weight = self.mesures.value(0).toDouble()[0]
                size = self.mesures.value(1).toDouble()[0]
                temperature = self.mesures.value(2).toDouble()[0]
                frequence = self.mesures.value(3).toDouble()[0]

                """Les boutons"""
                self.buttons = list()
                self.buttons.append(buttonId("BMI", curId, "bmi", firstName + " " + lastName))
                self.buttons.append(buttonId("Poids", curId, "poids", firstName + " " + lastName))
                self.buttons.append(buttonId("Taille", curId, "taille", firstName + " " + lastName))
                self.buttons.append(buttonId("Temperature", curId, "temperature", firstName + " " + lastName))
                self.buttons.append(buttonId("Frequence", curId, "frequence", firstName + " " + lastName))

                """Les labels"""
                self.labels = list()
                self.labels.append(QtGui.QLabel(str((weight**2)/size)[0:5]))
                self.labels.append(QtGui.QLabel(str(weight)[0:5]))
                self.labels.append(QtGui.QLabel(str(size)[0:5]))
                self.labels.append(QtGui.QLabel(str(temperature)[0:5]))
                self.labels.append(QtGui.QLabel(str(frequence)[0:4]))

                """Affiche les info dans un layout"""
                self.info = QtGui.QFormLayout()
                self.info.addRow(QtGui.QLabel("<b>"+firstName+" "+lastName+"</b>"))
                for button, label in zip(self.buttons, self.labels):
                    self.info.addRow(button, label)
                    #connecte button to caller
                    button.clikedId.connect(self._graphCaller)

                """Cadre contenant les infos permettre de voir des vues spécifiques"""
                self.cell = QtGui.QFrame()#buttonId(curId)
                self.cell.setFrameShape(QtGui.QFrame.WinPanel)
                #self.button.clickedId.connect(......) Chaque bouton sera connecté
                self.cell.setLayout(self.info)
                self.layout.addWidget(self.cell, self.x, self.y) #ajoute bouton au grid

                """Prépare les coordonées du prochain bouton"""
                self.x += 1
                if self.x > 1:
                    self.x = 0
                    self.y += 1
