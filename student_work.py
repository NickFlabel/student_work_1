import json
from typing import List, Dict
import os


class Resident:
    def __init__(self, full_name: str, years_old: int):
        self.full_name = full_name
        self.years_old = years_old

    def to_dict(self):
        return {"full_name": self.full_name, "years_old": self.years_old}

    @classmethod
    def from_dict(cls, data):
        return cls(data["full_name"], data["years_old"])


class Apartment:
    def __init__(self, num: int, lvl: int, category: str):
        self.num = num
        self.lvl = lvl
        self.category = category
        self.occupants: List[Resident] = []

    def settle_resident(self, person: Resident):
        self.occupants.append(person)

    def evict_resident(self, person_name: str):
        self.occupants = [p for p in self.occupants if p.full_name != person_name]

    def to_dict(self):
        return {
            "num": self.num,
            "lvl": self.lvl,
            "category": self.category,
            "occupants": [p.to_dict() for p in self.occupants]
        }

    @classmethod
    def from_dict(cls, data):
        apartment = cls(data["num"], data["lvl"], data["category"])
        apartment.occupants = [Resident.from_dict(p) for p in data["occupants"]]
        return apartment


class Building:
    def __init__(self):
        self.units: Dict[int, Apartment] = {}

    def register_apartment(self, apartment: Apartment):
        self.units[apartment.num] = apartment
        self.save_data()

    def demolish_apartment(self, num: int):
        if num in self.units:
            del self.units[num]
            self.save_data()

    def export_data(self, file_path: str = "house_data.json"):
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump({num: apt.to_dict() for num, apt in self.units.items()}, file, indent=4, ensure_ascii=False)

    def import_data(self, file_path: str = "house_data.json"):
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                self.units = {int(k): Apartment.from_dict(v) for k, v in data.items()}

    def save_data(self):
        self.export_data()

    def show_residents(self):
        return [p.to_dict() for apt in self.units.values() for p in apt.occupants]

    def show_apartments(self):
        return [apt.to_dict() for apt in self.units.values()]

    def apartment_details(self, num: int):
        return self.units[num].to_dict() if num in self.units else None


def main():
    house = Building()
    house.import_data()

    while True:
        print("\nМеню:")
        print("1. Добавить квартиру")
        print("2. Удалить квартиру")
        print("3. Добавить жильца")
        print("4. Выселить жильца")
        print("5. Показать квартиры")
        print("6. Показать жильцов")
        print("7. Выйти")

        choice = input("Выберите действие: ")

        if choice == "1":
            while True:
                try:
                    num = int(input("Номер квартиры: "))
                    if num < 0:
                        print("Ошибка: Номер квартиры не может быть отрицательным. Попробуйте снова.")
                    else:
                        break
                except ValueError:
                    print("Ошибка: Введите корректный номер квартиры (целое число).")

            while True:
                try:
                    lvl = int(input("этаж: "))
                    if lvl < 0:
                        print("Ошибка: Этаж не может быть отрицательным. Попробуйте снова.")
                    else:
                        break
                except ValueError:
                    print("Ошибка: Введите корректный этаж (целое число).")

            category = input("Тип квартиры: ")
            house.register_apartment(Apartment(num, lvl, category))
            print(f"Квартира №{num} добавлена.")
        elif choice == "2":
            num = int(input("номер квартиры для удаления: "))
            if num in house.units:
                house.demolish_apartment(num)
                print(f"квартира №{num} удалена.")
            else:
                print(f"ввартира №{num} не найдена.")
        elif choice == "3":
            num = int(input("Номер квртиры: "))
            if num not in house.units:
                print(f"Ошибка: Квартира №{num} не существует. Добавьте её сначала")
                continue
            name = input("Имя жильца: ")
            while True:
                try:
                    age = int(input("Возвраст: "))
                    if age < 0:
                        print("Ошибка: возраст не может быть отрицательным. Попробуйте снова.")
                    else:
                        break
                except ValueError:
                    print("Ошибка: введите корректный возраст (число).")
            house.units[num].settle_resident(Resident(name, age))
            house.save_data()
            print(f"Жилец {name}, {age} лет добавлен в квартиру №{num}.")
        elif choice == "4":
            num = int(input("Номер квартиры: "))
            if num not in house.units:
                print(f"Ошибка: Квартира №{num} не найдена:(")
                continue
            name = input("нейм жильца для выселения: ")
            house.units[num].evict_resident(name)
            house.save_data()
            print(f"Жилец {name} выселен из квартиры №{num}.")
        elif choice == "5":
            print("\nСписок квартир:")
            for apt in house.show_apartments():
                print(f"Квартира №{apt['num']} (этаж {apt['lvl']}, тип: {apt['category']})")
                if apt["occupants"]:
                    print("  Жильцы:")
                    for occupant in apt["occupants"]:
                        print(f"    - {occupant['full_name']}, возраст {occupant['years_old']}")
        elif choice == "6":
            print("\nСписок жильцов:")
            for resident in house.show_residents():
                print(f"{resident['full_name']}, возраст {resident['years_old']} ")
        elif choice == "7":
            break
        else:
            print("неверный ввод попробуйте снова")


if __name__ == "__main__":
    main()
