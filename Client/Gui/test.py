from PySide6.QtCore import Slot, QCoreApplication
from PySide6.QtGui import QPixmap, QPalette, QBrush
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QDialog, QLineEdit, QVBoxLayout, QHBoxLayout, \
    QWidget, QSpacerItem, QSizePolicy


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set background image
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(QPixmap("background_image.jpg")))
        self.setPalette(palette)

        # Create buttons
        self.start_game_button = QPushButton("Start Game")
        self.start_game_button.setEnabled(False)
        self.start_game_button.setFixedHeight(100)  # Set height
        self.start_game_button.clicked.connect(self.start_game)  # Connect to start_game method

        start_game_layout = QHBoxLayout()
        start_game_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Fixed))  # Add spacer
        start_game_layout.addWidget(self.start_game_button)
        start_game_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Fixed))  # Add spacer

        self.login_button = QPushButton("Login")
        self.login_button.setFixedHeight(50)  # Set height

        self.exit_button = QPushButton("Exit")
        self.exit_button.setFixedHeight(50)  # Set height
        self.exit_button.clicked.connect(QCoreApplication.instance().quit)  # Connect to quit method

        # Create layout for smaller buttons
        button_layout = QHBoxLayout()
        button_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Fixed))  # Add spacer
        button_layout.addWidget(self.login_button)
        button_layout.addWidget(self.exit_button)
        button_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Fixed))  # Add spacer

        # Create main layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(start_game_layout)
        main_layout.addLayout(button_layout)

        # Create a central widget and set the layout
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Connect buttons
        self.login_button.clicked.connect(self.open_login_window)

    @Slot()
    def open_login_window(self):
        self.login_window = LoginWindow(self)
        self.login_window.show()

    @Slot()
    def start_game(self):
        # Add code here to start the game
        pass


class LoginWindow(QDialog):
    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window

        # Create username and password fields
        self.username_field = QLineEdit()
        self.password_field = QLineEdit()
        self.password_field.setEchoMode(QLineEdit.Password)

        # Create buttons
        self.back_button = QPushButton("Back")
        self.submit_button = QPushButton("Submit")

        # Arrange widgets vertically
        layout = QVBoxLayout()
        layout.addWidget(self.username_field)
        layout.addWidget(self.password_field)
        layout.addWidget(self.back_button)
        layout.addWidget(self.submit_button)
        self.setLayout(layout)

        # Connect buttons
        self.back_button.clicked.connect(self.close)
        self.submit_button.clicked.connect(self.check_credentials)

    @Slot()
    def check_credentials(self):
        # Check username and password (this is just a placeholder)
        if self.username_field.text() == "user" and self.password_field.text() == "pass":
            self.main_window.start_game_button.setEnabled(True)
            self.close()


app = QApplication([])
window = MainWindow()
window.show()
app.exec()
