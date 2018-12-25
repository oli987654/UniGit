amount = int(input('amount: '))
quarters = amount // 25
rest_amount = amount % 25
dimes = rest_amount // 10
rest_amount %= 10
nickels = rest_amount // 5
rest_amount %= 5
pennies = rest_amount
print('%d quarters %d dimes %d nickels %d pennies' %
(quarters, dimes, nickels, pennies))
