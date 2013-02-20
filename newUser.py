#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtCore, QtGui, QtSql

class newUser(QtGui.QWidget):
    def __init__(self, parent, mesures):
        super(newUser, self).__init__(parent)

        self.mesures = mesures

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

        """Boutons d'actions"""
        self.cancel = QtGui.QPushButton("Annuler") #Cancel (brings back to user selection could be performed with menu)
        self.submit = QtGui.QPushButton("Ajouter") #Ajoute les mesures au nouvel utilisateur

        self.cancel.clicked.connect(self.returnNoUserMesures)
        self.submit.clicked.connect(self.addUser)

        """Layout des boutons"""
        self.buttons = QtGui.QHBoxLayout()
        self.buttons.addWidget(self.cancel)
        self.buttons.addWidget(self.submit)

        """Layout du formulaire + label"""
        self.formulaire = QtGui.QFormLayout()
        self.formulaire.addRow("Mesures", self.table)
        self.formulaire.addRow("Prenom", self.firstName)
        self.formulaire.addRow("Nom", self.lastName)
        self.formulaire.addRow("Age", self.age)
        self.formulaire.addRow("Sexe", self.sexe)
        self.formulaire.addRow(self.buttons) #Ajoute un Layout

        self.setLayout(self.formulaire)
        self.show()

    def returnNoUserMesures(self):
        print "Nothing yet"

    def addUser(self):
        query = QtSql.QSqlQuery()

        """Ajouter le nouvel utilisateur"""
        query.exec_("INSERT INTO utilisateurs (nom, prenom, age, sexe) values('"+ self.lastName.text() +"', '"+ self.firstName.text() +"', DATE('"+ self.age.date().toString("yyyy-MM-dd") +"'), '"+ self.sexe.currentText()[0].toLower() +"')") #Crée un nouvel utilisateur

        """Trouver le dernier id"""
        query.exec_("SELECT id FROM utilisateurs") #Ya pe plus simple mais ça fct bien
        query.last()
        lastId = query.value(0).toInt()[0]

        """Ajoute l'utilisateur aux mesures'"""
        for index in self.mesures:
            query.exec_("UPDATE mesures SET utilisateur ="+ str(lastId) +" WHERE id ="+ str(index) +"")

        """Cache la fenetre"""
        self.hide()
