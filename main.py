import smtplib
import datetime as dt
from tkinter import messagebox
import random
import pandas

from_email = "your email @gmail.com"
password = "your app password"
to_email = "email address receiver"
data = None
celebrated = {}


def check_file_for_birthday_and_create_dict():
    global data, celebrated
    time_now = dt.datetime.now()

    try:
        data = pandas.read_csv("birthdays.csv")
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="File does not exist")

    celebrated = {(data_row["month"], data_row["day"], data_row["name"]): data_row
                  for (index, data_row) in data.iterrows()
                  if data_row.month == time_now.month and data_row.day == time_now.day}

    if celebrated:
        prepare_and_send_letter()
    else:
        messagebox.showinfo(title="Info", message="No birthdays today!")


def prepare_and_send_letter():
    for name in celebrated:
        celebrated_person = celebrated[name]
        letter_number = random.randint(1, 3)
        try:
            with open(f"letter_templates/letter_{letter_number}.txt", mode='r') as my_letter:
                message = my_letter.read()

        except FileNotFoundError:
            messagebox.showerror(title="Error", message="File does not exist")
        else:
            send_letter(message.replace("[NAME]", celebrated_person["name"]))


def send_letter(message):
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=to_email, password=password)
        connection.sendmail(from_addr=to_email, to_addrs=to_email, msg=f"Subject:Happy Birthday\n\n{message}")


check_file_for_birthday_and_create_dict()
