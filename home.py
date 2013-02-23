#!/usr/bin/python
# -*- coding: utf-8 -*-
#BMI taille²/poids
import sys
from PyQt4 import QtCore, QtGui, QtSql

class home(QtGui.QWidget):
    def __init__(self):
        super(home, self).__init__()

        self.layout = QtGui.QGridLayout # Chaque fiche d'utilisateur sera rangé ds un grid layout en 2 collones

        utilisateurs = QtSql.QSqlQuery() #Requete : utilisateur
        mesures = QtSql.QSqlQuery() #Requete : mesures
        utilisateurs.exec_("SELECT id, nom, prenom FROM utilisateurs")
        while utilisateurs.next():
            curId = utilisateurs.value(0).toInt()[0] #Id utilisateur
            lastName = utilisateurs.value(1).toString() #Nom
            firstName = utilisateurs.value(2).toString() #Prénom
            mesures.exec_("SELECT poids, taille, temperature FROM mesures WHERE utilisateur="+str(curId)+" ORDER BY time LIMIT 1")
            if mesures.first():
                poids = mesures.value(0).toDouble()[0]
                taille = mesures.value(1).toDouble()[0]
                temperature = mesures.value(2).toDouble()[0]
                print str(curId) + ", " +firstName + " " + lastName + ": (" + str(poids) + ", " + str(taille) + ", " + str(temperature) + ")" #Line temporaire pour montrer que tout fct bien :)

