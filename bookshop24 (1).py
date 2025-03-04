import json
import tkinter as tk
from tkinter import messagebox
from datetime import datetime


class DataStorage:
    def __init__(self, filename="store.json"):
        self.filename = filename

    def save(self, data):
        with open(self.filename, "w") as file:
            json.dump(data, file, indent=4)

    def load(self):
        try:
            with open(self.filename, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {"employees": [], "books": [], "sales": []}


class StoreManager:
    def __init__(self):
        self.storage = DataStorage()
        self.data = self.storage.load()

    def save_data(self):
        self.storage.save(self.data)

    def add_employee(self, name, position, phone, email):
        self.data["employees"].append(
            {"name": name.title(), "position": position.title(), "phone": phone, "email": email}
        )
        self.save_data()

    def add_book(self, title, year, author, genre, cost, price):
        self.data["books"].append(
            {"title": title.title(), "year": year, "author": author.title(), "genre": genre.title(), "cost": cost, "price": price}
        )
        self.save_data()

    def record_sale(self, employee_name, book_title, sale_price):
        employee_name = employee_name.lower()
        book_title = book_title.lower()

        employee = next((e for e in self.data["employees"] if e["name"].lower() == employee_name), None)
        book = next((b for b in self.data["books"] if b["title"].lower() == book_title), None)

        if not employee or not book:
            raise ValueError("Сотрудник или книга не найдены")

        sale = {
            "employee": employee["name"],
            "book": book["title"],
            "date": datetime.now().strftime("%Y-%m-%d"),
            "sale_price": sale_price,
            "profit": sale_price - book["cost"]
        }

        self.data["sales"].append(sale)
        self.save_data()

    def calculate_profit(self):
        return sum(s["profit"] for s in self.data["sales"])

    def get_sales(self):
        return self.data["sales"]


class BookstoreApp:
    def __init__(self, root):
        self.manager = StoreManager()
        root.title("Учёт продаж книг")

        label_font = ("Arial", 12, "bold")
        entry_font = ("Arial", 12)

        tk.Label(root, text="Добавить сотрудника", font=label_font).grid(row=0, column=0, columnspan=2, pady=5)
        tk.Label(root, text="ФИО:", font=entry_font).grid(row=1, column=0)
        self.emp_name = tk.Entry(root)
        self.emp_name.grid(row=1, column=1)

        tk.Label(root, text="Должность:", font=entry_font).grid(row=2, column=0)
        self.emp_position = tk.Entry(root)
        self.emp_position.grid(row=2, column=1)

        tk.Label(root, text="Телефон:", font=entry_font).grid(row=3, column=0)
        self.emp_phone = tk.Entry(root)
        self.emp_phone.grid(row=3, column=1)

        tk.Label(root, text="Email:", font=entry_font).grid(row=4, column=0)
        self.emp_email = tk.Entry(root)
        self.emp_email.grid(row=4, column=1)

        tk.Button(root, text="Добавить сотрудника", command=self.add_employee).grid(row=5, column=0, columnspan=2, pady=5)

        tk.Label(root, text="Добавить книгу", font=label_font).grid(row=6, column=0, columnspan=2, pady=5)
        tk.Label(root, text="Название:", font=entry_font).grid(row=7, column=0)
        self.book_title = tk.Entry(root)
        self.book_title.grid(row=7, column=1)

        tk.Label(root, text="Год:", font=entry_font).grid(row=8, column=0)
        self.book_year = tk.Entry(root)
        self.book_year.grid(row=8, column=1)

        tk.Label(root, text="Автор:", font=entry_font).grid(row=9, column=0)
        self.book_author = tk.Entry(root)
        self.book_author.grid(row=9, column=1)

        tk.Label(root, text="Жанр:", font=entry_font).grid(row=10, column=0)
        self.book_genre = tk.Entry(root)
        self.book_genre.grid(row=10, column=1)

        tk.Label(root, text="Себестоимость:", font=entry_font).grid(row=11, column=0)
        self.book_cost = tk.Entry(root)
        self.book_cost.grid(row=11, column=1)

        tk.Label(root, text="Цена продажи:", font=entry_font).grid(row=12, column=0)
        self.book_price = tk.Entry(root)
        self.book_price.grid(row=12, column=1)

        tk.Button(root, text="Добавить книгу", command=self.add_book).grid(row=13, column=0, columnspan=2, pady=5)

        tk.Label(root, text="Оформить продажу", font=label_font).grid(row=14, column=0, columnspan=2, pady=5)
        tk.Label(root, text="Сотрудник:", font=entry_font).grid(row=15, column=0)
        self.sale_emp = tk.Entry(root)
        self.sale_emp.grid(row=15, column=1)

        tk.Label(root, text="Книга:", font=entry_font).grid(row=16, column=0)
        self.sale_book = tk.Entry(root)
        self.sale_book.grid(row=16, column=1)

        tk.Label(root, text="Цена продажи:", font=entry_font).grid(row=17, column=0)
        self.sale_price = tk.Entry(root)
        self.sale_price.grid(row=17, column=1)

        tk.Button(root, text="Оформить продажу", command=self.record_sale).grid(row=18, column=0, columnspan=2, pady=5)

        tk.Button(root, text="Посчитать прибыль", command=self.show_profit).grid(row=19, column=0, columnspan=2, pady=5)

        self.sales_list = tk.Text(root, height=10, width=50)
        self.sales_list.grid(row=20, column=0, columnspan=2)
        self.show_sales()

    def add_employee(self):
        self.manager.add_employee(self.emp_name.get(), self.emp_position.get(), self.emp_phone.get(), self.emp_email.get())
        messagebox.showinfo("Успешное сохранение", "Сотрудник добавлен!")

    def add_book(self):
        title = self.book_title.get().strip().title()
        year = self.book_year.get().strip()
        author = self.book_author.get().strip().title()
        genre = self.book_genre.get().strip().title()
        cost = self.book_cost.get().strip()
        price = self.book_price.get().strip()

        if not year.isdigit():
            messagebox.showerror("Ошибка", "Год публикации должен содержать только цифры!")
            return

        try:
            cost = float(cost)
            price = float(price)
        except ValueError:
            messagebox.showerror("Ошибка", "Себестоимость и цена продажи должны быть числами!")
            return

        self.manager.add_book(title, year, author, genre, cost, price)
        messagebox.showinfo("Успешное сохранение", "Книга добавлена!")

    def record_sale(self):
        try:
            self.manager.record_sale(self.sale_emp.get(), self.sale_book.get(), float(self.sale_price.get()))
            messagebox.showinfo("Успешное сохранение", "Продажа записана!")
            self.show_sales()
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))

    def show_profit(self):
        profit = self.manager.calculate_profit()
        messagebox.showinfo("Прибыль", f"Общая прибыль: {profit}тг.")

    def show_sales(self):
        self.sales_list.delete(1.0, tk.END)
        for sale in self.manager.get_sales():
            self.sales_list.insert(tk.END, f"{sale['date']} - {sale['employee']} продал {sale['book']} за {sale['sale_price']}₸\n")


if __name__ == "__main__":
    root = tk.Tk()
    app = BookstoreApp(root)
    root.mainloop()
