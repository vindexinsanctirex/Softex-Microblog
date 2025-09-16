class User:
    def __init__(self, user_name, password, email):
        self.user_name = user_name
        self.__password = password
        self.email = email
        self.posts = []
        self.seguidores = []
        
    def __str__(self):
        return(f'Usuário: ${self.user_name}, Email: ${self.email}')
    
    def __repr__(self):
        return f'{User.__qualname__}(user_name: {self.user_name}, email: {self.email})'
    
    def get_password(self):
        return self.__password
    
    def seguir(self, user_name, users):
        for user in users:
            print(user)
            if user.user_name == user_name:
                continue
            if user_name not in self.seguidores:
                self.seguidores.append(user_name)
                break
            print('Usuário inexistente!')