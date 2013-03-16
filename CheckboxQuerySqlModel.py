#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtCore, QtSql

class CheckboxQuerySqlModel(QtSql.QSqlRelationalTableModel):
    def __init__(self, column):
        super(CheckboxQuerySqlModel, self).__init__()
        self.column = column
        self.checkboxes = list() #List de l'état des checkbox
        self.first = list() #Utilisé pour initialiser les checkbox

    #Rend la deuxième colonne éditable
    def flags(self, index):
        flags = QtSql.QSqlQueryModel.flags(self, index)
        if index.column() == self.column:
            flags |= QtCore.Qt.ItemIsUserCheckable
        return flags

    def data(self, index, role=QtCore.Qt.DisplayRole):
        row = index.row()
        #Si colonne checkbox
        if index.column() == self.column and role == QtCore.Qt.CheckStateRole:
            #Si pas encore initialisé
            if row not in self.first :
                index = self.createIndex(row, self.column)
                self.first.append(row)
                self.checkboxes.append(False)
                return QtCore.Qt.Unchecked
            #Si checked
            elif self.checkboxes[row]:
                return QtCore.Qt.Checked
            else:
                return QtCore.Qt.Unchecked
        else:
            return QtSql.QSqlQueryModel.data(self, index, role)

    def setData(self, index, value, role=QtCore.Qt.DisplayRole):
        row = index.row()
        if index.column() == self.column and role == QtCore.Qt.CheckStateRole:
            if value.toBool():
                self.checkboxes[row] = True
            else:
                self.checkboxes[row] = False
            #On a changé la case en index (2 index (haut gauche -> bas droite))
            self.dataChanged.emit(index, index)
            #Le changement a bien eu lieu
            return True
        else:
            #On a rien changé
            return False

    def listChecked(self):
        index = list() #List des id cochés
        for i in self.first:
            if self.checkboxes[i]:
                index.append(self.data(self.index(i, 0)).toInt()[0])
        return index

    def changeCheck(self, checkState):
        for i in self.first:
            self.setData(self.index(i, self.column), QtCore.QVariant(checkState), QtCore.Qt.CheckStateRole)
