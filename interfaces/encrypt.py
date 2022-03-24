import PyQt5.QtWidgets as qtw
from PyQt5.QtGui import * 
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox

from datetime import datetime

import modules.keygen as keyg
import modules.encrypt as enc

import math

class encrypyWidget(qtw.QWidget):
    def __init__(self, parent):
        super(qtw.QWidget, self).__init__(parent)   
        self.initUI()
    
    def initUI(self):
        def pickFile():
            try:
                options = qtw.QFileDialog.Options()
                options |= qtw.QFileDialog.DontUseNativeDialog
                fileName, _ = qtw.QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All files (*)", options=options)
                if fileName:
                    eFileLabel.setText(fileName)

                    pictureList = ["jpeg","jpg","png","gif","bmp"]
                    if fileName.split(".")[-1] in pictureList:
                        count = fileLayout.layout().count()
                        if count > 1:
                            fileLayout.layout().removeItem(fileLayout.layout().itemAt(count-1))

                        fileDetailsImage = qtw.QLabel(self)
                        fileDetailsImage.setText("")

                        pixmap = QPixmap(fileName)
                        scaled = pixmap.scaledToWidth(200)
                        fileDetailsImage.setPixmap(scaled)

                        fileLayout.layout().addWidget(fileDetailsImage,count-1,Qt.AlignVCenter)
                    else:
                        count = fileLayout.layout().count()
                        if count > 1:
                            fileLayout.layout().removeItem(fileLayout.layout().itemAt(count-1))

                        fileDetails = qtw.QPlainTextEdit(self)
                        fileDetails.setReadOnly(True)
                        fileDetails.setPlainText("text")

                        fileDetails.setPlainText(str(open(fileName,"rb").read().decode("ISO-8859-1"))[0:1000])

                        fileLayout.layout().addWidget(fileDetails,count-1,Qt.AlignVCenter)

                    if len(nfillInput.text())>0:
                        fileOpen = open(eFileLabel.text(),"rb")
                        fileBin = fileOpen.read()
                        fileSize = len(fileBin)
                        print(nfillInput.text())
                        n = math.floor(math.log2(int(nfillInput.text())))
                        estimatedSize = fileSize*(1 + (1/n))
                        sizeTextLabel.setText(f"Ukuran File: {estimatedSize:.2f} Bytes")
                    else:
                        sizeTextLabel.setText("Ukuran File: - Bytes")
                    
                else:
                    eFileLabel.setText("Belum ada file dipilih!")
                    if fileLayout.layout().count() > 1:
                        fileLayout.layout().removeItem(fileLayout.layout().itemAt(-1))
                    raise Exception("file tidak ditemukan!")
            except Exception as e:
                eFileLabel.setText("Belum ada file dipilih!")
                sizeTextLabel.setText("Ukuran File: - Bytes")
                msg = QMessageBox()
                msg.setText("File gagal dipilih")
                msg.setInformativeText(f'File anda gagal dipilih karena {e}')
                msg.setWindowTitle("File gagal")
                msg.exec_()
        def pickKey():
            try:
                options = qtw.QFileDialog.Options()
                options |= qtw.QFileDialog.DontUseNativeDialog
                fileName, _ = qtw.QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","Public key files (*.pub)", options=options)
                if fileName:
                    eCatch, nCatch = keyg.openKeyFile(fileName)
                    efillInput.setText(str(eCatch))
                    nfillInput.setText(str(nCatch))
                    if len(eFileLabel.text())>0:
                        fileOpen = open(eFileLabel.text(),"rb")
                        fileBin = fileOpen.read()
                        fileSize = len(fileBin)
                        n = math.floor(math.log2(int(nfillInput.text())))
                        estimatedSize = fileSize*(1 + (1/n))
                        sizeTextLabel.setText(f"Ukuran File: {estimatedSize:.2f} Bytes")
                    else:
                        sizeTextLabel.setText("Ukuran File: - Bytes")      
                else:
                    raise Exception("File not found!")
            except Exception as e:
                msg = QMessageBox()
                msg.setText("Key gagal dipilih")
                msg.setInformativeText(f'Key anda gagal dipilih karena {e}')
                msg.setWindowTitle("Key gagal")
                msg.exec_()
        def encrypt():
            try:
                if (eFileLabel.text() != "Belum ada file dipilih!"):
                    if (len(efillInput.text()) > 0) and (len(nfillInput.text()) > 0):
                        if (keyg.relativePrime(int(efillInput.text()),int(nfillInput.text()))):
                            now = datetime.now()
                            enc.encryptFile(eFileLabel.text(),int(efillInput.text()),int(nfillInput.text()))
                            s = datetime.now() - now
                            msg = QMessageBox()
                            msg.setText("File berhasil dienkripsi")
                            msg.setInformativeText(f'File berhasil dienkripsi setelah {str(s)}\n')
                            msg.setWindowTitle("Enkripsi erhasil")
                            msg.exec_()
                        else:
                            msg = QMessageBox()
                            msg.setText("File gagal dienkripsi!")
                            msg.setInformativeText(f'Kunci tidak relatif prima!')
                            msg.setWindowTitle("Enkripsi Gagal")
                            msg.exec_() 

                    else:
                        msg = QMessageBox()
                        msg.setText("File gagal dienkripsi!")
                        msg.setInformativeText(f'Kunci tidak boleh kosong!')
                        msg.setWindowTitle("Enkripsi Gagal")
                        msg.exec_() 
                else:
                        msg = QMessageBox()
                        msg.setText("File gagal dienkripsi!")
                        msg.setInformativeText(f'File tidak boleh kosong!')
                        msg.setWindowTitle("Enkripsi Gagal")
                        msg.exec_() 

            except Exception as e:
                msg = QMessageBox()
                msg.setText("File gagal dienkripsi!")
                msg.setInformativeText(f'File gagal dienkripsi karena {e}')
                msg.setWindowTitle("Enkripsi Gagal")
                msg.exec_()

        self.layout = qtw.QGridLayout(self)
        self.setLayout(self.layout)

        filePickLayout = qtw.QGroupBox()
        filePickLayout.setLayout(qtw.QVBoxLayout())

        etextLabel = qtw.QLabel("File", self)
        getFont = etextLabel.font()
        getFont.setBold(True)
        etextLabel.setFont(getFont)
        eFileLabel = qtw.QLabel("Belum ada file dipilih!", self)
        efilePick = qtw.QPushButton("Pilih file")
        efilePick.clicked.connect(lambda: pickFile())

        filePickLayout.layout().addWidget(etextLabel,0,Qt.AlignTop) 
        filePickLayout.layout().addWidget(eFileLabel,1,Qt.AlignLeft)
        filePickLayout.layout().addWidget(efilePick,2,Qt.AlignVCenter)
        self.layout.addWidget(filePickLayout,0,0)


        keyLabel = qtw.QLabel("Public Key", self)
        keyLabel.setFont(getFont)

        eBoxLayout = qtw.QGroupBox()
        eBoxLayout.setLayout(qtw.QGridLayout())

        eFillLabel = qtw.QLabel("E:",self)
        efillInput = qtw.QLineEdit(self)

        nFillLabel = qtw.QLabel("N:",self)
        nfillInput = qtw.QLineEdit(self)

        kfilePick = qtw.QPushButton("Pilih file")
        kfilePick.clicked.connect(lambda: pickKey())

        eBoxLayout.layout().addWidget(keyLabel,0,0,1,2,Qt.AlignTop)
        eBoxLayout.layout().addWidget(eFillLabel,1,0,Qt.AlignLeft)
        eBoxLayout.layout().addWidget(efillInput,1,1,Qt.AlignLeft)
        eBoxLayout.layout().addWidget(nFillLabel,2,0,Qt.AlignLeft)
        eBoxLayout.layout().addWidget(nfillInput,2,1,Qt.AlignLeft)
        eBoxLayout.layout().addWidget(kfilePick,3,0,1,2,Qt.AlignVCenter)

        self.layout.addWidget(eBoxLayout,0,1)

        infoLayout = qtw.QGroupBox()
        infoLayout.setLayout(qtw.QVBoxLayout())

        infoTextLabel = qtw.QLabel("Estimasi", self)
        infoTextLabel.setFont(getFont)
        sizeTextLabel = qtw.QLabel("Ukuran File: - Bytes", self)
        # timeTextLabel = qtw.QLabel("Waktu Enkripsi: - Menit", self)

        infoLayout.layout().addWidget(infoTextLabel,1,Qt.AlignTop)
        infoLayout.layout().addWidget(sizeTextLabel,1,Qt.AlignLeft)
        # infoLayout.layout().addWidget(timeTextLabel,1,Qt.AlignLeft)

        self.layout.addWidget(infoLayout,0,2)
        
        fileLayout = qtw.QGroupBox()
        fileLayout.setLayout(qtw.QVBoxLayout())

        fileTextLabel = qtw.QLabel("Isi Cipherteks", self)
        fileTextLabel.setFont(getFont)

        fileLayout.layout().addWidget(fileTextLabel,0,Qt.AlignTop)

        self.layout.addWidget(fileLayout,1,0)
        
        saveButton = qtw.QPushButton("Enkripsi")  
        saveButton.clicked.connect(lambda: encrypt()) 

        self.layout.addWidget(saveButton,3,1,Qt.AlignVCenter)

