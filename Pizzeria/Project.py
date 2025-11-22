import customtkinter as CTk
import asyncio
import re
import time
from PIL import Image
CTk.set_appearance_mode("Dark")

app = CTk.CTk()
app.geometry("600x600")
app.title("Pizzeria")

users = []

def open_account(line):
    return account(line[2], line[3])

def dish_info(cost, dish):
    for widget in app.winfo_children():
        widget.destroy()
    dish_name = CTk.CTkLabel(app, width=200, height=50, text=f"{dish[0]}", font=CTk.CTkFont("Comic Sans MS", size = 25))
    dish_name.pack(pady = 15)
    dish_image = CTk.CTkImage(size=(250, 250), light_image=Image.open(f"{dish[0]}.png"), dark_image=Image.open(f"{dish[0]}.png"))
    image_label = CTk.CTkLabel(app, image=dish_image, height=250, width=250, text='')
    image_label.pack(pady = 20)
    try:
        for element in dish[2]:
            element_check_box = CTk.CTkCheckBox(app, text=element, font=CTk.CTkFont("Comic Sans MS", size = 20), variable=CTk.IntVar(value=1))
            element_check_box.pack()
    except IndexError:
        pass
    button_leave = CTk.CTkButton(app, width=140, height=28, text="Назад", command=lambda: check_opened(), fg_color="red", hover_color="#7A0303", font = CTk.CTkFont("Comfortaa", size = 15, weight="bold"))
    button_leave.pack(side = "right", padx = 10)
    button_order = CTk.CTkButton(app, width=200, height=35, text="Добавить в корзину", fg_color="#38C92A", hover_color="#178530")
    button_order.pack(pady = 20, side = "right", padx = 40)
    
    
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

def account(surname, name):
    menu_costs = {"Пицца":

                        {750: ["Маргорита", "350г", ["Сыр", "Базилик", "Соус"]],
                        790: ["Пепперони", "400г", ["Сыр", "Базилик", "Соус", "Колбаса пепперони"]],
                        1260: ["Пицца 4 сыра", "550г", ["Моццарела", "Пармезан", "Блю-чиз", "Алтайский", "Соус"]],
                        1350: ["Мясная", "620г", ["Колбаса пепперони", "Ветчина", "Курица", "Фарш", "Сыр", "Соус"]]},
                    "Напитки":

                        {130: ["Вода", "250мл"],
                        200: ["Клюквенный морс", "300мл", ["Ягоды"]]}}
    for widget in app.winfo_children():
        widget.destroy()
    # hello_frame = CTk.CTkFrame(app, width=0, height=0)
    # hello_frame.grid(padx = 5, pady = 5)
    hello_label = CTk.CTkLabel(app, text=f"Здравствуйте, {surname} {name}", font = CTk.CTkFont("Comfortaa", size = 20, weight="bold"))
    hello_label.pack(pady = 20)
    scrolling_frame = CTk.CTkScrollableFrame(app, width=400, height=350, corner_radius=15)
    scrolling_frame.pack(pady = 50)
    for dish_type, dishes in menu_costs.items():
        dish_type_frame = CTk.CTkFrame(scrolling_frame, width=200, height=300, corner_radius=10, fg_color="transparent")
        dish_type_frame.pack(pady = 10)
        dish_type_name = CTk.CTkLabel(dish_type_frame, width=200, height=50, text=f"---------{dish_type}---------", font=CTk.CTkFont("Comic Sans MS", size = 25))
        dish_type_name.pack()
        for cost, dish in dishes.items():
            dish_frame(cost, dish, dish_type_frame)
    button_leave = CTk.CTkButton(app, width=140, height=28, text="Выйти", command=main_screen, fg_color="red", hover_color="#7A0303", font = CTk.CTkFont("Comfortaa", size = 15, weight="bold"))
    button_leave.pack()

def check_register():
    global data
    if re.fullmatch(r"\w+@\w+\.\w+", email_textbox.get()):
        data = open("Data.txt", "r")
        for line in data:
            email = line.split()[0]
            login = line.split()[1]
            if email == email_textbox.get() or login == login_textbox.get():
                button_check.configure(fg_color="red", hover_color="red")
                app.after(500, lambda: button_check.configure(fg_color='#1F6AA5', hover_color='#1F6AA5'))
                data.close()
                return
        data = open("Data.txt", "a")
        data.write(f"{email_textbox.get()} {login_textbox.get()} {name_textbox.get().split()[0]} {name_textbox.get().split()[1]}\n")
        button_check.configure(fg_color="green", hover_color="green")
        app.after(500, lambda: button_check.configure(fg_color='#1F6AA5', hover_color='#1F6AA5'))
        data.close()
    else:
        button_check.configure(fg_color="red", hover_color="red")
        app.after(500, lambda: button_check.configure(fg_color='#1F6AA5', hover_color='#1F6AA5'))
    
def check_log_in():
    data = open("Data.txt", "r")
    for line in data:
        email = line.split()[0]
        login = line.split()[1]
        surname = line.split()[2]
        name = line.split()[3]
        if email.lower() == email_textbox.get().lower() and login.lower() == login_textbox.get().lower():
            opened = open("Opened.txt", "w")
            opened.write(f"{email} {login}")
            opened.close()
            line = line.split()
            return open_account(line)
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
    data = open("Data.txt", "r")
    for user in opened:
        user = user.split()
        email = user[0]
        login = user[1]
        for line in data:
            line = line.split()
            if email == line[0] and login == line[1]:
                return open_account(line)
    return main_screen()

check_opened()
app.mainloop()