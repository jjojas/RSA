import PyQt5.QtWidgets as qtw
from PyQt5.QtGui import * 
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox

import modules.keygen as keyg
import modules.decrypt as dec
from datetime import datetime
import math
import os

class decryptWidget(qtw.QWidget):
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
                    fileDetails.setPlainText(str(open(fileName,"rb").read().hex())[0:1000])

                    if len(nfillInput.text())>0:
                        fileOpen = open(eFileLabel.text(),"rb")
                        fileBin = fileOpen.read()
                        fileSize = len(fileBin)
                        print(nfillInput.text())
                        n = math.floor(math.log2(int(nfillInput.text())))
                        estimatedSize = fileSize/(1 + (1/n))
                        sizeTextLabel.setText(f"Ukuran File: {estimatedSize/1024:.2f} KB")
                    else:
                        sizeTextLabel.setText("Ukuran File: - Bytes")

                else:
                    eFileLabel.setText("Belum ada file dipilih!")
                    sizeTextLabel.setText("Ukuran File: - Bytes")
                    fileDetails.setPlainText("")
                    raise Exception("file tidak ditemukan!")
            except Exception as e:
                eFileLabel.setText("Belum ada file dipilih!")
                sizeTextLabel.setText("Ukuran File: - Bytes")
                fileDetails.setPlainText("")
                msg = QMessageBox()
                msg.setText("File gagal dipilih")
                msg.setInformativeText(f'File anda gagal dipilih karena {e}')
                msg.setWindowTitle("File gagal")
                msg.exec_()
        def pickKey():
            try:
                options = qtw.QFileDialog.Options()
                options |= qtw.QFileDialog.DontUseNativeDialog
                fileName, _ = qtw.QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","Private key files (*.pri)", options=options)
                if fileName:
                    dCatch, nCatch = keyg.openKeyFile(fileName)
                    dfillInput.setText(str(dCatch))
                    nfillInput.setText(str(nCatch))

                    if len(eFileLabel.text())>0:
                        fileOpen = open(eFileLabel.text(),"rb")
                        fileBin = fileOpen.read()
                        fileSize = len(fileBin)
                        print(nfillInput.text())
                        n = math.floor(math.log2(int(nfillInput.text())))
                        estimatedSize = fileSize/(1 + (1/n))
                        sizeTextLabel.setText(f"Ukuran File: {estimatedSize/1024:.2f} KB")
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
        def decrypt():
            try:
                if (eFileLabel.text() != "Belum ada file dipilih!"):
                    if (len(dfillInput.text()) > 0) and (len(nfillInput.text()) > 0):
                        if (keyg.relativePrime(int(dfillInput.text()),int(nfillInput.text()))):
                            now = datetime.now()
                            dec.decryptFile(eFileLabel.text(),int(dfillInput.text()),int(nfillInput.text()))
                            s = datetime.now() - now
                            msg = QMessageBox()
                            msg.setText("File berhasil didekripsi")
                            fileName = eFileLabel.text().split("/")[-1]
                            fileEncrypted = f"files/decrypted_{fileName}"
                            msg.setInformativeText(f'File berhasil didekripsi setelah {str(s)}\ndengan ukuran {(os.path.getsize(fileEncrypted)/1024):.2f} KB')
                            msg.setWindowTitle("Dekripsi berhasil")
                            msg.exec_()

                    else:
                        msg = QMessageBox()
                        msg.setText("File gagal didekripsi!")
                        msg.setInformativeText(f'Kunci tidak boleh kosong!')
                        msg.setWindowTitle("Dekripsi Gagal")
                        msg.exec_() 
                else:
                        msg = QMessageBox()
                        msg.setText("File gagal didekripsi!")
                        msg.setInformativeText(f'File tidak boleh kosong!')
                        msg.setWindowTitle("Dekripsi Gagal")
                        msg.exec_() 

            except Exception as e:
                msg = QMessageBox()
                msg.setText("File gagal didekripsi!")
                msg.setInformativeText(f'File gagal didekripsi karena {e}')
                msg.setWindowTitle("Dekripsi Gagal")
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


        keyLabel = qtw.QLabel("Private Key", self)
        keyLabel.setFont(getFont)

        eBoxLayout = qtw.QGroupBox()
        eBoxLayout.setLayout(qtw.QGridLayout())

        dFillLabel = qtw.QLabel("D:",self)
        dfillInput = qtw.QLineEdit(self)

        nFillLabel = qtw.QLabel("N:",self)
        nfillInput = qtw.QLineEdit(self)

        kfilePick = qtw.QPushButton("Pilih file")
        kfilePick.clicked.connect(lambda: pickKey())

        eBoxLayout.layout().addWidget(keyLabel,0,0,1,2,Qt.AlignTop)
        eBoxLayout.layout().addWidget(dFillLabel,1,0,Qt.AlignLeft)
        eBoxLayout.layout().addWidget(dfillInput,1,1,Qt.AlignLeft)
        eBoxLayout.layout().addWidget(nFillLabel,2,0,Qt.AlignLeft)
        eBoxLayout.layout().addWidget(nfillInput,2,1,Qt.AlignLeft)
        eBoxLayout.layout().addWidget(kfilePick,3,0,1,2,Qt.AlignVCenter)

        self.layout.addWidget(eBoxLayout,0,1)

        infoLayout = qtw.QGroupBox()
        infoLayout.setLayout(qtw.QVBoxLayout())

        infoTextLabel = qtw.QLabel("Estimasi", self)
        infoTextLabel.setFont(getFont)
        sizeTextLabel = qtw.QLabel("Ukuran File: - Mb", self)

        infoLayout.layout().addWidget(infoTextLabel,1,Qt.AlignTop)
        infoLayout.layout().addWidget(sizeTextLabel,1,Qt.AlignLeft)

        self.layout.addWidget(infoLayout,0,2)

        fileLayout = qtw.QGroupBox()
        fileLayout.setLayout(qtw.QVBoxLayout())

        fileTextLabel = qtw.QLabel("Isi Cipherteks", self)
        fileTextLabel.setFont(getFont)
        fileDetails = qtw.QPlainTextEdit(self)
        fileDetails.setReadOnly(True)
        fileDetails.setPlainText("")

        fileLayout.layout().addWidget(fileTextLabel,0,Qt.AlignTop)
        fileLayout.layout().addWidget(fileDetails,1,Qt.AlignVCenter)

        self.layout.addWidget(fileLayout,1,0)
        
        saveButton = qtw.QPushButton("Dekripsi")  
        saveButton.clicked.connect(lambda: decrypt()) 

        self.layout.addWidget(saveButton,3,1,Qt.AlignVCenter)