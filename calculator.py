
print("===================================")
print("         SIMPLE CALCULATOR")
print("===================================")

try:
    # Input two numbers
    num1 = float(input("Enter First Number: "))
    num2 = float(input("Enter Second Number: "))

    # Select operation
    print("\nSelect Operation:")
    print("+  Addition")
    print("-  Subtraction")
    print("*  Multiplication")
    print("/  Division")

    operator = input("\nEnter Operation (+, -, *, /): ")

    # Perform calculation
    if operator == "+":
        result = num1 + num2

    elif operator == "-":
        result = num1 - num2

    elif operator == "*":
        result = num1 * num2

    elif operator == "/":
        if num2 == 0:
            print("\nError: Cannot divide by zero!")
            exit()
        result = num1 / num2

    else:
        print("\nInvalid Operation!")
        exit()

    # Display result
    print("\n===================================")
    print("Result:", result)
    print("===================================")

except ValueError:
    print("\nError: Please enter valid numbers!")
