import PyQt5.QtWidgets as qtw
from PyQt5.QtGui import * 
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox

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
                else:
                    raise Exception("File not found!")
            except Exception as e:
                msg = QMessageBox()
                msg.setText("File gagal dipilih")
                msg.setInformativeText(f'File anda gagal dipilih karena {e}')
                msg.setWindowTitle("File gagal")
                msg.exec_()
        def pickKey():
            try:
                options = qtw.QFileDialog.Options()
                options |= qtw.QFileDialog.DontUseNativeDialog
                fileName, _ = qtw.QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","Private key files (*.priv)", options=options)
                if fileName:
                    keyFile.setText(fileName)        
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
                pass
            except Exception as e:
                msg = QMessageBox()
                msg.setText("Kunci gagal dibuat!")
                msg.setInformativeText(f'Kunci anda gagal dibuat karena {e}')
                msg.setWindowTitle("Pembangkitan kunci gagal")
                msg.exec_()

        self.layout = qtw.QGridLayout(self)
        self.setLayout(self.layout)

        etextLabel = qtw.QLabel("File untuk didekripsi:", self)
        eFileLabel = qtw.QLabel("Belum ada file dipilih!", self)
        efilePick = qtw.QPushButton("Pilih file")
        efilePick.clicked.connect(lambda: pickFile())

        self.layout.addWidget(etextLabel,0,0)
        self.layout.addWidget(eFileLabel,1,0)
        self.layout.addWidget(efilePick,2,0)


        keyLabel = qtw.QLabel("Private key untuk mendekripsi:", self)
        keyFile = qtw.QLabel("Belum ada file dipilih!", self)
        kfilePick = qtw.QPushButton("Pilih file")
        kfilePick.clicked.connect(lambda: pickKey())

        self.layout.addWidget(keyLabel,0,1)
        self.layout.addWidget(keyFile,1,1)
        self.layout.addWidget(kfilePick,2,1)

        infoTextLabel = qtw.QLabel("Estimasi", self)
        sizeTextLabel = qtw.QLabel("Ukuran File: - Mb", self)
        timeTextLabel = qtw.QLabel("Waktu Enkripsi: - Menit", self)

        self.layout.addWidget(infoTextLabel,0,2)
        self.layout.addWidget(sizeTextLabel,1,2)
        self.layout.addWidget(timeTextLabel,2,2)

        saveBoxLayout = qtw.QGroupBox()
        saveBoxLayout.setLayout(qtw.QVBoxLayout())
        saveButton = qtw.QPushButton("Dekripsi")  
        saveButton.clicked.connect(lambda: decrypt()) 

        saveBoxLayout.layout().addWidget(saveButton,2,Qt.AlignHCenter)

        self.layout.addWidget(saveBoxLayout,3,1)