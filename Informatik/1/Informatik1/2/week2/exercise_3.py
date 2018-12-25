a = float(input('a = '))
b = float(input('b = '))
c = float(input('c = '))

x_1 = (-b + (b ** 2 - 4 * a * c) ** (1/2.0)) / (2*a)
x_2 = (-b - (b ** 2 - 4 * a * c) ** (1/2.0)) / (2*a)
print('Solutions: %.2f, %.2f'% (x_1, x_2))
