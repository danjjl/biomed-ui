#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtCore, QtGui, QtSql

if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)

    db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
    db.setDatabaseName('biomed.sql')
    db.open()

    model = QtSql.QSqlQueryModel()
    model.setQuery('select * from mesures WHERE utilisateur=0 ORDER BY time')
    model.insertColumn(2)

    view = QtGui.QTableView()
    view.setModel(model)
    view.hideColumn(0);
    view.hideColumn(1);

    view.setWindowTitle("Test")

    view.show()

    sys.exit(app.exec_())
