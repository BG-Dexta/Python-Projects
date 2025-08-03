def showField(field):
    print(field['top-left'] + ' | ' + field['top-middle'] + ' | ' + field['top-right'])
    print('- + - + -')
    print(field['middle-left'] + ' | ' + field['middle-middle'] + ' | ' + field['middle-right'])
    print('- + - + -')
    print(field['bottom-left'] + ' | ' + field['bottom-middle'] + ' | ' + field['bottom-right'])

def changeTurn(turn):
    if turn == 'X':
        turn = 'O'
    else:
        turn = 'X'
    return turn

def checkWinner(gameField, turn):
    if gameField['top-left'] == turn and gameField['top-middle'] == turn and gameField['top-right'] == turn or gameField['middle-left'] == turn and gameField['middle-middle'] == turn and gameField['middle-right'] == turn or gameField['bottom-left'] == turn and gameField['bottom-middle'] == turn and gameField['bottom-right'] == turn or gameField['top-left'] == turn and gameField['middle-left'] == turn and gameField['bottom-left'] == turn or gameField['top-middle'] == turn and gameField['middle-middle'] == turn and gameField['bottom-middle'] == turn or gameField['top-right'] == turn and gameField['middle-right'] == turn and gameField['bottom-right'] == turn or gameField['top-left'] == turn and gameField['middle-middle'] == turn and gameField['bottom-right'] == turn or gameField['top-right'] == turn and gameField['middle-middle'] == turn and gameField['bottom-left'] == turn:
        print('Player ' + turn + ' wins.')
#        gameField = resetField(gameField)


def resetField(field):
    field = {'top-left': ' ', 'top-middle': ' ', 'top-right': ' ',
                 'middle-left': ' ', 'middle-middle': ' ', 'middle-right': ' ',
                 'bottom-left': ' ', 'bottom-middle': ' ', 'bottom-right': ' '}
    return field




gameField = {'top-left': ' ', 'top-middle': ' ', 'top-right': ' ',
         'middle-left': ' ', 'middle-middle': ' ', 'middle-right': ' ',
         'bottom-left': ' ', 'bottom-middle': ' ', 'bottom-right': ' '}

turn = 'X'
while True:
    showField(gameField)
    pos = input('Place your mark ' + turn + ': ')
    if pos in gameField.keys():
        if gameField[pos] == ' ':
            gameField[pos] = turn
            if gameField['top-left'] == turn and gameField['top-middle'] == turn and gameField['top-right'] == turn or \
                    gameField['middle-left'] == turn and gameField['middle-middle'] == turn and gameField[
                'middle-right'] == turn or gameField['bottom-left'] == turn and gameField['bottom-middle'] == turn and \
                    gameField['bottom-right'] == turn or gameField['top-left'] == turn and gameField[
                'middle-left'] == turn and gameField['bottom-left'] == turn or gameField['top-middle'] == turn and \
                    gameField['middle-middle'] == turn and gameField['bottom-middle'] == turn or gameField[
                'top-right'] == turn and gameField['middle-right'] == turn and gameField['bottom-right'] == turn or \
                    gameField['top-left'] == turn and gameField['middle-middle'] == turn and gameField[
                'bottom-right'] == turn or gameField['top-right'] == turn and gameField['middle-middle'] == turn and \
                    gameField['bottom-left'] == turn:
                print('Player ' + turn + ' wins.')
                gameField = resetField(gameField)

            turn = changeTurn(turn)
        else:
            print('Wrong mark or already taken mark. Please choose another.')
            continue
    elif pos == 'quit':
        break
    else:
        print('Incorrect place. Please choose the correct one')



