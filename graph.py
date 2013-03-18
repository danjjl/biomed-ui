#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtCore, QtGui, QtSql

import datetime

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg

"""Graph"""
class graph(QtGui.QWidget):
    hideCall = QtCore.pyqtSignal() #Signal utilisé sur retour utilisateurs

    def __init__(self):
        super(graph, self).__init__()

        self.mesures = QtSql.QSqlQuery() #Requete : des mesures

        self.fig = Figure() #données à plotter
        self.canvas = FigureCanvasQTAgg(self.fig) #Widget d'un graph
        self.canvas.setParent(self)

        self.toolbar = NavigationToolbar2QTAgg(self.canvas, self) #Widget d'une barre d'outil

        self.button = QtGui.QPushButton("Retour Utilisateurs")
        self.button.clicked.connect(self._hideCaller)

        self.title = QtGui.QLabel("<b>Graph<b>")
        self.title.setMaximumHeight(16)
        self.title.setScaledContents(True)
        self.title.setAlignment(QtCore.Qt.AlignHCenter)

        """Barre de menu complète contenant outils graph et retour utilisateur"""
        self.sublayout = QtGui.QHBoxLayout()
        self.sublayout.addWidget(self.button)
        self.sublayout.addWidget(self.toolbar)
        """Layout contenant le graph et la barre de menu"""
        self.layout = QtGui.QVBoxLayout(self)
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.canvas)
        self.layout.addLayout(self.sublayout)

        self.hide()

    def _hideCaller(self):
        self.hideCall.emit()

    def redraw(self, index, mesure, name):
        self.title.setText("<b>" + name + " - " + mesure + "</>")

        """Collecte données"""
        if mesure != "bmi":
            self.mesures.exec_("SELECT "+mesure+", time FROM mesures WHERE utilisateur="+str(index)+" ORDER BY time")
            self.x = list()
            self.y = list()
            while self.mesures.next():
                self.y.append(self.mesures.value(0).toDouble()[0])
                self.x.append(self.mesures.value(1).toDateTime().toPyDateTime()) #Qvariant -> QDateTime -> dateTime
        else: #->BMI
            self.mesures.exec_("SELECT poids, taille, time FROM mesures WHERE utilisateur="+str(index)+" ORDER BY time")
            self.x = list()
            self.y = list()
            while self.mesures.next():
                self.y.append(self.mesures.value(0).toDouble()[0]**2/self.mesures.value(1).toDouble()[0])
                self.x.append(self.mesures.value(2).toDateTime().toPyDateTime())
        """Trace données"""
        self.fig.clf()
        self.plots = self.fig.add_subplot(111)
        self.plots.plot(self.x, self.y, 'o-')
        self.fig.autofmt_xdate() #TODO reformater l'axe des x pour les divisions soient pertinantes

        self.canvas.draw()
        self.show()
