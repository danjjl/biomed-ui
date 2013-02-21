#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui, QtSql

from home import home
from sync import sync
from noUserMesures import noUserMesures
from editUsers import editUsers
from editMesures import editMesures

def callUpdate(index):
    main.widget(index).update()

if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)

    """Connection à la db; chargement des données dans le modèle"""
    db = QtSql.QSqlDatabase.addDatabase('QSQLITE') #Défini le type de db (ici SqlLite)
    db.setDatabaseName('biomed.sql') #nom de la db à ouvrir
    db.open()

    "Fenetre principale"
    main = QtGui.QTabWidget()
    main.setWindowTitle("Test")
    main.setGeometry(200,60, 500, 400)

    """2 Vues indépendantes"""
    homeScreen = home()
    syncScreen = sync()

    """Ecrans d'édition"""
    noUsers = noUserMesures()
    editUsers = editUsers()
    editMesures = editMesures()

    """Tab contenant les écrans d'édition"""
    editTabs = QtGui.QTabWidget()

    editTabs.currentChanged.connect(callUpdate)#Signal chg tab connecté aux != fct update

    """Association écran-tab"""
    editTabs.addTab(noUsers, "Mesures sans utilisateur")
    editTabs.addTab(editUsers, "Editer les utilisateurs")
    editTabs.addTab(editMesures, "Editer les mesures")

    main.addTab(homeScreen, "Accueil")
    main.addTab(syncScreen, "Synchroniser")
    main.addTab(editTabs, "Editer")

    main.show()

    sys.exit(app.exec_())
