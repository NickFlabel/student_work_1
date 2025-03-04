import json
import datetime
from collections import Counter

DATA_FILE = "data.json"


def load_data():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"employees": [], "cars": [], "sales": []}


def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)


data = load_data()


class Employee:
    def __init__(self, name, position, phone, email):
        self.name = name
        self.position = position
        self.phone = phone
        self.email = email

    def to_dict(self):
        return {"name": self.name, "position": self.position, "phone": self.phone, "email": self.email}


class Car:
    def __init__(self, manufacturer, year, model, cost_price, sale_price):
        self.manufacturer = manufacturer
        self.year = year
        self.model = model
        self.cost_price = cost_price
        self.sale_price = sale_price

    def to_dict(self):
        return {"manufacturer": self.manufacturer, "year": self.year, "model": self.model,
                "cost_price": self.cost_price, "sale_price": self.sale_price}


class Sale:
    def __init__(self, employee, car, date, real_price):
        self.employee = employee
        self.car = car
        self.date = date
        self.real_price = real_price

    def to_dict(self):
        return {"employee": self.employee, "car": self.car, "date": self.date, "real_price": self.real_price}


class Factory:
    @staticmethod
    def create_employee(name, position, phone, email):
        return Employee(name, position, phone, email)

    @staticmethod
    def create_car(manufacturer, year, model, cost_price, sale_price):
        return Car(manufacturer, year, model, cost_price, sale_price)

    @staticmethod
    def create_sale(employee, car, date, real_price):
        return Sale(employee, car, date, real_price)


def add_employee():
    name = input("Введите ФИО: ")
    position = input("Введите должность: ")
    phone = input("Введите телефон: ")
    email = input("Введите email: ")
    employee = Factory.create_employee(name, position, phone, email)
    data["employees"].append(employee.to_dict())
    save_data(data)
    print("Сотрудник добавлен.")


def add_car():
    manufacturer = input("Введите производителя: ")
    year = input("Введите год выпуска: ")
    model = input("Введите модель: ")
    cost_price = float(input("Введите себестоимость: "))
    sale_price = float(input("Введите потенциальную цену продажи: "))
    car = Factory.create_car(manufacturer, year, model, cost_price, sale_price)
    data["cars"].append(car.to_dict())
    save_data(data)
    print("Автомобиль добавлен.")


def add_sale():
    employee_name = input("Введите ФИО продавца: ")
    car_model = input("Введите модель автомобиля: ")
    sale_date = input("Введите дату продажи (ГГГГ-ММ-ДД): ")
    real_price = float(input("Введите реальную цену продажи: "))
    sale = Factory.create_sale(employee_name, car_model, sale_date, real_price)
    data["sales"].append(sale.to_dict())
    save_data(data)
    print("Продажа добавлена.")


def delete_employee():
    employee_name = input("Введите ФИО сотрудника для удаления: ")
    employee_found = False
    for employee in data["employees"]:
        if employee["name"] == employee_name:
            data["employees"].remove(employee)
            employee_found = True
            break
    if employee_found:
        save_data(data)
        print(f"Сотрудник {employee_name} удален.")
    else:
        print("Сотрудник не найден.")


def delete_car():
    car_model = input("Введите модель автомобиля для удаления: ")
    car_found = False
    for car in data["cars"]:
        if car["model"] == car_model:
            data["cars"].remove(car)
            car_found = True
            break
    if car_found:
        save_data(data)
        print(f"Автомобиль модели {car_model} удален.")
    else:
        print("Автомобиль не найден.")


def delete_sale():
    employee_name = input("Введите ФИО сотрудника продавца: ")
    car_model = input("Введите модель автомобиля: ")
    sale_date = input("Введите дату продажи (ГГГГ-ММ-ДД): ")
    sale_found = False
    for sale in data["sales"]:
        if sale["employee"] == employee_name and sale["car"] == car_model and sale["date"] == sale_date:
            data["sales"].remove(sale)
            sale_found = True
            break
    if sale_found:
        save_data(data)
        print(f"Продажа сотрудника {employee_name} по автомобилю {car_model} от {sale_date} удалена.")
    else:
        print("Продажа не найдена.")


def report_sales_by_date():
    start_date = input("Введите начальную дату (ГГГГ-ММ-ДД): ")
    end_date = input("Введите конечную дату (ГГГГ-ММ-ДД): ")
    sales = [s for s in data["sales"] if start_date <= s["date"] <= end_date]
    print(json.dumps(sales, indent=4, ensure_ascii=False))


def report_total_profit():
    start_date = input("Введите начальную дату (ГГГГ-ММ-ДД): ")
    end_date = input("Введите конечную дату (ГГГГ-ММ-ДД): ")
    total_profit = sum(s["real_price"] for s in data["sales"] if start_date <= s["date"] <= end_date)
    print(f"Суммарная прибыль: {total_profit}")


def report_best_seller():
    start_date = input("Введите начальную дату (ГГГГ-ММ-ДД): ")
    end_date = input("Введите конечную дату (ГГГГ-ММ-ДД): ")
    employees = [s["employee"] for s in data["sales"] if start_date <= s["date"] <= end_date]
    if not employees:
        print("Нет продаж в указанный период.")
        return
    best_seller = Counter(employees).most_common(1)
    print(f"Лучший продавец: {best_seller[0][0]} ({best_seller[0][1]} продаж)")


def report_sales_by_employee():
    employee_name = input("Введите ФИО сотрудника: ")
    sales = [s for s in data["sales"] if s["employee"] == employee_name]
    print(json.dumps(sales, indent=4, ensure_ascii=False))


def main():
    while True:
        print("\nМеню:")
        print("1. Добавить сотрудника")
        print("2. Добавить автомобиль")
        print("3. Добавить продажу")
        print("4. Отчет по продажам за дату")
        print("5. Отчет по прибыли за период")
        print("6. Лучший продавец")
        print("7. Полная информация о сотрудниках")
        print("8. Полная информация об автомобилях")
        print("9. Самый продаваемый автомобиль")
        print("10. Продажи сотрудника")
        print("11. Удалить сотрудника")
        print("12. Удалить автомобиль")
        print("13. Удалить продажу")
        print("0. Выход")

        choice = input("Выберите действие: ")
        if choice == "1":
            add_employee()
        elif choice == "2":
            add_car()
        elif choice == "3":
            add_sale()
        elif choice == "4":
            report_sales_by_date()
        elif choice == "5":
            report_total_profit()
        elif choice == "6":
            report_best_seller()
        elif choice == "7":
            print(json.dumps(data["employees"], indent=4, ensure_ascii=False))
        elif choice == "8":
            print(json.dumps(data["cars"], indent=4, ensure_ascii=False))
        elif choice == "9":
            report_sales_by_date()
        elif choice == "10":
            report_sales_by_employee()
        elif choice == "11":
            delete_employee()
        elif choice == "12":
            delete_car()
        elif choice == "13":
            delete_sale()
        elif choice == "0":
            break
        else:
            print("Некорректный ввод, попробуйте снова.")


if __name__ == "__main__":
    main()
