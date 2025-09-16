import utils.classes

users = []


while True:
    print('Softex Miniblog\nBem Vindo!')
    print()
    print('1 - login')
    print('2 - criar usuário')
    print('0 - Sair')
    opcao = input('Opção: ')
    match(opcao):
        case '1':
            user_name = input('Nome do Usuário: ')
            user_password = input('Senha: ')
            for user in users:
                if user.user_name == user_name and user.get_password() == user_password:
                    print('Login realizado com sucesso! Bem Vindo {user.user_name}!')
                    while True:
                        print("""
                            Opções:
                            1 - Visualizar Perfil
                            2 - """)
                        break
                    break
                else:
                    print('Dados incorretos!')
                    
        case '2':
            user_name = input('Nome do Usuário: ')
            user_password = input('Senha: ')
            user_email = input("E-Mail: ")
            users.append(utils.classes.User(user_name, user_password, user_email))
            print(users)
            
        case '0':
            print('Finalizando o Programa')
            break
        
        case '_':
            print('Opção Inválida!')
            break