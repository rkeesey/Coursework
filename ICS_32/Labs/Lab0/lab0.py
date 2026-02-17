# lab0.py

# Starter code for lab 0 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.
# Please see the README in this repository for the requirements of this lab exercise

# Ruby Keesey
# rkeesey@uci.edu
# 76645012

def pycalc(operand1, operand2, operation):

    statement = "The result of your calculation is: "

    if operation == '+':
        sum = operand1 + operand2
        phrase = f'\n{statement}{sum}'
        return phrase
    elif operation == '-':
        dif = operand1 - operand2
        phrase = f'\n{statement}{dif}'
        return phrase
    elif operation == 'x':
        prod = operand1 * operand2
        phrase = f'\n{statement}{prod}'
        return phrase
    else:
        return "\nInvalid operator! Please use one of the following: +, -, x."

if __name__=='__main__':

    print("Welcome to ICS 32 PyCalc!\n")
    
    operand1 = int(input("Enter your first operand: "))
    operand2 = int(input("Enter your second operand: "))
    operation = input("Enter your desired operator (+, -, or x): ")

    ans = pycalc(operand1, operand2, operation)

    print(ans)