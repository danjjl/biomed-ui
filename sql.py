#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtCore, QtGui, QtSql

class noUserMesures(QtGui.QWidget):
    def __init__(self, parent):
        super(noUserMesures, self).__init__(parent)

        """Connection à la db; chargement des données dans le modèle"""
        self.db = QtSql.QSqlDatabase.addDatabase('QSQLITE') #Défini le type de db (ici SqlLite)
        self.db.setDatabaseName('biomed.sql') #nom de la db à ouvrir
        self.db.open()

        self.model = QtSql.QSqlQueryModel() #Modèle dans lequel la db sera chargée
        self.model.setQuery('select * from mesures WHERE utilisateur=0 ORDER BY time') #Requête pour récupérer les mesures n'ayant d'utilisateurs

        self.model.insertColumn(2) #Colonne dans laquelle on mettra les checkbox
        self.model.setHeaderData(2, QtCore.Qt.Horizontal, "ajouter") #titre de la colonne

        """Associe le modèle à une vue"""
        self.table = QtGui.QTableView(parent) #associe les données à une vue
        self.table.setModel(self.model)

        self.table.hideColumn(0) #cache les colonnes id
        self.table.hideColumn(1)

        """Liste des checkbox(PAS ENCORE FONCTIONNEL)"""
        self.checkboxes = list()#liste ou l'on stoque les index et les checkbox
        for i in range(0, self.model.rowCount()):
            self.checkboxes.append((self.model.data(self.model.index(i, 0)).toInt()[0], QtGui.QCheckBox())) #(index, QCheckbox)
            #TROUVER LIGNE AJOUTER WIDGET DANS MODEL OU VUE

if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)

    main = QtGui.QWidget()
    main.setWindowTitle("Test")
    user = noUserMesures(main)
    main.show()

    sys.exit(app.exec_())
