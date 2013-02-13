#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtSql

db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
db.setDatabaseName('biomed.sql')
if db.open():
    query = QtSql.QSqlQuery()
    query.exec_("CREATE TABLE mesures (id INTEGER PRIMARY KEY, utilisateur INTEGER, poids DOUBLE, taille DOUBLE, temperature DOUBLE, frequence DOUBLE, time DATE)")
    query.exec_("CREATE TABLE utilisateurs (id INTEGER PRIMARY KEY, nom VARCHAR(25), prenom VARCHAR(25), age DATE, sexe VARCHAR(1))")

    query.exec_("INSERT INTO mesures (utilisateur, poids, taille, temperature, frequence, time) values(1, 60.5, 173.6, 36.6, 1000.1, DATETIME('NOW'))")
    query.exec_("INSERT INTO mesures (utilisateur, poids, taille, temperature, frequence, time) values(0, 61.5, 173.6, 36.6, 1000.1, DATETIME('NOW'))")
    query.exec_("INSERT INTO mesures (utilisateur, poids, taille, temperature, frequence, time) values(0, 62.5, 173.6, 36.6, 1000.1, DATETIME('NOW'))")
    query.exec_("INSERT INTO mesures (utilisateur, poids, taille, temperature, frequence, time) values(0, 63.5, 173.6, 36.6, 1000.1, DATETIME('NOW'))")

    query.exec_("INSERT INTO utilisateurs (nom, prenom, age, sexe) values('Dan', 'Jonathan', DATE('1992-05-24'), 'h')")
    query.exec_("INSERT INTO utilisateurs (nom, prenom, age, sexe) values('Dan', 'Natania', DATE('1995-02-14'), 'f')")
