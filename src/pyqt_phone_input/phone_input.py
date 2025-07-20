from PyQt5.QtWidgets import QWidget, QLineEdit, QHBoxLayout
from country_dropdown import CountryDropdown

class PhoneInput(QWidget):
    def __init__(self):
        super().__init__()

        # LineEdit per il numero
        self.text = QLineEdit()
        self.text.setMaxLength(20)  # limite generico, sovrascritto dalla formattazione
        self.text.setPlaceholderText("123-456-7890")
        self.text.textChanged.connect(self.format_input)

        self.text.setStyleSheet("""
            QLineEdit {
                border: 1px solid gray;
                border-top-left-radius: 0px;
                border-bottom-left-radius: 0px;
                border-top-right-radius: 8px;
                border-bottom-right-radius: 8px;
                padding: 5px;
            }
        """)

        # Dropdown paese
        self.country_dropdown = CountryDropdown()
        phone_code_edit = QLineEdit()
        phone_code_edit.setReadOnly(True)
        phone_code_edit.setStyleSheet("""
            QLineEdit {
                border: 1px solid gray;
                border-right: none;
                border-top-left-radius: 8px;
                border-bottom-left-radius: 8px;
                border-top-right-radius: 0px;
                border-bottom-right-radius: 0px;
                padding: 5px;
                background-color: #f0f0f0;
            }
        """)
        self.country_dropdown.setPhoneCodeLineEdit(phone_code_edit)

        # Quando si cambia paese, aggiorna il formato
        self.country_dropdown.currentTextChanged.connect(
            lambda _: self.set_format(self.country_dropdown.getFormat())
        )

        # Layout orizzontale
        layout = QHBoxLayout()
        layout.addWidget(self.country_dropdown)
        layout.addWidget(self.text)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        # Inizializza il formato iniziale
        self.set_format(self.country_dropdown.getFormat())

    def set_format(self, phone_format: str):
        """Imposta il formato come '000-000-0000'"""
        self.phone_format = phone_format
        self.separator_positions = []
        self.total_digits = 0

        # Registra le posizioni dei separatori e conta le cifre
        for i, c in enumerate(phone_format):
            if c != '0':
                self.separator_positions.append((i, c))
            else:
                self.total_digits += 1

        # Riformatta il testo esistente
        self.format_input(self.text.text())

    def format_input(self, text: str):
        digits = ''.join(filter(str.isdigit, text))[:self.total_digits]
        formatted = ''
        digit_index = 0

        for i in range(len(self.phone_format)):
            if any(pos == i for pos, _ in self.separator_positions):
                sep = next(sep for pos, sep in self.separator_positions if pos == i)
                formatted += sep
            elif digit_index < len(digits):
                formatted += digits[digit_index]
                digit_index += 1
            else:
                break

        # Mantiene la posizione del cursore dopo la formattazione
        cursor_pos = self.text.cursorPosition()
        self.text.blockSignals(True)
        self.text.setText(formatted)
        self.text.blockSignals(False)
        self.text.setCursorPosition(min(cursor_pos, len(formatted)))

    def getPhoneNumber(self) -> str:
        """Restituisce il numero formattato completo con prefisso"""
        return self.country_dropdown.getCountryPhoneCode() + self.text.text().replace(' ', '')

    def setPhoneNumber(self, number: str):
        """Imposta il numero, riformattandolo"""
        digits_only = ''.join(filter(str.isdigit, number))
        self.text.setText(digits_only)
