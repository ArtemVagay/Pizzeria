import re
from datetime import *
def main(turn = 0, name = "", surname = "", middle_name = "", age = 0):
    if turn == 0:
        name, surname, middle_name, age, email, number = task()
        hello_user(name, surname, middle_name)
    else:
        again = input("Вы хотите сделать еще один заказ(Да Нет): ")
        if again.lower() == "нет":
            return print("Ожидаем вас в нашей пиццерии снова!")
    menu_cost = menu(age)
    dishes, names, costs, pay, cost = buy(age, menu_cost)
    check(names, costs, name, surname, middle_name, dishes, menu_cost, pay, cost)
    return main(turn + 1, name, surname, middle_name, age)
def check_email(email, again = False):
    if again:
        email = input("Попробуйте еще раз ввести ваш email: ")
    if re.fullmatch(r"\w+@\w+\.\w+", email) or email.lower() == "нет":
        return email
    return check_email(email, again = True)

def check_number(number, again = False):
    if again:
        number = input("Попробуйте еще раз ввести ваш номер +7: ")
    if re.fullmatch(r"\d{10}", number):
        return number
    return check_number(number, again = True)

def check_bitrhday(birthday, again = False):
    if again:
        birthday = input("Попробуйте еще раз ввести ваш день рождения: ")
    if re.fullmatch(r"\d{0-31}.\d{0-12}.[-2025]}", birthday):
        return birthday
    return check_bitrhday(birthday, again=True)

def task() -> (str, str, str, int):
    name = input("Как к вам обращаться(Имя): ")
    surname = input("Как к вам обращаться(Фамилия): ")
    middle_name = input("Как к вам обращаться(Отчество): ")
    birthday = int(input("Дата рождения (пример: 10.20.2000): "))
    birthday = check_bitrhday(birthday)
    email = input("Введите ваш email или нет: ")
    email = check_email(email)
    number = input("Введите ваш номер телефона: +7")
    number = check_number(number)
    return name, surname, middle_name, birthday, email, number

def hello_user(name: str, surname: str, middle_name: str) -> print():
    return print(f"Добро пожаловать в пиццерию Артёма Вагайцева, {surname} {name} {middle_name}!")

def menu(age):
    if age < 18:
        menu_cost = {"Пицца":

                        {750: ["Маргорита", "350г"],
                        790: ["Пепперони", "400г"],
                        1260: ["Пицца 4 сыра", "550г"],
                        1350: ["Мясная", "620г"]},
                    "Напитки":

                        {130: ["Вода", "250мл"],
                        200: ["Клюквенный морс", "300мл"]}}
        print(f"----- Меню -----\n")
        count = 0
        for dish_type in menu_cost.keys():
            print(f"\t----- {dish_type} -----"),
            for cost, dish in menu_cost[dish_type].items():
                count += 1
                print(f"\t{count}. {dish[0]}  {cost}р / {dish[1]}")
        return menu_cost
    else:
        menu_cost = {"Пицца":

                         {850: ["Маргорита", "350г"],
                          900: ["Пепперони", "400г"],
                          1500: ["Пицца 4 сыра", "550г"],
                          1750: ["Мясная", "620г"]},
                     "Напитки":

                         {250: ["Вода", "250мл"],
                          370: ["Клюквенный морс", "300мл"]},
                     "Кофе":

                         {500: ["Капучино", "300мл"],
                          550: ["Американо", "350мл"]}}
        print(f"----- Меню -----\n")
        count = 0
        for dish_type in menu_cost.keys():
            print(f"----- {dish_type} -----\n"),
            for cost, dish in menu_cost[dish_type].items():
                count += 1
                print(f"{count}. {dish[0]}  {cost}р / {dish[1]}")
        return menu_cost

def buy(age, menu_cost):
    while True:
        costs = []
        for dish_type in menu_cost.keys():
            for cost in menu_cost[dish_type].keys():
                costs.append(cost)
        dishes = list(map(int, input("\nНапишите, что вы хотите заказать (Через пробел и цифрами): ").split()))
        names = {}
        count = 0
        for dish_type in menu_cost.keys():
            for dish in menu_cost[dish_type].values():
                count += 1
                names.update({count: dish[0]})
        cost = 0
        cant = False
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
            pay = int(input("Оплата картой или наличкой(1 2): "))
            if pay == 1:
                print(f"Хорошо с вас {cost}р, вот ваш терминал")
            elif pay == 2:
                print(f"Хорошо, c вас {cost}р")
            return dishes, names, costs, pay, cost
        else:
            print("\nХорошо, попробуйте сделать заказ еще раз!\n")

def check(names, costs, name, surname, middle_name, dishes, menu_cost, pay, cost):
    print("Оплата прошла успешно, ожидайте заказ")
    if pay == 2:
        print(f"Вот ваша сдача: {cost // 10}р")
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