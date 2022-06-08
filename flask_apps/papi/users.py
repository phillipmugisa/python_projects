class User:

    users = []

    def __init__(self, first_name, second_name, user_name, password, img_src = None) -> None:
        self.first_name = first_name 
        self.second_name = second_name
        self.user_name = user_name
        self.password = password
        self.img_src = img_src

        self.users.append(self)

    
