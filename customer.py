import sqlite3
from termcolor import colored

connection = sqlite3.connect('clinic.db')
cursor = connection.cursor()

def createTable():
    cursor.execute('create table if not exists client(cpf text PRIMARY KEY, name text, email text, cellphone text)')

def validateOption(opc):
    while True:
        try:
            opcao = int(input(opc))
            if opcao not in range(0, 6):
                print('\033[031mDigite uma opção válida!\033[m')
                print()
            else:
                return opcao
        except (ValueError, TypeError):
            print('\033[031mDigite um valor válido!\033[m')
            print()

def consultClient():
    cpf = str(input('digite seu cpf: '))
    cursor.execute('select * from client where cpf = ?', (cpf,))
    result = cursor.fetchone()

    if result:
        return result
    else:
        return False

def insertClient():
    keepConsultClient = consultClient()
    if keepConsultClient:
        print(colored(f'Paciente já cadastrado!\n', 'red'))
    else:
        name = str(input('nome: '))
        cpf = str(input('cpf: '))
        email = str(input('email: '))
        cellphone = str(input('cel/tel: '))

        cursor.execute('insert into client(cpf, name, email, cellphone) values(?, ?, ?, ?)',
                       (cpf, name, email, cellphone))
        
        if cursor.rowcount >= 1:
            connection.commit()
            print(colored('inserção efetuada com sucesso!\n', 'green'))
        else:
            connection.rollback()
            print(colored('Algo deu errado!\n', 'red'))

def changeField():
    keepConsultClient = consultClient()
    if keepConsultClient:
        opc = str(input('qual campo deseja alterar >> e-mail/telefone/ambos: ')).lower()
        if opc in 'email' or opc in 'telefone' or opc == 'ambos':
            if opc == 'email':
                newEmail = str(input('novo email: '))
                cursor.execute("update client set email = ? where email = ?", (newEmail, keepConsultClient[2]))

                if cursor.rowcount >=1:
                    connection.commit()
                    print(colored('atualizaçao efetuada com sucesso!\n', 'green'))
                else:
                    connection.rollback()

            if opc == 'telefone':
                newCellphone = str(input('novo cel/tel: '))

                cursor.execute("update client set cellphone = ? where cellphone = ?", (newCellphone, keepConsultClient[3]))

                if cursor.rowcount >=1:
                    connection.commit()
                    print(colored('atualizaçao efetuada com sucesso!\n', 'green'))
                else:
                    connection.rollback()

            if opc == 'ambos':
                newEmail = str(input('novo email: '))
                newCellphone = str(input('novo cel/tel: '))
                cursor.execute("update client set email = ? where email = ?", (newEmail, keepConsultClient[2]))
                cursor.execute("update client set cellphone = ? where cellphone = ?", (newCellphone, keepConsultClient[3]))

                if cursor.rowcount >=1:
                    connection.commit()
                    print(colored('atualizaçao efetuada com sucesso!\n', 'green'))
                else:
                    connection.rollback()
    else:
        print(colored(f'Paciente não cadastrado!\n', 'red'))

def verifyIfClientHasHistoric(cpf):
    cursor.execute('select * from client INNER JOIN historical ON historical.client_cpf = client.cpf')
    result = cursor.fetchall()

    return result

def deleteClient():
    keepConsultClient = consultClient()
    if keepConsultClient:
        clientCpf = keepConsultClient[0]

        if not verifyIfClientHasHistoric(clientCpf):
            cursor.execute('delete from client where cpf = ?', (keepConsultClient[0],))
            print('registros apagados: ', cursor.rowcount)

            if cursor.rowcount >= 1:
                connection.commit()
                print(colored('deletado com sucesso!\n', 'green'))
            else:
                connection.rollback()
                print(colored(f'Operação falhou!\n', 'red'))
        else:
            print(colored(f'Paciente possui histórico cadastrado! Para poder excluir o paciente do banco de dados, exclua seus históricos completamente.\n', 'red'))
    else:
        print(colored(f'Paciente não cadastrado!\n', 'red'))


def listClients():
    cursor.execute('select * from client')
    result = cursor.fetchall()

    if result != []:
        for client in result:
            clientCPF = client[0]
            clientName = client[1]
            clientEmail = client[2]
            clientCellphone = client[3]
            print(f'\nCPF: {clientCPF}\nNome: {clientName}\nE-mail: {clientEmail}\nCel/tel: {clientCellphone}')

    else:
        print(colored('Nenhum cliente cadastrado!\n', 'red'))

createTable()
def menu_customer():
    while True:
        opc = validateOption("\n1. Consultar"
                        "\n2. Inserir"
                        "\n3. Alterar campo"
                        "\n4. Excluir"
                        "\n5. Listar"
                        "\n0. Sair"
                        "\nOpção -> ")

        if opc == 0:
            break

        if opc == 1:
            consultResult = consultClient()

            if consultResult:
                clientCPF = consultResult[0]
                clientName = consultResult[1]
                clientEmail = consultResult[2]
                clientCellphone = consultResult[3]
                print(f'CPF: {clientCPF}\nNome: {clientName}\nE-mail: {clientEmail}\nCel/tel: {clientCellphone}')
            else:
                print(colored(f'CPF não cadastrado!\n', 'red'))

        if opc == 2:
            insertClient()

        if opc == 3:
            changeField()

        if opc == 4:
            deleteClient()

        if opc == 5:
            listResult = listClients()
            
