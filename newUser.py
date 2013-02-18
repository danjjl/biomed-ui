#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtCore, QtGui, QtSql

class newUser(QtGui.QWidget):
    def __init__(self, parent, mesures):
        super(newUser, self).__init__(parent)

        """Champs présent dans le formulaire"""
        firstName = QtGui.QLineEdit() #Champs texte
        firstName.setMaxLength(25)

        lastName = QtGui.QLineEdit() #Champs texte
        lastName.setMaxLength(25)

        age = QtGui.QDateTimeEdit() #Champs date
        age.setDisplayFormat("dd MMM yyyy") #ex : 24 mai 1992
        age.setCalendarPopup(True)

        sexe = QtGui.QComboBox() #Liste déroulante
        sexe.addItem("Femme")
        sexe.addItem("Homme")

        """Layout du formulaire + label"""
        formulaire = QtGui.QFormLayout(parent)
        formulaire.addRow("Prenom", firstName)
        formulaire.addRow("Nom", lastName)
        formulaire.addRow("Age", age)
        formulaire.addRow("Sexe", sexe)
