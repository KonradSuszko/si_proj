# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import cv2
import math
import sys
import clasterWindow
import offer
import claster
import algorithm
import scrapping
import allegro_api
import clastersWindow
import threading

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Klasyfikacja obrazów")
        self.setupUi()

    def setupUi(self):
        self.setObjectName("Dialog")
        self.resize(225, 213)
        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setGeometry(QtCore.QRect(-430, 160, 621, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.checkBox = QtWidgets.QCheckBox(self)
        self.checkBox.setGeometry(QtCore.QRect(40, 50, 171, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.checkBox.setFont(font)
        self.checkBox.setCheckable(True)
        self.checkBox.setChecked(True)
        self.checkBox_2 = QtWidgets.QCheckBox(self)
        self.checkBox_2.setGeometry(QtCore.QRect(40, 80, 161, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.checkBox_2.setFont(font)
        self.checkBox_2.setCheckable(True)
        self.checkBox_2.setChecked(True)
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(40, 10, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.retranslateUi(self)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        QtCore.QMetaObject.connectSlotsByName(self)

        self.progressBar = QtWidgets.QProgressBar(self)
        self.progressBar.setGeometry(QtCore.QRect(60, 120, 118, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(True)
        self.progressBar.setInvertedAppearance(False)
        self.show()

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.checkBox.setText(_translate("Dialog", "Podobieństwo obrazów"))
        self.checkBox_2.setText(_translate("Dialog", "Podobieństwo tekstu"))
        self.label.setText(_translate("Dialog", "Kryteria klasteryzacji:"))

    def reject(self):
        self.close();

    @QtCore.pyqtSlot()
    def notify(self, val):
        self.progressBar.setProperty("value", val)

    def accept(self):
        offers = []
        self.progressBar.setProperty("value", 0)
        # texts = scrapping.download_and_get_text()
        texts = allegro_api.download_and_get_texts(self.progressBar, 100)
        words_vector = scrapping.create_words_vector(texts)
        images = {}

        for i in range(len(texts)):
            new_offer = offer.Offer("imgs/" + str(i + 1) + ".jpg", texts[i])
            new_offer.text_to_vector(words_vector)
            offers.append(new_offer)
            image = cv2.imread("imgs/" + str(i + 1) + ".jpg")
            images[str(i + 1) + ".jpg"] = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            self.progressBar.setProperty("value", 20+((i+1)/len(texts))*20)

        claster_array = []
        i = 0
        for e in offers:
            i += 1
            claster_array.append(claster.Claster([e]))
            self.progressBar.setProperty("value", 40 + (i/len(offers))*10)

        x = algorithm.algorithm(claster_array, self.checkBox.isChecked(), self.checkBox_2.isChecked(), self.progressBar, 10)
        self.windows = {}
        i = 0
        for a in x:
            self.windows[i] = clasterWindow.Ui_Dialog()
            self.windows[i].setupUi(a.list)
            #self.windows[i].show()
            i += 1
            self.progressBar.setProperty("value", 90 + (i/len(x))*10)
        self.clasterWindow = clastersWindow.Ui_Dialog()
        self.clasterWindow.setupUi(self.windows)
        self.clasterWindow.show()


def init():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()
    app.exec()
