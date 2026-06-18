'''
Your Tasks
Your job is to extend the functionality of the ContactManager class by 
implementing the following requirements. Ensure you do not break the existing features.

Task 1: Data Validation (20 Points)
Currently, a user can enter any text for a phone number or email. 
Modify the code to add basic validation:

Phone Validation: In add_contact and update_contact, 
ensure the phone number contains only digits and hyphens (e.g., "+256-701"). 
If it contains illegal characters, print an error message and cancel the operation.

Email Validation: Ensure that if an email is provided, it contains an @ symbol and a . (period).


Task 2: Advanced Search (25 Points)
The current Contacts method only filters by name and phone number.

Modify Contactss so that it can also search by email.

Write a helper method or modify the search printout so it displays the search results in a clean, 
user-friendly format rather than just returning a raw Python list of tuples.


Task 3: Interactive CLI Menu (35 Points)
Create an interactive Command Line Interface (CLI) loop inside a function called main(). 
When run, the program should present the user with a recurring menu until they choose to exit.

The menu should look similar to this:

=== Contact Manager Menu ===CRUD
1. Add Contact
2. View Contact
3. Update Contact
4. Delete Contact
5. Search Contacts
6. List All Contacts
7. Exit
Choose an option (1-7):

Implement proper input handling for each menu item, 
prompting the user for necessary arguments (like name, phone, etc.) 
and passing them to your class methods.

Submission Guidelines:
1. Add a single python script to your github link, 
2. Submit a single Python file named name_contact_assignment.py.
'''

import re

class ContactManager:
    def __init__(self):
        self.contacts = {
            1: {
                "name": "Jane",
                "phone": "+256-789-567890",
                "email": "jdoe@gmail.com"
            },
            2: {
                "name": "John",
                "phone": "+256-786-560090",
                "email": "jodoe@gmail.com"
            },
        }
        self.next_id = 3

    #Phone Validation
    def validate_phone(self, phone):
        pattern = r"^\+[\d\-]+$"
        return bool(re.match(pattern, phone))

    #Email Validation
    def validate_email(self, email):
        if not email:
            return True
        pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
        return bool(re.match(pattern, email))
    
    #Add Contacts
    def add_contact(self, name, phone, email):
        if not self.validate_phone(phone):
            print("Invalid phone number. Only digits, +, hyphens, and spaces are allowed.\n")
            return False

        if not self.validate_email(email):
            print("Invalid email. It must contain '@' and '.'.\n")
            return False

        self.contacts[self.next_id] = {
            "name": name,
            "phone": phone,
            "email": email
        }
        print(f"Contact entered successfully with id {self.next_id}! ✅\n")
        self.next_id += 1
        return True

    #Update Contacts
    def update_contact(self, id):
        if id not in self.contacts:
            print(f"Contact id {id} does not exist.\n")
            return False

        while True:
            choice = input("What do you want to change? (name, phone, email, all): ").strip().lower()
            if choice == "name":
                name = input("Enter new name: ").strip()
                self.contacts[id]["name"] = name
                break

            elif choice in ("phone", "contact", "phone contact", "number"):
                phone = input("Enter the new phone number: ").strip()
                if not self.validate_phone(phone):
                    print("Invalid phone number. Only digits, + and hyphens are allowed.\n")
                    return False
                self.contacts[id]["phone"] = phone
                break

            elif choice == "email":
                email = input("Enter the email: ").strip()
                if email and not self.validate_email(email):
                    print("Invalid email. It must contain '@' and '.'.\n")
                    return False
                self.contacts[id]["email"] = email
                break

            elif choice == "all":
                name = input("Enter new name: ").strip()
                phone = input("Enter the new phone number: ").strip()
                if not self.validate_phone(phone):
                    print("Invalid phone number. Only digits, + and hyphens are allowed.\n")
                    return False

                email = input("Enter the email: ").strip()
                if email and not self.validate_email(email):
                    print("Invalid email. It must contain '@' and '.'.\n")
                    return False

                self.contacts[id] = {
                    "name": name,
                    "phone": phone,
                    "email": email
                }
                break

            else:
                print("Invalid choice❗️ Please choose a valid option (name, phone, email, all).\n")

        print(f"Contact id {id} updated successfully! ✅\n")
        return True

    #View a Contact
    def view_contact(self, id):
        if id not in self.contacts:
            print(f"Contact id {id} does not exist.\n")
            return False

        for key, value in self.contacts[id].items():
            print(f"{key}: {value}")
        print("\n")    
     
    #View all contacts       
    def view_all_contacts(self):
        for id, details in self.contacts.items():
            print(f"\nid: {id}")
            for key, value in details.items():
                print(f"{key}: {value}")
        print("\n")
            
    
    #Filter by email, phone, name
    def search_contacts(self, query):
        query = query.strip().lower()
        results = []
        
        for id, contact in self.contacts.items():
            name = contact["name"].lower()
            phone = contact["phone"].lower()
            email = contact["email"].lower()
            
            if query in name or query in phone or query in email:
                results.append((id, contact))

        if not results:
            print("🔍 No matching contacts found.\n")
            return []

        self.display_search_results(results)
        return results
    
    #Helper to display results
    def display_search_results(self, results):
        print("============= 🔍 Search Results ============\n")
        print(f"{'ID':<6} | {'NAME':<15} | {'PHONE':<18} | {'EMAIL':<20}")
        print("-"*65)
        for id, contact in results:
            print(f"{id:<6} | {contact['name']:<15} | {contact['phone']:<18} | {contact['email']:<20}")
            print("-"*65)
        
        print("\n")
        
    def delete(self, id):
        if id not in self.contacts:
            print(f"Contact id {id} does not exist\n")
            return False
        else:
            del self.contacts[id]
            print(f"Contact id {id} deleted!🗑️\n")
            return True

#Runing the contact manager code
def main():
    choices = [1,2,3,4,5,6,7]
    manager = ContactManager()
    
    while True:
        print("=== Contact Manager Menu ===")
        print("1. Add Contact", "\n2. View Contact", "\n3. Update Contact", "\n4. Delete Contact", "\n5. Search Contacts", "\n6. List All Contacts", "\n7. Exit")
        
        try:
            choice = int(input("\nChoose an option (1-7): ").strip())
            if choice == 7:
                print("\nThank you for using the Contact Manager!👋")
                break
            
            elif choice in choices:
                match choice:
                    case 1:
                        name = input("Enter the name: ").strip()
                        phone = input("Enter the phone number: ").strip()
                        email = input("Enter the email: ").strip()
                        
                        manager.add_contact(name, phone, email)
                         
                    case 2:
                        id = int(input("Enter the contact id: ").strip())
                        manager.view_contact(id)
                        
                    case 3:
                        id = int(input("Enter the contact id to update: ").strip())
                        manager.update_contact(id)
                         
                    case 4:
                        id = int(input("Enter the contact id to delete: ").strip())
                        manager.delete(id) 
                        
                    case 5:
                        query = input("Enter the name, email or phone to search...").strip()
                        manager.search_contacts(query) 
                        
                    case 6:
                        manager.view_all_contacts() 
            
            else:
                print("Invalid Choice. Please choose a valid option")
                
        except ValueError:
            print("Invalid Value. Please enter numbers only")
    


if __name__ == "__main__":
    main()