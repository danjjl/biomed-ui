#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui, QtSql

from editUser import editUserVirtual

class newUser(editUserVirtual):
    def __init__(self, parent, mesures):
        super(newUser, self).__init__(parent, mesures, None, None, "1992-05-24", "f")

        """chargement des données dans le modèle"""
        self.model = QtSql.QSqlQueryModel() #Modèle dans lequel la db sera chargée
        self.model.setQuery('SELECT poids, taille, temperature, frequence, time FROM mesures WHERE id in('+ str(mesures)[1:-1] +') ORDER BY time') #Requête pour récupérer les mesures avec un id ds mesures

        """Associe le modèle à une vue"""
        self.table = QtGui.QTableView() #associe les données à une vue
        self.table.setModel(self.model)

        """Modifie affichage"""
        self.submit.setText("Ajouter")
        self.formulaire.insertRow(0, "Mesures", self.table)
        self.formulaire.update()
        self.exec_()

    def modifyUser(self):
        query = QtSql.QSqlQuery()

        """Ajouter le nouvel utilisateur"""
        query.exec_("INSERT INTO utilisateurs (nom, prenom, age, sexe) values('"+ self.lastName.text() +"', '"+ self.firstName.text() +"', DATE('"+ self.age.date().toString("yyyy-MM-dd") +"'), '"+ self.sexe.currentText()[0].toLower() +"')") #Crée un nouvel utilisateur

        """Trouver le dernier id"""
        query.exec_("SELECT id FROM utilisateurs") #Ya pe plus simple mais ça fct bien
        query.last()
        lastId = query.value(0).toInt()[0]

        """Ajoute l'utilisateur aux mesures'"""
        for index in self.indexes:
            query.exec_("UPDATE mesures SET utilisateur ="+ str(lastId) +" WHERE id ="+ str(index) +"")

        """Cache la fenetre"""
        self.parent.update()
        self.close()
