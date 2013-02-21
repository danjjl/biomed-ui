#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtCore, QtGui, QtSql

class editUserVirtual(QtGui.QDialog):
    def __init__(self, parent, indexes, lastName, firstName, age, sexe):
        super(editUserVirtual, self).__init__(parent)

        self.parent = parent
        self.indexes = indexes

        """Champs présent dans le formulaire"""
        self.firstName = QtGui.QLineEdit(firstName) #Champs texte
        self.firstName.setMaxLength(25)

        self.lastName = QtGui.QLineEdit(lastName) #Champs texte
        self.lastName.setMaxLength(25)

        self.age = QtGui.QDateTimeEdit(QtCore.QDate(int(age[0:4]), int(age[5:7]), int(age[8:10]))) #Champs date
        self.age.setDisplayFormat("dd MMM yyyy") #ex : 24 mai 1992
        self.age.setCalendarPopup(True)

        self.sexe = QtGui.QComboBox() #Liste déroulante
        self.sexe.addItem("Femme")
        self.sexe.addItem("Homme")
        if sexe == "h":
            self.sexe.setCurrentIndex(1)

        """Boutons d'actions"""
        self.cancel = QtGui.QPushButton("Annuler") #Cancel
        self.submit = QtGui.QPushButton("Modifier") #Ajoute les mesures au nouvel utilisateur

        self.cancel.clicked.connect(self.returnNoUserMesures)
        self.submit.clicked.connect(self.modifyUser)

        """Layout des boutons"""
        self.buttons = QtGui.QHBoxLayout()
        self.buttons.addWidget(self.cancel)
        self.buttons.addWidget(self.submit)

        """Layout du formulaire + label"""
        self.formulaire = QtGui.QFormLayout()
        self.formulaire.addRow("Prenom", self.firstName)
        self.formulaire.addRow("Nom", self.lastName)
        self.formulaire.addRow("Age", self.age)
        self.formulaire.addRow("Sexe", self.sexe)
        self.formulaire.addRow(self.buttons) #Ajoute un Layout

        self.setLayout(self.formulaire)

    def returnNoUserMesures(self):
        self.close() #Retourne à la sélection des mesures

class editUser(editUserVirtual):
    def __init__(self, parent, indexes, firstName, lastName, age, sexe):
        super(editUser, self).__init__(parent, indexes, firstName, lastName, age, sexe)
        self.exec_()

    def modifyUser(self):
        query = QtSql.QSqlQuery()

        """Edite l'utilisateur"""
        for index in self.indexes:
            query.exec_("UPDATE utilisateurs SET nom = '"+ self.lastName.text() +"', prenom = '"+ self.firstName.text() +"', age = DATE('"+ self.age.date().toString("yyyy-MM-dd") +"'), sexe = '"+ self.sexe.currentText()[0].toLower() +"' WHERE id ="+ str(index) +"")

        """Cache la fenetre"""
        self.parent.update()
        self.close()
