import sqlite3
from termcolor import colored

connection = sqlite3.connect('clinic.db')
cursor = connection.cursor()


def createTable():
    cursor.execute('create table if not exists historical(id integer PRIMARY KEY AUTOINCREMENT, date text, client_cpf text, description text, procedure text, treatment text, FOREIGN KEY(client_cpf) REFERENCES client(cpf))')

def validateOption(opc):
    while True:
        try:
            opcao = int(input(opc))
            if opcao not in range(0, 4):
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

def showHistoric(cpf):
    cursor.execute('select * from client INNER JOIN historical ON historical.client_cpf = client.cpf')
    result = cursor.fetchall()

    return result

def insertClient():
    keepConsultClient = consultClient()
    if keepConsultClient:
        print(colored('Paciente cadastrado! Prossiga com o cadastro\n', 'green'))

        date = str(input('data: '))
        client_cpf = keepConsultClient[0]
        description = str(input('Descrição: '))
        procedures = str(input('Procedimentos realizados: '))
        treatment = str(input('Tratamentos recomendados: '))

        cursor.execute(
            'insert into historical(date, client_cpf, description, procedure, treatment) values(?, ?, ?, ?, ?)',
            (date, client_cpf, description, procedures, treatment))
        connection.commit()
        print(colored('inserção efetuada com sucesso!\n', 'green'))
    else:
        print(colored(f'Paciente não cadastrado!\n', 'red'))

createTable()
def menu_historic():
    
    while True:
        opc = validateOption("\n1. Consultar"
                        "\n2. Inserir"
                        "\n3. Excluir"
                        "\n0. Sair"
                        "\nOpção -> ")

        if opc == 0:
            break

        if opc == 1:
            consultResult = consultClient()
            if consultResult:

                for client in showHistoric(consultResult[0]):
                    print(f'\nData: {client[5]}\nCPF: {client[6]}\nDescrição: {client[7]}\nProcedimento realizado: {client[8]}\nTratamento recomendado: {client[9]}\n')

            else:
                print(colored(f'CPF não cadastrado!\n', 'red'))

        if opc == 2:
            insertClient()

        if opc == 3:
            consultResult = consultClient()
            if consultResult:

                for client in showHistoric(consultResult[0]):
                    print(client[4:])

                id = int(input('digite o código do histórico que deseja excluir: '))
                cursor.execute('delete from historical where id = ?', (id,))

                if cursor.rowcount >= 1:
                    connection.commit()
                    print(colored('Registro excluído!\n', 'green'))
                else:
                    connection.rollback()
                    print(colored(f'Registro não encontrado!\n', 'red'))


            else:
                print(colored(f'CPF não cadastrado!\n', 'red'))

