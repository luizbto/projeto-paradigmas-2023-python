import psycopg2
import pandas as pd
from flask import Flask, render_template, request

def conectar_banco():
    conexao = psycopg2.connect(
        database="ProgramPython",
        host="localhost",
        user="postgres",
        password="postgres",
        port="5432"
    )
    return conexao

app = Flask(__name__)
@app.route('/cadastro', methods=['GET', 'POST'])
def insert_bd():
    if request.method == 'POST': 
        conexao = conectar_banco()
        cur = conexao.cursor()

        email = request.form.get("email")
        usuario = request.form.get("username")
        senha_hash = request.form.get("password")
        nome = request.form.get("nome")
        idade = request.form.get("idade")
        peso = request.form.get("peso")
        sexo = request.form.get("sexo")

        

        cur.execute("INSERT INTO cliente (email, usuario, senha_hash, nome, idade, peso, sexo) VALUES (%s, %s, %s, %s, %s, %s, %s );", (email, usuario, senha_hash, nome, idade, peso, sexo))

        conexao.commit()
        cur.close()
        conexao.close()

        return render_template('login.html', mensagem="Dados inseridos com sucesso! Faça Login")
    else:
        return render_template('cadastro.html') 




@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        conexao = conectar_banco()
        cur = conexao.cursor()

        usuario = request.form.get("username")
        senha_hash = request.form.get("senha")

        cur.execute("SELECT nome FROM cliente WHERE usuario = %s AND senha_hash = %s;", (usuario, senha_hash))
        resultado = cur.fetchone()

        if resultado:
            nome_do_usuario = resultado[0]
            mensagem = f"Login bem-sucedido! Bem-vindo, {nome_do_usuario}!"
            cur.close()
            conexao.close()
            return render_template('sucesso.html', mensagem=mensagem)  
        else:
            mensagem = "Usuário ou Senha incorreta. Tente novamente."
            return render_template('login.html', mensagem=mensagem) 

    return render_template('login.html')


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
        app.run(debug=True)
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
            continuar = input("Deseja continuar? (SIM ou NAO) ").upper()
            if continuar != "SIM":
                break
        elif(option == "5"):
            login()
            continuar = input("Deseja continuar? (SIM ou NAO) ").upper()
            if continuar != "SIM":
                break
        elif(option == "6"):
            insert_bd()
            continuar = input("Deseja continuar? (SIM ou NAO) ").upper()
            if continuar != "SIM":
                break
        elif(option == "7"):
            print("Saindo do sistema!")
            break
        elif option in ["1", "2", "3"]:
            obter_dieta(option)
            continuar = input("Deseja continuar? (SIM ou NAO) ").upper()
            if continuar != "SIM":
                break
        

print("Sistema encerrado.")