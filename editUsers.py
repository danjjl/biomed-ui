#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtCore, QtGui, QtSql

from editUser import editUser
from CheckboxSqlModel import CheckboxSqlModel

class RadioSqlModel(CheckboxSqlModel):
    #Réimplémente pour que ce soit un radio
    def setData(self, index, value, role=QtCore.Qt.DisplayRole):
        row = index.row()
        if index.column() == self.column and role == QtCore.Qt.CheckStateRole:
            if value.toBool():
                self.changeCheck(QtCore.Qt.Unchecked)
                self.checkboxes[row] = True
            else:
                self.checkboxes[row] = False
            #On a changé la case en index (2 index (haut gauche -> bas droite))
            self.dataChanged.emit(index, index)
            #Le changement a bien eu lieu
            return True
        else:
            #On a rien changé
            return False

class editUsers(QtGui.QWidget):
    dbChange = QtCore.pyqtSignal() #Signal utilisé sur modif db

    def __init__(self):
        super(editUsers, self).__init__()

        """Connection à la db; chargement des données dans le modèle"""
        self.model = RadioSqlModel(1) #Modèle dans lequel la db sera chargée
        self.model.setQuery('select * from utilisateurs') #Requête pour récupérer les utilisateurs

        """Associe le modèle à une vue"""
        self.table = QtGui.QTableView() #associe les données à une vue
        self.table.setModel(self.model)

        self.table.hideColumn(0) #cache la colonne id

        """Action buttons"""
        self.deleteUser = QtGui.QPushButton("Supprimer l'utilisateur") #Boutons
        self.editUser = QtGui.QPushButton("Editer l'utilisateur")

        self.deleteUser.clicked.connect(self.delUser) #Action se déclenchant après un click sur un bouton
        self.editUser.clicked.connect(self.modifyUser)

        """Build layouts"""
        self.buttons = QtGui.QVBoxLayout() #Conteneur vertical pour les boutons
        self.buttons.addWidget(self.editUser)
        self.buttons.addWidget(self.deleteUser)

        self.mainView = QtGui.QHBoxLayout() #Conteneur horizontal pour la table et le conteneur des boutons
        self.mainView.addWidget(self.table)
        self.mainView.addLayout(self.buttons)

        self.setLayout(self.mainView) #Display
        self.show()

    def _infoUser(self):
        for i in range(0, self.model.rowCount()):
            if self.radios[i][1].isChecked():
                lastName = self.model.data(self.model.index(i, 1)).toString()
                firstName = self.model.data(self.model.index(i, 2)).toString()
                age = self.model.data(self.model.index(i, 3)).toString()
                sexe = self.model.data(self.model.index(i, 4)).toString()
        return (lastName, firstName, age, sexe)

    def delUser(self):
        index = self.model.listChecked()
        if index: #Si liste non vide
            answer = QtGui.QMessageBox.critical(self, "Suppression utilisateur", "Etes-vous sur de vouloir supprimer l'utilisateur?\nCette action est irrevoquable et supprimera egalement toutes les mesures associees a l'utilisateur", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
            if answer == QtGui.QMessageBox.Yes:
                query = QtSql.QSqlQuery()
                query.exec_("DELETE FROM utilisateurs WHERE id="+str(index[0])+"")
                query.exec_("DELETE FROM mesures WHERE utilisateur="+str(index[0])+"")
                self.dbChange.emit()

    def modifyUser(self):
        index = self.model.listChecked()
        if index: #Si liste non vide
            (lastName, firstName, age, sexe) = self._infoUser()
            editUser(self, index, lastName, firstName, age, sexe)
            self.dbChange.emit()

    def update(self):
        self.model.setQuery('select * from utilisateurs') #Recrée le modèle
