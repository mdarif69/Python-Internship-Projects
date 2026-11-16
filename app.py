from flask import Flask, render_template_string, request, redirect, url_for
import json
import os

app = Flask(__name__)
FILE = "contacts.json"

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Contact Book</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
    body {
        font-family: Arial, sans-serif;
        background: #f1f5f9;
        margin: 0;
        padding: 10px;
    }

    .container {
        max-width: 1100px;
        width: 95%;
        margin: auto;
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-sizing: border-box;
    }

    h1 {
        text-align: center;
        color: #2563eb;
    }

    input, button {
        width: 100%;
        padding: 12px;
        margin: 7px 0;
        box-sizing: border-box;
        border-radius: 6px;
    }

    input {
        border: 1px solid #ccc;
    }

    button {
        background: #2563eb;
        color: white;
        border: none;
        cursor: pointer;
    }

    .contact {
        background: #f1f5f9;
        padding: 15px;
        margin-top: 12px;
        border-radius: 8px;
        overflow-wrap: anywhere;
    }

    .delete { background: #dc2626; }
    .edit { background: #16a34a; }
    .cancel { background: #64748b; }

    .message {
        background: #dcfce7;
        padding: 10px;
        border-radius: 6px;
        color: #166534;
    }
</style>
<body>
<div class="container">
    <h1>📒 Contact Book</h1>

    {% if message %}
        <p class="message">{{ message }}</p>
    {% endif %}

    {% if editing %}
    <h3>Update Contact</h3>
    <form action="/update/{{ editing.id }}" method="POST">
        <input name="name" placeholder="Full Name"
               value="{{ editing.name }}" required>
        <input name="phone" placeholder="Phone Number"
               value="{{ editing.phone }}" required>
        <input name="email" type="email" placeholder="Email"
               value="{{ editing.email }}" required>
        <input name="address" placeholder="Address"
               value="{{ editing.address }}" required>
        <button class="edit" type="submit">Save Changes</button>
    </form>
    <a href="{{ url_for('home') }}">
        <button class="cancel" type="button">Cancel</button>
    </a>
    {% else %}
    <h3>Add New Contact</h3>
    <form action="/add" method="POST">
        <input name="name" placeholder="Full Name" required>
        <input name="phone" placeholder="Phone Number" required>
        <input name="email" type="email" placeholder="Email" required>
        <input name="address" placeholder="Address" required>
        <button type="submit">Add Contact</button>
    </form>
    {% endif %}

    <h3>Search Contact</h3>
    <form method="GET">
        <input name="q" placeholder="Search by name or phone"
               value="{{ query }}">
        <button type="submit">Search</button>
    </form>

    <h3>Contact List ({{ contacts|length }})</h3>

    {% for c in contacts %}
    <div class="contact">
        <strong>{{ c.name }}</strong>
        <p>Phone: {{ c.phone }}</p>
        <p>Email: {{ c.email }}</p>
        <p>Address: {{ c.address }}</p>

        <a href="{{ url_for('edit_contact', contact_id=c.id) }}">
            <button class="edit" type="button">Edit Contact</button>
        </a>

        <form action="/delete/{{ c.id }}" method="POST"
              onsubmit="return confirm('Delete this contact?')">
            <button class="delete" type="submit">Delete Contact</button>
        </form>
    </div>
    {% else %}
        <p>No contacts found.</p>
    {% endfor %}
</div>
</body>
</html>
"""


def load_contacts():
    if os.path.exists(FILE):
        try:
            with open(FILE, "r", encoding="utf-8") as f:
                contacts = json.load(f)
                if not isinstance(contacts, list):
                    return []
                # Give older contacts an ID if they don't have one.
                changed = False
                for i, contact in enumerate(contacts, start=1):
                    if "id" not in contact:
                        contact["id"] = i
                        changed = True
                if changed:
                    save_contacts(contacts)
                return contacts
        except (json.JSONDecodeError, OSError):
            return []
    return []


def save_contacts(contacts):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(contacts, f, indent=4)


def next_id(contacts):
    return max((c.get("id", 0) for c in contacts), default=0) + 1


@app.route("/")
def home():
    query = request.args.get("q", "").strip().lower()
    message = request.args.get("message", "")
    contacts = load_contacts()

    if query:
        contacts = [
            c for c in contacts
            if query in c["name"].lower()
            or query in c["phone"].lower()
        ]

    return render_template_string(
        HTML,
        contacts=contacts,
        query=request.args.get("q", ""),
        editing=None,
        message=message
    )


@app.route("/add", methods=["POST"])
def add_contact():
    contacts = load_contacts()
    phone = request.form["phone"].strip()

    if any(c["phone"] == phone for c in contacts):
        return redirect(url_for("home", message="Phone number already exists."))

    contacts.append({
        "id": next_id(contacts),
        "name": request.form["name"].strip(),
        "phone": phone,
        "email": request.form["email"].strip(),
        "address": request.form["address"].strip()
    })

    save_contacts(contacts)
    return redirect(url_for("home", message="Contact added successfully!"))


@app.route("/edit/<int:contact_id>")
def edit_contact(contact_id):
    contacts = load_contacts()
    editing = next(
        (c for c in contacts if c.get("id") == contact_id), None
    )

    if editing is None:
        return redirect(url_for("home", message="Contact not found."))

    return render_template_string(
        HTML,
        contacts=contacts,
        query="",
        editing=editing,
        message=""
    )


@app.route("/update/<int:contact_id>", methods=["POST"])
def update_contact(contact_id):
    contacts = load_contacts()
    contact = next(
        (c for c in contacts if c.get("id") == contact_id), None
    )

    if contact is None:
        return redirect(url_for("home", message="Contact not found."))

    phone = request.form["phone"].strip()

    if any(
        c["phone"] == phone and c.get("id") != contact_id
        for c in contacts
    ):
        return redirect(url_for("home", message="Phone number already exists."))

    contact["name"] = request.form["name"].strip()
    contact["phone"] = phone
    contact["email"] = request.form["email"].strip()
    contact["address"] = request.form["address"].strip()

    save_contacts(contacts)
    return redirect(url_for("home", message="Contact updated successfully!"))


@app.route("/delete/<int:contact_id>", methods=["POST"])
def delete_contact(contact_id):
    contacts = load_contacts()
    updated = [c for c in contacts if c.get("id") != contact_id]

    if len(updated) == len(contacts):
        return redirect(url_for("home", message="Contact not found."))

    save_contacts(updated)
    return redirect(url_for("home", message="Contact deleted successfully!"))


if __name__ == "__main__":
    app.run(debug=True)