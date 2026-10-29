"""
main.py - Community Vaccination Tracker (PROG211 Object-Oriented Programming 1)

Run:  python main.py          -> interactive menu
      python main.py --demo   -> automatic demonstration with sample data
"""

import sys
from datetime import date, datetime

from models import Vaccine, Recipient, VaccinationRecord, AGE_GROUPS
from tracker import VaccinationTracker

# Fixed reference data kept as a tuple of tuples: (name, doses, min gap in days)
VACCINE_CATALOGUE = (
    ("Measles", 2, 28),
    ("COVID-19", 2, 21),
    ("Polio", 3, 28),
    ("Yellow Fever", 1, 0),
)


def build_vaccines():
    """Create Vaccine objects from the catalogue; returns {name: Vaccine}."""
    return {name: Vaccine(name, doses, gap) for name, doses, gap in VACCINE_CATALOGUE}


def demo(tracker, vaccines):
    print("=== DEMONSTRATION: Community Vaccination Tracker ===\n")
    print("--- Vaccines available ---")
    for vaccine in vaccines.values():
        vaccine.display_info()

    print("\n--- Task 1: creating objects ---")
    child = Recipient.from_age(3, "Western Area")
    adult = Recipient("15-49", "Bo")
    elder = Recipient.from_age(67, "Kenema")
    for person in (child, adult, elder):
        person.display_info()

    print("\n--- Task 2: adding records to the dictionary ---")
    r1 = tracker.add_record(VaccinationRecord(child, vaccines["Measles"]))
    r2 = tracker.add_record(VaccinationRecord(adult, vaccines["COVID-19"]))
    r3 = tracker.add_record(VaccinationRecord(elder, vaccines["Yellow Fever"]))
    print(f"Added: {r1.record_id}, {r2.record_id}, {r3.record_id}")

    print("\n--- Task 3: instance method administer_dose() ---")
    print(r1.administer_dose(date(2026, 9, 1))[1])
    print(r1.administer_dose(date(2026, 9, 10))[1])   # too early
    print(r1.administer_dose(date(2026, 10, 1))[1])   # valid
    print(r1.administer_dose(date(2026, 11, 1))[1])   # already complete
    print(r2.administer_dose(date(2026, 9, 5))[1])
    print(r3.administer_dose(date(2026, 9, 8))[1])

    print("\n--- update_record(): move recipient to another district ---")
    r2.update_record(district="Freetown")
    r2.display_info()

    print("\n--- All records ---")
    tracker.display_records()

    print("\n--- Summary (class method + dictionary counts) ---")
    tracker.display_summary()
    print("\nStatic check: Recipient.age_to_group(10) ->", Recipient.age_to_group(10))


def ask_choice(prompt, options):
    """Ask until the user types one of the options (case-insensitive)."""
    lookup = {option.lower(): option for option in options}
    while True:
        value = input(prompt).strip().lower()
        if value in lookup:
            return lookup[value]
        print(f"  Please choose one of: {', '.join(options)}")


def ask_date(prompt):
    while True:
        text = input(prompt).strip()
        try:
            return datetime.strptime(text, "%Y-%m-%d").date()
        except ValueError:
            print("  Use the format YYYY-MM-DD (e.g. 2026-10-05).")


def menu(tracker, vaccines):
    options = {
        "1": "Register recipient & start vaccination record",
        "2": "Record a dose",
        "3": "Display all records",
        "4": "Show summary",
        "5": "Exit",
    }
    while True:
        print("\n===== Community Vaccination Tracker =====")
        for key, text in options.items():
            print(f" {key}. {text}")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            try:
                age = int(input("Age in years (stored only as an age group): "))
            except ValueError:
                print("  Error: age must be a whole number.")
                continue
            district = input("District: ").strip()
            if not district:
                print("  District cannot be empty.")
                continue
            try:
                recipient = Recipient.from_age(age, district)
            except ValueError as error:
                print(f"  Error: {error}")
                continue
            print("Vaccines:", ", ".join(vaccines))
            name = ask_choice("Vaccine name: ", tuple(vaccines))
            record = tracker.add_record(VaccinationRecord(recipient, vaccines[name]))
            print(f"Created {record.record_id} for anonymous code {recipient.recipient_id}.")
        elif choice == "2":
            record = tracker.get_record(input("Record ID (e.g. VR-001): "))
            if record is None:
                print("  Record not found.")
                continue
            ok, message = record.administer_dose(ask_date("Dose date (YYYY-MM-DD): "))
            print(("  OK: " if ok else "  Not recorded: ") + message)
        elif choice == "3":
            tracker.display_records()
        elif choice == "4":
            tracker.display_summary()
        elif choice == "5":
            print("Goodbye - stay healthy!")
            break
        else:
            print("  Invalid option, please choose 1-5.")


if __name__ == "__main__":
    tracker = VaccinationTracker()
    vaccines = build_vaccines()
    if "--demo" in sys.argv:
        demo(tracker, vaccines)
    else:
        try:
            menu(tracker, vaccines)
        except (EOFError, KeyboardInterrupt):
            print("\nProgram closed. Goodbye!")
