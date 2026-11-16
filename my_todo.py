import json
import os
import tkinter as tk
from tkinter import messagebox, simpledialog

FILE = "tasks.json"

# ---------- Theme ----------
BG = "#eef4ff"
CARD = "#ffffff"
ROW_ALT = "#f6f9ff"
TEXT = "#1e293b"
MUTED = "#94a3b8"
BORDER = "#dbe5f5"
PRIMARY = ("#2b7bf0", "#1d63cc")   # (normal, hover)
SUCCESS = ("#12a87f", "#0d8564")
WARNING = ("#ff9a1a", "#e08100")
DANGER = ("#f02d55", "#cc1d42")
FONT = "Segoe UI"
PLACEHOLDER = "Naya task likho..."


# ---------- Data ----------
def load_tasks():
    if os.path.exists(FILE):
        with open(FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_tasks():
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2)


# ---------- UI helpers ----------
def refresh():
    listbox.delete(0, tk.END)
    for i, t in enumerate(tasks, 1):
        mark = "✓" if t["done"] else "○"
        listbox.insert(tk.END, f"   {i}.    {mark}    {t['text']}")
        listbox.itemconfig(tk.END, bg=ROW_ALT if i % 2 == 0 else CARD,
                           fg=MUTED if t["done"] else TEXT)
    done = sum(t["done"] for t in tasks)
    counter.config(text=f"{len(tasks) - done} pending  •  {done} done")


def set_placeholder():
    entry.delete(0, tk.END)
    entry.insert(0, PLACEHOLDER)
    entry.config(fg=MUTED)


def on_focus_in(_):
    if entry.cget("fg") == MUTED:
        entry.delete(0, tk.END)
        entry.config(fg=TEXT)


def on_focus_out(_):
    if not entry.get():
        set_placeholder()


def make_button(parent, text, colors, cmd):
    b = tk.Button(parent, text=text, bg=colors[0], fg="white",
                  activebackground=colors[1], activeforeground="white",
                  font=(FONT, 11, "bold"), relief="flat", bd=0,
                  cursor="hand2", command=cmd)
    b.bind("<Enter>", lambda e: b.config(bg=colors[1]))
    b.bind("<Leave>", lambda e: b.config(bg=colors[0]))
    return b


def get_selected():
    sel = listbox.curselection()
    if not sel:
        messagebox.showwarning("No selection", "Pehle ek task select karo.")
        return None
    return sel[0]


# ---------- Actions ----------
def add_task():
    text = entry.get().strip()
    if entry.cget("fg") == MUTED or not text:
        messagebox.showwarning("Empty", "Pehle task likho.")
        return
    tasks.append({"text": text, "done": False})
    entry.delete(0, tk.END)
    save_tasks()
    refresh()


def toggle_task(_=None):
    i = get_selected()
    if i is not None:
        tasks[i]["done"] = not tasks[i]["done"]
        save_tasks()
        refresh()


def edit_task():
    i = get_selected()
    if i is None:
        return
    new = simpledialog.askstring("Edit Task", "Task update karo:",
                                 initialvalue=tasks[i]["text"])
    if new and new.strip():
        tasks[i]["text"] = new.strip()
        save_tasks()
        refresh()


def delete_task():
    i = get_selected()
    if i is not None and messagebox.askyesno("Delete", "Ye task delete karna hai?"):
        tasks.pop(i)
        save_tasks()
        refresh()


# ---------- Window ----------
tasks = load_tasks()

root = tk.Tk()
root.title("My To-Do List")
root.geometry("580x620")
root.minsize(480, 520)
root.configure(bg=BG)

# Header
header = tk.Frame(root, bg=BG)
header.pack(fill="x", padx=24, pady=(20, 8))
tk.Label(header, text="✓  MY TO-DO LIST", font=(FONT, 20, "bold"),
         bg=BG, fg="#0b2a6f").pack(anchor="w")
counter = tk.Label(header, text="", font=(FONT, 10), bg=BG, fg="#64748b")
counter.pack(anchor="w", pady=(2, 0))

# Add row
add_row = tk.Frame(root, bg=BG)
add_row.pack(fill="x", padx=24, pady=8)

entry_box = tk.Frame(add_row, bg=CARD, highlightbackground=BORDER,
                     highlightcolor=PRIMARY[0], highlightthickness=2)
entry_box.pack(side="left", fill="x", expand=True)
entry = tk.Entry(entry_box, font=(FONT, 12), bd=0, bg=CARD, fg=TEXT,
                 insertbackground=TEXT)
entry.pack(fill="x", padx=10, ipady=9)
entry.bind("<FocusIn>", on_focus_in)
entry.bind("<FocusOut>", on_focus_out)
entry.bind("<Return>", lambda e: add_task())

make_button(add_row, "+ Add", PRIMARY, add_task).pack(
    side="left", padx=(8, 0), ipadx=14, ipady=7)

# List card
card = tk.Frame(root, bg=CARD, highlightbackground=BORDER, highlightthickness=1)
card.pack(fill="both", expand=True, padx=24, pady=8)

scroll = tk.Scrollbar(card)
scroll.pack(side="right", fill="y")
listbox = tk.Listbox(card, font=(FONT, 12), bd=0, highlightthickness=0,
                     bg=CARD, fg=TEXT, selectbackground="#d6e6ff",
                     selectforeground=TEXT, activestyle="none",
                     yscrollcommand=scroll.set)
listbox.pack(side="left", fill="both", expand=True, ipady=4)
scroll.config(command=listbox.yview)
listbox.bind("<Double-Button-1>", toggle_task)

# Buttons
btn_row = tk.Frame(root, bg=BG)
btn_row.pack(fill="x", padx=24, pady=(8, 20))
for text, colors, cmd in [("✓ Complete / Undo", SUCCESS, toggle_task),
                          ("✎ Edit", WARNING, edit_task),
                          ("✕ Delete", DANGER, delete_task)]:
    make_button(btn_row, text, colors, cmd).pack(
        side="left", expand=True, fill="x", padx=4, ipady=8)

set_placeholder()
refresh()
root.mainloop()