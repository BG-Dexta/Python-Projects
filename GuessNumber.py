import random

max_number = input("Input upper range: ")

guesses = 0

if max_number.isdigit():
    max_number = int(max_number)
    if max_number <= 0:
        print("Enter the number above 0 please")
        quit()
else:
    print("Enter the number please")
    quit()

random_number = random.randint(0, max_number)

while True:
    guesses += 1
    user_number = input("Guess a number: ")
    if user_number.isdigit():
        user_number = int(user_number)
    else:
        print("Enter the number please")
        continue

    if user_number == random_number:
        print("Correct!")
        break
    elif user_number > random_number:
        print("Less")
    else:
        print("More")

print("You got it in", guesses, "attempts.")

