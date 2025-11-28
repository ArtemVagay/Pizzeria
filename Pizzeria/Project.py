import customtkinter as CTk
import re
from PIL import Image
import json
import async_tkinter_loop
import fpdf
import pathlib
CTk.set_appearance_mode("Dark")

app = CTk.CTk()
app.geometry("650x650")
app.title("Pizzeria")

def buy(_value):
    data = json.load(open("Data.json", "r"))
    for widget in app.winfo_children():
        widget.destroy()
    pdf = fpdf.FPDF()
    pdf.add_page()
    pdf.add_font('DejaVu', '', 'DejaVuSans-Bold.ttf', uni=True)
    pdf.set_font('DejaVu', '', 14)
    pdf.cell(0, 10, txt="Спасибо что выбираете нас!", ln=2)
    pdf.cell(0, 10, txt="ИП Пиццерия Артёма Вагайцева", ln=1)
    for dish in _value[0]["shop_cart"]:
        pdf.cell(0, 10, txt=f"{dish[0]}...{dish[3]}р", ln = 1)
        for element in dish[2]:
            pdf.cell(10, 0, txt="", ln = 0)
            pdf.cell(0, 10, txt=f"{element[0]}...{element[1]}г", ln = 1)
    downloads_path = pathlib.Path.home() / "Downloads"
    print(downloads_path)
    pdf.output(f"{downloads_path}/Receipt.pdf")
    for user, value in data.items():
        if value == _value:
            thanks_attention = CTk.CTkLabel(app, width=140, height=28, text=f"Спасибо за покупку, будем ждать вас сново!", font = CTk.CTkFont("Comfortaa", size = 20, weight="bold"))
            thanks_attention.pack()
            value[0]["shop_cart"] = []
    open("Data.json", "w").write(json.dumps(data, indent=2))
    button_leave = CTk.CTkButton(app, width=140, height=28, text="Выйти", command=check_opened, fg_color="red", hover_color="#7A0303", font = CTk.CTkFont("Comfortaa", size = 10, weight="bold"))
    button_leave.pack(pady = 20)

def user_order(value):
    for widget in app.winfo_children():
        widget.destroy()
    scrolling_frame = CTk.CTkScrollableFrame(app, width=600, height=400, corner_radius=15)
    scrolling_frame.pack(pady = 30)
    global_cost = 0
    for dish in value[0]["shop_cart"]:
        order_dish_frame(cost=dish[3], dish=dish, frame=scrolling_frame, value=value)
        global_cost += dish[3]
    if value[0]["shop_cart"] != []:
        global_cost_label = CTk.CTkLabel(app, width=140, height=28, text=f"Всего: {global_cost}р")
        global_cost_label.pack()
        buy_button = CTk.CTkButton(app, width=140, height=28, text="Заказать", fg_color="#24D418", hover_color="#0B870D", font = CTk.CTkFont("Comfortaa", size = 10, weight="bold"), command=lambda: buy(value))
        buy_button.pack()
    button_leave = CTk.CTkButton(app, width=140, height=28, text="Назад", command=check_opened, fg_color="red", hover_color="#7A0303", font = CTk.CTkFont("Comfortaa", size = 10, weight="bold"))
    button_leave.pack(pady = 20)

def open_account(line, value):
    cost = 0
    for dish in value[0]["shop_cart"]:
        cost += dish[3]
    return account(name=value[0]["name"], surname=value[0]["surname"], value=value, all_cost=cost)

def user_dishes(shop_cart, cost):
    opened = open("Opened.txt", "r")
    data = json.load(open("Data.json", "r"))
    if len(shop_cart) != 2:
        shop_cart[2] = []
        for widget in app.winfo_children():
            if isinstance(widget, CTk.CTkCheckBox):
                if widget.get() == True:
                    shop_cart[2].append([widget.cget("text").split(" ")[0], int(widget.cget("text").split(" ")[1])])
    else:
        shop_cart.append([])
    for line in opened:
        for user, value in data.items():
            if line.split()[1] == value[0]["login"] and line.split()[0] == value[0]["email"]:
                shop_cart.append(cost)
                for dish in shop_cart[2]:
                    shop_cart[1] += dish[1]
                value[0]["shop_cart"].append(shop_cart)
                open("Data.json", "w").write(json.dumps(data, indent=2))

def delete_from_order(_value, dish):
    data = json.load(open("Data.json", "r"))
    for user, value in data.items():
        if value == _value:
            value[0]["shop_cart"].remove(dish)
            open("Data.json", "w").write(json.dumps(data, indent=2))
            user_order(value)

def dish_info(cost = 0, dish = 0, _value = 0):
    for widget in app.winfo_children():
        widget.destroy()
    dish_name = CTk.CTkLabel(app, width=200, height=50, text=f"{dish[0]}", font=CTk.CTkFont("Comic Sans MS", size = 25))
    dish_name.pack(pady = 15)
    dish_image = CTk.CTkImage(size=(250, 250), light_image=Image.open(f"{dish[0]}.png"), dark_image=Image.open(f"{dish[0]}.png"))
    image_label = CTk.CTkLabel(app, image=dish_image, height=250, width=250, text='')
    image_label.pack(pady = 20)
    if cost != 0:
        try:
            for element in dish[2]:
                element_check_box = CTk.CTkCheckBox(app, text=f"{element[0]} {element[1]}", font=CTk.CTkFont("Comic Sans MS", size = 20), variable=CTk.IntVar(value=1))
                element_check_box.pack()
        except IndexError:
            pass
    
    if cost == 0:
        button_leave = CTk.CTkButton(app, width=140, height=28, text="Назад", command=lambda: user_order(_value), fg_color="red", hover_color="#7A0303", font = CTk.CTkFont("Comfortaa", size = 15, weight="bold"))
        button_leave.pack(side = "right", padx = 10)
        button_order = CTk.CTkButton(app, width=200, height=35, text="Удалить из корзины", fg_color="red", hover_color="#7A0303",font = CTk.CTkFont("Comfortaa", size = 10, weight="bold"), command=lambda: delete_from_order(_value=_value, dish=dish))
        button_order.pack(side = "right", padx = 40)
    else:
        button_leave = CTk.CTkButton(app, width=140, height=28, text="Назад", command=lambda: check_opened(), fg_color="red", hover_color="#7A0303", font = CTk.CTkFont("Comfortaa", size = 15, weight="bold"))
        button_leave.pack(side = "right", padx = 10)
        button_order = CTk.CTkButton(app, width=200, height=35, text="Добавить в корзину", fg_color="#38C92A", hover_color="#178530", command=lambda: user_dishes(dish, cost))
        button_order.pack(pady = 10, side = "right", padx = 40)
   
def order_dish_frame(cost, dish, frame, value):
    image_frame = CTk.CTkFrame(frame, height=140, width=150, corner_radius=20, fg_color="transparent", bg_color="transparent")
    image_frame.pack(side = "bottom")
    dish_image = CTk.CTkImage(size=(150, 150), light_image=Image.open(f"{dish[0]}.png"), dark_image=Image.open(f"{dish[0]}.png"))
    if dish[2] == [] and dish[3] < 700:
        dish_type_name = CTk.CTkLabel(image_frame, width=200, height=50, text=f"{dish[0]} {dish[1]}мл", font=CTk.CTkFont("Comic Sans MS", size = 12))
        dish_type_name.pack()
    elif dish[2] == []:
        dish_type_name = CTk.CTkLabel(image_frame, width=200, height=50, text=f"{dish[0]} {dish[1]} без ингридиентов", font=CTk.CTkFont("Comic Sans MS", size = 12))
        dish_type_name.pack()
    else:
        dish_type_name = CTk.CTkLabel(image_frame, width=200, height=50, text=f"{dish[0]} {dish[1]}г: {', '.join(_dish[0] for _dish in dish[2])}", font=CTk.CTkFont("Comic Sans MS", size = 12))
        dish_type_name.pack()
    cost_label = CTk.CTkLabel(image_frame, height=50, width=20, text=f"{dish[3]}р", font=CTk.CTkFont("Comic Sans MS", size = 15))
    cost_label.pack()
    image_button = CTk.CTkButton(image_frame, image=dish_image, height=150, width=150, text='', command=lambda: dish_info(dish=dish, _value=value), bg_color="transparent", fg_color="transparent", hover_color="white")
    image_button.pack()
    
def dish_frame(cost, dish, frame):
    dish_frame = CTk.CTkFrame(frame, width=200, height=200, corner_radius=10, bg_color="transparent")
    dish_frame.pack(pady = 10)
    dish_image = CTk.CTkImage(size=(150, 150), light_image=Image.open(f"{dish[0]}.png"), dark_image=Image.open(f"{dish[0]}.png"))
    image_frame = CTk.CTkFrame(dish_frame, height=140, width=150, corner_radius=20, fg_color="transparent", bg_color="transparent")
    image_frame.pack(side = "bottom")
    image_button = CTk.CTkButton(image_frame, image=dish_image, height=150, width=150, text='', command=lambda: dish_info(cost, dish), bg_color="transparent", fg_color="transparent", hover_color="white")
    image_button.pack()
    dish_name = CTk.CTkLabel(dish_frame, width=100, height=25, text=f"{dish[0]}", font=CTk.CTkFont("Comic Sans MS", 20, weight="bold"))
    dish_name.pack(pady = 10)

def account(surname, name, value, all_cost):
    menu_costs = {"Пицца":

                        {750: ["Маргорита", 200, [["Моццарела", 80], ["Базилик", 20], ["Соус", 120]]],
                        790: ["Пепперони", 200, [["Моццарела", 80], ["Базилик", 20], ["Соус", 120], ["Колбаса⠀пепперони", 200]]],
                        1260: ["Пицца 4 сыра", 200, [["Моццарела", 100], ["Пармезан", 80], ["Блю-чиз", 50], ["Алтайский", 120], ["Соус", 120]]],
                        1350: ["Мясная", 200, [["Колбаса⠀пепперони", 200], ["Ветчина", 130], ["Курица", 80], ["Фарш", 180], ["Моццарела", 80], ["Соус", 120]]],
                        1200: ["Кастомная", 200, [["Грибы", 100], ["Ветчина", 100], ["Моццарела", 100], ["Пармезан", 80], ["Блю-чиз", 50], ["Фарш", 180], ["Соус", 120], ["Колбаса⠀пепперони", 200]]]},
                    "Напитки":

                        {130: ["Вода", 200],
                        200: ["Клюквенный морс", 300]},
                        
                    "Кофе":
                        {300: ["Каппучино", 500],
                        350: ["Американо", 500]}}
    for widget in app.winfo_children():
        widget.destroy()
    hello_label = CTk.CTkLabel(app, text=f"Здравствуйте, {surname} {name}", font = CTk.CTkFont("Comfortaa", size = 20, weight="bold"))
    hello_label.pack(pady = 20)
    scrolling_frame = CTk.CTkScrollableFrame(app, width=400, height=350, corner_radius=15)
    scrolling_frame.pack(pady = 40)
    for dish_type, dishes in menu_costs.items():
        dish_type_frame = CTk.CTkFrame(scrolling_frame, width=200, height=300, corner_radius=10, fg_color="transparent")
        dish_type_frame.pack(pady = 10)
        dish_type_name = CTk.CTkLabel(dish_type_frame, width=200, height=50, text=f"---------{dish_type}---------", font=CTk.CTkFont("Comic Sans MS", size = 25))
        dish_type_name.pack()
        for cost, dish in dishes.items():
            dish_frame(cost, dish, dish_type_frame)
    button_leave = CTk.CTkButton(app, width=140, height=28, text="Выйти", command=main_screen, fg_color="red", hover_color="#7A0303", font = CTk.CTkFont("Comfortaa", size = 15, weight="bold"))
    button_leave.pack()
    order = CTk.CTkButton(app, width=100, height=20, text=f"Корзина: {all_cost}р", command=lambda: user_order(value))
    order.pack(side = "right", padx = 20)

def check_register():
    global data
    data = json.load(open("Data.json", "r"))

    if re.fullmatch(r"\w+@\w+\.\w+", email_textbox.get()):
        for user, value in data.items():
            email = value[0]["email"]
            login = value[0]["login"]
            if email == email_textbox.get() or login == login_textbox.get():
                button_check.configure(fg_color="red", hover_color="red")
                app.after(500, lambda: button_check.configure(fg_color='#1F6AA5', hover_color='#1F6AA5'))
                return
        data[f"{login_textbox.get()}"] = {"email": email_textbox.get(), "login": login_textbox.get(), "name": name_textbox.get().split()[1], "surname": name_textbox.get().split()[0], "shop_cart": []},
        open("Data.json", "w").write(json.dumps(data, indent=2))
        button_check.configure(fg_color="green", hover_color="green")
        app.after(500, lambda: button_check.configure(fg_color='#1F6AA5', hover_color='#1F6AA5'))
    else:
        button_check.configure(fg_color="red", hover_color="red")
        app.after(500, lambda: button_check.configure(fg_color='#1F6AA5', hover_color='#1F6AA5'))
    
def check_log_in():
    data = json.load(open("Data.json", "r"))
    for user, user_data in data.items():
        email = user_data[0]["email"]
        login = user
        surname = user_data[0]["surname"]
        name = user_data[0]["name"]
        if email.lower() == email_textbox.get().lower() and login.lower() == login_textbox.get().lower():
            opened = open("Opened.txt", "w")
            opened.write(f"{email} {login}")
            opened.close()
            return open_account(user, user_data)
    button_check.configure(fg_color="red", hover_color="red")
    app.after(500, lambda: button_check.configure(fg_color='#1F6AA5', hover_color='#1F6AA5'))
    data.close()
def log_in():
    for widget in app.winfo_children():
        widget.destroy()
    global email_textbox, login_textbox, button_check
    log_in_label = CTk.CTkLabel(app, width=250, height=50, text="Вход", font = CTk.CTkFont("Comfortaa", size = 25, weight="bold"))
    log_in_label.pack(pady = 40, padx = 300 - 250 / 2)
    email_textbox = CTk.CTkEntry(app, width=140, height=28, placeholder_text="Email")
    email_textbox.pack(pady = 20)
    login_textbox = CTk.CTkEntry(app, width=140, height=28, placeholder_text="Login")
    login_textbox.pack()
    button_check = CTk.CTkButton(app, width=140, height=28, text="Войти", command=check_log_in, font = CTk.CTkFont("Comfortaa", size = 15, weight="bold"))
    button_check.pack(pady = 20)
    button_leave = CTk.CTkButton(app, width=140, height=28, text="Назад", command=main_screen, fg_color="red", hover_color="#7A0303", font = CTk.CTkFont("Comfortaa", size = 15, weight="bold"))
    button_leave.pack(pady = 40)
def reg():
    for widget in app.winfo_children():
        widget.destroy()
    global email_textbox, login_textbox, button_check, name_textbox
    log_in_label = CTk.CTkLabel(app, width=250, height=50, text="Регистрация", font = CTk.CTkFont("Comfortaa", size = 25, weight="bold"))
    log_in_label.pack(pady = 40, padx = 300 - 250 / 2)
    email_textbox = CTk.CTkEntry(app, width=140, height=28, placeholder_text="Email")
    email_textbox.pack(pady = 20)
    login_textbox = CTk.CTkEntry(app, width=140, height=28, placeholder_text="Login")
    login_textbox.pack()
    name_textbox = CTk.CTkEntry(app, width=140, height=28, placeholder_text="ФИ")
    name_textbox.pack(pady = 20)
    button_check = CTk.CTkButton(app, width=140, height=28, text="Зарегистрироваться", command=check_register, font = CTk.CTkFont("Comfortaa", size = 15, weight="bold"))
    button_check.pack()
    button_leave = CTk.CTkButton(app, width=140, height=28, text="Назад", command=main_screen, fg_color="red", hover_color="#7A0303", font = CTk.CTkFont("Comfortaa", size = 15, weight="bold"))
    button_leave.pack(pady = 60)
    
def main_screen():
    opened = open("Opened.txt", "w")
    opened.write("")
    opened.close()
    for widget in app.winfo_children():
        widget.destroy()
    global button_log_in, button_reg, app_name
    app_name = CTk.CTkLabel(app, width=250, height=50, text="Добро пожаловать в Пиццерию!", font = CTk.CTkFont("Comfortaa", size = 25, weight="bold"))
    app_name.pack(pady = 20)
    button_log_in = CTk.CTkButton(app, width=200, height=75, text="Войти", corner_radius=15, command=log_in, font = CTk.CTkFont("Comfortaa", size = 20, weight="bold"))
    button_log_in.pack(pady = 70)

    button_reg = CTk.CTkButton(app, width=200, height=75, text="Регистрация", corner_radius=15, command=reg, font = CTk.CTkFont("Comfortaa", size = 20, weight="bold"))
    button_reg.pack(pady = 10)
    
def check_opened():
    opened = open("Opened.txt", "r")
    file = open("Data.json", "r")
    data = json.load(file)
    for user in opened:
        user = user.split()
        email = user[0]
        login = user[1]
        for line, value in data.items():
            if email == value[0]["email"] and login == value[0]["login"]:
                return open_account(line, value)
    return main_screen()


check_opened()
async_tkinter_loop.async_mainloop(app)