import psycopg2
from psycopg2 import Error

# --- CAMADA DE CONEXÃO (Baseada em Conexao.java) ---
def conectar():
    try:
        return psycopg2.connect(
            host="localhost",
            database="FLASHArquival",
            user="postgres",
            password="root"
        )
    except Error as e:
        print(f"Erro ao conectar ao banco: {e}")
        return None

# --- CAMADA DE SERVIÇO (Baseada em UsuarioService.java) ---
def validar_dados(nome, email, senha, tipo):
    if not nome or not email or not senha:
        raise ValueError("Todos os campos devem ser preenchidos.")
    
    if "@" not in email or ".com" not in email:
        raise ValueError("E-mail inválido. Deve conter '@' e '.com'.")
    
    if len(senha) < 8 or len(senha) > 16:
        raise ValueError("A senha deve ter entre 8 e 16 caracteres.")
    
    if tipo not in [0, 1]:
        raise ValueError("Tipo inválido. Use 0 para Admin ou 1 para Comum.")

# --- CAMADA DAO (Baseada em UsuarioDAO.java) ---
def salvar(nome, email, senha, tipo):
    try:
        validar_dados(nome, email, senha, tipo)
        conn = conectar()
        if conn:
            cursor = conn.cursor()
            # Incluindo campos extras para paridade com o banco do projeto
            sql = "INSERT INTO usuario (nome, email, senha, usuario_tipo) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (nome, email, senha, tipo))
            conn.commit()
            print(f"Usuário {nome} cadastrado com sucesso!")
            cursor.close()
            conn.close()
    except Exception as e:
        print(f"Erro no Cadastro: {e}")

def listar():
    conn = conectar()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id_usuario, nome, email, usuario_tipo FROM usuario ORDER BY id_usuario")
        usuarios = cursor.fetchall()
        
        print("\n" + "="*60)
        print(f"{'ID':<5} | {'NOME':<15} | {'EMAIL':<25} | {'TIPO'}")
        print("-" * 60)
        for u in usuarios:
            tipo = "Admin" if u[3] == 0 else "Comum"
            print(f"{u[0]:<5} | {u[1]:<15} | {u[2]:<25} | {tipo}")
        print("="*60)
        
        cursor.close()
        conn.close()

def deletar(id_usuario):
    conn = conectar()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM usuario WHERE id_usuario=%s", (id_usuario,))
        conn.commit()
        if cursor.rowcount > 0:
            print(f"Usuário ID {id_usuario} removido!")
        else:
            print("Usuário não encontrado.")
        cursor.close()
        conn.close()

# --- INTERFACE DE MENU (Baseada no fluxo das Telas Java) ---
def menu():
    while True:
        print("\nFLASHArquival - Gestão de Usuários")
        print("1 - Cadastrar Novo (Fluxo TelaCriacao)")
        print("2 - Listar Todos (Fluxo TelaConteudo)")
        print("3 - Deletar Usuário")
        print("0 - Sair")

        op = input("\nEscolha uma opção: ")

        if op == "1":
            nome = input("Nome: ")
            email = input("E-mail: ")
            senha = input("Senha (8-16 chars): ")
            tipo = int(input("Tipo (0: Admin, 1: Comum): "))
            salvar(nome, email, senha, tipo)

        elif op == "2":
            listar()

        elif op == "3":
            id_del = input("ID do usuário para remover: ")
            deletar(id_del)

        elif op == "0":
            print("Encerrando sistema...")
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    menu()