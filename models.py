"""
models.py - Core classes for the Community Vaccination Tracker (PROG211 OOP1).

Classes
-------
Vaccine            : describes a vaccine and its dosing rules.
Recipient          : an ANONYMOUS person who is vaccinated (no name, no exact age).
VaccinationRecord  : links one Recipient to one Vaccine and tracks doses given.

DPG note: privacy is built into the design. Only an auto-generated code,
an age GROUP and a district are stored - never names, phone numbers or
exact dates of birth.
"""

from datetime import date

# Tuples are used for fixed (immutable) reference data.
AGE_GROUPS = ("0-4", "5-14", "15-49", "50+")
STATUS_LABELS = ("Not started", "In progress", "Complete")


class Vaccine:
    """A vaccine and the rules for how it must be given."""

    def __init__(self, name, doses_required, min_interval_days):
        if doses_required < 1:
            raise ValueError("A vaccine needs at least one dose.")
        if min_interval_days < 0:
            raise ValueError("Interval between doses cannot be negative.")
        self.name = name
        self.doses_required = doses_required
        self.min_interval_days = min_interval_days

    def display_info(self):
        """Print a short description of the vaccine."""
        print(f"Vaccine: {self.name} | Doses required: {self.doses_required} "
              f"| Minimum gap between doses: {self.min_interval_days} days")


class Recipient:
    """An anonymous vaccine recipient (privacy-respecting by design)."""

    _counter = 0  # class attribute shared by all Recipient objects

    def __init__(self, age_group, district):
        if not Recipient.is_valid_age_group(age_group):
            raise ValueError(f"Age group must be one of {AGE_GROUPS}.")
        self.recipient_id = Recipient.next_code()
        self.age_group = age_group
        self.district = district.strip().title()

    # ---- class methods -------------------------------------------------
    @classmethod
    def next_code(cls):
        """Generate the next anonymous code, e.g. R-001."""
        cls._counter += 1
        return f"R-{cls._counter:03d}"

    @classmethod
    def from_age(cls, age, district):
        """Alternative constructor: converts an exact age into an age group
        so that the exact age is never stored (data minimisation)."""
        return cls(cls.age_to_group(age), district)

    # ---- static methods ------------------------------------------------
    @staticmethod
    def is_valid_age_group(group):
        return group in AGE_GROUPS

    @staticmethod
    def age_to_group(age):
        if age < 0 or age > 120:
            raise ValueError("Age must be between 0 and 120.")
        if age <= 4:
            return AGE_GROUPS[0]
        if age <= 14:
            return AGE_GROUPS[1]
        if age <= 49:
            return AGE_GROUPS[2]
        return AGE_GROUPS[3]

    # ---- instance method -----------------------------------------------
    def display_info(self):
        print(f"Recipient {self.recipient_id} | Age group: {self.age_group} "
              f"| District: {self.district}")


class VaccinationRecord:
    """Tracks the doses of ONE vaccine given to ONE recipient.

    This class shows interaction between objects: it uses a Recipient
    and a Vaccine and checks the Vaccine's rules before adding a dose.
    """

    _record_count = 0

    def __init__(self, recipient, vaccine):
        VaccinationRecord._record_count += 1
        self.record_id = f"VR-{VaccinationRecord._record_count:03d}"
        self.recipient = recipient
        self.vaccine = vaccine
        self.doses_received = 0
        self.last_dose_date = None

    # ---- class method --------------------------------------------------
    @classmethod
    def total_records_created(cls):
        """Return how many records have been created so far."""
        return cls._record_count

    # ---- static method -------------------------------------------------
    @staticmethod
    def days_between(earlier, later):
        return (later - earlier).days

    # ---- instance methods ----------------------------------------------
    def get_status(self):
        """Return 'Not started', 'In progress' or 'Complete'."""
        if self.doses_received == 0:
            return STATUS_LABELS[0]
        if self.doses_received >= self.vaccine.doses_required:
            return STATUS_LABELS[2]
        return STATUS_LABELS[1]

    def administer_dose(self, dose_date):
        """Try to record a dose. Returns a tuple: (success, message)."""
        if not isinstance(dose_date, date):
            return (False, "Invalid date supplied.")
        if self.get_status() == STATUS_LABELS[2]:
            return (False, "Course already complete - no more doses needed.")
        if self.last_dose_date is not None:
            gap = VaccinationRecord.days_between(self.last_dose_date, dose_date)
            if gap < 0:
                return (False, "Dose date is before the previous dose.")
            if gap < self.vaccine.min_interval_days:
                return (False, f"Too early: wait {self.vaccine.min_interval_days} "
                               f"days between doses (only {gap} passed).")
        self.doses_received += 1
        self.last_dose_date = dose_date
        return (True, f"Dose {self.doses_received} of "
                      f"{self.vaccine.doses_required} recorded on {dose_date}.")

    def update_record(self, district=None, age_group=None):
        """Update non-sensitive details of the recipient."""
        if district:
            self.recipient.district = district.strip().title()
        if age_group:
            if not Recipient.is_valid_age_group(age_group):
                raise ValueError(f"Age group must be one of {AGE_GROUPS}.")
            self.recipient.age_group = age_group

    def display_info(self):
        last = self.last_dose_date if self.last_dose_date else "N/A"
        print(f"{self.record_id} | {self.recipient.recipient_id} | "
              f"{self.recipient.age_group:<5} | {self.recipient.district:<12} | "
              f"{self.vaccine.name:<12} | "
              f"{self.doses_received}/{self.vaccine.doses_required:<3} | "
              f"{str(last):<10} | {self.get_status()}")
