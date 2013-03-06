#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtCore, QtGui, QtSql

from editUser import editUser

class editUsers(QtGui.QWidget):
    dbChange = QtCore.pyqtSignal() #Signal utilisé sur modif db

    def __init__(self):
        super(editUsers, self).__init__()

        """Connection à la db; chargement des données dans le modèle"""
        self.model = QtSql.QSqlQueryModel() #Modèle dans lequel la db sera chargée
        self.model.setQuery('select * from utilisateurs') #Requête pour récupérer les utilisateurs

        """Associe le modèle à une vue"""
        self.table = QtGui.QTableView() #associe les données à une vue
        self.table.setModel(self.model)

        self.table.hideColumn(0) #cache la colonne id

        """Liste des radio(Solution temporaire (prob esthétique))"""
        self.radioLayout = QtGui.QVBoxLayout() #Conteneur vertical à radio
        self._radioList()

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
        self.mainView.addLayout(self.radioLayout)
        self.mainView.addWidget(self.table)
        self.mainView.addLayout(self.buttons)

        self.setLayout(self.mainView) #Display
        self.show()

    def _radioList(self): #Fonction privée à ne pas utiliser hors de la classe
        self.radios = list()#liste ou l'on stoque les index et les radio
        for i in range(0, self.model.rowCount()):
            self.radios.append((self.model.data(self.model.index(i, 0)).toInt()[0], QtGui.QRadioButton())) #(index, Qradio)
            self.radioLayout.addWidget(self.radios[-1][1])

    def _emptyCheckboxList(self): #Fonction privée à ne pas utiliser hors de la classe
        for box in self.radios:
            self.radioLayout.removeWidget(box[1]) #L'enlève du layout
            box[1].hide()
            box[1].close() #Delete le radio

    def _listChecked(self): #Fonction privée à ne pas utiliser hors de la classe
        index = list() #List des id cochés
        for box in self.radios:
            if box[1].isChecked():
                index.append(box[0])
        return index

    def _infoUser(self):
        for i in range(0, self.model.rowCount()):
            if self.radios[i][1].isChecked():
                lastName = self.model.data(self.model.index(i, 1)).toString()
                firstName = self.model.data(self.model.index(i, 2)).toString()
                age = self.model.data(self.model.index(i, 3)).toString()
                sexe = self.model.data(self.model.index(i, 4)).toString()
        return (lastName, firstName, age, sexe)

    def delUser(self):
        index = self._listChecked()
        if index: #Si liste non vide
            answer = QtGui.QMessageBox.critical(self, "Suppression utilisateur", "Etes-vous sur de vouloir supprimer l'utilisateur?\nCette action est irrevoquable et supprimera egalement toutes les mesures associees a l'utilisateur", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
            if answer == QtGui.QMessageBox.Yes:
                query = QtSql.QSqlQuery()
                query.exec_("DELETE FROM utilisateurs WHERE id="+str(index[0])+"")
                query.exec_("DELETE FROM mesures WHERE utilisateur="+str(index[0])+"")
                self.dbChange.emit()

    def modifyUser(self):
        index = self._listChecked()
        if index: #Si liste non vide
            (lastName, firstName, age, sexe) = self._infoUser()
            editUser(self, index, lastName, firstName, age, sexe)
            self.dbChange.emit()

    def update(self):
        self.model.setQuery('select * from utilisateurs') #Recrée le modèle
        self._emptyCheckboxList() #Delete les anciennes radio
        self._radioList() #en crée des nouvelles
