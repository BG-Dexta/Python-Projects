import random

options = ["rock", "paper", "scissors"]

user_wins = 0
comp_wins = 0

while True:
    user_pick = input("Enter your choice or Q to quit: ").lower()
    if user_pick == "q":
        break
    if user_pick not in options:
        continue

    comp_pick = options[random.randint(0, 2)]
    print("Computer picked:", comp_pick)
    if user_pick == "rock" and comp_pick == "scissors":
        print("You Won!")
        user_wins += 1
    elif user_pick == "paper" and comp_pick == "rock":
        print("You Won!")
        user_wins += 1
    elif user_pick == "scissors" and comp_pick == "paper":
        print("You Won!")
        user_wins += 1
    elif user_pick == comp_pick:
        print("Tie")
    else:
        print("You Lost")
        comp_wins += 1

print("You won", user_wins, "times.")
print("Computer won", comp_wins, "times.")
