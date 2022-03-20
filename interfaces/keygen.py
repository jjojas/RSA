import PyQt5.QtWidgets as qtw
from PyQt5.QtGui import * 
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox

import modules.keygen as keyg

cipherCache = ""

class keygenWidget(qtw.QWidget):
    def __init__(self, parent):
        super(qtw.QWidget, self).__init__(parent)   
        self.initUI()
    
    def initUI(self):
        def generate():
            try:
                p = int(ptextBox.text())
                q = int(qtextBox.text())
                e = int(etextBox.text())
                name = saveLine.text()
                keyg.createKeyFile(name,p,q,e)
                msg = QMessageBox()
                msg.setText("Kunci berhasil dibuat!")
                msg.setInformativeText(f'Kunci publik Anda dapat diakses di key/{saveLine.text()}.pub dan \n Kunci privat Anda dapat diakses di key/{saveLine.text()}.pri ')
                msg.setWindowTitle("Pembangkitan kunci berhasil")
                msg.exec_()
            except Exception as e:
                msg = QMessageBox()
                msg.setText("Kunci gagal dibuat!")
                msg.setInformativeText(f'Kunci anda gagal dibuat karena {e}')
                msg.setWindowTitle("Pembangkitan kunci gagal")
                msg.exec_()

        self.layout = qtw.QGridLayout(self)
        self.setLayout(self.layout)

        ptextLabel = qtw.QLabel("P:", self)
        ptextBox = qtw.QLineEdit(self)

        self.layout.addWidget(ptextLabel,0,0)
        self.layout.addWidget(ptextBox,1,0)

        qtextLabel = qtw.QLabel("Q:", self)
        qtextBox = qtw.QLineEdit(self)

        self.layout.addWidget(qtextLabel,0,1)
        self.layout.addWidget(qtextBox,1,1)

        etextLabel = qtw.QLabel("E:", self)
        etextBox = qtw.QLineEdit(self)

        self.layout.addWidget(etextLabel,0,2)
        self.layout.addWidget(etextBox,1,2)

        saveBoxLayout = qtw.QGroupBox()
        saveBoxLayout.setLayout(qtw.QVBoxLayout())
        saveLabel = qtw.QLabel("Key Name:", self)
        saveLine = qtw.QLineEdit(self)
        saveButton = qtw.QPushButton("Generate Key")  
        saveButton.clicked.connect(lambda: generate()) 

        saveBoxLayout.layout().addWidget(saveLabel,0,Qt.AlignHCenter)
        saveBoxLayout.layout().addWidget(saveLine,1,Qt.AlignHCenter)
        saveBoxLayout.layout().addWidget(saveButton,2,Qt.AlignHCenter)

        self.layout.addWidget(saveBoxLayout,2,1)



