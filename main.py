#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui

from noUserMesures import noUserMesures


if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)

    main = QtGui.QWidget()
    main.setWindowTitle("Test")
    main.setGeometry(200,60, 500, 400)

    layout = QtGui.QVBoxLayout()

    noUsers = noUserMesures(layout)

    layout.addWidget(noUsers)
    main.setLayout(layout)
    main.show()

    sys.exit(app.exec_())
