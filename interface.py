from imports import *

class FirstPage(QWidget): #0
    def __init__(self, parent):
        super().__init__(parent)

        layout = QVBoxLayout(self)

        admin_button = QPushButton('Admin', self)
        admin_button.clicked.connect(self.admin_clicked)

        user_button  = QPushButton('User', self)
        user_button.clicked.connect(self.user_clicked)

        layout.addWidget(admin_button)
        layout.addWidget(user_button)

    def admin_clicked(self):
        self.parent().setCurrentIndex(1)  
    
    def user_clicked(self):
        self.parent().setCurrentIndex(2)  

class AdmLogPage(QWidget): #1
    def __init__(self, parent):
        super().__init__(parent)

        layout = QFormLayout(self)

        username_edit = QLineEdit(self)
        password_edit = QLineEdit(self)
        login_button  = QPushButton('Login', self)
        back_button   = QPushButton('Back', self)

        username_edit.setObjectName('username_edit')
        password_edit.setObjectName('password_edit')
        password_edit.setEchoMode(QLineEdit.Password)
        username_edit.setMaxLength(20)
        password_edit.setMaxLength(20)

        layout.addRow('Username:', username_edit)
        layout.addRow('Password:', password_edit)
        layout.addRow(back_button, login_button)

        back_button.clicked.connect(self.back_clicked)
        login_button.clicked.connect(self.login_clicked)

    def back_clicked(self):
        self.reset_data()
        self.parent().setCurrentIndex(0)

    def login_clicked(self):
        username = self.findChild(QLineEdit, 'username_edit').text()
        passwrd = self.findChild(QLineEdit, 'password_edit').text()

        success = try_log(self.parent().crs, username, passwrd, 1)

        if success:
            self.parent().conn.commit()
            self.reset_data()
            self.parent().setCurrentIndex(5)
        else:
            QMessageBox.warning(self, 'Error', f'Failed to Login user.\n Invalid Account')
    def reset_data(self):
        for widget in self.findChildren(QLineEdit):
            if isinstance(widget, QLineEdit):
                widget.clear()
    
class UserPage(QWidget): #2
    def __init__(self, parent):
        super().__init__(parent)

        layout = QFormLayout(self)

        username_edit   = QLineEdit(self)
        password_edit   = QLineEdit(self)
        login_button    = QPushButton('Login', self)
        register_button = QPushButton('Register', self)
        back_button     = QPushButton('Back', self)

        username_edit.setObjectName('username_edit')
        password_edit.setObjectName('password_edit')
        password_edit.setEchoMode(QLineEdit.Password)
        username_edit.setMaxLength(20)
        password_edit.setMaxLength(20)

        layout.addRow('Username:', username_edit)
        layout.addRow('Password:', password_edit)
        layout.addRow(register_button, login_button)
        layout.addRow(back_button)

        back_button.clicked.connect(self.back_clicked)
        register_button.clicked.connect(self.register_clicked)
        login_button.clicked.connect(self.login_clicked)

    def login_clicked(self):
        username = self.findChild(QLineEdit, 'username_edit').text()
        passwrd  = self.findChild(QLineEdit, 'password_edit').text()

        success  = try_log(self.parent().crs, username, passwrd, 0)

        if success:
            self.reset_data()
            self.parent().conn.commit()
            self.parent().setCurrentIndex(4)
            self.parent().findChild(QStackedWidget, "shop_page").findChild(QWidget, "second_page").update_data()
            self.parent().CID = get_cid(self.parent().crs, username, passwrd)
        else:
            QMessageBox.warning(self, 'Error', f'Failed to Login user.\n Invalid Account')
    def back_clicked(self):
        self.reset_data()
        self.parent().setCurrentIndex(0) 

    def register_clicked(self):
        self.reset_data()
        self.parent().setCurrentIndex(3)  

    def reset_data(self):
        for widget in self.findChildren(QLineEdit):
            if isinstance(widget, QLineEdit):
                widget.clear()

class RegisterPage(QWidget): #3
    def __init__(self, parent):
        super().__init__(parent)

        layout = QFormLayout(self)

        username_edit     = QLineEdit(self)
        email_edit        = QLineEdit(self)
        pnumber_edit      = QLineEdit(self)
        password_edit     = QLineEdit(self)
        confpassword_edit = QLineEdit(self)

        username_edit.setObjectName('username_edit')
        email_edit.setObjectName('email_edit')
        pnumber_edit.setObjectName('pnumber_edit')
        password_edit.setObjectName('password_edit')
        confpassword_edit.setObjectName('confpassword_edit')

        username_edit.setMaxLength(20)  
        email_edit.setMaxLength(30)     
        pnumber_edit.setMaxLength(10)   
        password_edit.setMaxLength(20)  
        confpassword_edit.setMaxLength(20)

        password_edit.setEchoMode(QLineEdit.Password)
        confpassword_edit.setEchoMode(QLineEdit.Password)

        register_button = QPushButton('Register', self)
        back_button = QPushButton('Back', self)

        layout.addRow('Username:', username_edit)
        layout.addRow('Email:', email_edit)
        layout.addRow('Phone Number:', pnumber_edit)
        layout.addRow('Password:', password_edit)
        layout.addRow('Confirm Password:', confpassword_edit)

        layout.addRow(back_button, register_button)

        back_button.clicked.connect(self.back_clicked)
        register_button.clicked.connect(self.register_clicked)

    def register_clicked(self):
        passwrd      = self.findChild(QLineEdit, 'password_edit').text()
        confpassword = self.findChild(QLineEdit, 'confpassword_edit').text()
        username     = self.findChild(QLineEdit, 'username_edit').text()
        pnumber      = self.findChild(QLineEdit, 'pnumber_edit').text()
        email        = self.findChild(QLineEdit, 'email_edit').text()

        if passwrd == confpassword and len(passwrd) > 7:
                success, err_msg = new_user(self.parent().crs, username, email, pnumber, passwrd)
                if success:
                    self.reset_data()
                    self.parent().conn.commit()
                    self.parent().setCurrentIndex(2)
                else:
                    QMessageBox.warning(self, 'Error', f'Failed to register user.\n {err_msg}')

        else:
            QMessageBox.warning(self, 'Error', 'Passwords do not match. Or Password too short')
    
    def reset_data(self):
        for widget in self.findChildren(QLineEdit):
            if isinstance(widget, QLineEdit):
                widget.clear()
    
    def back_clicked(self):
        self.reset_data()
        self.parent().setCurrentIndex(2) 

class GameDetailsPage(QWidget):
    def __init__(self, game_name, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)

        name_label = QLabel(f"Details for {game_name}:\n", self)
        layout.addWidget(name_label)
        self.crs = self.parent().parent().parent().crs
        self.CID = self.parent().parent().parent().CID
        price, stock, release_date, game_desc = get_games_details(self.crs, game_name)
        publisher = get_publisher(self.crs, game_name)
        publisher_label = QLabel(f"Publisher: {publisher}", self)
        layout.addWidget(publisher_label)

        price_label = QLabel(f"Price: {price}", self)
        layout.addWidget(price_label)

        stock_label = QLabel(f"Stock: {stock}", self)
        layout.addWidget(stock_label)

        release_date_label = QLabel(f"Release Date: {release_date}", self)
        layout.addWidget(release_date_label)

        game_desc_label = QLabel(f"Details for {game_desc}", self)
        layout.addWidget(game_desc_label)
        
        self.game_name = game_name
        buy_button = QPushButton("Buy", self)
        buy_button.clicked.connect(self.buy_item)
        layout.addWidget(buy_button)

        back_button = QPushButton("Back", self)
        back_button.clicked.connect(self.back_to_shop)
        layout.addWidget(back_button)

    def back_to_shop(self):
        self.parent().setCurrentIndex(0)

    def buy_item(self):
        if(buy_item(self.crs, self.game_name, self.CID)):
            self.parent().setCurrentIndex(1)
        else:
            QMessageBox.warning(self, 'Error', f'Failed to buy game.\n Not enough Stock')

class ThanksForBuyPage(QWidget):
    def __init__(self, game_name, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        thanks_label = QLabel(f"Thanks for buying from us!!\n")
        thanks_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(thanks_label)

        back_button = QPushButton("Back", self)
        back_button.clicked.connect(self.back_to_shop)
        layout.addWidget(back_button)

    def back_to_shop(self):
        self.parent().setCurrentIndex(0)

class GameListPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        layout = QVBoxLayout(self)

        top_bar_layout = QHBoxLayout()
        text_box = QLabel("Choose 1 game to buy", self)
        text_box.setAlignment(Qt.AlignCenter)

        logout_button = QPushButton("Logout", self)
        logout_button.clicked.connect(self.back_to_log)
        top_bar_layout.addWidget(logout_button, alignment=Qt.AlignRight)
        top_bar_layout.addWidget(text_box)

        layout.addLayout(top_bar_layout)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_area.setWidget(self.scroll_widget)

        layout.addWidget(text_box)
        layout.addWidget(self.scroll_area)

        self.populate_game_buttons()

    def populate_game_buttons(self):
        crs = self.parent().parent().crs
        name_games = get_games_name(crs)

        for game_name in name_games:
            game_button = QPushButton(game_name, self)
            game_button.clicked.connect(lambda _, name=game_name: self.show_game_details(name))
            self.scroll_layout.addWidget(game_button)

    def update_data(self):
        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        self.populate_game_buttons()

    def show_game_details(self, game_name):
        game_details_page = GameDetailsPage(game_name, self)
        self.parent().addWidget(game_details_page)
        self.parent().setCurrentWidget(game_details_page)

    def back_to_log(self):
        self.parent().parent().setCurrentIndex(1)


class ShopPage(QStackedWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.second_page = GameListPage(self)
        self.second_page.setObjectName("second_page")
        self.addWidget(self.second_page)

        self.first_page = ThanksForBuyPage(self)
        self.addWidget(self.first_page)

class ManPage(QWidget): #5
    def __init__(self, parent):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        top_bar_layout = QHBoxLayout()
        logout_button = QPushButton("Logout", self)
        logout_button.clicked.connect(self.back_to_log)
        top_bar_layout.addWidget(logout_button, alignment=Qt.AlignRight)
        layout.addLayout(top_bar_layout)
        
        add_button = QPushButton("Add Game", self)
        add_button.clicked.connect(self.add_game)
        layout.addWidget(add_button)

        remove_button = QPushButton("Remove Game", self)
        remove_button.clicked.connect(self.remove_game)
        layout.addWidget(remove_button)

        update_button = QPushButton("Update Game", self)
        update_button.clicked.connect(self.update_game)
        layout.addWidget(update_button)


    def add_game(self):
        self.parent().setCurrentIndex(6)

    def remove_game(self):
        self.parent().findChild(QWidget, 'remove_game_page').update_game_list()
        self.parent().setCurrentIndex(7)   
    
    def update_game(self):
        self.parent().findChild(QWidget, 'update_game_page').update_game_list()
        self.parent().setCurrentIndex(8)   


    def back_to_log(self):
         self.parent().setCurrentIndex(1)

class AddGamePage(QWidget): #6
    def __init__(self, parent):
        super().__init__(parent)
        
        layout = QFormLayout(self)

        game_name_edit    = QLineEdit(self)
        price_edit        = QLineEdit(self)
        stock_edit        = QLineEdit(self)
        release_date_edit = QLineEdit(self)
        game_desc_edit    = QLineEdit(self)
        publisher_edit    = QLineEdit(self)


        game_name_edit.setObjectName('game_name_edit')
        publisher_edit.setObjectName('publisher_edit')
        price_edit.setObjectName('price_edit')
        stock_edit.setObjectName('stock_edit')
        release_date_edit.setObjectName('release_date_edit')
        game_desc_edit.setObjectName('game_desc_edit')


        game_name_edit.setMaxLength(30)  
        publisher_edit.setMaxLength(200)
        price_edit.setMaxLength(3)     
        stock_edit.setMaxLength(5)
        release_date_edit.setMaxLength(10)  
        game_desc_edit.setMaxLength(30)

        register_button = QPushButton('Add', self)
        back_button = QPushButton('Back', self)

        layout.addRow('Game Name:', game_name_edit)
        layout.addRow('Game Publisher:', publisher_edit)
        layout.addRow('Price:', price_edit)
        layout.addRow('Stock:', stock_edit)
        layout.addRow('Release Date(YYYY-MM-DD):', release_date_edit)
        layout.addRow('Game Description:', game_desc_edit)

        layout.addRow(back_button, register_button)

        back_button.clicked.connect(self.back_clicked)
        register_button.clicked.connect(self.ADD_clicked)

    def ADD_clicked(self):
        game_name    = self.findChild(QLineEdit, 'game_name_edit').text()
        publisher    = self.findChild(QLineEdit, 'publisher_edit').text()
        price        = self.findChild(QLineEdit, 'price_edit').text()
        stock        = self.findChild(QLineEdit, 'stock_edit').text()
        release_date = self.findChild(QLineEdit, 'release_date_edit').text()
        game_desc    = self.findChild(QLineEdit, 'game_desc_edit').text()

        if game_name is not None and publisher is not None and price is not None and stock and release_date is not None and game_desc is not None:
                success, err_msg = new_game(self.parent().crs, game_name, publisher, price, stock, release_date, game_desc)
                if success:
                    self.parent().conn.commit()
                    self.reset_data()
                    self.parent().setCurrentIndex(5)
                else:
                    QMessageBox.warning(self, 'Error', f'Failed to add game.\n {err_msg}')

        else:
            QMessageBox.warning(self, 'Error', 'Empty Fields')
    def reset_data(self):
        for widget in self.findChildren(QLineEdit):
            if isinstance(widget, QLineEdit):
                widget.clear()

    def back_clicked(self):
        self.reset_data()
        self.parent().setCurrentIndex(5) 

class RemoveGamePage(QWidget): #7
    def __init__(self, parent):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        back_button = QPushButton("Back", self)
        back_button.clicked.connect(self.back_clicked)

        remove_button = QPushButton("Remove Game", self)
        remove_button.clicked.connect(self.remove_game)

        self.dropdown = QComboBox(self)
        layout.addWidget(self.dropdown)
        for game in get_games_name(self.parent().crs):
            self.dropdown.addItem(game)
        layout.addWidget(remove_button)
        layout.addWidget(back_button)
    
    def update_game_list(self):
        self.dropdown.clear()
        for game in get_games_name(self.parent().crs):
            self.dropdown.addItem(game)

    def back_clicked(self):
        self.update_game_list()
        self.parent().setCurrentIndex(5)

    def remove_game(self):
        selected_index = self.dropdown.currentIndex()
        if selected_index != -1:
            game_name = self.dropdown.itemText(selected_index)
            print(game_name)
            delete_game(self.parent().crs, game_name)
            self.parent().conn.commit()
            self.dropdown.removeItem(selected_index)
        else:
            QMessageBox.warning(self, 'Error', f'No more games.\n')

class UpdateGamePage(QWidget): #8
    def __init__(self, parent):
        super().__init__(parent)

        self.layout = QVBoxLayout()

        self.tableWidget = QTableWidget(self)
        self.populate_table()

        self.backButton = QPushButton("Back", self)
        self.backButton.clicked.connect(self.back_clicked)

        self.updateButton = QPushButton("Update", self)
        self.updateButton.clicked.connect(self.update_data)

        self.layout.addWidget(self.tableWidget)
        self.layout.addWidget(self.updateButton)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.backButton)
        button_layout.addStretch()  
        button_layout.addWidget(self.updateButton)

        self.layout.addLayout(button_layout)

        self.setLayout(self.layout)

    def back_clicked(self):
        self.parent().setCurrentIndex(5)

    def update_game_list(self):
        self.tableWidget.clearContents()
        self.populate_table()

    def populate_table(self):
        data = get_games_data(self.parent().crs)
        self.gid = []
        self.data = []
        for g in data:
            self.gid.append(g[0])
        for temp in data:
            self.data.append(temp[1:])
        
        self.tableWidget.setRowCount(len(self.data))
        self.tableWidget.setColumnCount(len(self.data[0]))

        column_names = ["Game", "Price", "Stock", "Release Date", "Description", "Publisher"]
        self.tableWidget.setHorizontalHeaderLabels(column_names)

        for row in range(len(self.data)):
            for col in range(len(self.data[0])):
                item = QTableWidgetItem(str(self.data[row][col]))
                self.tableWidget.setItem(row, col, item)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

    def update_data(self):
        updated_data = []
        for row in range(self.tableWidget.rowCount()):
            row_data = []
            for col in range(self.tableWidget.columnCount()):
                item = self.tableWidget.item(row, col)
                if item is not None:
                    row_data.append(item.text())
                else:
                    row_data.append("")  
            updated_data.append(row_data)

        print("Updated Data:")
        for index, row in enumerate(updated_data):
            updated_data[index].append(self.gid[index])
            success, err_msg = update_games_data(self.parent().crs, updated_data[index])
            if success:
                    self.parent().conn.commit()
            else:
                    QMessageBox.warning(self, 'Error', f'Failed to update table.\n {err_msg}')
        self.parent().conn.commit()

class MainWindow(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.CID = -1

        self.setGeometry(100, 100, 1600, 800)
        self.conn = connect()
        self.crs = self.conn.cursor()

        self.first_page = FirstPage(self)
        self.admlog_page = AdmLogPage(self)

        self.user_page = UserPage(self)
        self.register_page = RegisterPage(self)

        self.shop_page = ShopPage(self)
        self.shop_page.setObjectName("shop_page")

        self.man_page = ManPage(self)

        self.add_game_page = AddGamePage(self)
        self.remove_game_page = RemoveGamePage(self)
        self.remove_game_page.setObjectName("remove_game_page")
        self.update_game_page = UpdateGamePage(self)
        self.update_game_page.setObjectName("update_game_page")

        self.addWidget(self.first_page)
        self.addWidget(self.admlog_page)
        self.addWidget(self.user_page)
        self.addWidget(self.register_page)

        self.addWidget(self.shop_page)
        self.addWidget(self.man_page)

        self.addWidget(self.add_game_page)
        self.addWidget(self.remove_game_page)
        self.addWidget(self.update_game_page)

        self.setCurrentIndex(0)  

    def goBack(self):
        self.setCurrentIndex(0)  


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())