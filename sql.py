#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtCore, QtGui, QtSql

if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)

    db = QtSql.QSqlDatabase.addDatabase('QSQLITE') #Défini le type de db (ici SqlLite)
    db.setDatabaseName('biomed.sql') #nom de la db à ouvrir
    db.open()

    model = QtSql.QSqlQueryModel() #Modèle dans lequel la db sera chargée
    model.setQuery('select * from mesures WHERE utilisateur=0 ORDER BY time') #Requête pour récupérer les mesures n'ayant d'utilisateurs

    model.insertColumn(2) #Colonne dans lesquels on mettra les checkbox
    model.setHeaderData(2, QtCore.Qt.Horizontal, "ajouter") #titre de la collone

    checkboxes = list()#liste ou l'on stoque les index et les checkbox
    for i in range(0, model.rowCount()):
        checkboxes.append((model.data(model.index(i, 0)).toInt()[0], QtGui.QCheckBox())) #(index, QCheckbox)
        #TROUVER LIGNE AJOUTER WIDGET DANS MODEL OU VUE

    view = QtGui.QTableView() #associe les données à une vue
    view.setModel(model)
    view.hideColumn(0); #cache les colonnes id
    view.hideColumn(1);

    view.setWindowTitle("Test")

    view.show()

    sys.exit(app.exec_())
