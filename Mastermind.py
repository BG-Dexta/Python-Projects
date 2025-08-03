import random

COLORS = ["R", "G", "B", "O", "W", "Y"]
CODE_LENGTH = 4
TURNS = 10

def generate_code():
    code = []
    for _ in range(1, CODE_LENGTH + 1):
        code.append(random.choice(COLORS))
    return code

def guess_code():
    while True:
        guess = input("Guess the code: ").upper().split(" ")
        if len(guess) != CODE_LENGTH:
            print(f"You must guess {CODE_LENGTH} colors.")
            continue

        for color in guess:
            if color not in COLORS:
                print(f"Wrong color: {color}. Try again.")
                break
        else:
            break
    return guess

def check_code(guess, real_code):
    color_counts = {}
    correct_position = 0
    incorrect_position = 0

    for color in real_code:
        if color not in color_counts:
            color_counts[color] = 0
        color_counts[color] += 1

    for guess_color, real_color in zip(guess, real_code):
        if (guess_color == real_color):
            correct_position += 1
            color_counts[guess_color] -= 1

    for guess_color, real_color in zip(guess, real_code):
        if (guess_color in color_counts) and (color_counts[guess_color] > 0):
            incorrect_position += 1
            color_counts[guess_color] -= 1
    
    return correct_position, incorrect_position

def game():
    print(f"Welcome to mastermind! You have {TURNS} attempts to guess the code.")
    print("Available colors are: ", *COLORS)

    code = generate_code()
    for attempt in range(1, TURNS + 1):
        guess = guess_code()
        correct, incorrect = check_code(guess, code)
        if correct == CODE_LENGTH:
            print(f"You guessed the code in {attempt} attempts!")
            break
        print(f"Correct positions: {correct} | Incorrect positions: {incorrect}")

    else:
        print("You ran out of attempts. The code was ", *code)


if __name__ == "__main__":
    game()
    
