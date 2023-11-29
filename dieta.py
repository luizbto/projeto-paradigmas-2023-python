import psycopg2
import pandas as pd
from flask import Flask, render_template, request, session, redirect, url_for
import os

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
app.secret_key = 'ProgramPython'
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
        altura = request.form.get("altura")

        

        cur.execute("INSERT INTO cliente (email, usuario, senha_hash, nome, idade, peso, sexo, altura) VALUES (%s, %s, %s, %s, %s, %s, %s, %s );", (email, usuario, senha_hash, nome, idade, peso, sexo, altura))

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
            session['logged_in'] = True  # Definir a sessão como logada
            session['username'] = usuario  # Armazenar o nome de usuário na sessão
            cur.close()
            conexao.close()
            return redirect(url_for('perfil'))  # Redirecionar para a página de perfil
        else:
            mensagem = "Usuário ou Senha incorreta. Tente novamente."
            return render_template('login.html', mensagem=mensagem)

    return render_template('login.html')

def obter_dados_do_usuario(username):
    conexao = conectar_banco()
    cur = conexao.cursor()

    cur.execute("SELECT nome, idade, peso, altura, sexo FROM cliente WHERE usuario = %s;", (username,))
    resultado = cur.fetchone()

    cur.close()
    conexao.close()

    if resultado:
        dados_usuario = {
            'nome': resultado[0],
            'idade': resultado[1],
            'peso': resultado[2],
            'altura': resultado[3],
            'sexo': resultado[4]
        }
        return dados_usuario
    else:
        return None

@app.route('/perfil')
def perfil():
    if 'logged_in' in session:
        username = session['username']
        dados_usuario = obter_dados_do_usuario(username)  # Obter os dados do usuário logado

        if dados_usuario:
            return render_template('perfil.html', dados_usuario=dados_usuario)
        else:
            return "Usuário não encontrado no banco de dados"  # Tratamento de erro, caso necessário
    else:
        return redirect(url_for('login'))
    
@app.route('/atualizar_perfil', methods=['POST'])
def atualizar_perfil():
    if 'logged_in' in session:
        conexao = conectar_banco()
        cur = conexao.cursor()
    
        username = session['username']
        dados_usuario = obter_dados_do_usuario(username)
        campo_atualizar = request.form.get("campo_atualizar")
        novo_valor = request.form.get("novo_valor")

        
        if campo_atualizar in ['nome', 'idade', 'peso', 'altura', 'sexo']:
            cur.execute(f"UPDATE cliente SET {campo_atualizar} = %s WHERE usuario = %s;",
                        (novo_valor, username))
            conexao.commit()

            cur.close()
            conexao.close()
        if 'dados_usuario' in session:
                session['dados_usuario'][campo_atualizar] = novo_valor

        return redirect(url_for('perfil'))
    else:
        return redirect(url_for('login'))
    

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.route('/imc')    
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