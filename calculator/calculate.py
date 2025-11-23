import sys

if len(sys.argv) != 6:
    print("Usage: calculate.py num1 op1 num2 op2 num3")
    sys.exit(1)

try:
    num1 = float(sys.argv[1])
    op1 = sys.argv[2]
    num2 = float(sys.argv[3])
    op2 = sys.argv[4]
    num3 = float(sys.argv[5])
except ValueError:
    print("Error: Invalid number format")
    sys.exit(1)

if op1 not in ["+", "-", "*", "/"] or op2 not in ["+", "-", "*", "/"]:
    print("Error: Invalid operator")
    sys.exit(1)

if op2 in ["*", "/"]:
    if op2 == "*":
        num2 = num2 * num3
    else:
        if num3 == 0:
            print("Error: Division by zero")
            sys.exit(1)
        num2 = num2 / num3
    op2 = "+" #dummy operator to avoid further calculations
    num3 = 0

if op1 == "+":
    result = num1 + num2
elif op1 == "-":
    result = num1 - num2
elif op1 == "*":
    result = num1 * num2
else:
    if num2 == 0:
        print("Error: Division by zero")
        sys.exit(1)
    result = num1 / num2

print(result)
