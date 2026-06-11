#Bill Splitter Calculator App
print("Welcome to the Bill Splitter Calculator App!")

#INPUT
#Validating user input for total bill amount, number of people splitting the bill, and tip percentage
while True:
    try:
        total_bill_amount = int(input("Enter the total bill amount: "))
        if total_bill_amount < 0:
            print("The Total bill amount cannot be negative. Please enter a valid amount.")
        else:
            break  
    except ValueError:
        print("Invalid input. Please enter a valid number.")
 
#Validating user input for number of people splitting the bill       
while True:    
    try:
        number_of_people = int(input("Enter the number of people splitting the bill: "))
        if(number_of_people <= 0):
            print("The Number of people splitting the bill cannot be zero or negative.")
        else:
            break
    except ValueError:
        print("Invalid input. Please enter a valid number.")
 
#Validating user input for tip percentage       
while True:
    try:
        tip_percentage = int(input("Enter the tip percentage: "))
        if(tip_percentage < 0):
            print("The Tip percentage cannot be negative.")
        else:
            break
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        
        
#CALCULATIONS
tip_amount = (tip_percentage / 100) * total_bill_amount
total_bill = tip_amount + total_bill_amount
amount_per_person = total_bill / number_of_people

#OUTPUT
print("----------RECEIPT---------------")

print(f"\nInitial Total Bill Amount: {total_bill_amount:,.2f}")
print(f"Tip Percentage: {tip_percentage}%")
print(f"Number of People: {number_of_people}")

print("--------------------------------")
print(f"Tip Amount: {tip_amount:.2f}")
print(f"Final Bill Amount: {total_bill:,.2f}")
print(f"Amount per Person: {amount_per_person:,.2f}")
