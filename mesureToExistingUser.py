#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui, QtSql

class mesureToExistingUser(QtGui.QDialog):
    def __init__(self, parent, mesures):
        super(mesureToExistingUser, self).__init__(parent)

        self.parent = parent
        self.mesures = mesures

        """chargement des données dans le modèle""" #Partage le même code que NewUser pour tout ce qui est modèle/vue
        self.model = QtSql.QSqlQueryModel() #Modèle dans lequel la db sera chargée
        self.model.setQuery('SELECT poids, taille, temperature, frequence, time FROM mesures WHERE id in('+ str(mesures)[1:-1] +') ORDER BY time') #Requête pour récupérer les mesures avec un id ds mesures

        """Associe le modèle à une vue"""
        self.table = QtGui.QTableView() #associe les données à une vue
        self.table.setModel(self.model)

        """Récupère les utilisateurs, les range dans une QComboBox"""
        self.query = QtSql.QSqlQuery()
        self.query.exec_("SELECT id, nom, prenom FROM utilisateurs")
        self.utlisateurs = QtGui.QComboBox() #Liste déroulante
        while self.query.next():
            curId = self.query.value(0).toInt()[0] #Id utilisateur
            lastName = self.query.value(1).toString() #Nom
            firstName = self.query.value(2).toString() #Prénom
            self.utlisateurs.addItem(firstName + " " + lastName, curId)

        """Boutons d'actions"""
        self.cancel = QtGui.QPushButton("Annuler") #Cancel
        self.submit = QtGui.QPushButton("Ajouter") #Ajoute les mesures à l'utilisateur

        self.cancel.clicked.connect(self.returnNoUserMesures)
        self.submit.clicked.connect(self.addToUser)

        """Layout des boutons"""
        self.buttons = QtGui.QHBoxLayout()
        self.buttons.addWidget(self.cancel)
        self.buttons.addWidget(self.submit)

        """Layout du formulaire + label"""
        self.formulaire = QtGui.QFormLayout()
        self.formulaire.addRow("Mesures", self.table)
        self.formulaire.addRow("Utilisateur", self.utlisateurs)
        self.formulaire.addRow(self.buttons) #Ajoute un Layout

        self.setLayout(self.formulaire)
        self.exec_()

    def returnNoUserMesures(self):
        self.close() #Retourne à la sélection des mesures

    def addToUser(self):
        "Récupère l'id de l'utilisateur sélectionné"
        curId = self.utlisateurs.itemData(self.utlisateurs.currentIndex()).toInt()[0] #(C'est horrible comme ligne !)

        """Ajoute l'utilisateur aux mesures'"""
        for index in self.mesures:
            self.query.exec_("UPDATE mesures SET utilisateur ="+ str(curId) +" WHERE id ="+ str(index) +"")

        """Cache la fenetre"""
        self.parent.update()
        self.close()
