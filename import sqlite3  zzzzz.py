import sqlite3

class Coffee:
    def __init__(self, name, menu):
        self.name = name
        self.menu = menu
        self.orders = []

    def order(self, item):
        if item in self.menu:
            self.orders.append(item)
        else:
            raise ValueError("Извините, этого напитка нет в меню.")

    def calculate_total(self):
        total = sum(self.menu[item] for item in self.orders)
        return total

    def register_customer(self, name, role):
        if role.lower() == 'клиент' or role.lower() == 'администратор':
            try:
                conn = sqlite3.connect('coffee22.db')
                c = conn.cursor()
                c.execute('''
                    CREATE TABLE IF NOT EXISTS customers_admin (
                        name text, 
                        role text
                    )
                ''')
                c.execute("INSERT INTO customers_admin VALUES (?, ?)", (name, role))
                conn.commit()
                conn.close()
                return f"Здравствуйте, {name}! Вы успешно зарегистрированы как {role}."
            except Exception as e:
                return f"Ошибка при регистрации: {e}"
        else:
            return "Роль должна быть клиентом или администратором."
        
    def remove_from_db(self, table_name, data_id):
        conn = sqlite3.connect('coffee22.db')
        c = conn.cursor()
        try:
            c.execute(f"DELETE FROM {table_name} WHERE ID = ?", (data_id,))
            conn.commit()
            print("Данные удалены")
        except sqlite3.Error as e:
            print(f"Ошибка при удалении данных из базы данных: {e}")
        finally:
            conn.close()

    def add_to_db(self, table_name, data):
        conn = sqlite3.connect('coffee22.db')
        c = conn.cursor()
        try:
            if table_name == 'orders':
                c.execute('''
                    CREATE TABLE IF NOT EXISTS orders (
                        product text, 
                        price real
                    )
                ''')
                c.executemany("INSERT INTO orders VALUES (?, ?)", [data]) 
            elif table_name == 'menu(подарок для покупателя!)':
                c.execute('''
                    CREATE TABLE IF NOT EXISTS menu (
                        item text, 
                        price real
                    )
                ''')
                c.executemany("INSERT INTO menu VALUES (?, ?)", (data, "подарок"))
            elif table_name == 'customers':
                c.execute('''
                    CREATE TABLE IF NOT EXISTS customers (
                        name text, 
                        role text
                    )
                ''')
                c.execute("INSERT INTO customers VALUES (?, ?)", (data, "Клиент"))
            elif table_name == 'reviews':
                c.execute('''
                    CREATE TABLE IF NOT EXISTS reviews (
                        review text, 
                        role text
                    )
                ''')
                c.execute("INSERT INTO reviews VALUES (?, ?)", (data, "Ваш посетитель"))
            else:
                return "Неверное имя таблицы."
            
        except sqlite3.Error as e:
            return f"Ошибка при добавлении данных в базу данных: {e}"
        finally:
            conn.commit()
            conn.close()

menu = {
    "Эспрессо": 100,
    "Латте": 150,
    "Капучино": 130,
    "Американо": 120
    
}

coffee = Coffee("Кофейня", menu)

try:
    customer_name = input("Добрый день! Введите ваше имя: ")
    role = input("Вы регистрируетесь как клиент или администратор? ").strip().lower()
    print(coffee.register_customer(customer_name, role))
    
    if role == 'клиент':
        while True:
            order = input("Что вы будете заказывать сегодня? (для завершения введите 'завершить'): ").strip().capitalize()
            
            if order == "Завершить":
                for item in coffee.orders:
                    coffee.add_to_db('orders', (item, coffee.menu[item]))
                break
            try:
                coffee.order(order)
            except ValueError as e:
                print(e)
            
            total_amount = coffee.calculate_total()
            print(f"Итоговая сумма вашего заказа: {total_amount} рублей")
    else:
        item = input("Введите новый товар для меню: ")
        price = float(input(f"Введите цену для {item}: "))
        coffee.menu[item] = price
        coffee.add_to_db('menu(подарок для покупателя!)', (item, price))

    table_name = input("Введите имя таблицы для добавления данных ('orders', 'menu(подарок для покупателя!)', 'customers', 'reviews'): ")
    if table_name in ['orders', 'menu(подарок для покупателя!)', 'customers', 'reviews']:
        data = input("Введите данные для добавления в таблицу: ")
        print(coffee.add_to_db(table_name, data))
    else:
        print("Неверное имя таблицы.")
        
except Exception as e:
    print(f"Произошла ошибка: {e}")                               