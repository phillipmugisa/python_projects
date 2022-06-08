from random import randint

user_input = input('Enter Play<to play> or Quit<to quit> ')
dice_face = None
while user_input[0].upper() != 'Q':
    user_input = input('roll or show: ')
    try:
        if user_input[0].upper() == 'R':
            dice_face = randint(1,6)
        
        if user_input[0].upper() == 'S':
            print(dice_face)
    except:
        break