import calculator

print(calculator.add(22, 11))
print(calculator.sub(22, 11))
print(calculator.mul(22, 11))
print(calculator.div(22, 11))
print()
print(calculator.add(11.23, 11.13))
print(calculator.sub(11.23, 11.13))
print(calculator.mul(11.23, 11.13))
print(calculator.div(11.23, 2.1))
try:
    calculator.div(10, 0)
except:
    print('Division by zero')
