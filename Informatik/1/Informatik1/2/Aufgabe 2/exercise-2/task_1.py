# Please do not modify this part of the code!
price_banana = 1.5
price_milk = 2.0
number_of_bananas_purchased = 4
number_of_milks_purchased = 3

# Your code goes here
subtotal_price=price_banana*number_of_bananas_purchased+price_milk*number_of_milks_purchased
promotion_percentage=float(input("Enter discount percentage:"))
print("The subtotal of your purchase is "+str(subtotal_price))
savings=subtotal_price*promotion_percentage/100
print("Your savings are "+str(savings))
total_price=subtotal_price-savings
print("The total price of your purchase is "+str(total_price))

