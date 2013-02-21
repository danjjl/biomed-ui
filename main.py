#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui, QtSql

from noUserMesures import noUserMesures


if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)

    """Connection à la db; chargement des données dans le modèle"""
    db = QtSql.QSqlDatabase.addDatabase('QSQLITE') #Défini le type de db (ici SqlLite)
    db.setDatabaseName('biomed.sql') #nom de la db à ouvrir
    db.open()

    main = QtGui.QWidget()
    main.setWindowTitle("Test")
    main.setGeometry(200,60, 500, 400)

    layout = QtGui.QVBoxLayout()

    noUsers = noUserMesures(layout)

    layout.addWidget(noUsers)
    main.setLayout(layout)
    main.show()

    sys.exit(app.exec_())
