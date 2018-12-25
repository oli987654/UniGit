# Please do not modify this part of the code! 
# This is just to show how you should name the variables containing your answers
task_0 = 'Python is cool!' * 3
print('Task 0:', task_0)


# Your code goes here
# Task 1
if(((65**12%3233)**413)%3233==65):
    task_1=True
else:
    task_1=False

print (task_1)

# Task 2
doghouse = "doghouse"
task_2_p1 = doghouse[:3]
task_2_p2 = doghouse[3:]
print (task_2_p1)
print (task_2_p2)

# Task 3
word_given=input("Enter a word: ")
task_3=word_given[::-1]
print(task_3)

# Task 4
task_4= "alpha" in "alphanumeric"
print(task_4)

# Task 5
#This comment is an alternate solution that allows the user to enter a word.
#String_given=input("Enter a string: ")
#Multiplier=int(input("Enter the number of times it should be multiplied: "))
String_given="Python is cool!"
Multiplier=3
task_5 = String_given*Multiplier
print(task_5)

# Task_6
percentage=95.66666666666667
task_6 = float("{0:.2f}".format(percentage))
print (task_6)