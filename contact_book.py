import json
import os

FILE = "contacts.json"


def load_contacts():
    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            return json.load(f)
    return []


def save_contacts(contacts):
    with open(FILE, "w") as f:
        json.dump(contacts, f, indent=4)


def add_contact(contacts):
    print("\n--- Add Contact ---")
    contact = {
        "name": input("Enter name: ").strip(),
        "phone": input("Enter phone number: ").strip(),
        "email": input("Enter email: ").strip(),
        "address": input("Enter address: ").strip()
    }

    if not all(contact.values()):
        print("All fields are required!")
        return

    contacts.append(contact)
    save_contacts(contacts)
    print("Contact added successfully!")


def view_contacts(contacts):
    print("\n--- Contact List ---")
    if not contacts:
        print("No contacts found.")
        return

    for i, c in enumerate(contacts, 1):
        print(f"\n{i}. Name: {c['name']}")
        print(f"   Phone: {c['phone']}")
        print(f"   Email: {c['email']}")
        print(f"   Address: {c['address']}")


def search_contact(contacts):
    query = input("Enter name or phone number to search: ").strip().lower()

    found = [
        c for c in contacts
        if query in c["name"].lower() or query in c["phone"].lower()
    ]

    if found:
        view_contacts(found)
    else:
        print("Contact not found.")


def update_contact(contacts):
    phone = input("Enter phone number of contact to update: ").strip()

    for c in contacts:
        if c["phone"] == phone:
            print("Press Enter to keep the existing value.")

            name = input(f"Name [{c['name']}]: ").strip()
            new_phone = input(f"Phone [{c['phone']}]: ").strip()
            email = input(f"Email [{c['email']}]: ").strip()
            address = input(f"Address [{c['address']}]: ").strip()

            c["name"] = name or c["name"]
            c["phone"] = new_phone or c["phone"]
            c["email"] = email or c["email"]
            c["address"] = address or c["address"]

            save_contacts(contacts)
            print("Contact updated successfully!")
            return

    print("Contact not found.")


def delete_contact(contacts):
    phone = input("Enter phone number of contact to delete: ").strip()

    for c in contacts:
        if c["phone"] == phone:
            contacts.remove(c)
            save_contacts(contacts)
            print("Contact deleted successfully!")
            return

    print("Contact not found.")


def main():
    contacts = load_contacts()

    while True:
        print("\n===== PYTHON CONTACT BOOK =====")
        print("1. Add Contact")
        print("2. View Contact List")
        print("3. Search Contact")
        print("4. Update Contact")
        print("5. Delete Contact")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            add_contact(contacts)
        elif choice == "2":
            view_contacts(contacts)
        elif choice == "3":
            search_contact(contacts)
        elif choice == "4":
            update_contact(contacts)
        elif choice == "5":
            delete_contact(contacts)
        elif choice == "6":
            print("Thank you for using Contact Book!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()