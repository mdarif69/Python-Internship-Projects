
import tkinter as tk
from tkinter import messagebox
import secrets
import string


def generate_password():
    try:
        length = int(length_entry.get())

        if length < 4 or length > 128:
            messagebox.showerror(
                "Invalid Length",
                "Enter a password length between 4 and 128."
            )
            return

        characters = ""
        required = []

        if upper_var.get():
            characters += string.ascii_uppercase
            required.append(secrets.choice(string.ascii_uppercase))

        if lower_var.get():
            characters += string.ascii_lowercase
            required.append(secrets.choice(string.ascii_lowercase))

        if number_var.get():
            characters += string.digits
            required.append(secrets.choice(string.digits))

        if symbol_var.get():
            symbols = "!@#$%^&*()-_=+?"
            characters += symbols
            required.append(secrets.choice(symbols))

        if not characters:
            messagebox.showwarning(
                "Select Options",
                "Please select at least one character type."
            )
            return

        if length < len(required):
            messagebox.showerror(
                "Invalid Length",
                "Increase the length to match selected options."
            )
            return

        password = required[:]

        while len(password) < length:
            password.append(secrets.choice(characters))

        secrets.SystemRandom().shuffle(password)
        final_password = "".join(password)

        password_entry.config(state="normal")
        password_entry.delete(0, tk.END)
        password_entry.insert(0, final_password)
        password_entry.config(state="readonly")

        status_label.config(
            text="Password generated successfully!",
            fg="#16a34a"
        )

    except ValueError:
        messagebox.showerror(
            "Invalid Input",
            "Please enter a valid number."
        )


def copy_password():
    password = password_entry.get()

    if not password:
        messagebox.showwarning(
            "No Password",
            "Generate a password first."
        )
        return

    root.clipboard_clear()
    root.clipboard_append(password)
    root.update()

    status_label.config(
        text="Password copied to clipboard!",
        fg="#16a34a"
    )


def clear_password():
    password_entry.config(state="normal")
    password_entry.delete(0, tk.END)
    password_entry.config(state="readonly")
    status_label.config(text="")


root = tk.Tk()
root.title("Password Generator")
root.geometry("480x590")
root.resizable(False, False)
root.configure(bg="#f1f5f9")

# Header
header = tk.Frame(root, bg="#172554", height=120)
header.pack(fill="x")
header.pack_propagate(False)

tk.Label(
    header,
    text="PASSWORD GENERATOR",
    font=("Arial", 20, "bold"),
    bg="#172554",
    fg="white"
).pack(pady=(25, 5))

tk.Label(
    header,
    text="Create a strong and secure password",
    font=("Arial", 10),
    bg="#172554",
    fg="#bfdbfe"
).pack()

# Main card
card = tk.Frame(
    root,
    bg="white",
    padx=28,
    pady=20,
    highlightbackground="#e2e8f0",
    highlightthickness=1
)
card.pack(fill="both", expand=True, padx=22, pady=20)

tk.Label(
    card,
    text="Password Length",
    font=("Arial", 11, "bold"),
    bg="white",
    fg="#1e293b"
).pack(anchor="w")

length_entry = tk.Entry(
    card,
    font=("Arial", 12),
    relief="solid",
    bd=1
)
length_entry.pack(fill="x", pady=(7, 15), ipady=6)
length_entry.insert(0, "12")

tk.Label(
    card,
    text="Include Characters",
    font=("Arial", 11, "bold"),
    bg="white",
    fg="#1e293b"
).pack(anchor="w", pady=(0, 8))

upper_var = tk.BooleanVar(value=True)
lower_var = tk.BooleanVar(value=True)
number_var = tk.BooleanVar(value=True)
symbol_var = tk.BooleanVar(value=True)


def add_option(text, variable):
    tk.Checkbutton(
        card,
        text=text,
        variable=variable,
        font=("Arial", 10),
        bg="white",
        fg="#334155",
        activebackground="white",
        selectcolor="white"
    ).pack(anchor="w", pady=2)


add_option("Uppercase letters (A-Z)", upper_var)
add_option("Lowercase letters (a-z)", lower_var)
add_option("Numbers (0-9)", number_var)
add_option("Special symbols (!@#$)", symbol_var)

tk.Label(
    card,
    text="Your Password",
    font=("Arial", 11, "bold"),
    bg="white",
    fg="#1e293b"
).pack(anchor="w", pady=(15, 7))

password_entry = tk.Entry(
    card,
    font=("Consolas", 13),
    justify="center",
    readonlybackground="#f8fafc",
    fg="#172554",
    state="readonly",
    relief="solid",
    bd=1
)
password_entry.pack(fill="x", ipady=8)

tk.Button(
    card,
    text="Generate Password",
    command=generate_password,
    font=("Arial", 11, "bold"),
    bg="#2563eb",
    fg="white",
    activebackground="#1d4ed8",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    pady=10
).pack(fill="x", pady=(15, 8))

button_row = tk.Frame(card, bg="white")
button_row.pack(fill="x")

tk.Button(
    button_row,
    text="Copy Password",
    command=copy_password,
    font=("Arial", 10, "bold"),
    bg="#dcfce7",
    fg="#166534",
    relief="flat",
    cursor="hand2",
    pady=8
).pack(side="left", fill="x", expand=True, padx=(0, 5))

tk.Button(
    button_row,
    text="Clear",
    command=clear_password,
    font=("Arial", 10, "bold"),
    bg="#fee2e2",
    fg="#991b1b",
    relief="flat",
    cursor="hand2",
    pady=8
).pack(side="left", fill="x", expand=True, padx=(5, 0))

status_label = tk.Label(
    card,
    text="",
    font=("Arial", 9),
    bg="white"
)
status_label.pack(pady=(8, 0))

root.mainloop()
