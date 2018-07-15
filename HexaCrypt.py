# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from math import *
import random, struct, os, datetime
def bitstr(n, width=None):
   """return the binary representation of n as a string and
      optionally zero-fill (pad) it to a given length
   """
   result = list()
   while n:
      result.append(str(n%2))
      n = int(n/2)
   if (width is not None) and len(result) < width:
      result.extend(['0'] * (width - len(result)))
   result.reverse()
   return ''.join(result)

def mask(n):
   """Return a bitmask of length n (suitable for masking against an
      int to coerce the size to a given length)
   """
   if n >= 0:
       return 2**n - 1
   else:
       return 0

def testme():
    print("LOL")

def rol(n, rotations=1, width=8):
    """Return a given number of bitwise left rotations of an integer n,
       for a given bit field width.
    """
    rotations %= width
    if rotations < 1:
        return n
    n &= mask(width) ## Should it be an error to truncate here?
    return ((n << rotations) & mask(width)) | (n >> (width - rotations))

def ror(n, rotations=1, width=8):
    """Return a given number of bitwise right rotations of an integer n,
       for a given bit field width.
    """
    rotations %= width
    if rotations < 1:
        return n
    n &= mask(width)
    return (n >> rotations) | ((n << (width - rotations)) & mask(width))



def print_matrix(a):
    s = ""
    for i in range(8):
        s=""
        for j in range(8):
            s = s + str(hex(a[i][j])) + "\t"
        print(s + "\n")

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(QtGui.QMainWindow):


    def createCipherTable(self):
        x = 0
        self.__cphtbl__ = []
        y = 255
        z = 0
        while z in range(8):
            self.__cphtbl__.append([random.randint(69, y),random.randint(x, y),random.randint(x, y),random.randint(x, y),random.randint(x, y),random.randint(x, y),random.randint(x, y),random.randint(x, y)])
            z+=1
        print("Cipher Table Finished")
        self.createKey(self.__cphtbl__)

    def createKey(self, __cphtbl__):
        self.__key__ = 0
        for i in range(8):
            for j in range(8):
                self.__key__ += __cphtbl__[i][j]
                self.__key__ = self.__key__ << 8
        self.__key__ = self.__key__ >> 8
        self.keyEncryptionField.clear()
        self.keyEncryptionField.setText(str(hex(self.__key__)))
        print("Key Generated: \n" + str(hex(self.__key__)))


    def singleKeyBrowse(self):
        self.keyFilePath = QtGui.QFileDialog.getOpenFileName(self, 'Browse Item...')
        if self.keyFilePath == "":
            print("No Key file was selected")
            return -1
        print('Key from: ',self.keyFilePath, '\n')
        self.createDecryptionTable()




    def createDecryptionTable(self):
        if self.keyFilePath == "":
            return print("No Key file selected!")
        else:
            keyFile = open(self.keyFilePath, "rb")
            self.__key__ = 0
            for z in range(8):
                self.__cphtbl__.append([0,0,0,0,0,0,0,0])
            for i in range(8):
                for j in range(8):
                    byte = keyFile.read(1)
                    self.__cphtbl__[i][j]= int.from_bytes(byte, byteorder = 'big')
                    self.__key__ += (self.__cphtbl__[i][j])
                    self.__key__ <<= 8
            self.__key__ >>= 8
            self.keyDecryptionField.setText(str(hex(self.__key__)))

    def startDecryptionMode1(self):
        fileSize = self.file_size(str(self.filePath))
        completed = 0

        #Open files: file to encrypt,
        cryptedFile = open(self.filePath, "rb")
        decryptedFile = open(self.getFilePath(self.filePath) + "/" + self.filename(self.filePath) + ".decrypted", "wb")
        byte = cryptedFile.read(1)
        while 1:
            for i in range(8):
                for j in range(8):
                    temp = rol(self.__cphtbl__[i][j], i%(j+1))
                    byte = (int.from_bytes(byte, byteorder = 'big') ^ temp).to_bytes(1, byteorder = 'big')
                    decryptedFile.write(byte)
                    completed+=1
                    self.updateProgressBar(completed/fileSize, "decryption")
                    byte = cryptedFile.read(1)
                    if len(byte) == 0:
                        cryptedFile.close()
                        decryptedFile.close()
                        return print("Decryption Complete")

    def startDecryptionMode2(self):
        fileSize = self.file_size(str(self.filePath))
        completed = 0

        #Open files: file to encrypt,
        cryptedFile = open(self.filePath, "rb")
        decryptedFile = open(self.getFilePath(self.filePath) + "/" + self.filename(self.filePath) + ".decrypted", "wb")
        byte = cryptedFile.read(1)
        while 1:
            for i in range(8):
                for j in range(8):
                    if i*j%2 ==0:
                        temp = ror(self.__cphtbl__[i][j], i%(j+1))
                    else:
                        temp = rol(self.__cphtbl__[i][j], i%(j+1))
                    byte = (int.from_bytes(byte, byteorder = 'big') ^ temp).to_bytes(1, byteorder = 'big')
                    decryptedFile.write(byte)
                    completed+=1
                    self.updateProgressBar(completed/fileSize, "decryption")
                    byte = cryptedFile.read(1)
                    if len(byte) == 0:
                        cryptedFile.close()
                        decryptedFile.close()
                        return print("Decryption Complete")


    def file_size(self, file_path):
        if os.path.isfile(file_path):
            file_info = os.stat(file_path)
            return file_info.st_size

    def updateProgressBar(self, progress, mode):
        if mode == "encryption":
            self.encryptionProgressBar.setValue(progress*100)
        elif mode == "decryption":
            self.decryptionProgressBar.setValue(progress*100)



    def filename(self, path):
        import os.path
        b = os.path.split(path)[1]  # path, *filename*
        f = os.path.splitext(b)[0]  # *file*, ext
        return f

    def getFileName(self, path):
        import os.path
        (filepath, filename) = os.path.split(path)
        return str(filename)

    def getFilePath(self, path):
        import os.path
        (filepath, filename) = os.path.split(path)
        return str(filepath)


    def startEncryptionMode1(self):
        fileSize = self.file_size(str(self.filePath))
        completed = 0

        #Open files: file to encrypt,
        noncryptedFile = open(self.filePath, "rb")
        cryptedFile = open(self.getFilePath(self.filePath) + "/" + self.filename(self.filePath) + ".crypted", "wb")
        keyFile = open(self.getFilePath(self.filePath) + "/" + self.filename(self.filePath) + ".key", "wb")
        byte = noncryptedFile.read(1)
        while 1:
            for i in range(8):
                for j in range(8):
                    temp = rol(self.__cphtbl__[i][j], i%(j+1))
                    byte = (int.from_bytes(byte, byteorder = 'big') ^ temp).to_bytes(1, byteorder = 'big')
                    cryptedFile.write(byte)
                    completed+=1
                    self.updateProgressBar(completed/fileSize, "encryption")
                    byte = noncryptedFile.read(1)
                    if len(byte) == 0:
                        # When Encryption is over, write binnary file with Key
                        byteKey = self.__key__.to_bytes(64, byteorder = 'big')
                        keyFile.write(byteKey)
                        #delete old file ?
                        cryptedFile.close()
                        noncryptedFile.close()
                        keyFile.close()
                        if self.deleteItemCheckBox.isChecked() == 1:
                            self.deleteOldFile()
                        return print("Encryption Complete")



    def startEncryptionMode2(self):
        fileSize = self.file_size(str(self.filePath))
        completed = 0

        #Open files: file to encrypt,
        noncryptedFile = open(self.filePath, "rb")
        cryptedFile = open(self.getFilePath(self.filePath) + "/" + self.filename(self.filePath) + ".crypted", "wb")
        keyFile = open(self.getFilePath(self.filePath) + "/" + self.filename(self.filePath) + ".key", "wb")
        byte = noncryptedFile.read(1)
        while 1:
            for i in range(8):
                for j in range(8):
                    if i*j%2 ==0:
                        temp = ror(self.__cphtbl__[i][j], i%(j+1))
                    else:
                        temp = rol(self.__cphtbl__[i][j], i%(j+1))
                    byte = (int.from_bytes(byte, byteorder = 'big') ^ temp).to_bytes(1, byteorder = 'big')
                    cryptedFile.write(byte)
                    completed+=1
                    self.updateProgressBar(completed/fileSize, "encryption")
                    byte = noncryptedFile.read(1)
                    if len(byte) == 0:
                        # When Encryption is over, write binnary file with Key
                        byteKey = self.__key__.to_bytes(64, byteorder = 'big')
                        keyFile.write(byteKey)
                        #delete old file ?
                        cryptedFile.close()
                        noncryptedFile.close()
                        keyFile.close()
                        if self.deleteItemCheckBox.isChecked() == 1:
                            self.deleteOldFile()
                        return print("Encryption Complete")


    def singleBrowse(self):
        self.filePath = QtGui.QFileDialog.getOpenFileName(self, 'Browse Item...')
        if self.filePath == "":
            print("No file was selected")
            return -1
        self.filePathEncryptionField.setText(self.filePath)
        self.filePathDecryptionField.setText(self.filePath)
        print('filePath',self.filePath, '\n')



    def encryptionMode(self):
        if self.encryptionComboBox.currentIndex() == 0:
            print("Hexa Encryption Mode: 1\nStarting...")
            self.startEncryptionMode1()
        if self.encryptionComboBox.currentIndex() == 1:
            print("Hexa Encryption Mode: 2\nStarting...")
            self.startEncryptionMode2()

    def decryptionMode(self):
        if self.encryptionComboBox_2.currentIndex() == 0:
            print("Hexa Decryption Mode: 1\nStarting...")
            self.startDecryptionMode1()
        if self.encryptionComboBox_2.currentIndex() == 1:
            print("Hexa Decryption Mode: 2\nStarting...")
            self.startDecryptionMode2()

    def deleteOldFile(self):

        if os.path.isfile(self.filePath):
            os.remove(self.filePath)
            print("%s removed" % self.filePath)
        else:    ## Show an error ##
            print("Error: %s file not found" % self.filePath)




    def setupUi(self, MainWindow):

        MainWindow.setObjectName(_fromUtf8("Hexa Crypt"))
        MainWindow.resize(800, 304)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("images/icon.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        key_icon = QtGui.QIcon()
        key_icon.addPixmap(QtGui.QPixmap(_fromUtf8("images/key_icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setStyleSheet(_fromUtf8("background-image: url(\"images/background.png\")"))
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.uberGridLayout = QtGui.QGridLayout(self.centralwidget)
        self.uberGridLayout.setObjectName(_fromUtf8("uberGridLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.titleLabel = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(28)
        font.setBold(True)
        font.setWeight(75)
        self.titleLabel.setFont(font)
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.titleLabel.setObjectName(_fromUtf8("titleLabel"))
        self.gridLayout.addWidget(self.titleLabel, 0, 0, 1, 1)
        self.mainTabs = QtGui.QTabWidget(self.centralwidget)
        self.mainTabs.setAutoFillBackground(False)
        self.mainTabs.setStyleSheet(_fromUtf8("background-color: none"))
        self.mainTabs.setIconSize(QtCore.QSize(24, 24))
        self.mainTabs.setObjectName(_fromUtf8("mainTabs"))
        self.encryptionTab = QtGui.QWidget()
        self.encryptionTab.setStyleSheet(_fromUtf8("background-color: none"))
        self.encryptionTab.setObjectName(_fromUtf8("encryptionTab"))
        self.gridLayout_4 = QtGui.QGridLayout(self.encryptionTab)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.encryptionTabMainGridLayout = QtGui.QGridLayout()
        self.encryptionTabMainGridLayout.setObjectName(_fromUtf8("encryptionTabMainGridLayout"))
        self.browseEncryptionButton = QtGui.QPushButton(self.encryptionTab)
        self.browseEncryptionButton.setObjectName(_fromUtf8("browseEncryptionButton"))
        self.encryptionTabMainGridLayout.addWidget(self.browseEncryptionButton, 0, 1, 1, 1)
        self.generateButton = QtGui.QPushButton(self.encryptionTab)
        self.generateButton.setObjectName(_fromUtf8("generateButton"))
        self.generateButton.setIcon(key_icon)
        self.encryptionTabMainGridLayout.addWidget(self.generateButton, 1, 1, 1, 1)
        self.encryptionProgressBar = QtGui.QProgressBar(self.encryptionTab)
        self.encryptionProgressBar.setProperty("value", 0)
        self.encryptionProgressBar.setObjectName(_fromUtf8("encryptionProgressBar"))
        self.encryptionTabMainGridLayout.addWidget(self.encryptionProgressBar, 4, 0, 1, 1)
        self.filePathEncryptionField = QtGui.QLineEdit(self.encryptionTab)
        self.filePathEncryptionField.setObjectName(_fromUtf8("filePathEncryptionField"))
        self.encryptionTabMainGridLayout.addWidget(self.filePathEncryptionField, 0, 0, 1, 1)
        self.keyEncryptionField = QtGui.QLineEdit(self.encryptionTab)
        self.keyEncryptionField.setObjectName(_fromUtf8("keyEncryptionField"))
        self.encryptionTabMainGridLayout.addWidget(self.keyEncryptionField, 1, 0, 1, 1)
        self.encryptionTabFormatGridLayout = QtGui.QGridLayout()
        self.encryptionTabFormatGridLayout.setObjectName(_fromUtf8("encryptionTabFormatGridLayout"))
        self.encryptionComboBox = QtGui.QComboBox(self.encryptionTab)
        self.encryptionComboBox.setObjectName(_fromUtf8("encryptionComboBox"))
        self.encryptionComboBox.addItem(_fromUtf8(""))
        self.encryptionComboBox.addItem(_fromUtf8(""))
        self.encryptionTabFormatGridLayout.addWidget(self.encryptionComboBox, 1, 0, 1, 1)
        self.formatLabel = QtGui.QLabel(self.encryptionTab)
        self.formatLabel.setObjectName(_fromUtf8("formatLabel"))
        self.encryptionTabFormatGridLayout.addWidget(self.formatLabel, 0, 0, 1, 1)
        self.encryptionTabMainGridLayout.addLayout(self.encryptionTabFormatGridLayout, 2, 0, 1, 1)
        self.startEncryptionHorizontalLayout = QtGui.QHBoxLayout()
        self.startEncryptionHorizontalLayout.setObjectName(_fromUtf8("startEncryptionHorizontalLayout"))
        self.startEncryptionButton = QtGui.QPushButton(self.encryptionTab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.startEncryptionButton.sizePolicy().hasHeightForWidth())
        self.startEncryptionButton.setSizePolicy(sizePolicy)
        self.startEncryptionButton.setObjectName(_fromUtf8("startEncryptionButton"))
        self.startEncryptionHorizontalLayout.addWidget(self.startEncryptionButton)
        self.deleteItemCheckBox = QtGui.QCheckBox(self.encryptionTab)
        self.deleteItemCheckBox.setObjectName(_fromUtf8("deleteItemCheckBox"))
        self.startEncryptionHorizontalLayout.addWidget(self.deleteItemCheckBox)
        self.encryptionTabMainGridLayout.addLayout(self.startEncryptionHorizontalLayout, 3, 0, 1, 1)
        self.gridLayout_4.addLayout(self.encryptionTabMainGridLayout, 1, 0, 1, 1)
        self.mainTabs.addTab(self.encryptionTab, _fromUtf8(""))
        self.decryptionTab = QtGui.QWidget()
        self.decryptionTab.setStyleSheet(_fromUtf8("background-color: none"))
        # self.gridLayout.setStyleSheet(_fromUtf8("background-color: none"))
        # self.encryptionTabMainGridLayout.setStyleSheet(_fromUtf8("background-color: none"))
        # self.encryptionTabFormatGridLayout.setStyleSheet(_fromUtf8("background-color: none"))
        self.decryptionTab.setObjectName(_fromUtf8("decryptionTab"))
        self.gridLayout_6 = QtGui.QGridLayout(self.decryptionTab)
        self.gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
        self.decryptionTabMainGridLayout = QtGui.QGridLayout()
        self.decryptionTabMainGridLayout.setObjectName(_fromUtf8("decryptionTabMainGridLayout"))
        self.browseDecryptionButton = QtGui.QPushButton(self.decryptionTab)
        self.browseDecryptionButton.setObjectName(_fromUtf8("browseDecryptionButton"))
        self.decryptionTabMainGridLayout.addWidget(self.browseDecryptionButton, 0, 1, 1, 1)
        self.filePathDecryptionField = QtGui.QLineEdit(self.decryptionTab)
        self.filePathDecryptionField.setObjectName(_fromUtf8("filePathDecryptionField"))
        self.decryptionTabMainGridLayout.addWidget(self.filePathDecryptionField, 0, 0, 1, 1)
        self.startDecryptionButton = QtGui.QPushButton(self.decryptionTab)
        self.startDecryptionButton.setObjectName(_fromUtf8("startDecryptionButton"))
        self.decryptionTabMainGridLayout.addWidget(self.startDecryptionButton, 3, 0, 1, 1)
        self.keyDecryptionField = QtGui.QLineEdit(self.decryptionTab)
        self.keyDecryptionField.setObjectName(_fromUtf8("keyDecryptionField"))
        self.decryptionTabMainGridLayout.addWidget(self.keyDecryptionField, 1, 0, 1, 1)
        self.decryptionProgressBar = QtGui.QProgressBar(self.decryptionTab)
        self.decryptionProgressBar.setProperty("value", 0)
        self.decryptionProgressBar.setObjectName(_fromUtf8("decryptionProgressBar"))
        self.decryptionTabMainGridLayout.addWidget(self.decryptionProgressBar, 4, 0, 1, 1)
        self.decryptionFormatVerticalLayout = QtGui.QVBoxLayout()
        self.decryptionFormatVerticalLayout.setObjectName(_fromUtf8("decryptionFormatVerticalLayout"))
        self.formatLabel_2 = QtGui.QLabel(self.decryptionTab)
        self.formatLabel_2.setObjectName(_fromUtf8("formatLabel_2"))
        self.decryptionFormatVerticalLayout.addWidget(self.formatLabel_2)
        self.encryptionComboBox_2 = QtGui.QComboBox(self.decryptionTab)
        self.encryptionComboBox_2.setObjectName(_fromUtf8("encryptionComboBox_2"))
        self.encryptionComboBox_2.addItem(_fromUtf8(""))
        self.encryptionComboBox_2.addItem(_fromUtf8(""))
        self.decryptionFormatVerticalLayout.addWidget(self.encryptionComboBox_2)
        self.decryptionTabMainGridLayout.addLayout(self.decryptionFormatVerticalLayout, 2, 0, 1, 1)
        self.browseKeyButton = QtGui.QPushButton(self.decryptionTab)
        self.browseKeyButton.setObjectName(_fromUtf8("browseKeyButton"))
        self.browseKeyButton.setIcon(key_icon)
        # self.insertKeyLabel = QtGui.QLabel(self.decryptionTab)
        # self.insertKeyLabel.setObjectName(_fromUtf8("insertKeyLabel"))
        # self.decryptionTabMainGridLayout.addWidget(self.insertKeyLabel, 1, 1, 1, 1)
        self.decryptionTabMainGridLayout.addWidget(self.browseKeyButton, 1, 1, 1, 1)
        self.gridLayout_6.addLayout(self.decryptionTabMainGridLayout, 1, 0, 1, 1)
        self.mainTabs.addTab(self.decryptionTab, _fromUtf8(""))
        self.gridLayout.addWidget(self.mainTabs, 1, 0, 1, 1)
        self.uberGridLayout.addLayout(self.gridLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.mainTabs.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        QtCore.QObject.connect(self.generateButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.createCipherTable)
        QtCore.QObject.connect(self.browseKeyButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.singleKeyBrowse)
        self.browseEncryptionButton.clicked.connect(self.singleBrowse)
        self.browseDecryptionButton.clicked.connect(self.singleBrowse)
        self.startEncryptionButton.clicked.connect(self.encryptionMode)
        self.startDecryptionButton.clicked.connect(self.decryptionMode)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.completed = 0
        self.__cphtbl__ = []
        self.__plntxt__ = []
        self.__key__ = 0
        self.filePath = ""
        self.keyPath = ""
        self.fileSize = 0


    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.titleLabel.setText(_translate("MainWindow", "HexaCrypt", None))
        self.browseEncryptionButton.setText(_translate("MainWindow", "Browse item...", None))
        self.generateButton.setText(_translate("MainWindow", "Generate Key", None))
        self.encryptionComboBox.setItemText(0, _translate("MainWindow", "Hexa Encryption 1", None))
        self.encryptionComboBox.setItemText(1, _translate("MainWindow", "Hexa Encryption 2", None))
        self.formatLabel.setText(_translate("MainWindow", "Encryption format:", None))
        self.startEncryptionButton.setText(_translate("MainWindow", "Start encryption", None))
        self.deleteItemCheckBox.setText(_translate("MainWindow", "Delete item after encryption", None))
        self.mainTabs.setTabText(self.mainTabs.indexOf(self.encryptionTab), _translate("MainWindow", "Encryption", None))
        self.browseDecryptionButton.setText(_translate("MainWindow", "Browse item...", None))
        self.startDecryptionButton.setText(_translate("MainWindow", "Start decryption", None))
        self.formatLabel_2.setText(_translate("MainWindow", "Encryption format:", None))
        self.encryptionComboBox_2.setItemText(0, _translate("MainWindow", "Hexa Encryption 1", None))
        self.encryptionComboBox_2.setItemText(1, _translate("MainWindow", "Hexa Encryption 2", None))
        # self.insertKeyLabel.setText(_translate("MainWindow", "Insert key", None))
        self.browseKeyButton.setText(_translate("MainWindow", " Browse Key... ", None))
        self.mainTabs.setTabText(self.mainTabs.indexOf(self.decryptionTab), _translate("MainWindow", "Decryption", None))



if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    mainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(mainWindow)
    print("SETUPED")
    mainWindow.show()
    input()
    sys.exit(app.exec_())
