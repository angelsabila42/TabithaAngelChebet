# Assignment
# Student Record Management System
# Develop a menu-driven Python application that demonstrates all concepts covered in this lesson.
# The system should:
# Store student records in a CSV file.
# Save additional student details (e.g., address, contact, program) in a JSON file.

# Allow users to: Add a new student. View all students. 
# Search for a student by registration number. Update student details. Delete a student record.

# Handle all possible errors using try, except, finally, and at least one custom exception.
# Log all user actions and system errors to a log file (student_system.log).
# Include clear comments throughout the code, user-friendly prompts, and appropriate input validation.

# Submission Requirements
# Python source code (student_management.py)
# Sample students.csv
# Sample students.json
# Generated student_system.log
# A short report (1–2 pages) explaining the program design, key functions, exception handling strategy, and testing results.

import logging
import csv
import re
import json
from pathlib import Path

#Debugging
logging.basicConfig(
    filename = "TabithaAngelChebet/StudentRecordManagementSystem/student_system.log",
    level = logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

#Custom Exception
class InvalidAgeException(Exception):
    pass

class StudentRecordManager:
    def __init__(self, csv_path, json_path):
        self.csv_path = csv_path
        self.json_path = json_path
        self.fieldnames = ["RegistrationNo", "Name", "Gender", "Age"]
      
    #Read CSV data   
    def _read_csv(self, reg_no=None):
        csv_rows = []
        target_student_csv = None
        
        if self.csv_path.exists():
            with open(self.csv_path, "r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    csv_rows.append(row)
                    if reg_no and row["RegistrationNo"].upper() == reg_no.upper():
                        target_student_csv = row
        return target_student_csv, csv_rows
    
    #Read JSON data
    def _read_json(self):
        if self.json_path.exists():
            try:
                all_json_data = json.loads(self.json_path.read_text(encoding='utf-8'))
            except (json.JSONDecodeError, ValueError):
                all_json_data = {}
        else:
            all_json_data = {}
        return all_json_data
    
    #Helper to display results
    def _display_search_results(self, results):
        print("========== 🔍 STUDENT MATCH FOUND =========\n")
        print(f"Registration No : {results.get('RegistrationNo')}")
        print(f"Name            : {results.get('Name')}")
        print(f"Gender          : {results.get('Gender')}")
        print(f"Age             : {results.get('Age')}")
        print(f"Program/Course  : {results.get('Program', 'N/A')}")
        print(f"Phone Number    : {results.get('Phone', 'N/A')}")
        print(f"Email Address   : {results.get('Email', 'N/A')}")
        
        print("\n")

    #Phone Validation
    def _validate_phone(self, phone):
        phone = phone.strip()
        
        #Must start with +, followed by numbers, spaces, or hyphens
        pattern = r"^\+[0-9][- 0-9]*$"
        if not re.match(pattern, phone):
            return False
            
        #Strip spaces/hyphens and count actual numbers
        digits_only = "".join(c for c in phone if c.isdigit())
        
        #Only 12 digits in total
        return len(digits_only) == 12

    #Email Validation
    def _validate_email(self, email):
        if not email:
            return True
        pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
        return bool(re.match(pattern, email))
    
    #Age Validation
    def _validate_age(self, age):
        try:
            age_value = int(age)
            if age_value <= 0:
                raise InvalidAgeException("Age must be a positive number greater than 0.")
            return age_value
        except (TypeError, ValueError):
            logging.error(f"Age Validation failed.")
            print("Invalid age. Please enter a whole number greater than 0.\n")
            return None
        except InvalidAgeException as e:
            logging.error(f"Age Validation failed.")
            print(f"Error: {e}\n")
            return None
        
        
    
    #ADDING A RECORD
    def add_record(self,reg_no, name, gender, age, program, phone, email):
        reg_no = reg_no.upper()
        # Validate age as a positive integer greater than 0
        age = self._validate_age(age)
        if age is None:
            logging.warning(f"Data Entry Failed: Wrong age input")
            return False
        
        #Validating Input for the gender
        if gender not in ('M', 'F'):
            logging.warning(f"Data Entry Failed: Wrong gender input")
            print("Invalid. Please enter M or F for the gender\n")
            return False
        
        if not self._validate_phone(phone):
            logging.warning(f"Data Entry Failed: Wrong phone number format")
            print("Invalid phone number. Use a country code, spaces or hyphens, and exactly 12 digits.\n")
            return False

        if not self._validate_email(email):
            logging.warning(f"Data Entry Failed: Wrong Email format")
            print("Invalid email. It must contain '@' and '.'.\n")
            return False
        
        #Main csv file
        students = {
            "RegistrationNo":reg_no,
            "Name": name,
            "Gender": gender,
            "Age": age,
        }
        
        #Additional detils for the json file
        extra_details = {
            "Program":program,
            "Phone": phone,
            "Email": email
        }
        
        try:
            print("\nSaving updated records to disk...")
            #CSV file
            #Appending to the existing data in the file
            with open(self.csv_path, "a", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=self.fieldnames)
                writer.writerow(students)
                
            #Read Json file
            all_students = self._read_json()
            #Reg No as the key, extra_details as the value   
            all_students[reg_no] = extra_details
            
            #Converting the python disctionary to a string
            json_data = json.dumps(all_students, indent=4)
            #Writing the data back to the file
            self.json_path.write_text(json_data, encoding="utf-8")
        except IOError as e:
            logging.error(f"System failed to add data for {reg_no} to CSV.")
            print(f"Database Write Error: Could not save data. {e}")
            return False
        finally:
            print("File operation sequence completed.")

        
        print(f"Record entered successfully ✅\n")
        logging.info(f"Successfully added record: {reg_no}")
        return True
        
    
    #UPDATING A RECORD
    def update_records(self, reg_no):
        reg_no = reg_no.upper()
        #Read CSV data
        target_student_csv, csv_rows = self._read_csv(reg_no)
                        
        #Read JSON data
        all_json_data = self._read_json()
            
        #Check if reg_no exists
        if not target_student_csv:
            logging.warning(f"Update failed: Registration number {reg_no} not found.")
            print(f"Student with registration number {reg_no} does not exist.\n")
            return False
        
        #Json dictionary
        target_student_json = all_json_data.get(reg_no, {})

        print("---- Update Record ----")
        old_reg_no = reg_no
        
        while True:
            print("Options:")
            print("1.Reg_no\n2.Name\n3.Gender\n4.Age\n5.Program\n6.Phone\n7.Email\n8.All")
            choice = input("What do you want to change? (1-8): ").strip().lower()
            
            try:
                choice = int(choice)
            except ValueError:
                print("Invalid Choice. Please use only numeric input.\n")
                continue
            
            #Reg no
            if choice == 1:
                new_reg_no = input("Enter the new reg_no: ").strip().upper()
                target_student_csv["RegistrationNo"] = new_reg_no
                reg_no = new_reg_no
                break
            
            #Name
            elif choice == 2:
                name = input("Enter new name: ").strip()
                target_student_csv["Name"] = name
                break
            
            #Gender
            elif choice == 3:
                gender = input("Enter the gender(M/F): ").strip().upper()
                if gender not in ('M', 'F'):
                    logging.warning(f"Update failed: Wrong gender input.")
                    print("Invalid. Please enter M or F for the gender\n")
                    return False
                target_student_csv["Gender"] = gender
                break
            #Age
            elif choice == 4:
                age = input("Enter the new age: ").strip()
                validated_age = self._validate_age(age)
                if validated_age is None:
                    logging.warning(f"Update failed: Wrong age input.")
                    return False
                target_student_csv["Age"] = validated_age
                break
            
            #Program
            elif choice == 5:
                program = input("Enter the new program: ").strip()
                target_student_json["Program"] = program
                break
            
            #Phone
            elif choice == 6:
                phone = input("Enter the new phone number: ").strip()
                if not self._validate_phone(phone):
                    logging.warning(f"Update failed: Wrong phone number format.")
                    print("Invalid phone number. Use a country code, spaces or hyphens, and exactly 12 digits.\n")
                    return False
                target_student_json["Phone"] = phone
                break

            #Email
            elif choice == 7:
                email = input("Enter the new email: ").strip()
                if email and not self._validate_email(email):
                    logging.warning(f"Update failed: Wrong email format.")
                    print("Invalid email. It must contain '@' and '.'.\n")
                    return False
                target_student_json["Email"] = email
                break
            

            #All
            elif choice == 8:
                new_reg_no = input("Enter the new reg_no: ").strip()
                name = input("Enter new name: ").strip()
                
                gender = input("Enter the gender(M/F): ").strip().upper()
                if gender not in ('M', 'F'):
                    logging.warning(f"Update failed: Wrong phone gender input.")
                    print("Invalid. Please enter M or F for the gender\n")
                    return False
        
                age = input("Enter the new age: ").strip()
                validated_age = self._validate_age(age)
                if validated_age is None:
                    logging.warning(f"Update failed: Wrong phone age input.")
                    return False
                
                phone = input("Enter the new phone number: ").strip()
                if not self._validate_phone(phone):
                    logging.warning(f"Update failed: Wrong phone number format.")
                    print("Invalid phone number. Use a country code, spaces or hyphens, and exactly 12 digits.\n")
                    return False
               
                program = input("Enter the new program: ").strip()
                
                email = input("Enter the email: ").strip()
                if email and not self._validate_email(email):
                    logging.warning(f"Update failed: Wrong email format.")
                    print("Invalid email. It must contain '@' and '.'.\n")
                    return False

                target_student_csv["RegistrationNo"] = new_reg_no
                target_student_csv["Name"] = name
                target_student_csv["Gender"] = gender
                target_student_csv["Age"] = validated_age
                
                reg_no = new_reg_no
                
                target_student_json["Program"] = program
                target_student_json["Phone"] = phone
                target_student_json["Email"] = email
                break

            else:
                print("Invalid choice❗️ Please choose a valid option (1-8).\n")
                
        if old_reg_no.upper() != reg_no:
            all_json_data.pop(old_reg_no, None)
            
        #Remove old entry if reg_no has changed  
        all_json_data[reg_no] = target_student_json
        
        try:
            print("\nSaving updated records to disk...")
            #Re-writing the csv file back to the disk
            with open(self.csv_path, 'w', newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=self.fieldnames)
                writer.writeheader()
                writer.writerows(csv_rows)
                
            #Re-writing json file back to disk
            json_string = json.dumps(all_json_data, indent=4)
            self.json_path.write_text(json_string, encoding='utf-8')  
        except IOError as e:
            logging.error(f"System failed to write update for {reg_no} to CSV.")
            print(f"Database Write Error: Could not save data. {e}")
            return False
            
        finally:
            print("File operation sequence completed.")

        print(f"Record updated successfully! ✅\n")
        logging.info(f"Successfully updated record: {reg_no}")
        return True
    
    
    #SEARCHING FOR A RECORD USING REG NO
    def search_records(self, query):
        query = query.strip().upper()
        
        #Read CSV data
        target_csv ,_ = self._read_csv(query)                
        #Read JSON data
        all_json_data = self._read_json()
            
        #Check if reg_no exists
        if not target_csv:
            logging.warning(f"Search failed: Registration number {query} not found.")
            print(f"🔍 No matching records found registration number {query}.\n")
            return []
        
        #Json dictionary
        unformatted_reg_no = target_csv["RegistrationNo"]
        target_json = all_json_data.get(unformatted_reg_no, {})
        
        full_profile = target_csv | target_json

        self._display_search_results(full_profile)
        logging.info(f"User searched for record under registration number: {query}")
        return full_profile

        
    #VIEWING ALL RECORDS    
    def view_all_records(self):
        logging.info(f"User viewed all records")
        _, csv_rows = self._read_csv()
                    
        #All json data            
        all_json_data = self._read_json()
                    
        if not csv_rows:
            logging.warning(f"No student records found in the database.")
            print("No student records found in the database.\n")
            return False
        
        print("\n========================================================== STUDENT DATA ==========================================================")
        print(f"{'Reg No':<15} | {'Name':<18} | {'Gen':<3} | {'Age':<3} | {'Program':<30} | {'Phone':<20} | {'Email':<20}" )
        print("-" * 130)
        
        #Iterating through the csv rows
        for row in csv_rows:
            reg_no = row['RegistrationNo']
            extra_details = all_json_data.get(reg_no, {})
            
            full_profile = row | extra_details
            
            #Display the values
            print(f"{full_profile.get('RegistrationNo', 'N/A'):<15} | "
                  f"{full_profile.get('Name', 'N/A'):<18} | "
                  f"{full_profile.get('Gender', 'N/A'):<3} | "
                  f"{full_profile.get('Age', 'N/A'):<3} | "
                  f"{full_profile.get('Program', 'N/A'):<30} | "
                  f"{full_profile.get('Phone', 'N/A'):<20} | "
                  f"{full_profile.get('Email', 'N/A'):<20}"
                  )
        print("="*130 +"\n")
        return True
        

    #DELETING A RECORD
    def delete(self, reg_no):
        logging.info(f"User initiated deletion for registration number: {reg_no}")
        reg_no = reg_no.strip().upper()
        target_student_csv, csv_rows = self._read_csv(reg_no)
        
        #Check if reg_no exists
        if not target_student_csv:
            logging.warning(f"Delete failed: Registration number {reg_no} not found.")
            print(f"🔍 No matching records found registration number {reg_no}.\n")
            return False
        
        all_json_data = self._read_json()
        
        #Filter out the target student from the CSV array
        csv_rows = [row for row in csv_rows if row["RegistrationNo"].strip().upper() != reg_no]
        #Deleting from the json data
        all_json_data.pop(reg_no, None)
                
        try:
            print("\nSaving updated records to disk...")
            #Re-writing the csv file back to the disk
            with open(self.csv_path, 'w', newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=self.fieldnames)
                writer.writeheader()
                writer.writerows(csv_rows)
                
            #Re-writing json file back to disk
            json_string = json.dumps(all_json_data, indent=4)
            self.json_path.write_text(json_string, encoding='utf-8')  
            
        except IOError as e:
            logging.error(f"System failed to write update for {reg_no} to CSV.")
            print(f"Database Write Error: Could not save data. {e}")
            return False   
        finally:
            print("File operation sequence completed.")
    
        print(f"Student record {reg_no} deleted from database! 🗑️\n")
        logging.info(f"Successfully deleted record: {reg_no}")
        return True
 
    
#Main Execution
def main():
    choices = [1,2,3,4,5,6]
    csv_path = "TabithaAngelChebet/StudentRecordManagementSystem/students.csv"
    json_path = "TabithaAngelChebet/StudentRecordManagementSystem/students.json"
    manager = StudentRecordManager(Path(csv_path), Path(json_path))
    
    while True:
        print("=== Student Record Management System ===")
        print("1. View all Records", "\n2. Add Record", "\n3. Update Record", "\n4. Search Records", "\n5. Delete Record", "\n6. Exit")
        
        choice_input = input("\nChoose an option (1-6): ").strip()
        try:
            choice = int(choice_input)
        except ValueError:
            print("Invalid Choice. Please enter numbers only for the menu option.\n")
            continue

        if choice == 6:
            print("\nThank you for using the Student Management Sysyem!👋")
            break

        if choice not in choices:
            print("Invalid Choice. Please choose a valid option\n")
            continue

        match choice:
            case 1:
                manager.view_all_records()
                
            case 2:
                name = input("Enter the name: ").strip()
                reg_no = input("Enter the registration number: ").strip().upper()
                age = input("Enter the age: ").strip()
                gender = input("Enter the gender(M or F): ").strip().upper()
                program = input("Enter Program/Course: ").strip()
                phone = input("Enter the phone number: ").strip()
                email = input("Enter the email: ").strip()
                
                manager.add_record(reg_no, name, gender, age, program, phone, email)
            
            case 3:
                reg_no = input("Enter the registration number to update: ").strip()
                manager.update_records(reg_no)
                
            case 4:
                query = input("Enter the registration number to search...").strip()
                manager.search_records(query)
                
            case 5:
                reg_no = input("Enter the registration number to delete: ").strip()
                manager.delete(reg_no) 
                 


if __name__ == "__main__":
    main()     