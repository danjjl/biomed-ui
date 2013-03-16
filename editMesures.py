#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtCore, QtGui, QtSql

from mesureToExistingUser import mesureToExistingUser
from CheckboxQuerySqlModel import CheckboxQuerySqlModel

"""Empeche l'édition d'un d'un QSqlRelationalTableModel"""
class customQSqlRelationalTableModel(QtSql.QSqlRelationalTableModel):
    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled

class editMesures(QtGui.QWidget):
    dbChange = QtCore.pyqtSignal() #Signal utilisé sur modif db

    def __init__(self):
        super(editMesures, self).__init__()
        """Connection à la db; chargement des données dans le modèle"""
        self.model = CheckboxQuerySqlModel(1) #Modèle dans lequel la db sera chargée
        self.model.setTable("mesures")
        self.model.setRelation(1, QtSql.QSqlRelation('utilisateurs', 'id', 'prenom'))
        self.model.select()

        """Associe le modèle à une vue"""
        self.table = QtGui.QTableView() #associe les données à une vue
        self.table.setModel(self.model)

        self.table.hideColumn(0) #cache les colonnes id

        """Action buttons"""
        self.changeUser = QtGui.QPushButton("Changer d'utilisateur") #Boutons
        self.deleteMesure = QtGui.QPushButton("Supprimer mesure(s)")
        self.checkAll = QtGui.QPushButton("Tout selectionner")
        self.uncheckAll = QtGui.QPushButton("Tout deselectionner")

        self.changeUser.clicked.connect(self.changeUsers) #Action se déclenchant après un click sur un bouton
        self.deleteMesure.clicked.connect(self.delMesures)
        self.checkAll.clicked.connect(self.check)
        self.uncheckAll.clicked.connect(self.uncheck)

        """Build layouts"""
        self.buttons = QtGui.QVBoxLayout() #Conteneur vertical pour les boutons
        self.buttons.addWidget(self.changeUser)
        self.buttons.addWidget(self.deleteMesure)
        self.buttons.addWidget(self.checkAll)
        self.buttons.addWidget(self.uncheckAll)

        self.mainView = QtGui.QHBoxLayout() #Conteneur horizontal pour la table et le conteneur des boutons
        self.mainView.addWidget(self.table)
        self.mainView.addLayout(self.buttons)

        self.setLayout(self.mainView) #Display
        self.show()

    def changeUsers(self):
        index = self.model.listChecked()
        if index: #Si liste non vide
            mesureToExistingUser(self, index)
            self.dbChange.emit()

    def delMesures(self):
        indexes = self.model.listChecked()
        if indexes: #Si liste non vide
            answer = QtGui.QMessageBox.critical(self, "Suppression de mesures", "Etes-vous sur de vouloir supprimer ces mesures?\nCette action est irrevoquable", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
            if answer == QtGui.QMessageBox.Yes:
                query = QtSql.QSqlQuery()
                for index in indexes:
                    query.exec_("DELETE FROM mesures WHERE id="+str(index)+"")
                self.dbChange.emit()

    def check(self):
        self.model.changeCheck(QtCore.Qt.Checked) #Coche tous les checkbox

    def uncheck(self):
        self.model.changeCheck(QtCore.Qt.Unchecked) #Décoche tous les checkbox

    def update(self):
        self.model.setTable("mesures")
        self.model.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
        self.model.setRelation(1, QtSql.QSqlRelation('utilisateurs', 'id', 'prenom'))
        self.model.select()
