from PyQt5.QtWidgets import QDialog,QFormLayout,QLineEdit,QPushButton
from contatto import contatto
from src.pyqt_phone_input.phone_input import PhoneInput

class WinAddContact(QDialog):
        def __init__(self, parent = None):
            super().__init__(parent)
            flo = QFormLayout()
            

            self.nome = QLineEdit()
            self.numero = PhoneInput()

            aggiungi_button = QPushButton('+ Aggiungi', self)
            aggiungi_button.clicked.connect(self.aggiungi_contatto)
            
            flo.addRow("Nome: ",self.nome)
            flo.addRow("Numero: ",self.numero)
            flo.addRow(aggiungi_button)

            self.setLayout(flo)
            self.setWindowTitle("Aggiungi contatto")

        def aggiungi_contatto(self):
            nome = self.nome.text().strip()
            numero = self.numero.getPhoneNumber()
            # Controllo che nome non sia vuoto e che numero sia completo (non contenga spazi)
            if not nome:
                # Qui puoi mostrare un messaggio d'errore oppure ignorare
                print("Inserisci un nome valido")
                return
            if len(numero) < len(self.numero.getCountryDropdown().getPhoneFormat()):
                print("numero no valido")
                return

            contatto(nome,numero,self.numero.getCountryDropdown().getCountry())
            self.accept()
