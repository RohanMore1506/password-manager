from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    new_password = "".join(password_list)
    password_entry.insert(0, new_password)
    pyperclip.copy(new_password)
# ---------------------------- SAVE PASSWORD ------------------------------- #


def add_entry():
    site = website_entry.get().title()
    mail = email_entry.get()
    gen_pass = password_entry.get()
    new_data = {
        site: {
            "email": mail,
            "password": gen_pass,
        }
    }
    if not site or not mail or not gen_pass:
        messagebox.showerror(title="Field Empty", message="No field should be empty")
    else:
        try:
            with open("Password Manager.json", "r") as file:
                data_json = json.load(file)
        except FileNotFoundError:
            with open("Password Manager.json", "w") as file:
                json.dump(new_data, file, indent=4)
        else:
            data_json.update(new_data)
            with open("Password Manager.json", "w") as file:
                json.dump(data_json, file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)

# ---------------------------- SEARCH PASSWORD ------------------------------- #


def search_website():
    site_input = website_entry.get().title()
    try:
        with open("Password Manager.json") as file:
            data_json = json.load(file)
    except FileNotFoundError:
        messagebox.showerror(title="Oops", message="Data File Not Found")
    else:
        if site_input in data_json:
            mail = data_json[site_input]["email"]
            req_pass = data_json[site_input]["password"]
            messagebox.showinfo(title=site_input, message=f"Email    : {mail}\n"
                                                          f"Password : {req_pass}")
        else:
            messagebox.showerror(title="ERROR", message="No details for website exists")
    finally:
        website_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(pady=40, padx=40)
canvas = Canvas(width=200, height=200)
lock_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=lock_img)
canvas.grid(row=0, column=1)

# ---------------------------- Buttons, Entries and Labels ------------------------------- #

website = Label(text="Website:")
website.grid(row=1, column=0)

website_entry = Entry(width=33)
website_entry.focus()
website_entry.grid(row=1, column=1)

email = Label(text="Email/Username:")
email.grid(row=2, column=0)

email_entry = Entry(width=52)
email_entry.insert(0, string="rsm@gmail.com")
email_entry.grid(row=2, column=1, columnspan=2)

password = Label(text="Password:")
password.grid(row=3, column=0)

password_entry = Entry(width=33)
password_entry.grid(row=3, column=1)

generate_button = Button(text="Generate Password", command=generate_password)
generate_button.grid(row=3, column=2)

add_password = Button(text="Add", width=44, command=add_entry)
add_password.grid(row=4, column=1, columnspan=2)

search_button = Button(text="Search", width=14, command=search_website)
search_button.grid(row=1, column=2)

window.mainloop()
