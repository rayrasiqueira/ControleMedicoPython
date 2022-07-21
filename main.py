from customer import *
from historic import *

def fillet(text):
    textToUppercase = text.upper()
    print("~" * 50)
    print(f"{' '.join(textToUppercase)}".center(50))
    print("~" * 50)

while True:
    fillet("Controle de clientes")
    opc = input("1. Clientes"
               "\n2. Histórico"
               "\n0. Sair"
               "\nOpção -> ")
    if opc == '0':
        break
    elif opc == '1':
        menu_customer()
    elif opc == '2':
        menu_historic()
    else:
        print(colored("Opção inválida!!", 'red'))
