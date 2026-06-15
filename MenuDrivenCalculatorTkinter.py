#Menu Driven Calculator Tkinter
import tkinter as tk
from tkinter import messagebox

#Functions
def add(x,y): return x + y

def subtract(x,y): return x - y

def multiply(x,y): return x * y

def divide(x, y):
    if y == 0:
        return None
    return x / y


def calculate(operator):
    try:
        num1 = float(entry1.get())
        num2 = float(entry2.get())

        match operator:
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

            case _:
                messagebox.showerror("Error", f"Unknown operator: {operator}")
                return

        if answer is None:
            messagebox.showerror("Error", "Division by zero")
            label_result.config(text="Error: Division by zero", fg="red")
            return

        label_result.config(text=f"Result = {answer:.2f}", fg="teal")

    except ValueError:
        messagebox.showerror("Input Error", "Please enter numbers only")
    


#Initialize the main window
root = tk.Tk()
root.title("Calculator")
root.geometry("400x300")

font = ("Consolas", 12) 

#First Number
label1 = tk.Label(root, text="First Number:", font=font)
label1.grid(row=0, column=0, padx=10, pady=10, sticky="w")

entry1 = tk.Entry(root, font=font, width=15)
entry1.grid(row=0, column=1, padx=10, pady=10)

#Second Number
label2 = tk.Label(root, text="Second Number:", font=font)
label2.grid(row=1, column=0, padx=10, pady=10, sticky="w")

entry2 = tk.Entry(root, font=font, width=15)
entry2.grid(row=1, column=1, padx=10, pady=10)

#Buttons
button_frame = tk.Frame(root)
button_frame.grid(row=2, column=0, columnspan=2, pady=10)

btn_add = tk.Button(button_frame, text="+", width=5, command=lambda: calculate('+'))
btn_add.pack(side="left", padx=5)

btn_sub = tk.Button(button_frame, text="-", width=5, command=lambda: calculate('-'))
btn_sub.pack(side="left", padx=5)

btn_div = tk.Button(button_frame, text="÷", width=5, command=lambda: calculate('/'))
btn_div.pack(side="left", padx=5)

btn_mult = tk.Button(button_frame, text="×", width=5, command=lambda: calculate('x'))
btn_mult.pack(side="left", padx=5)

#Result Display Area
label_result = tk.Label(root, text="Result = ", font=("Consolas", 12, "bold"), fg="teal")
label_result.grid(row=3, column=0, columnspan=2, pady=10)
root.mainloop()

