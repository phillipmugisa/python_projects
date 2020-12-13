import random

def showNums(nums):
    vals = [i for i in nums]
    hidden_index = random.randint(0,2)
    vals[hidden_index] = "#"
    print(f"[ {nums[0]} {nums[1]} {nums[2]} ]")
    print(f"[ {vals[0]} {vals[1]} {vals[2]} ]...Guess the missing number")
    return nums[hidden_index]

def showResults(score):
    print(f"Thank you for playing, your score is {score}")

def getAnswer(guess, score):
    answer = int(input("Enter your guess: "))
    while answer != guess:
        try_again = input("WRONG GUESS!!! Try Again[y/n]: ")
        if try_again[0].upper() == "Y":
            answer = int(input("Enter your guess: "))
        elif try_again[0].upper() == "N":
            return score
        else:
            print("Invalid Input!!")
    else:
        score = score + 1
        return score

def getSequence():
    nums = [random.randint(0,9), random.randint(0,9), random.randint(0,9)]
    return nums

def play(score):
    guess = showNums(getSequence())
    playGame(guess, score)
    
def playGame(guess, score):
    score = getAnswer(guess, score)
    play_again = input("play again[y/n]: ")
    if play_again[0].upper() == "Y":
        play(score)
    elif play_again[0].upper() == "N":
        showResults(score)
    else:
        print("Invalid Input: ")

def main():
    score = 0
    play(score)

if __name__ == "__main__":
    main()