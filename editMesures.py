#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtCore, QtGui, QtSql

from mesureToExistingUser import mesureToExistingUser

"""Empeche l'édition d'un d'un QSqlRelationalTableModel"""
class customQSqlRelationalTableModel(QtSql.QSqlRelationalTableModel):
    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled

class editMesures(QtGui.QWidget):
    dbChange = QtCore.pyqtSignal() #Signal utilisé sur modif db

    def __init__(self):
        super(editMesures, self).__init__()
#TODO GET LAST NAME
        """Connection à la db; chargement des données dans le modèle"""
        self.model = customQSqlRelationalTableModel() #Modèle dans lequel la db sera chargée
        self.model.setTable("mesures")
        self.model.setRelation(1, QtSql.QSqlRelation('utilisateurs', 'id', 'prenom'))
        self.model.select()

        """Associe le modèle à une vue"""
        self.table = QtGui.QTableView() #associe les données à une vue
        self.table.setModel(self.model)

        self.table.hideColumn(0) #cache les colonnes id

        """Liste des checkbox(Solution temporaire (prob esthétique))"""
        self.checkboxLayout = QtGui.QVBoxLayout() #Conteneur vertical à checkbox
        self._checkboxList()

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
        self.mainView.addLayout(self.checkboxLayout)
        self.mainView.addWidget(self.table)
        self.mainView.addLayout(self.buttons)

        self.setLayout(self.mainView) #Display
        self.show()

    def _checkboxList(self): #Fonction privée à ne pas utiliser hors de la classe
        self.checkboxes = list()#liste ou l'on stoque les index et les checkbox
        for i in range(0, self.model.rowCount()):
            self.checkboxes.append((self.model.data(self.model.index(i, 0)).toInt()[0], QtGui.QCheckBox())) #(index, QCheckbox)
            self.checkboxLayout.addWidget(self.checkboxes[-1][1])

    def _emptyCheckboxList(self): #Fonction privée à ne pas utiliser hors de la classe
        for box in self.checkboxes:
            self.checkboxLayout.removeWidget(box[1]) #L'enlève du layout
            box[1].close() #Delete le checkbox

    def _listChecked(self): #Fonction privée à ne pas utiliser hors de la classe
        index = list() #List des id cochés
        for box in self.checkboxes:
            if box[1].isChecked():
                index.append(box[0])
        return index

    def changeUsers(self):
        index = self._listChecked()
        if index: #Si liste non vide
            mesureToExistingUser(self, index)
            self.dbChange.emit()

    def delMesures(self):
        indexes = self._listChecked()
        if indexes: #Si liste non vide
            answer = QtGui.QMessageBox.critical(self, "Suppression de mesures", "Etes-vous sur de vouloir supprimer ces mesures?\nCette action est irrevoquable", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
            if answer == QtGui.QMessageBox.Yes:
                query = QtSql.QSqlQuery()
                for index in indexes:
                    query.exec_("DELETE FROM mesures WHERE id="+str(index)+"")
                self.dbChange.emit()

    def check(self):
        for box in self.checkboxes:
            box[1].setCheckState(QtCore.Qt.Checked) #Coche tous les checkbox

    def uncheck(self):
        for box in self.checkboxes:
            box[1].setCheckState(QtCore.Qt.Unchecked) #Décoche tous les checkbox

    def update(self):
        self.model.setTable("mesures")
        self.model.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
        self.model.setRelation(1, QtSql.QSqlRelation('utilisateurs', 'id', 'prenom'))
        self.model.select()

        self._emptyCheckboxList() #Delete les anciennes checkbox
        self._checkboxList() #en crée des nouvelles
