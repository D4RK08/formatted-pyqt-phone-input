from PyQt5.QtWidgets import QApplication,QLineEdit,QWidget,QFormLayout, QPushButton,QHBoxLayout, QDialog,QLabel
from PyQt5.QtGui import QIntValidator,QDoubleValidator,QFont
from PyQt5.QtCore import Qt
import sys
from contatto import contatto
from WinAddContact import WinAddContact
from qtpy.QtGui import QPixmap
from countries import countries
import os


class lineEditDemo(QWidget):
        def __init__(self,parent=None):
                super().__init__(parent)
                self.__directory = os.path.dirname(os.path.realpath(__file__))
                self.contieni_contatti = QFormLayout()
                
                aggiungi_button = QPushButton('+ Aggiungi', self)
                aggiungi_button.clicked.connect(self.aggiungi_contatto)

                barra_ricerca = QLineEdit()
                barra_ricerca.textChanged.connect(self.textchanged)

                mainBox = QHBoxLayout()
                mainBox.addWidget(aggiungi_button)
                mainBox.addWidget(barra_ricerca)

                self.flo = QFormLayout()
                self.flo.addRow(mainBox)

                self.mostra_contatti(contatto.contatti)


                self.setLayout(self.flo)
                self.setWindowTitle("QLineEdit Example")

        def clear_layout(self, layout=None):
            if layout is None:
                layout = self.contieni_contatti

            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                else:
                    child_layout = item.layout()
                    if child_layout is not None:
                        self.clear_layout(child_layout)

        def mostra_contatti(self,contatti):
            self.clear_layout()

            for contact in contatti:
                    boxContatto = QHBoxLayout()
                    name = QLineEdit(contact.nome)
                    name.setReadOnly(True)
                    name.editingFinished.connect(self.enterPress)
                    country_flag = QLabel()
                    flag_path = self.__directory + '/flag_icons/{}.png'.format(contact.country)
                    country_flag.setPixmap(QPixmap(flag_path).scaled(32, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                    country_flag.setToolTip('{} ({})'.format(countries[contact.country][0], countries[contact.country][1]))

                    number = QLineEdit(str(contact.numero))
                    number.setReadOnly(True)
                    number.editingFinished.connect(self.enterPress)
                    boxContatto.addWidget(name)
                    boxContatto.addWidget(country_flag)
                    boxContatto.addWidget(number)
                    self.contieni_contatti.addRow(boxContatto)

            self.flo.addRow(self.contieni_contatti)

        def aggiungi_contatto(self):
            dialog = WinAddContact(self)
            if dialog.exec_() == QDialog.Accepted:
                self.mostra_contatti(contatto.contatti)

        def textchanged(self,text):
            contact_list = []
            for contact in contatto.contatti:
                if text in contact.nome:
                    contact_list.append(contact)
            self.mostra_contatti(contact_list)

        def enterPress(self):
            print("Invio premuto o editing completato")

if __name__ == "__main__":
        app = QApplication(sys.argv)
        win = lineEditDemo()
        win.show()
        sys.exit(app.exec_())
