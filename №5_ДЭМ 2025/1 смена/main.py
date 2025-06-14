import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QScrollArea, QFrame, QPushButton, QGridLayout, QSizePolicy, QMessageBox,
    QLineEdit, QComboBox, QDialog, QDialogButtonBox, QFormLayout, QDoubleSpinBox,
    QStackedWidget, QSpinBox, QGraphicsDropShadowEffect
)
from PySide6.QtGui import (
    QFont, QPixmap, QIcon, QColor, QPalette, QLinearGradient, QBrush, QPainter
)
from PySide6.QtCore import Qt, QPoint


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Система управления - Главная")
        self.setWindowIcon(QIcon("logo.ico"))
        self.setMinimumSize(1200, 800)

        # Установка цветовой схемы
        self.setup_colors()

        # Подключение к базе данных
        self.db_connection = self.connect_to_db()

        # Создаем стек виджетов для навигации
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Создаем страницы приложения
        self.main_page = MainPage(self)
        self.products_page = ProductsPage(self)
        self.materials_page = MaterialsPage(self)

        # Добавляем страницы в стек
        self.stacked_widget.addWidget(self.main_page)
        self.stacked_widget.addWidget(self.products_page)
        self.stacked_widget.addWidget(self.materials_page)

        # Показываем главную страницу
        self.show_main_page()

    def setup_colors(self):
        """Настройка цветовой схемы приложения"""
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#FFFFFF"))
        palette.setColor(QPalette.WindowText, QColor("#000000"))
        palette.setColor(QPalette.Base, QColor("#FFFFFF"))
        palette.setColor(QPalette.AlternateBase, QColor("#E8F4E5"))
        palette.setColor(QPalette.Button, QColor("#2D6033"))
        palette.setColor(QPalette.ButtonText, QColor("#FFFFFF"))
        palette.setColor(QPalette.Highlight, QColor("#3E8043"))
        self.setPalette(palette)

    def connect_to_db(self):
        """Установка соединения с PostgreSQL"""
        try:
            import psycopg2
            conn = psycopg2.connect(
                dbname="demvar",
                user="postgres",
                password="toor",
                host="localhost",
                port="5432"
            )
            return conn
        except Exception as e:
            self.show_error_message(
                "Ошибка подключения к базе данных",
                f"Не удалось подключиться к базе данных: {str(e)}"
            )
            return None

    # Методы навигации
    def show_main_page(self):
        self.setWindowTitle("Система управления - Главная")
        self.stacked_widget.setCurrentWidget(self.main_page)

    def show_products_page(self):
        self.setWindowTitle("Система управления - Продукция")
        self.products_page.load_products()
        self.stacked_widget.setCurrentWidget(self.products_page)

    def show_materials_page(self):
        self.setWindowTitle("Система управления - Материалы")
        self.materials_page.load_materials()
        self.stacked_widget.setCurrentWidget(self.materials_page)

    def show_error_message(self, title, message):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #FFFFFF;
                font-family: Gabriola;
                font-size: 14px;
            }
            QMessageBox QLabel {
                color: #333333;
            }
        """)
        msg.exec()

    def show_warning_message(self, title, message):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #FFFFFF;
                font-family: Gabriola;
                font-size: 14px;
            }
            QMessageBox QLabel {
                color: #333333;
            }
        """)
        msg.exec()

    def show_info_message(self, title, message):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #FFFFFF;
                font-family: Gabriola;
                font-size: 14px;
            }
            QMessageBox QLabel {
                color: #333333;
            }
        """)
        msg.exec()

    def closeEvent(self, event):
        if self.db_connection:
            self.db_connection.close()
        event.accept()


class MainPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):
        # Градиентный фон
        self.setAutoFillBackground(True)
        palette = self.palette()
        gradient = QLinearGradient(QPoint(0, 0), QPoint(0, self.height()))
        gradient.setColorAt(0, QColor("#FFFFFF"))
        gradient.setColorAt(1, QColor("#E8F4E5"))
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)

        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(30)

        # Заголовок с логотипом
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 180);
                border-radius: 15px;
            }
        """)
        header_frame.setGraphicsEffect(self.create_shadow())

        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(20, 20, 20, 20)

        # Логотип с рамкой
        logo_container = QFrame()
        logo_container.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                border: 2px solid #2D6033;
            }
        """)
        logo_layout = QHBoxLayout()
        logo_layout.setContentsMargins(10, 10, 10, 10)
        logo_label = QLabel()
        logo_pixmap = QPixmap("logo.png").scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(logo_pixmap)
        logo_layout.addWidget(logo_label)
        logo_container.setLayout(logo_layout)

        header_layout.addWidget(logo_container)
        header_layout.addSpacing(30)

        title_label = QLabel("Главное меню")
        title_label.setFont(QFont("Gabriola", 36, QFont.Bold))
        title_label.setStyleSheet("color: #2D6033;")
        header_layout.addWidget(title_label)
        header_layout.addStretch()

        header_frame.setLayout(header_layout)
        layout.addWidget(header_frame)

        # Кнопки навигации
        buttons_frame = QFrame()
        buttons_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 180);
                border-radius: 15px;
            }
        """)
        buttons_frame.setGraphicsEffect(self.create_shadow())

        buttons_layout = QVBoxLayout()
        buttons_layout.setContentsMargins(30, 30, 30, 30)
        buttons_layout.setSpacing(20)

        products_btn = QPushButton("Управление продукцией")
        products_btn.setFont(QFont("Gabriola", 18))
        products_btn.setStyleSheet(self.get_button_style())
        products_btn.clicked.connect(self.main_window.show_products_page)

        materials_btn = QPushButton("Управление материалами")
        materials_btn.setFont(QFont("Gabriola", 18))
        materials_btn.setStyleSheet(self.get_button_style())
        materials_btn.clicked.connect(self.main_window.show_materials_page)

        buttons_layout.addWidget(products_btn)
        buttons_layout.addWidget(materials_btn)
        buttons_layout.addStretch()

        buttons_frame.setLayout(buttons_layout)
        layout.addWidget(buttons_frame, 1)

    def create_shadow(self):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(5, 5)
        return shadow

    def get_button_style(self):
        return """
            QPushButton {
                background-color: #2D6033;
                color: white;
                border: none;
                padding: 15px 30px;
                border-radius: 8px;
                min-width: 250px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3E8043;
            }
            QPushButton:pressed {
                background-color: #1D4023;
            }
        """


class ProductsPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):
        # Градиентный фон
        self.setAutoFillBackground(True)
        palette = self.palette()
        gradient = QLinearGradient(QPoint(0, 0), QPoint(0, self.height()))
        gradient.setColorAt(0, QColor("#FFFFFF"))
        gradient.setColorAt(1, QColor("#E8F4E5"))
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)

        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(25)

        # Заголовок с кнопкой "Назад"
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 180);
                border-radius: 15px;
            }
        """)
        header_frame.setGraphicsEffect(self.create_shadow())

        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(20, 15, 20, 15)

        back_btn = QPushButton("Назад")
        back_btn.setFont(QFont("Gabriola", 14))
        back_btn.setStyleSheet(self.get_button_style())
        back_btn.clicked.connect(self.main_window.show_main_page)
        header_layout.addWidget(back_btn)

        title_label = QLabel("Управление продукцией")
        title_label.setFont(QFont("Gabriola", 28, QFont.Bold))
        title_label.setStyleSheet("color: #2D6033;")
        header_layout.addWidget(title_label)
        header_layout.addStretch()

        header_frame.setLayout(header_layout)
        layout.addWidget(header_frame)

        # Область с продукцией (скроллинг)
        scroll_container = QFrame()
        scroll_container.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 180);
                border-radius: 15px;
            }
        """)
        scroll_container.setGraphicsEffect(self.create_shadow())

        scroll_layout = QVBoxLayout()
        scroll_layout.setContentsMargins(15, 15, 15, 15)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.NoFrame)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                width: 14px;
                background: rgba(187, 217, 178, 50);
                border-radius: 7px;
                margin: 5px 0px 5px 0px;
            }
            QScrollBar::handle:vertical {
                background: #2D6033;
                min-height: 30px;
                border-radius: 7px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)

        self.scroll_widget = QWidget()
        self.scroll_content_layout = QVBoxLayout()
        self.scroll_content_layout.setContentsMargins(5, 5, 15, 5)
        self.scroll_content_layout.setSpacing(25)
        self.scroll_widget.setLayout(self.scroll_content_layout)
        self.scroll_area.setWidget(self.scroll_widget)

        scroll_layout.addWidget(self.scroll_area)
        scroll_container.setLayout(scroll_layout)
        layout.addWidget(scroll_container, 1)

        # Кнопки управления
        buttons_frame = QFrame()
        buttons_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 180);
                border-radius: 15px;
            }
        """)
        buttons_frame.setGraphicsEffect(self.create_shadow())

        buttons_layout = QHBoxLayout()
        buttons_layout.setContentsMargins(20, 15, 20, 15)

        self.add_button = QPushButton("Добавить продукт")
        self.add_button.setFont(QFont("Gabriola", 14))
        self.add_button.setStyleSheet(self.get_button_style())
        self.add_button.clicked.connect(self.show_add_product_dialog)

        self.refresh_button = QPushButton("Обновить")
        self.refresh_button.setFont(QFont("Gabriola", 14))
        self.refresh_button.setStyleSheet(self.get_button_style())
        self.refresh_button.clicked.connect(self.load_products)

        self.calculate_button = QPushButton("Пересчитать стоимость")
        self.calculate_button.setFont(QFont("Gabriola", 14))
        self.calculate_button.setStyleSheet(self.get_button_style())
        self.calculate_button.clicked.connect(self.recalculate_all_prices)

        buttons_layout.addWidget(self.add_button)
        buttons_layout.addWidget(self.refresh_button)
        buttons_layout.addWidget(self.calculate_button)
        buttons_layout.addStretch()

        buttons_frame.setLayout(buttons_layout)
        layout.addWidget(buttons_frame)

    def create_shadow(self):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(5, 5)
        return shadow

    def load_products(self):
        """Загрузка списка продукции из базы данных"""
        if not self.main_window.db_connection:
            return

        # Очищаем предыдущие данные
        for i in reversed(range(self.scroll_content_layout.count())):
            widget = self.scroll_content_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        try:
            cursor = self.main_window.db_connection.cursor()

            # Получаем данные о продукции
            query = """SELECT 
                    p.id_product,
                    tp.type_product,
                    p.product_name,
                    p.min_cost,
                    p.acrticul,
                    p.width
                FROM products p
                JOIN type_product tp ON p.id_type_product = tp.id_type_product
                ORDER BY p.product_name"""

            cursor.execute(query)
            products = cursor.fetchall()

            if not products:
                self.main_window.show_info_message("Информация", "В базе данных нет продукции.")
                return

            for product in products:
                self.add_product_card(*product)

        except Exception as e:
            self.main_window.show_error_message(
                "Ошибка загрузки продукции",
                f"Произошла ошибка при загрузке продукции: {str(e)}"
            )
        finally:
            if 'cursor' in locals():
                cursor.close()

    def add_product_card(self, product_id, product_type, product_name, min_cost, acrticul, width):
        """Добавляет карточку продукта в интерфейс"""
        card = QFrame()
        card.setFrameShape(QFrame.StyledPanel)
        card.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 200);
                border-radius: 12px;
                padding: 5px;
                border: 1px solid #BBD9B2;
            }
        """)
        card.setGraphicsEffect(self.create_shadow())
        card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Основной макет карточки
        main_card_layout = QVBoxLayout()
        main_card_layout.setContentsMargins(15, 15, 15, 15)
        main_card_layout.setSpacing(10)

        # Верхняя часть карточки (заголовок)
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background-color: #2D6033;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(5, 0, 5, 0)

        type_label = QLabel(product_type)
        type_label.setFont(QFont("Gabriola", 14, QFont.Bold))
        type_label.setStyleSheet("color: white;")

        name_label = QLabel(product_name)
        name_label.setFont(QFont("Gabriola", 18, QFont.Bold))
        name_label.setStyleSheet("color: white;")

        cost_label = QLabel(f"{min_cost:.2f} ₽")
        cost_label.setFont(QFont("Gabriola", 16, QFont.Bold))
        cost_label.setStyleSheet("color: white;")

        header_layout.addWidget(type_label)
        header_layout.addWidget(name_label)
        header_layout.addStretch()
        header_layout.addWidget(cost_label)
        header_frame.setLayout(header_layout)
        main_card_layout.addWidget(header_frame)

        # Детали продукта
        details_frame = QFrame()
        details_layout = QGridLayout()
        details_layout.setContentsMargins(5, 5, 5, 5)
        details_layout.setVerticalSpacing(8)
        details_layout.setHorizontalSpacing(15)

        # Артикул
        articul_title = QLabel("Артикул:")
        articul_title.setFont(QFont("Gabriola", 12))
        articul_title.setStyleSheet("color: #555555; font-weight: bold;")

        articul_value = QLabel(acrticul)
        articul_value.setFont(QFont("Gabriola", 12))
        articul_value.setStyleSheet("color: #333333;")

        # Ширина
        width_title = QLabel("Ширина:")
        width_title.setFont(QFont("Gabriola", 12))
        width_title.setStyleSheet("color: #555555; font-weight: bold;")

        width_value = QLabel(f"{width} м")
        width_value.setFont(QFont("Gabriola", 12))
        width_value.setStyleSheet("color: #333333;")

        # Стоимость
        cost_title = QLabel("Мин. стоимость:")
        cost_title.setFont(QFont("Gabriola", 12))
        cost_title.setStyleSheet("color: #555555; font-weight: bold;")

        cost_value = QLabel(f"{min_cost:.2f} ₽")
        cost_value.setFont(QFont("Gabriola", 12))
        cost_value.setStyleSheet("color: #333333;")

        # Размещаем элементы в сетке
        details_layout.addWidget(articul_title, 0, 0)
        details_layout.addWidget(articul_value, 0, 1)
        details_layout.addWidget(width_title, 1, 0)
        details_layout.addWidget(width_value, 1, 1)
        details_layout.addWidget(cost_title, 2, 0)
        details_layout.addWidget(cost_value, 2, 1)

        details_frame.setLayout(details_layout)
        main_card_layout.addWidget(details_frame)

        # Кнопка редактирования
        edit_button = QPushButton("Редактировать")
        edit_button.setFont(QFont("Gabriola", 12))
        edit_button.setStyleSheet(self.get_button_style())
        edit_button.clicked.connect(lambda: self.show_edit_product_dialog(product_id))
        main_card_layout.addWidget(edit_button, alignment=Qt.AlignRight)

        card.setLayout(main_card_layout)
        self.scroll_content_layout.addWidget(card)

    def show_add_product_dialog(self):
        """Показывает диалог добавления нового продукта"""
        dialog = ProductDialog(self.main_window, self.main_window.db_connection)
        if dialog.exec() == QDialog.Accepted:
            self.load_products()
            self.main_window.show_info_message("Успех", "Продукт успешно добавлен.")

    def show_edit_product_dialog(self, product_id):
        """Показывает диалог редактирования продукта"""
        dialog = ProductDialog(self.main_window, self.main_window.db_connection, product_id)
        if dialog.exec() == QDialog.Accepted:
            self.load_products()
            self.main_window.show_info_message("Успех", "Продукт успешно обновлен.")

    def recalculate_all_prices(self):
        """Пересчет стоимости для всей продукции"""
        if not self.main_window.db_connection:
            return

        reply = QMessageBox.question(
            self, 'Подтверждение',
            'Вы уверены, что хотите пересчитать стоимость для всей продукции?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )

        if reply != QMessageBox.Yes:
            return

        try:
            cursor = self.main_window.db_connection.cursor()

            # Получаем список всех продуктов
            cursor.execute("SELECT id_product FROM products")
            product_ids = [row[0] for row in cursor.fetchall()]

            if not product_ids:
                self.main_window.show_info_message("Информация", "Нет продукции для пересчета.")
                return

            # Пересчитываем стоимость для каждого продукта
            updated_count = 0
            for product_id in product_ids:
                new_price = self.calculate_product_cost(product_id)

                if new_price is not None:
                    # Обновляем стоимость в базе данных
                    update_query = """UPDATE products 
                                    SET min_cost = %s 
                                    WHERE id_product = %s"""
                    cursor.execute(update_query, (new_price, product_id))
                    updated_count += 1

            self.main_window.db_connection.commit()
            self.load_products()

            self.main_window.show_info_message(
                "Пересчет завершен",
                f"Стоимость пересчитана для {updated_count} продуктов."
            )

        except Exception as e:
            self.main_window.db_connection.rollback()
            self.main_window.show_error_message(
                "Ошибка пересчета стоимости",
                f"Произошла ошибка при пересчете стоимости: {str(e)}"
            )
        finally:
            if 'cursor' in locals():
                cursor.close()

    def calculate_product_cost(self, product_id):
        """Рассчитывает стоимость продукта на основе типа продукта и его ширины"""
        if not self.main_window.db_connection:
            return None

        try:
            cursor = self.main_window.db_connection.cursor()

            # Получаем данные о продукте: ширину и коэффициент типа продукта
            cursor.execute("""
                SELECT p.width, tp.coefficient_type_product 
                FROM products p
                JOIN type_product tp ON p.id_type_product = tp.id_type_product
                WHERE p.id_product = %s
            """, (product_id,))

            product_data = cursor.fetchone()

            if not product_data:
                self.main_window.show_warning_message(
                    "Предупреждение",
                    f"Для продукта ID {product_id} не найдены данные. Стоимость не будет пересчитана."
                )
                return None

            width, coefficient = product_data

            # Базовая стоимость за метр ширины (можно настроить)
            BASE_COST_PER_METER = 100.0

            # Рассчитываем стоимость: ширина * базовая стоимость * коэффициент типа
            total_cost = width * BASE_COST_PER_METER * coefficient

            # Округляем до 2 знаков после запятой
            return round(total_cost, 2)

        except Exception as e:
            self.main_window.show_error_message(
                "Ошибка расчета стоимости",
                f"Не удалось рассчитать стоимость для продукта ID {product_id}: {str(e)}"
            )
            return None
        finally:
            if 'cursor' in locals():
                cursor.close()

    def get_button_style(self):
        return """
            QPushButton {
                background-color: #2D6033;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
                min-width: 180px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3E8043;
            }
            QPushButton:pressed {
                background-color: #1D4023;
            }
        """


class MaterialsPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):
        # Градиентный фон
        self.setAutoFillBackground(True)
        palette = self.palette()
        gradient = QLinearGradient(QPoint(0, 0), QPoint(0, self.height()))
        gradient.setColorAt(0, QColor("#FFFFFF"))
        gradient.setColorAt(1, QColor("#E8F4E5"))
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)

        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(25)

        # Заголовок с кнопкой "Назад"
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 180);
                border-radius: 15px;
            }
        """)
        header_frame.setGraphicsEffect(self.create_shadow())

        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(20, 15, 20, 15)

        back_btn = QPushButton("Назад")
        back_btn.setFont(QFont("Gabriola", 14))
        back_btn.setStyleSheet(self.get_button_style())
        back_btn.clicked.connect(self.main_window.show_main_page)
        header_layout.addWidget(back_btn)

        title_label = QLabel("Управление материалами")
        title_label.setFont(QFont("Gabriola", 28, QFont.Bold))
        title_label.setStyleSheet("color: #2D6033;")
        header_layout.addWidget(title_label)
        header_layout.addStretch()

        header_frame.setLayout(header_layout)
        layout.addWidget(header_frame)

        # Область с материалами (скроллинг)
        scroll_container = QFrame()
        scroll_container.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 180);
                border-radius: 15px;
            }
        """)
        scroll_container.setGraphicsEffect(self.create_shadow())

        scroll_layout = QVBoxLayout()
        scroll_layout.setContentsMargins(15, 15, 15, 15)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.NoFrame)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                width: 14px;
                background: rgba(187, 217, 178, 50);
                border-radius: 7px;
                margin: 5px 0px 5px 0px;
            }
            QScrollBar::handle:vertical {
                background: #2D6033;
                min-height: 30px;
                border-radius: 7px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)

        self.scroll_widget = QWidget()
        self.scroll_content_layout = QVBoxLayout()
        self.scroll_content_layout.setContentsMargins(5, 5, 15, 5)
        self.scroll_content_layout.setSpacing(25)
        self.scroll_widget.setLayout(self.scroll_content_layout)
        self.scroll_area.setWidget(self.scroll_widget)

        scroll_layout.addWidget(self.scroll_area)
        scroll_container.setLayout(scroll_layout)
        layout.addWidget(scroll_container, 1)

        # Кнопки управления
        buttons_frame = QFrame()
        buttons_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 180);
                border-radius: 15px;
            }
        """)
        buttons_frame.setGraphicsEffect(self.create_shadow())

        buttons_layout = QHBoxLayout()
        buttons_layout.setContentsMargins(20, 15, 20, 15)

        self.add_button = QPushButton("Добавить материал")
        self.add_button.setFont(QFont("Gabriola", 14))
        self.add_button.setStyleSheet(self.get_button_style())
        self.add_button.clicked.connect(self.show_add_material_dialog)

        self.refresh_button = QPushButton("Обновить")
        self.refresh_button.setFont(QFont("Gabriola", 14))
        self.refresh_button.setStyleSheet(self.get_button_style())
        self.refresh_button.clicked.connect(self.load_materials)

        buttons_layout.addWidget(self.add_button)
        buttons_layout.addWidget(self.refresh_button)
        buttons_layout.addStretch()

        buttons_frame.setLayout(buttons_layout)
        layout.addWidget(buttons_frame)

    def create_shadow(self):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(5, 5)
        return shadow

    def load_materials(self):
        """Загрузка списка материалов из базы данных"""
        if not self.main_window.db_connection:
            return

        # Очищаем предыдущие данные
        for i in reversed(range(self.scroll_content_layout.count())):
            widget = self.scroll_content_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        try:
            cursor = self.main_window.db_connection.cursor()

            # Получаем данные о материалах
            query = """SELECT 
                    m.id_material,
                    tm.type_material,
                    m.material_name,
                    m.unit_price,
                    m.stock_quantity,
                    m.min_quantity,
                    m.package_quantity,
                    m.unit
                FROM materials m
                JOIN type_material tm ON m.id_type_material = tm.id_type_material
                ORDER BY m.material_name"""

            cursor.execute(query)
            materials = cursor.fetchall()

            if not materials:
                self.main_window.show_info_message("Информация", "В базе данных нет материалов.")
                return

            for material in materials:
                self.add_material_card(*material)

        except Exception as e:
            self.main_window.show_error_message(
                "Ошибка загрузки материалов",
                f"Произошла ошибка при загрузке материалов: {str(e)}"
            )
        finally:
            if 'cursor' in locals():
                cursor.close()

    def add_material_card(self, material_id, material_type, material_name, unit_price, stock_quantity, min_quantity,
                          package_quantity, unit):
        """Добавляет карточку материала в интерфейс"""
        card = QFrame()
        card.setFrameShape(QFrame.StyledPanel)
        card.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 200);
                border-radius: 12px;
                padding: 5px;
                border: 1px solid #BBD9B2;
            }
        """)
        card.setGraphicsEffect(self.create_shadow())
        card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Основной макет карточки
        main_card_layout = QVBoxLayout()
        main_card_layout.setContentsMargins(15, 15, 15, 15)
        main_card_layout.setSpacing(10)

        # Верхняя часть карточки (заголовок)
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background-color: #2D6033;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(5, 0, 5, 0)

        type_label = QLabel(material_type)
        type_label.setFont(QFont("Gabriola", 14, QFont.Bold))
        type_label.setStyleSheet("color: white;")

        name_label = QLabel(material_name)
        name_label.setFont(QFont("Gabriola", 18, QFont.Bold))
        name_label.setStyleSheet("color: white;")

        price_label = QLabel(f"{unit_price:.2f} ₽/{unit}")
        price_label.setFont(QFont("Gabriola", 16, QFont.Bold))
        price_label.setStyleSheet("color: white;")

        header_layout.addWidget(type_label)
        header_layout.addWidget(name_label)
        header_layout.addStretch()
        header_layout.addWidget(price_label)
        header_frame.setLayout(header_layout)
        main_card_layout.addWidget(header_frame)

        # Детали материала
        details_frame = QFrame()
        details_layout = QGridLayout()
        details_layout.setContentsMargins(5, 5, 5, 5)
        details_layout.setVerticalSpacing(8)
        details_layout.setHorizontalSpacing(15)

        # Количество на складе
        stock_title = QLabel("На складе:")
        stock_title.setFont(QFont("Gabriola", 12))
        stock_title.setStyleSheet("color: #555555; font-weight: bold;")

        stock_value = QLabel(f"{stock_quantity} {unit}")
        stock_value.setFont(QFont("Gabriola", 12))
        stock_value.setStyleSheet("color: #333333;")

        # Минимальное количество
        min_qty_title = QLabel("Мин. заказ:")
        min_qty_title.setFont(QFont("Gabriola", 12))
        min_qty_title.setStyleSheet("color: #555555; font-weight: bold;")

        min_qty_value = QLabel(f"{min_quantity} {unit}")
        min_qty_value.setFont(QFont("Gabriola", 12))
        min_qty_value.setStyleSheet("color: #333333;")

        # Упаковка
        package_title = QLabel("Упаковка:")
        package_title.setFont(QFont("Gabriola", 12))
        package_title.setStyleSheet("color: #555555; font-weight: bold;")

        package_value = QLabel(f"{package_quantity} {unit}")
        package_value.setFont(QFont("Gabriola", 12))
        package_value.setStyleSheet("color: #333333;")

        # Размещаем элементы в сетке
        details_layout.addWidget(stock_title, 0, 0)
        details_layout.addWidget(stock_value, 0, 1)
        details_layout.addWidget(min_qty_title, 1, 0)
        details_layout.addWidget(min_qty_value, 1, 1)
        details_layout.addWidget(package_title, 2, 0)
        details_layout.addWidget(package_value, 2, 1)

        details_frame.setLayout(details_layout)
        main_card_layout.addWidget(details_frame)

        # Кнопка редактирования
        edit_button = QPushButton("Редактировать")
        edit_button.setFont(QFont("Gabriola", 12))
        edit_button.setStyleSheet(self.get_button_style())
        edit_button.clicked.connect(lambda: self.show_edit_material_dialog(material_id))
        main_card_layout.addWidget(edit_button, alignment=Qt.AlignRight)

        card.setLayout(main_card_layout)
        self.scroll_content_layout.addWidget(card)

    def show_add_material_dialog(self):
        """Показывает диалог добавления нового материала"""
        dialog = MaterialDialog(self.main_window, self.main_window.db_connection)
        if dialog.exec() == QDialog.Accepted:
            self.load_materials()
            self.main_window.show_info_message("Успех", "Материал успешно добавлен.")

    def show_edit_material_dialog(self, material_id):
        """Показывает диалог редактирования материала"""
        dialog = MaterialDialog(self.main_window, self.main_window.db_connection, material_id)
        if dialog.exec() == QDialog.Accepted:
            self.load_materials()
            self.main_window.show_info_message("Успех", "Материал успешно обновлен.")

    def get_button_style(self):
        return """
            QPushButton {
                background-color: #2D6033;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
                min-width: 180px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3E8043;
            }
            QPushButton:pressed {
                background-color: #1D4023;
            }
        """


class ProductDialog(QDialog):
    """Диалог для добавления/редактирования продукта"""

    def __init__(self, parent=None, db_connection=None, product_id=None):
        super().__init__(parent)
        self.db_connection = db_connection
        self.product_id = product_id
        self.setModal(True)
        self.setWindowTitle("Редактирование продукта" if product_id else "Добавление продукта")
        self.setMinimumSize(500, 400)

        # Установка стиля для диалога
        self.setStyleSheet("""
            QDialog {
                background-color: #FFFFFF;
                font-family: Gabriola;
                font-size: 14px;
            }
            QLabel {
                color: #2D6033;
            }
            QLineEdit, QComboBox, QDoubleSpinBox {
                border: 1px solid #BBD9B2;
                border-radius: 4px;
                padding: 5px;
            }
        """)

        self.init_ui()
        self.load_data()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Форма с полями
        self.form_layout = QFormLayout()
        self.form_layout.setSpacing(15)
        self.form_layout.setContentsMargins(20, 20, 20, 20)

        # Поле артикула
        self.articul_edit = QLineEdit()
        self.articul_edit.setFont(QFont("Gabriola", 12))
        self.form_layout.addRow("Артикул:", self.articul_edit)

        # Поле типа продукта
        self.type_combo = QComboBox()
        self.type_combo.setFont(QFont("Gabriola", 12))
        self.form_layout.addRow("Тип продукта:", self.type_combo)

        # Поле наименования
        self.name_edit = QLineEdit()
        self.name_edit.setFont(QFont("Gabriola", 12))
        self.form_layout.addRow("Наименование:", self.name_edit)

        # Поле минимальной стоимости
        self.min_cost_spin = QDoubleSpinBox()
        self.min_cost_spin.setFont(QFont("Gabriola", 12))
        self.min_cost_spin.setRange(0, 999999.99)
        self.min_cost_spin.setDecimals(2)
        self.min_cost_spin.setPrefix("₽ ")
        self.form_layout.addRow("Мин. стоимость:", self.min_cost_spin)

        # Поле ширины
        self.width_spin = QDoubleSpinBox()
        self.width_spin.setFont(QFont("Gabriola", 12))
        self.width_spin.setRange(0.01, 10.0)
        self.width_spin.setDecimals(2)
        self.width_spin.setSuffix(" м")
        self.form_layout.addRow("Ширина:", self.width_spin)

        layout.addLayout(self.form_layout)

        # Кнопки
        self.button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        self.button_box.setStyleSheet("""
            QDialogButtonBox {
                button-layout: 1;
            }
            QPushButton {
                min-width: 80px;
                padding: 5px 10px;
            }
        """)
        self.button_box.accepted.connect(self.validate_and_accept)
        self.button_box.rejected.connect(self.reject)

        layout.addWidget(self.button_box)

    def load_data(self):
        """Загрузка данных в форму"""
        if not self.db_connection:
            return

        try:
            cursor = self.db_connection.cursor()

            # Загружаем типы продуктов
            cursor.execute("SELECT id_type_product, type_product FROM type_product ORDER BY type_product")
            types = cursor.fetchall()

            self.type_combo.clear()
            for type_id, type_name in types:
                self.type_combo.addItem(type_name, type_id)

            # Если это редактирование, загружаем данные продукта
            if self.product_id:
                cursor.execute("""
                    SELECT acrticul, id_type_product, product_name, min_cost, width 
                    FROM products 
                    WHERE id_product = %s
                """, (self.product_id,))

                product_data = cursor.fetchone()
                if product_data:
                    self.articul_edit.setText(product_data[0])
                    self.name_edit.setText(product_data[2])
                    self.min_cost_spin.setValue(float(product_data[3]))
                    self.width_spin.setValue(float(product_data[4]))

                    # Устанавливаем правильный тип продукта
                    type_index = self.type_combo.findData(product_data[1])
                    if type_index >= 0:
                        self.type_combo.setCurrentIndex(type_index)

        except Exception as e:
            self.parent().show_error_message(
                "Ошибка загрузки данных",
                f"Не удалось загрузить данные: {str(e)}"
            )
            self.reject()
        finally:
            if 'cursor' in locals():
                cursor.close()

    def validate_and_accept(self):
        """Проверка данных и сохранение"""
        try:
            articul = self.articul_edit.text().strip()
            product_name = self.name_edit.text().strip()
            min_cost = self.min_cost_spin.value()
            width = self.width_spin.value()
            type_id = self.type_combo.currentData()

            # Проверка обязательных полей
            if not articul:
                raise ValueError("Артикул не может быть пустым")
            if not product_name:
                raise ValueError("Наименование не может быть пустым")
            if type_id is None:
                raise ValueError("Не выбран тип продукта")
            if min_cost <= 0:
                raise ValueError("Стоимость должна быть положительной")
            if width <= 0:
                raise ValueError("Ширина должна быть положительной")

            # Сохранение данных
            if self.save_product(articul, type_id, product_name, min_cost, width):
                self.accept()

        except ValueError as e:
            self.parent().show_warning_message("Проверка данных", str(e))
        except Exception as e:
            self.parent().show_error_message(
                "Ошибка сохранения",
                f"Не удалось сохранить продукт: {str(e)}"
            )

    def save_product(self, articul, type_id, product_name, min_cost, width):
        """Сохранение продукта в базу данных"""
        if not self.db_connection:
            return False

        try:
            cursor = self.db_connection.cursor()

            if self.product_id:
                # Обновление существующего продукта
                query = """
                    UPDATE products 
                    SET acrticul = %s, 
                        id_type_product = %s, 
                        product_name = %s, 
                        min_cost = %s, 
                        width = %s
                    WHERE id_product = %s
                """
                cursor.execute(query, (articul, type_id, product_name, min_cost, width, self.product_id))
            else:
                # Добавление нового продукта
                query = """
                    INSERT INTO products 
                    (acrticul, id_type_product, product_name, min_cost, width)
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(query, (articul, type_id, product_name, min_cost, width))

            self.db_connection.commit()
            return True

        except Exception as e:
            self.db_connection.rollback()
            raise e
        finally:
            if 'cursor' in locals():
                cursor.close()


class MaterialDialog(QDialog):
    """Диалог для добавления/редактирования материала"""

    def __init__(self, parent=None, db_connection=None, material_id=None):
        super().__init__(parent)
        self.db_connection = db_connection
        self.material_id = material_id
        self.setModal(True)
        self.setWindowTitle("Редактирование материала" if material_id else "Добавление материала")
        self.setMinimumSize(500, 500)

        # Установка стиля для диалога
        self.setStyleSheet("""
            QDialog {
                background-color: #FFFFFF;
                font-family: Gabriola;
                font-size: 14px;
            }
            QLabel {
                color: #2D6033;
            }
            QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox {
                border: 1px solid #BBD9B2;
                border-radius: 4px;
                padding: 5px;
            }
        """)

        self.init_ui()
        self.load_data()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Форма с полями
        self.form_layout = QFormLayout()
        self.form_layout.setSpacing(15)
        self.form_layout.setContentsMargins(20, 20, 20, 20)

        # Поле наименования
        self.name_edit = QLineEdit()
        self.name_edit.setFont(QFont("Gabriola", 12))
        self.form_layout.addRow("Наименование:", self.name_edit)

        # Поле типа материала
        self.type_combo = QComboBox()
        self.type_combo.setFont(QFont("Gabriola", 12))
        self.form_layout.addRow("Тип материала:", self.type_combo)

        # Поле цены за единицу
        self.price_spin = QDoubleSpinBox()
        self.price_spin.setFont(QFont("Gabriola", 12))
        self.price_spin.setRange(0, 999999.99)
        self.price_spin.setDecimals(2)
        self.price_spin.setPrefix("₽ ")
        self.form_layout.addRow("Цена за единицу:", self.price_spin)

        # Поле количества на складе
        self.stock_spin = QSpinBox()
        self.stock_spin.setFont(QFont("Gabriola", 12))
        self.stock_spin.setRange(0, 999999)
        self.form_layout.addRow("Количество на складе:", self.stock_spin)

        # Поле минимального количества
        self.min_qty_spin = QSpinBox()
        self.min_qty_spin.setFont(QFont("Gabriola", 12))
        self.min_qty_spin.setRange(0, 999999)
        self.form_layout.addRow("Минимальное количество:", self.min_qty_spin)

        # Поле количества в упаковке
        self.package_spin = QSpinBox()
        self.package_spin.setFont(QFont("Gabriola", 12))
        self.package_spin.setRange(0, 999999)
        self.form_layout.addRow("Количество в упаковке:", self.package_spin)

        # Поле единицы измерения
        self.unit_combo = QComboBox()
        self.unit_combo.setFont(QFont("Gabriola", 12))
        self.unit_combo.addItems(["шт", "м", "кг", "л", "упак"])
        self.form_layout.addRow("Единица измерения:", self.unit_combo)

        layout.addLayout(self.form_layout)

        # Кнопки
        self.button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        self.button_box.setStyleSheet("""
            QDialogButtonBox {
                button-layout: 1;
            }
            QPushButton {
                min-width: 80px;
                padding: 5px 10px;
            }
        """)
        self.button_box.accepted.connect(self.validate_and_accept)
        self.button_box.rejected.connect(self.reject)

        layout.addWidget(self.button_box)

    def load_data(self):
        """Загрузка данных в форму"""
        if not self.db_connection:
            return

        try:
            cursor = self.db_connection.cursor()

            # Загружаем типы материалов
            cursor.execute("SELECT id_type_material, type_material FROM type_material ORDER BY type_material")
            types = cursor.fetchall()

            self.type_combo.clear()
            for type_id, type_name in types:
                self.type_combo.addItem(type_name, type_id)

            # Если это редактирование, загружаем данные материала
            if self.material_id:
                cursor.execute("""
                    SELECT material_name, id_type_material, unit_price, 
                           stock_quantity, min_quantity, package_quantity, unit 
                    FROM materials 
                    WHERE id_material = %s
                """, (self.material_id,))

                material_data = cursor.fetchone()
                if material_data:
                    self.name_edit.setText(material_data[0])
                    self.price_spin.setValue(float(material_data[2]))
                    self.stock_spin.setValue(material_data[3])
                    self.min_qty_spin.setValue(material_data[4])
                    self.package_spin.setValue(material_data[5])

                    # Устанавливаем правильный тип материала
                    type_index = self.type_combo.findData(material_data[1])
                    if type_index >= 0:
                        self.type_combo.setCurrentIndex(type_index)

                    # Устанавливаем правильную единицу измерения
                    unit_index = self.unit_combo.findText(material_data[6])
                    if unit_index >= 0:
                        self.unit_combo.setCurrentIndex(unit_index)

        except Exception as e:
            self.parent().show_error_message(
                "Ошибка загрузки данных",
                f"Не удалось загрузить данные: {str(e)}"
            )
            self.reject()
        finally:
            if 'cursor' in locals():
                cursor.close()

    def validate_and_accept(self):
        """Проверка данных и сохранение"""
        try:
            material_name = self.name_edit.text().strip()
            unit_price = self.price_spin.value()
            stock_quantity = self.stock_spin.value()
            min_quantity = self.min_qty_spin.value()
            package_quantity = self.package_spin.value()
            unit = self.unit_combo.currentText()
            type_id = self.type_combo.currentData()

            # Проверка обязательных полей
            if not material_name:
                raise ValueError("Наименование не может быть пустым")
            if type_id is None:
                raise ValueError("Не выбран тип материала")
            if unit_price <= 0:
                raise ValueError("Цена должна быть положительной")
            if min_quantity <= 0:
                raise ValueError("Минимальное количество должно быть положительным")
            if package_quantity <= 0:
                raise ValueError("Количество в упаковке должно быть положительным")

            # Сохранение данных
            if self.save_material(material_name, type_id, unit_price, stock_quantity, min_quantity, package_quantity,
                                  unit):
                self.accept()

        except ValueError as e:
            self.parent().show_warning_message("Проверка данных", str(e))
        except Exception as e:
            self.parent().show_error_message(
                "Ошибка сохранения",
                f"Не удалось сохранить материал: {str(e)}"
            )

    def save_material(self, material_name, type_id, unit_price, stock_quantity, min_quantity, package_quantity, unit):
        """Сохранение материала в базу данных"""
        if not self.db_connection:
            return False

        try:
            cursor = self.db_connection.cursor()

            if self.material_id:
                # Обновление существующего материала
                query = """
                    UPDATE materials 
                    SET material_name = %s, 
                        id_type_material = %s, 
                        unit_price = %s, 
                        stock_quantity = %s, 
                        min_quantity = %s, 
                        package_quantity = %s, 
                        unit = %s
                    WHERE id_material = %s
                """
                cursor.execute(query, (
                material_name, type_id, unit_price, stock_quantity, min_quantity, package_quantity, unit,
                self.material_id))
            else:
                # Добавление нового материала
                query = """
                    INSERT INTO materials 
                    (material_name, id_type_material, unit_price, 
                     stock_quantity, min_quantity, package_quantity, unit)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (
                material_name, type_id, unit_price, stock_quantity, min_quantity, package_quantity, unit))

            self.db_connection.commit()
            return True

        except Exception as e:
            self.db_connection.rollback()
            raise e
        finally:
            if 'cursor' in locals():
                cursor.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Gabriola", 12))

    window = MainWindow()
    window.show()

    sys.exit(app.exec())