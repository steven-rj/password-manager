from tkinter import *
from tkinter import messagebox
from random import shuffle, randint, choice
import pyperclip
import json


def generate_password():
    """
    creates a password of variable length, comprised of random numbers, symbols, letters
    :return: None
    """
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '?']
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_numbers + password_symbols + password_letters
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)  # place password on password field
    pyperclip.copy(password)  # copy password to clipboard for convenience


def save_info():
    """
    saves data from site, username, password fields into a json file
    :return: None
    """
    # get info from each field
    site = site_entry.get()
    site = site.strip().lower()
    user = email_entry.get()
    passw = password_entry.get()
    new_info = {site: {"email": user, "password": passw}}

    # verify non-empty fields
    if len(site) == 0 or len(passw) == 0 or len(user) == 0:
        messagebox.showinfo(title="Oops!", message="You left a field blank..")
    else:
        # confirmation popup
        is_valid = messagebox.askokcancel(title=site, message=f"Entering:\n{site}\n{user}\n{passw}")
        if is_valid:
            try:
                # check if file already exists and load it
                with open("data.json", "r") as file:
                    data = json.load(file)

            except FileNotFoundError:
                # if file doesn't exist, create it and write to it
                with open("data.json", "w") as file:
                    json.dump(new_info, file, indent=4)
            else:
                # otherwise, simply write the inputs to it
                data.update(new_info)

                # write the updated data to the password file
                with open("data.json", "w") as file:
                    json.dump(new_info, file, indent=4)

            finally:
                # clear all fields on form except email
                site_entry.delete(0, END)
                password_entry.delete(0, END)
                site_entry.focus()


def search():
    """
    searches json file for a specified site name, pops up its associated user/pass
    :return: None
    """
    site = site_entry.get()
    site = site.strip().lower()
    try:
        with open("data.json") as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No password file found.")
    else:
        if site in data:
            email = data[site]['email']
            passw = data[site]['password']
            messagebox.showinfo(title=site, message=f"Email: {email}\nPassword: {passw}")
        else:
            messagebox.showinfo(title="Error", message=f"No data found for {site}")


# main UI setup
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

# logo
canvas = Canvas(width=200, height=200, highlightthickness=0)
logo_image = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_image)
canvas.grid(column=1, row=0)

# website area
site_label = Label(text="Website:")
site_label.grid(column=0, row=1)

site_entry = Entry(width=21)
site_entry.grid(column=1, row=1, sticky="EW")
site_entry.focus()

search_button = Button(text="Search", command=search)
search_button.grid(column=2, row=1, sticky="EW")

# email/username area
email_label = Label(text="Email/Username:")
email_label.grid(column=0, row=2)

email_entry = Entry(width=35)
email_entry.grid(column=1, row=2, columnspan=2, sticky="EW")
email_entry.insert(0, "srjordan82@gmail.com")

# password area
password_label = Label(text="Password:")
password_label.grid(column=0, row=3)

password_entry = Entry(width=21)
password_entry.grid(column=1, row=3, sticky="EW")

password_button = Button(text="Generate Password", command=generate_password)
password_button.grid(column=2, row=3, sticky="EW")

# add button
add_button = Button(text="Add", width=35, command=save_info)
add_button.grid(column=1, row=4, columnspan=2, sticky="EW")

# runs the tkinter app
window.mainloop()
