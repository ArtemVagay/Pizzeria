from datetime import *

def main():
    name, surname, middle_name, age = task()
    hello_user(name, surname, middle_name)
    margo, pepperoni, four_cheese, meat, water, fruit_drink, cappuccino, americano = menu(age)
    dishes, names, costs = buy(age, margo, pepperoni, four_cheese, meat, water, fruit_drink, cappuccino, americano)
    check(names, costs, name, surname, middle_name, dishes, margo, pepperoni, four_cheese, meat, water, fruit_drink, cappuccino, americano)


def task() -> (str, str, str, int):
    name = input("Как к вам обращаться(Имя): ")
    surname = input("Как к вам обращаться(Фамилия): ")
    middle_name = input("Как к вам обращаться(Отчество): ")
    age = int(input("Сколько вам лет: "))
    return name, surname, middle_name, age

def hello_user(name: str, surname: str, middle_name: str) -> print():
    return print(f"Добро пожаловать в пиццерию Артёма Вагайцева, {surname} {name} {middle_name}!")

def menu(age):
    if age < 18:
        margo = 750
        pepperoni = 790
        four_cheese = 1260
        meat = 1350
        water = 130
        fruit_drink = 200
        print(f"----- Меню -----\n",
              "----- Пицца -----\n",
              f"1. Пицца Маргорита  {margo}р / 350г\n",
              f"2. Пицца Пепперони  {pepperoni}р / 400г\n",
              f"3. Пицца 4 сыра  {four_cheese}р / 550г\n",
              f"4. Пицца Мясная  {meat}р / 620г\n",
              f"----- Напитки -----\n",
              f"5. Вода  {water}р / 250мл\n"
              f"6. Клюквенный морс  {fruit_drink}р / 300мл",)
        return margo, pepperoni, four_cheese, meat, water, fruit_drink, 0, 0
    else:
        margo = 850
        pepperoni = 900
        four_cheese = 1500
        meat = 1750
        water = 250
        fruit_drink = 370
        cappuccino = 500
        americano = 550
        print(f"----- Меню -----\n",
              "----- Пицца -----\n",
              f"1. Пицца Маргорита  {margo}р / 450г\n",
              f"2. Пицца Пепперони  {pepperoni}р / 400г\n",
              f"3. Пицца 4 сыра  {four_cheese}р / 700г\n",
              f"4. Пицца Мясная  {meat}р / 750г\n",
              f"----- Напитки -----\n",
              f"5. Вода  {water}р / 350мл\n"
              f"6. Клюквенный морс  {fruit_drink}р / 500мл\n",
              f"----- Кофе -----\n",
              f"7. Капучино   {cappuccino}р / 300мл\n",
              f"8. Американо   {americano}р / 350мл")
        return margo, pepperoni, four_cheese, meat, water, fruit_drink, cappuccino, americano

def buy(age, margo, pepperoni, four_cheese, meat, water, fruit_drink, cappuccino, americano):
    while True:
        costs = [margo, pepperoni, four_cheese, meat, water, fruit_drink, cappuccino, americano]
        dishes = input("\nНапишите, что вы хотите заказать (Через пробел и цифрами): ").split(" ")
        names = {1: "Пицца Маргорита", 2: "Пицца Пепперони", 3: "Пицца 4 сыра", 4: "Пицца Мясная", 5: "Вода",
                 6: "Клюквенный морс", 7: "Капучино", 8: "Американо"}
        cost = 0
        count = 0
        cant = False
        for num in dishes:
            dishes[count] = int(num)
            count += 1
        dishes.sort()
        for dish in dishes:
            if dish >= 7:
                cant = True
        for dish in dishes:
            if age < 18:
                dishes = [d for d in dishes if d < 7]
            else:
                cant = False
        dish_counts = {}
        for dish in dishes:
            dish_counts[dish] = dish_counts.get(dish, 0) + 1
        if cant:
            print(f"К сожалению, мы не можем приготовить вам продукцию для людей достигших 18 лет, но вот ваш заказ:")
            count = 0
            count1 = 0
            for dish_num, dish_count in dish_counts.items():
                count += 1
                count1 = 0
                dish_name = names[dish_num]
                cost += costs[dish_num - 1] * dish_count
                for dish in dishes:
                    count1 += 1
                    if count == count1:
                        print(f"\t{count}.{dish_name} * {dish_count}")
        else:
            print(f"Ваш заказ: ")
            count = 0
            count1 = 0
            for dish_num, dish_count in dish_counts.items():
                count += 1
                count1 = 0
                dish_name = names[dish_num]
                cost += costs[dish_num - 1] * dish_count
                for dish in dishes:
                    count1 += 1
                    if count == count1:
                        print(f"\t{count}.{dish_name} * {dish_count}")
        accept = input("\nВсе правильно(Да Нет)?: ")
        if accept.lower() == "да":
            print("\nХорошо, ожидайте заказ. Ваш чек:\n")
            return dishes, names, costs
        else:
            print("\nХорошо, попробуйте сделать заказ еще раз!\n")

def check(names, costs, name, surname, middle_name, dishes, margo, pepperoni, four_cheese, meat, water, fruit_drink, cappuccino, americano):
    dish_counts = {}
    dishes.sort()
    cost = 0
    for dish in dishes:
        dish_counts[dish] = dish_counts.get(dish, 0) + 1
    print("\t\tИП \"Пиццерия Артёма Вагайцева\"")
    count = 0
    count1 = 0
    for dish_num, dish_count in dish_counts.items():
        count += 1
        count1 = 0
        dish_name = names[dish_num]
        cost += costs[dish_num - 1] * dish_count
        for dish in dishes:
            count1 += 1
            if count == count1:
                print(f"\t\t{count}.{dish_name} * {dish_count}\n",
                      f"\t\tСтоимость.........{costs[dish_num - 1] * dish_count}р")
    print(f"\n\t\t{datetime.today().date()} {datetime.today().hour}:{datetime.today().minute}\n",
        f"\t\tВсего.........{cost}р")

main()