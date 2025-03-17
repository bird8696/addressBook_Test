import pickle
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QTextEdit, QMessageBox

class AddressBook(QWidget):
    def __init__(self):
        super().__init__()
        self.filename = "address_book.pkl"
        self.contacts = self.load_contacts()
        self.initUI()

    def load_contacts(self):
        try:
            with open(self.filename, "rb") as file:
                return pickle.load(file)
        except (FileNotFoundError, EOFError):
            return {}

    def save_contacts(self):
        with open(self.filename, "wb") as file:
            pickle.dump(self.contacts, file)

    def initUI(self):
        layout = QVBoxLayout()

        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("이름")
        layout.addWidget(self.name_input)

        self.phone_input = QLineEdit(self)
        self.phone_input.setPlaceholderText("전화번호")
        layout.addWidget(self.phone_input)

        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText("이메일")
        layout.addWidget(self.email_input)

        self.address_input = QTextEdit(self)
        self.address_input.setPlaceholderText("주소")
        layout.addWidget(self.address_input)

        self.add_button = QPushButton("연락처 추가", self)
        self.add_button.clicked.connect(self.add_contact)
        layout.addWidget(self.add_button)

        self.search_button = QPushButton("연락처 검색", self)
        self.search_button.clicked.connect(self.search_contact)
        layout.addWidget(self.search_button)

        self.delete_button = QPushButton("연락처 삭제", self)
        self.delete_button.clicked.connect(self.delete_contact)
        layout.addWidget(self.delete_button)

        self.display_button = QPushButton("연락처 전체 보기", self)
        self.display_button.clicked.connect(self.display_contacts)
        layout.addWidget(self.display_button)

        self.result_area = QTextEdit(self)
        self.result_area.setReadOnly(True)
        layout.addWidget(self.result_area)

        self.setLayout(layout)
        self.setWindowTitle("주소록")
        self.setGeometry(100, 100, 400, 500)
        self.show()

    def add_contact(self):
        name = self.name_input.text()
        phone = self.phone_input.text()
        email = self.email_input.text()
        address = self.address_input.toPlainText()
        
        if name:
            self.contacts[name] = {"phone": phone, "email": email, "address": address}
            self.save_contacts()
            QMessageBox.information(self, "성공", f"{name} 추가 완료!")
            self.clear_inputs()
        else:
            QMessageBox.warning(self, "오류", "이름을 입력하세요.")

    def search_contact(self):
        name = self.name_input.text()
        if name in self.contacts:
            info = self.contacts[name]
            self.result_area.setText(f"이름: {name}\n전화번호: {info['phone']}\n이메일: {info['email']}\n주소: {info['address']}")
        else:
            QMessageBox.warning(self, "오류", "연락처를 찾을 수 없습니다.")

    def delete_contact(self):
        name = self.name_input.text()
        if name in self.contacts:
            del self.contacts[name]
            self.save_contacts()
            QMessageBox.information(self, "성공", f"{name} 삭제 완료!")
            self.clear_inputs()
        else:
            QMessageBox.warning(self, "오류", "연락처를 찾을 수 없습니다.")

    def display_contacts(self):
        if self.contacts:
            contact_list = "\n".join([f"이름: {name}, 전화번호: {info['phone']}, 이메일: {info['email']}, 주소: {info['address']}" for name, info in self.contacts.items()])
            self.result_area.setText(contact_list)
        else:
            self.result_area.setText("주소록이 비어 있습니다.")

    def clear_inputs(self):
        self.name_input.clear()
        self.phone_input.clear()
        self.email_input.clear()
        self.address_input.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = AddressBook()
    sys.exit(app.exec_())
