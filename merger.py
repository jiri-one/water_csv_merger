from pathlib import Path
import csv
from dataclasses import dataclass, replace
from uuid import uuid4
from pprint import pprint

file1 = Path(__file__).parent / "data/export.csv"
file2 = Path(__file__).parent / "data/target.csv"
file3 = Path(__file__).parent / "data/final.csv"

@dataclass
class Doctor:
    advisor: str
    name: str
    surname: str = ""
    uid: uuid4 = None # internal variable to identify doctor
    all_lower: str = "" # internal variable for basic compare of doctors
    last_activity: str = ""
    address: str = ""
    psc: str = ""
    city: str = ""
    brick: str = ""
    originally_selected: str = ""
    finally_selected: str = ""
    typ: str = ""
    lecture: str = ""
    has_a_counselling_room: str = ""
    has_question: str = ""
    visit_4: str = ""
    visit_3: str = ""
    visit_2: str = ""
    visit_1: str = ""
    visit_5: str = ""
    title: str = "MUDr."

    def __post_init__(self):
        # remove "MUDr." from surname
        self.surname.strip("MUDr.")
        # remove whitespaces from both sides of name and surname
        self.surname.strip()
        self.name.strip()
        # fill all_lover attribute
        if self.name:
            self.all_lower = self.surname.lower() + " " + self.name.lower()
        else:
            self.all_lower = self.surname.lower()


doctors:list[Doctor] = list()
advisors:str = set()
result: list[dict] = list()

counter = 0
with open(file1) as exp_file, open(file2) as target_file:
    exp_reader = csv.DictReader(exp_file, delimiter=";")
    target_reader = csv.DictReader(target_file, delimiter=";")
    exp_reader.fieldnames[0] = "Scientific Advisor Name"
    target_reader.fieldnames[0] = "Scientific Advisor Name"
    # create set of doctors and advisors
    for target_row in target_reader:
        doctor = Doctor(advisor = target_row["Scientific Advisor Name"],
                        title = target_row["Titul"],
                        name = target_row["HCP First Name"],
                        surname = target_row["HCP Last Name"],
                        last_activity = target_row["last activity"],
                        address = target_row["Adresa"],
                        psc = target_row["PSČ"],
                        city = target_row["City"],
                        brick = target_row["Brick"],
                        originally_selected = target_row["Originally selected"],
                        finally_selected =  target_row["Finally selected"],
                        typ = target_row["Typ"],
                        lecture = target_row["Má zájem přednášet"],
                        has_a_counselling_room = target_row["Má poradnu"],
                        has_question = target_row["Má dotaz"],
                        visit_4 = target_row["4 návštěva"],
                        visit_3 = target_row["3 návštěva"],
                        visit_2 = target_row["2 návštěva"],
                        visit_1 = target_row["1 návštěva"],
                        visit_5 = target_row["5 návštěva"],
                        )
        # check if the such a doctor exists
        for saved_doctor in doctors:
            if saved_doctor.all_lower == doctor.all_lower:
                # doctor name is there two times, now we need to check his address
                if saved_doctor.address.lower() == doctor.address.lower():
                    # it is same doctor
                    break
                else:
                    # doctor has another address, so it is another doctor
                    doctor.uid = uuid4() # assign new uuid
                    doctors.append(doctor)
                    break
        else:
            doctor.uid = uuid4() # assign new uuid
            doctors.append(doctor)
        advisors.add(target_row["Scientific Advisor Name"])
    
    # check if all doctors have uuid
    for doctor in doctors:
        if not doctor.uid:
            raise ValueError("Doctor without UUID!")

    count_export_doctors = len(doctors)
    print("Number of doctors from target.csv:", count_export_doctors)

    # now update it with export.csv file
    updated_doctors = 0
    for exp_row in exp_reader:
        doctor = Doctor(advisor = exp_row["Scientific Advisor Name"],
                        title = exp_row["Titul"],
                        name = exp_row["HCP First Name"],
                        surname = exp_row["HCP Last Name"],
                        last_activity = exp_row["last activity"],
                        address = exp_row["Adresa"],
                        psc = exp_row["PSČ"],
                        city = exp_row["City"],
                        brick = exp_row["Brick"],
                        originally_selected = exp_row["Originally selected"],
                        finally_selected =  exp_row["Finally selected"],
                        typ = exp_row["Typ"],
                        lecture = exp_row["Má zájem přednášet"],
                        has_a_counselling_room = exp_row["Má poradnu"],
                        has_question = exp_row["Má dotaz"],
                        visit_4 = exp_row["4 návštěva"],
                        visit_3 = exp_row["3 návštěva"],
                        visit_2 = exp_row["2 návštěva"],
                        visit_1 = exp_row["1 návštěva"],
                        visit_5 = exp_row["5 návštěva"],
                        )

        # check if we will update existed doctor data or create new one
        for index, saved_doctor in enumerate(doctors):
            if saved_doctor.all_lower == doctor.all_lower:
                # this doctor exists, now we need to check his address
                if saved_doctor.address.lower() == doctor.address.lower():
                    # it is same doctor, so we will update his data
                    updated_doctors += 1
                    replace(doctors[index], **doctor.__dict__)
                    break
                else:
                    # doctor has another address, so it is another doctor, we will save a new one
                    doctor.uid = uuid4() # assign new uuid
                    doctors.append(doctor)
                    break
        else: # it is completely new doctor, we will save him
            doctor.uid = uuid4() # assign new uuid
            doctors.append(doctor)
    
    count_target_doctors = len(doctors)

    print("Number of doctors after export.csv:", count_target_doctors)
    print(f"There is {count_target_doctors - count_export_doctors} new doctors")
    print(f"And {updated_doctors} were updated.")


# again check if all doctors have uuid
for doctor in doctors:
    if not doctor.uid:
        raise ValueError("Doctor without UUID!")

# check if all UUIDs are unique
count_doctors = len(doctors)
count_unique_ids = len({d.uid for d in doctors})
assert count_doctors == count_unique_ids

# and save it to the file at the end
with open(file3, 'w') as csvfile:
    fieldnames = ["Scientific Advisor Name", "Titul", "HCP Last Name","HCP First Name","last activity","Adresa","PSČ","City","Brick","Originally selected","Finally selected","Typ","Má zájem přednášet","Má poradnu","Má dotaz","4 návštěva","3 návštěva","2 návštěva","1 návštěva","5 návštěva"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for doctor in doctors:
        writer.writerow({"Scientific Advisor Name": doctor.advisor,
                         "Titul": doctor.title,
                         "HCP Last Name": doctor.surname,
                         "HCP First Name": doctor.name,
                         "last activity": doctor.last_activity,
                         "Adresa": doctor.address,
                         "PSČ": doctor.psc,
                         "City": doctor.city,
                         "Brick": doctor.brick,
                         "Originally selected": doctor.originally_selected,
                         "Finally selected": doctor.finally_selected,
                         "Typ": doctor.typ,
                         "Má zájem přednášet": doctor.lecture,
                         "Má poradnu": doctor.has_a_counselling_room,
                         "Má dotaz": doctor.has_question,
                         "4 návštěva": doctor.visit_4,
                         "3 návštěva": doctor.visit_3,
                         "2 návštěva": doctor.visit_2,
                         "1 návštěva": doctor.visit_1,
                         "5 návštěva": doctor.visit_5,
        })
