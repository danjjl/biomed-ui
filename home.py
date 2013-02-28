#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtCore, QtGui, QtSql

"""Redéfini une nouvelle classe de bouton qui connait son id, permet d'émettre sur click en envoyant l'id du bouton)"""
class buttonId(QtGui.QPushButton):
    clikedId = QtCore.pyqtSignal(int) #Je sais pas pk le rentrer ds le constructeur fait planter le emit

    def __init__(self, label, index, mesure):
        super(buttonId, self).__init__(label)
        self.index = index #Id du bouton (id de l'utilisateur)
        self.mesure = mesure #Type de mesure

        self.clicked.connect(self.pushed) #Redéfini le signal clicked pour passer l'id en paramètre
    def pushed(self):
        self.clikedId.emit(self.index)

"""Ecran d'accueil"""
class home(QtGui.QWidget):
    def __init__(self):
        super(home, self).__init__()

        """On rangera les boutons dans ce layout"""
        self.layout = QtGui.QGridLayout(self) # Chaque fiche d'utilisateur sera rangé ds un grid layout en 2 collones
        x = 0 #Utilisé pour ranger les boutons proprement en 2 colonnes
        y = 0

        """Récupère les données et les affiche dans un bouton"""
        utilisateurs = QtSql.QSqlQuery() #Requete : des utilisateurs (pas self car peut être détruit après le constructeur)
        mesures = QtSql.QSqlQuery() #Requete : des mesures
        utilisateurs.exec_("SELECT id, nom, prenom FROM utilisateurs")

        #On parcours tous les utilisateurs
        while utilisateurs.next():

            #Récupère les identifiant des utilisateurs
            curId = utilisateurs.value(0).toInt()[0] #Id utilisateur
            lastName = utilisateurs.value(1).toString() #Nom
            firstName = utilisateurs.value(2).toString() #Prénom

            mesures.exec_("SELECT poids, taille, temperature, frequence FROM mesures WHERE utilisateur="+str(curId)+" ORDER BY time DESC LIMIT 1")
            #Si ils ont une mesure associé on récupère la dernière
            if mesures.first():

                #Récupère la dernière mesure
                weight = mesures.value(0).toDouble()[0]
                size = mesures.value(1).toDouble()[0]
                temperature = mesures.value(2).toDouble()[0]
                frequence = mesures.value(3).toDouble()[0]

                #Affiche les info dans un layout
                info = QtGui.QFormLayout()
                info.addRow(QtGui.QLabel("<b>"+firstName+" "+lastName+"</b>"))
                info.addRow(buttonId("BMI", curId, "bmi"), QtGui.QLabel(str((weight**2)/size)[0:5]))
                info.addRow(buttonId("Poids", curId, "weight"), QtGui.QLabel(str(weight)[0:5]))
                info.addRow(buttonId("Taille", curId, "size"), QtGui.QLabel(str(size)[0:5]))
                info.addRow(buttonId("Temperature", curId, "temp"), QtGui.QLabel(str(temperature)[0:5]))
                info.addRow(buttonId("Frequence", curId, "freq"), QtGui.QLabel(str(frequence)[0:4]))

                #Bouton contenant les infos permettre de voir des vues spécifiques
                self.button = QtGui.QFrame()#buttonId(curId)
                self.button.setFrameShape(QtGui.QFrame.WinPanel)
                #self.button.clickedId.connect(......) Chaque bouton sera connecté
                self.button.setLayout(info)
                self.button.setMinimumHeight(50) #Hauteur min du bouton
                self.layout.addWidget(self.button, x, y) #ajoute bouton au grid

                #Prépare les coordonées du prochain bouton
                x += 1
                if x > 1:
                    x = 0
                    y += 1
