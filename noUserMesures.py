#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtCore, QtGui, QtSql

from newUser import newUser
from mesureToExistingUser import mesureToExistingUser
from CheckboxSqlModel import CheckboxSqlModel


class noUserMesures(QtGui.QWidget):
    dbChange = QtCore.pyqtSignal() #Signal utilisé sur modif db

    def __init__(self):
        super(noUserMesures, self).__init__()

        """Connection à la db; chargement des données dans le modèle"""
        self.model = CheckboxSqlModel(2) #Modèle dans lequel la db sera chargée
        self.model.setQuery('select * from mesures WHERE utilisateur=0 ORDER BY time') #Requête pour récupérer les mesures n'ayant d'utilisateurs

        """Associe le modèle à une vue"""
        self.table = QtGui.QTableView() #associe les données à une vue
        self.table.setModel(self.model)

        self.table.hideColumn(0) #cache les colonnes id
        self.table.hideColumn(1)

        """Action buttons"""
        self.newUser = QtGui.QPushButton("Nouvel utilisateur") #Boutons
        self.existingUser = QtGui.QPushButton("Utilisateur existant")
        self.checkAll = QtGui.QPushButton("Tout selectionner")
        self.uncheckAll = QtGui.QPushButton("Tout deselectionner")

        self.newUser.clicked.connect(self.addNewUser) #Action se déclenchant après un click sur un bouton
        self.existingUser.clicked.connect(self.addExistingUser)
        self.checkAll.clicked.connect(self.check)
        self.uncheckAll.clicked.connect(self.uncheck)

        """Build layouts"""
        self.buttons = QtGui.QVBoxLayout() #Conteneur vertical pour les boutons
        self.buttons.addWidget(self.newUser)
        self.buttons.addWidget(self.existingUser)
        self.buttons.addWidget(self.checkAll)
        self.buttons.addWidget(self.uncheckAll)

        self.mainView = QtGui.QHBoxLayout() #Conteneur horizontal pour la table et le conteneur des boutons
        self.mainView.addWidget(self.table)
        self.mainView.addLayout(self.buttons)

        self.setLayout(self.mainView) #Display
        self.show()

    def addNewUser(self):
        index = self.model.listChecked()
        if index: #Si liste non vide
            newUser(self, index)
            self.dbChange.emit()

    def addExistingUser(self):
        index = self.model.listChecked()
        if index: #Si liste non vide
            mesureToExistingUser(self, index)
            self.dbChange.emit()

    def check(self):
        self.model.changeCheck(QtCore.Qt.Checked)

    def uncheck(self):
        self.model.changeCheck(QtCore.Qt.Unchecked)

    def update(self):
        self.model.setQuery('select * from mesures WHERE utilisateur=0 ORDER BY time') #Recrée le modèle
