#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtCore, QtGui, QtSql

class newUser(QtGui.QWidget):
    def __init__(self, parent, mesures):
        super(newUser, self).__init__(parent)

        """Connection à la db; chargement des données dans le modèle"""
        self.db = QtSql.QSqlDatabase.addDatabase('QSQLITE') #Défini le type de db (ici SqlLite)
        self.db.setDatabaseName('biomed.sql') #nom de la db à ouvrir
        self.db.open()

        self.model = QtSql.QSqlQueryModel() #Modèle dans lequel la db sera chargée
        self.model.setQuery('SELECT poids, taille, temperature, frequence, time FROM mesures WHERE id in('+ str(mesures)[1:-1] +') ORDER BY time') #Requête pour récupérer les mesures avec un id ds mesures


        """Associe le modèle à une vue"""
        self.table = QtGui.QTableView() #associe les données à une vue
        self.table.setModel(self.model)

        """Champs présent dans le formulaire"""
        self.firstName = QtGui.QLineEdit() #Champs texte
        self.firstName.setMaxLength(25)

        self.lastName = QtGui.QLineEdit() #Champs texte
        self.lastName.setMaxLength(25)

        self.age = QtGui.QDateTimeEdit() #Champs date
        self.age.setDisplayFormat("dd MMM yyyy") #ex : 24 mai 1992
        self.age.setCalendarPopup(True)

        self.sexe = QtGui.QComboBox() #Liste déroulante
        self.sexe.addItem("Femme")
        self.sexe.addItem("Homme")

        """Layout du formulaire + label"""
        self.formulaire = QtGui.QFormLayout(parent)
        self.formulaire.addRow("Mesures", self.table)
        self.formulaire.addRow("Prenom", self.firstName)
        self.formulaire.addRow("Nom", self.lastName)
        self.formulaire.addRow("Age", self.age)
        self.formulaire.addRow("Sexe", self.sexe)
