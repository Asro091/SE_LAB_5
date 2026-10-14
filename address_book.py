
"""Contact and address book manager.

Supports contact management, searching, city grouping, CSV export,
and safe JSON-based backup and restore.
"""

import csv
import hashlib
import json
import re
from pathlib import Path

DEFAULT_CSV_FILE = "contacts.csv"
DEFAULT_BACKUP_FILE = "contacts.bak"

ContactInfo = dict[str, str]
ContactBook = dict[str, ContactInfo]

contacts: ContactBook = {}


def add_contact(
    full_name: str,
    phone: str,
    email: str = "",
    city: str = "Unknown",
) -> bool:
    """Add a contact after validating the phone number."""
    if not re.fullmatch(r"[0-9]{10}", phone):
        print("Invalid phone number for", full_name)
        return False

    contacts[full_name] = {
        "phone": phone,
        "email": email,
        "city": city,
    }
    return True


def contact_id(full_name: str) -> str:
    """Return a stable, short identifier for a contact name."""
    return hashlib.sha256(full_name.encode("utf-8")).hexdigest()[:6]


def search_contacts(search_text: str) -> list[str]:
    """Find contacts by a partial name or phone number."""
    search_term = search_text.casefold()
    found = []

    for name, info in contacts.items():
        if search_term in name.casefold() or search_text in info["phone"]:
            found.append(name)

    return found


def update_city(full_name: str, city: str) -> bool:
    """Update a contact's city if the contact exists."""
    contact = contacts.get(full_name)

    if contact is None:
        print("No contact named", full_name)
        return False

    contact["city"] = city
    return True


def contacts_by_city() -> dict[str, list[str]]:
    """Group contact names by city."""
    grouped: dict[str, list[str]] = {}

    for name, info in contacts.items():
        grouped.setdefault(info["city"], []).append(name)

    return grouped


def print_directory() -> None:
    """Print a numbered directory of contacts."""
    for index, name in enumerate(sorted(contacts), start=1):
        print(index, name, contacts[name]["phone"])


def export_csv(file_name: str = DEFAULT_CSV_FILE) -> None:
    """Export all contacts to a CSV file with column headers."""
    with Path(file_name).open(
        "w", newline="", encoding="utf-8"
    ) as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Name", "Phone", "Email", "City"])

        for name, info in contacts.items():
            writer.writerow([
                name,
                info["phone"],
                info["email"],
                info["city"],
            ])


def backup_book(file_name: str = DEFAULT_BACKUP_FILE) -> None:
    """Save a JSON backup instead of using unsafe pickle serialization."""
    with Path(file_name).open("w", encoding="utf-8") as backup_file:
        json.dump(contacts, backup_file, indent=2)


def restore_book(file_name: str = DEFAULT_BACKUP_FILE) -> ContactBook:
    """Restore and validate contacts from a JSON backup."""
    with Path(file_name).open("r", encoding="utf-8") as backup_file:
        restored = json.load(backup_file)

    if not isinstance(restored, dict):
        raise ValueError("Backup must contain a contact dictionary.")

    for name, info in restored.items():
        if not isinstance(name, str) or not isinstance(info, dict):
            raise ValueError("Invalid contact entry in backup.")

        if not all(
            isinstance(info.get(field), str)
            for field in ("phone", "email", "city")
        ):
            raise ValueError(f"Invalid contact data for {name}.")

        if not re.fullmatch(r"[0-9]{10}", info["phone"]):
            raise ValueError(f"Invalid phone number for {name}.")

    return restored


def main() -> None:
    """Run a demonstration of the address book."""
    add_contact(
        "Neha Sharma",
        "9876543210",
        "neha@example.com",
        "Bengaluru",
    )
    add_contact(
        "Rahul Verma",
        "9123456780",
        "rahul@example.com",
        "Mysuru",
    )
    add_contact("Test User", "12345")
    add_contact("Kavya Nair", "9988776655", city="Bengaluru")

    update_city("Rahul Verma", "Chennai")
    update_city("Nobody", "Delhi")

    print_directory()
    print("Search 'ra':", search_contacts("ra"))
    print("By city:", contacts_by_city())
    print("ID for Neha:", contact_id("Neha Sharma"))

    export_csv()
    backup_book()
    restored = restore_book()

    print(
        "Contacts restored:",
        len(restored),
        "| first:",
        sorted(restored)[0],
    )
    print(
        "Restored contacts match the in-memory address book:",
        restored == contacts,
    )


if __name__ == "__main__":
    main()
