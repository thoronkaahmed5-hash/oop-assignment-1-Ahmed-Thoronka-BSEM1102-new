# Community Vaccination Tracker

**Module:** PROG211 – Object-Oriented Programming 1 | **Assignment:** Real-World Solutions under DPG Standards
**Domain:** Health – Vaccination Tracker | **Language:** Python 3.8+ (no external libraries)

## 1. Problem Statement
In many communities, vaccination cards get lost and health workers cannot easily see who has finished a
multi-dose course (e.g. Measles, Polio, COVID-19). Missed or too-early doses reduce protection. This program
lets a health worker register recipients **anonymously**, record doses, and check who is complete, in progress
or not started.

## 2. Project Structure
| File | Purpose |
|------|---------|
| `models.py` | Classes `Vaccine`, `Recipient`, `VaccinationRecord` |
| `tracker.py` | Class `VaccinationTracker` – dictionary storage, add/display functions, summary |
| `main.py` | Demo mode and interactive menu |
| `README.md` | This documentation |
| `LICENSE` | MIT open-source licence |

## 3. How to Run
```bash
git clone <your-repository-url>
cd community-vaccination-tracker
python main.py --demo     # automatic demonstration
python main.py            # interactive menu
```

## 4. OOP Concepts Used
| Requirement | Where |
|-------------|-------|
| Two+ classes with attributes & methods | `Vaccine`, `Recipient`, `VaccinationRecord`, `VaccinationTracker` |
| Object creation & interaction | A `VaccinationRecord` combines a `Recipient` and a `Vaccine` and enforces the vaccine's dosing rules |
| One data structure | **Dictionary** `{record_id: VaccinationRecord}` in `VaccinationTracker.records` |
| Add / display functions | `add_record()` and `display_records()` |
| Instance methods | `administer_dose()`, `update_record()`, `display_info()`, `get_status()` |
| Class methods (`@classmethod`) | `Recipient.next_code()`, `Recipient.from_age()`, `VaccinationRecord.total_records_created()` |
| Static methods (`@staticmethod`) | `Recipient.is_valid_age_group()`, `Recipient.age_to_group()`, `VaccinationRecord.days_between()` |
| Tuples (optional) | `AGE_GROUPS`, `STATUS_LABELS`, `VACCINE_CATALOGUE`, and `(success, message)` return values |

## 5. How the Solution Meets Digital Public Goods (DPG) Standards
1. **Open-source** – Source code is published on GitHub under the MIT licence so anyone can use, study, adapt and share it.
2. **Inclusive & accessible** – Plain-text interface that runs on any low-spec computer, with no internet, accounts or paid software. Clear prompts and friendly error messages guide first-time users. Vaccines and districts are configurable, so it can be adapted to other languages and regions.
3. **Privacy-respecting** – **No names, phone numbers, addresses or exact birth dates are stored.** Each person gets an anonymous code (e.g. `R-001`), and age is converted to an age *group* (data minimisation). Data lives only in memory and is not sent anywhere.
4. **Modular & reusable** – Models, storage and user interface are in separate files; classes can be reused in a web, mobile or database-backed system without change.

## 6. Example Usage (sample input / output)
```
$ python main.py
Choose an option: 1
Age in years (stored only as an age group): 25
District: freetown
Vaccines: Measles, COVID-19, Polio, Yellow Fever
Vaccine name: polio
Created VR-001 for anonymous code R-001.

Choose an option: 2
Record ID (e.g. VR-001): VR-001
Dose date (YYYY-MM-DD): 2026-09-01
  OK: Dose 1 of 3 recorded on 2026-09-01.

Choose an option: 2
Record ID (e.g. VR-001): VR-001
Dose date (YYYY-MM-DD): 2026-09-05
  Not recorded: Too early: wait 28 days between doses (only 4 passed).

Choose an option: 3
ID     | Code  | Age   | District     | Vaccine      | Doses | Last dose  | Status
----------------------------------------------------------------------------------------
VR-001 | R-001 | 15-49 | Freetown     | Polio        | 1/3   | 2026-09-01 | In progress
```

## 7. Limitations & Future Work
Data is held in memory only (by design, for privacy). Future versions could add encrypted local storage, reminders for the next dose, and a translated interface (e.g. Krio).

## 8. Licence
MIT Licence – free to use, modify and distribute.
