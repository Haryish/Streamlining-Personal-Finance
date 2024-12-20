import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QFormLayout, QComboBox, QLineEdit, QPushButton, QLabel, QDateEdit, QStackedWidget
from PyQt5.QtCore import Qt, QDate
import json

# Django API URLs
API_URL = "http://127.0.0.1:8000/api/addmoney/"  # Change to your Django API URL for adding money
LOGIN_URL = "http://127.0.0.1:8000/api/login/"  # Change to your Django login API URL

# PyQt5 GUI application class
class AddMoneyApp(QWidget):
    def __init__(self):
        super().__init__()

        # Set up main window
        self.setWindowTitle('Merchant Vendor')
        self.setGeometry(100, 100, 600, 200)

        # Set up the main layout
        self.layout = QVBoxLayout(self)

        # Create stacked layout for switching between login and main form
        self.stacked_layout = QStackedWidget()

        # Create login page and main page
        self.main_page = self.create_main_page()
        self.login_page = self.create_login_page()

        # Add both pages to the stacked layout
        self.stacked_layout.addWidget(self.main_page)
        self.stacked_layout.addWidget(self.login_page)

        # Add the stacked layout to the main layout
        self.layout.addWidget(self.stacked_layout)

        # Show main page (Add Money page) initially
        self.stacked_layout.setCurrentWidget(self.main_page)

        # Placeholder for user data
        self.user_id = None
        self.add_money_data = None

    def create_login_page(self):
        """ Create the login page widget """
        login_widget = QWidget()
        layout = QVBoxLayout()

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)

        login_button = QPushButton('Login')
        login_button.clicked.connect(self.login)

        self.login_response_label = QLabel()

        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(login_button)
        layout.addWidget(self.login_response_label)

        login_widget.setLayout(layout)
        return login_widget

    def create_main_page(self):
        """ Create the main transaction form page widget """
        main_widget = QWidget()
        layout = QVBoxLayout()

        # Form layout for input fields
        form_layout = QFormLayout()

        self.add_money_combo = QComboBox()
        self.add_money_combo.addItems(["Expense"])
        form_layout.addRow('Add Type:', self.add_money_combo)

        self.category_combo = QComboBox()
        self.category_combo.addItems(["Food", "Travel", "Shopping", "Necessities", "Entertainment", "Other"])
        form_layout.addRow('Category:', self.category_combo)

        self.quantity_input = QLineEdit()
        self.quantity_input.setPlaceholderText('Enter Amount')
        form_layout.addRow('Expense Amount :', self.quantity_input)

        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setDisplayFormat("yyyy-MM-dd")
        form_layout.addRow('Date:', self.date_input)

        layout.addLayout(form_layout)

        submit_button = QPushButton('Submit')
        submit_button.clicked.connect(self.submit_form)

        self.response_label = QLabel()
        layout.addWidget(submit_button)
        layout.addWidget(self.response_label)

        # Logout button (only visible after successful login)
        logout_button = QPushButton('Logout')
        logout_button.clicked.connect(self.logout)


        main_widget.setLayout(layout)
        return main_widget

    def submit_form(self):
        """ Submit the form with transaction details only after login """
        # Store form data temporarily until login is successful
        add_money = self.add_money_combo.currentText()
        category = self.category_combo.currentText()
        quantity = self.quantity_input.text()
        date = self.date_input.date().toString("yyyy-MM-dd")

        # Validate the quantity input
        if not quantity:
            self.response_label.setText("Please enter a valid amount.")
            self.response_label.setStyleSheet("color: red")
            return

        try:
            quantity = float(quantity)  # Ensure quantity is a valid integer
        except ValueError:
            self.response_label.setText("Please enter a valid amount.")
            self.response_label.setStyleSheet("color: red")
            return

        # Prepare data to send after login is successful
        self.add_money_data = {
            "add_money": add_money,
            "quantity": quantity,
            "Date": date,
            "Category": category,
        }

        # Switch to login page for login
        self.stacked_layout.setCurrentWidget(self.login_page)

    def login(self):
        """ Handle user login """
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            self.login_response_label.setText("Please enter username and password.")
            self.login_response_label.setStyleSheet("color: red")
            return

        # Send login request to Django backend
        data = {
            'username': username,
            'password': password
        }
        try:
            response = requests.post(LOGIN_URL, data=data)

            if response.status_code == 200:
                # Login successful, get user data from the response (e.g., user ID or token)
                user_data = response.json()  # Assuming user data is returned in JSON format
                self.user_id = user_data['user_id']  # Adjust according to your response structure

                self.login_response_label.setText("Login successful!")
                self.login_response_label.setStyleSheet("color: green")

                # Now submit the Add Money data
                if self.add_money_data:
                    self.submit_add_money_data()

                # Switch to the Add Money page after successful login
                self.stacked_layout.setCurrentWidget(self.main_page)
            else:
                self.login_response_label.setText("Login failed. Please try again.")
                self.login_response_label.setStyleSheet("color: red")
        except requests.exceptions.RequestException as e:
            self.login_response_label.setText(f"Error: {e}")
            self.login_response_label.setStyleSheet("color: red")

    def submit_add_money_data(self):
        """ Send POST request with transaction data to Django backend after successful login """
        if not self.user_id:
            self.response_label.setText("User ID is missing, cannot submit data.")
            self.response_label.setStyleSheet("color: red")
            return

        # Add user ID to the transaction data before sending to the backend
        data = self.add_money_data.copy()
        data["user"] = self.user_id  # Add the authenticated user's ID

        try:
            response = requests.post(API_URL, data=json.dumps(data), headers={'Content-Type': 'application/json'})

            if response.status_code == 201:
                self.response_label.setText("Transaction posted successfully!")
                self.response_label.setStyleSheet("color: green")
            else:
                self.response_label.setText(f"Failed to post transaction. Status: {response.status_code}")
                self.response_label.setStyleSheet("color: red")

        except requests.exceptions.RequestException as e:
            self.response_label.setText(f"Error occurred: {e}")
            self.response_label.setStyleSheet("color: red")

    def logout(self):
        """ Handle logout functionality """
        # Clear the user session data
        self.user_id = None

        # Clear all fields
        self.username_input.clear()
        self.password_input.clear()

        # Switch back to the login page
        self.stacked_layout.setCurrentWidget(self.login_page)
        self.login_response_label.clear()

        # Optionally display a logout message
        self.response_label.setText("Logged out successfully.")
        self.response_label.setStyleSheet("color: blue")


def main():
    app = QApplication(sys.argv)
    window = AddMoneyApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
