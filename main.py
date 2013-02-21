#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui, QtSql

from noUserMesures import noUserMesures
from editUsers import editUsers
from editMesures import editMesures


if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)

    """Connection à la db; chargement des données dans le modèle"""
    db = QtSql.QSqlDatabase.addDatabase('QSQLITE') #Défini le type de db (ici SqlLite)
    db.setDatabaseName('biomed.sql') #nom de la db à ouvrir
    db.open()

    main = QtGui.QTabWidget()
    main.setWindowTitle("Test")
    main.setGeometry(200,60, 500, 400)

    noUsers = noUserMesures()
    editUsers = editUsers()
    editMesures = editMesures()
    main.addTab(noUsers, "Mesures sans utilisateur")
    main.addTab(editUsers, "Editer les utilisateurs")
    main.addTab(editMesures, "Editer les mesures")
    main.show()

    sys.exit(app.exec_())
