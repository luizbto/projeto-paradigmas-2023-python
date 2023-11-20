import psycopg2
import pandas as pd

def conectar_banco():
    conexao = psycopg2.connect(
        database="ProgramPython",
        host="localhost",
        user="postgres",
        password="postgres",
        port="5432"
    )
    return conexao
def insert_bd():

    conexao = conectar_banco()
    email = input("Digite o seu email: ")
    usuario = input("Digite o nome de usuário: ")
    senha_hash = input("Digite a sua senha: ")
    nome = input("Digite o seu nome: ")
    idade = input("Digite sua idade: ")
    peso = input("Digite o seu peso (ex: 62.5): ")
    sexo = input("Sexo (F ou M): ")

    cur = conexao.cursor()

    cur.execute("INSERT INTO cliente (email, usuario, senha_hash, nome, idade, peso, sexo) VALUES (%s, %s, %s, %s, %s, %s, %s );", (email, usuario, senha_hash, nome, idade, peso, sexo))

    conexao.commit()
    cur.close()
    conexao.close()

    print("Dados inseridos com sucesso!")

def login():
    
    while True: 
        conexao = conectar_banco()
        cur = conexao.cursor()

        usuario = input("Digite o nome de usuário: ")
        senha_hash = input("Digite a senha: ")

        cur.execute("SELECT nome FROM cliente WHERE usuario = %s AND senha_hash = %s;", (usuario, senha_hash))
        resultado = cur.fetchone()

        if resultado:
            nome_do_usuario = resultado[0]
            print(f"Login bem-sucedido! Bem-vindo, {nome_do_usuario}!")
            cur.close()
            conexao.close()
            break  
        else:
            print("Nome de Usuário ou Senha incorreta. Tente novamente.")

        cur.close()
        conexao.close() 

def obter_imc():
   altura = float(input("Digite sua altura: "))
   peso = float(input("Digite seu peso: "))
   imc = peso / (altura * altura)
   if (imc <= 18.5):
       print("Você esta abaixo do peso")
   elif (imc <= 24.9):
       print("Você esta no peso ideal")
   elif (imc <= 29.9):
       print("Você esta levemente acima do peso")
   elif(imc <= 34.9): 
       print("Você esta com Obesidade grau 1")
   elif(imc <= 39.9):
       print("Você esta com Obesidade grau 2")
   elif(imc > 40):
       print("Você esta com Obesidade grau 3")
    
def obter_dieta(tipo_dieta):
    conexao = conectar_banco()
    if conexao:
        tabela = None
        if tipo_dieta == '1':
            print("Selecionando a Dieta para emagrecer")
            tabela = 'emagrecer'
        elif tipo_dieta == '2':
            print("Selecionando a Dieta para ganho de massa")
            tabela = 'ganho_massa'

        elif tipo_dieta == '3':
            tabela = 'saudavel'
            print("Selecionando a Dieta saudável")
        else:
            print("Opção Inválida!")
        if tabela:
            dieta = pd.read_sql(f'SELECT * FROM {tabela}', conexao)
            print(dieta)
        conexao.close()


while True:
    if __name__ == "__main__":
        print('Seja Bem-Vindo a Nutri_Dev. Escolha a opção que Deseja')
        print('1. Dieta para emagrecer \n'
            '2. Dieta para ganho de massa \n'
            '3. Dieta para se alimentar melhor\n'
            '4. Consultar IMC\n'
            '5. Fazer login\n'  
            '6. Realizar Cadastro\n'
            '7. Sair do Sistema'
            )
        option = input()
        if (option == "4"): 
            obter_imc()
        elif(option == "5"):
            login()
        elif(option == "6"):
            insert_bd()
        elif(option == "7"):
            print("Saindo do sistema")
            break
        else: 
            obter_dieta(option)
        

print("Sistema encerrado.")

    
