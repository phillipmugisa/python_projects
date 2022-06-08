def tellTtory(username, age, nationality, gender, city, hobby):
    return f"{username} is a {age} year old {nationality} {gender}. {username} lives in {city}. {username} loves {hobby}."

def getData():
    username = input("Enter your name: ")
    age = input("Enter your age: ")
    nationality = input("Enter your nationality: ")
    gender = input("Enter your gender: ")
    city = input("Enter your city of residence: ")
    hobby = input("Enter your hobby: ")

    return username, age, nationality, gender, city, hobby

def main():
    username, age, nationality, gender, city, hobby = getData()
    story = tellTtory(username, age, nationality, gender, city, hobby)
    print(story)


if __name__ == "__main__":
    main()