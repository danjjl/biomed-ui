#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtCore, QtGui, QtSql

from newUser import newUser

class noUserMesures(QtGui.QWidget):
    def __init__(self, layout):
        super(noUserMesures, self).__init__()

        self.layout = layout

        """Connection à la db; chargement des données dans le modèle"""
        self.model = QtSql.QSqlQueryModel() #Modèle dans lequel la db sera chargée
        self.model.setQuery('select * from mesures WHERE utilisateur=0 ORDER BY time') #Requête pour récupérer les mesures n'ayant d'utilisateurs

        """Associe le modèle à une vue"""
        self.table = QtGui.QTableView() #associe les données à une vue
        self.table.setModel(self.model)

        self.table.hideColumn(0) #cache les colonnes id
        self.table.hideColumn(1)

        """Liste des checkbox(Solution temporaire (prob esthétique))"""
        self.checkboxLayout = QtGui.QVBoxLayout() #Conteneur vertical à checkbox
        self.checkboxes = list()#liste ou l'on stoque les index et les checkbox
        for i in range(0, self.model.rowCount()):
            self.checkboxes.append((self.model.data(self.model.index(i, 0)).toInt()[0], QtGui.QCheckBox())) #(index, QCheckbox)
            self.checkboxLayout.addWidget(self.checkboxes[-1][1])

        """Action buttons"""
        self.newUser = QtGui.QPushButton("Nouvel utilisateur") #Boutons
        self.existingUser = QtGui.QPushButton("Utilisateur existant")
        self.checkAll = QtGui.QPushButton("Tout selectionner")
        self.uncheckAll = QtGui.QPushButton("Tout deselectionner")

        self.newUser.clicked.connect(self.addNewUser) #Action se déclenchant après un click sur un bouton
        self.checkAll.clicked.connect(self.check)
        self.uncheckAll.clicked.connect(self.uncheck)

        """Build layouts"""
        self.buttons = QtGui.QVBoxLayout() #Conteneur vertical pour les boutons
        self.buttons.addWidget(self.newUser)
        self.buttons.addWidget(self.existingUser)
        self.buttons.addWidget(self.checkAll)
        self.buttons.addWidget(self.uncheckAll)

        self.mainView = QtGui.QHBoxLayout() #Conteneur horizontal pour la table et le conteneur des boutons
        self.mainView.addLayout(self.checkboxLayout)
        self.mainView.addWidget(self.table)
        self.mainView.addLayout(self.buttons)

        self.setLayout(self.mainView) #Display
        self.show()

    def addNewUser(self):
        index = list() #List des id cochés
        for box in self.checkboxes:
            if box[1].isChecked():
                index.append(box[0])
        if index: #Si liste non vide
            newUser(self, index)

    def check(self):
        for box in self.checkboxes:
            box[1].setCheckState(QtCore.Qt.Checked) #Coche tous les checkbox

    def uncheck(self):
        for box in self.checkboxes:
            box[1].setCheckState(QtCore.Qt.Unchecked) #Décoche tous les checkbox
