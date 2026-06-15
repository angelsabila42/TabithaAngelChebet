#Menu Driven Calculator

#Functions
def add(x,y): return x + y

def subtract(x,y): return x - y

def multiply(x,y): return x * y

def divide(x,y):
    if y == 0:
        return "Error. Division by 0" 
    else:
        return x / y
    
    
choices = ['/', '+', '-', 'x']

while(True):
    print("---------------------------------")
    print(" 🔢 Welcome to the Calculator app!")
    print("---------------------------------")
    print("\n1. Add (+) \n2. Subtract (-) \n3. Divide (/) \n4. Multiply (*) \n5. Exit")
    choice = input("Choose the operation you want to perform (/, +, -, x) or exit: ").strip().lower()
    
    try:
        if choice == "exit":
            print("\nThank you for using the app!👋")
            break
        
        elif choice in choices:
            num1 = float(input("Enter the first number: "))
            num2 = float(input("Enter the second number: "))

            match choice:
                case '/':
                    answer = divide(num1, num2)
                    operator = '/' 
                case '+':
                    answer = add(num1, num2)
                    operator = '+' 
                case '-':
                    answer = subtract(num1, num2)
                    operator = '-' 
                case 'x':
                    answer = multiply(num1, num2)
                    operator = 'x' 
                    
            if (isinstance(answer, str)):
                print(f"Result: {answer}")
            else:
                print(f"\n{num1} {operator} {num2} = {answer:.2f}")
            continue
        
        else:
            print("Invalid Choice. Please choose a valid option")
            
        
    except ValueError:
        print("Invalid Value. Please enter numbers only")     
    

