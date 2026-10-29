"""
tracker.py - Storage and reporting for vaccination records.

ONE data structure is used for storage: a DICTIONARY whose keys are the
unique record IDs (e.g. "VR-001") and whose values are VaccinationRecord
objects. Dictionary look-up by ID is fast and avoids duplicates.
"""

from models import VaccinationRecord, STATUS_LABELS


class VaccinationTracker:
    def __init__(self):
        self.records = {}  # {record_id: VaccinationRecord}

    def add_record(self, record):
        """Add a record to the dictionary (the 'add' function)."""
        if record.record_id in self.records:
            raise KeyError(f"Record {record.record_id} already exists.")
        self.records[record.record_id] = record
        return record

    def display_records(self):
        """Loop through the dictionary and print every record (the 'display' function)."""
        if not self.records:
            print("No records stored yet.")
            return
        print("ID     | Code  | Age   | District     | Vaccine      | Doses | Last dose  | Status")
        print("-" * 88)
        for record_id in sorted(self.records):
            self.records[record_id].display_info()

    def get_record(self, record_id):
        """Return a record or None if the ID is unknown."""
        return self.records.get(record_id.upper())

    def status_summary(self):
        """Count records by status, returned as a dictionary."""
        counts = {label: 0 for label in STATUS_LABELS}
        for record in self.records.values():
            counts[record.get_status()] += 1
        return counts

    def display_summary(self):
        print(f"Total records in tracker: {len(self.records)} "
              f"(created this session: {VaccinationRecord.total_records_created()})")
        for label, count in self.status_summary().items():
            print(f"  {label:<12}: {count}")
