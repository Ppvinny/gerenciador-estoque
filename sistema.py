import sqlite3
from tkinter import messagebox

# Função auxiliar: Configurar banco de dados e criar tabelas
def configurar_banco():
    conn = sqlite3.connect('estoque.db')
    cursor = conn.cursor()

    # Criando tabela de produtos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        descricao TEXT,
        quantidade INTEGER NOT NULL DEFAULT 0
    )
    ''')

    # Criando tabela de histórico de saídas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS historico_saidas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_produto INTEGER,
        nome_produto TEXT,
        quantidade INTEGER,
        colaborador TEXT,
        data TEXT,
        FOREIGN KEY (id_produto) REFERENCES produtos(id)
    )
    ''')

    conn.commit()
    conn.close()

# Função para consultar estoque
def consultar_estoque(listbox):
    try:
        conn = sqlite3.connect('estoque.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, nome, descricao, quantidade FROM produtos')
        produtos = cursor.fetchall()
        conn.close()

        listbox.delete(0, 'end')  # Limpa a lista antes de atualizar
        if produtos:
            for produto in produtos:
                id_produto, nome, descricao, quantidade = produto
                listbox.insert('end', f'ID: {id_produto} | Nome: {nome} | Descrição: {descricao} | Quantidade: {quantidade}')
        else:
            listbox.insert('end', 'Nenhum produto encontrado no estoque.')

    except Exception as e:
        messagebox.showerror('Erro', f'Erro ao consultar estoque: {e}')

# Chamada para garantir que o banco está configurado
configurar_banco()

def criar_tabela_historico_saida():
    try:
        conn = sqlite3.connect('estoque.db')
        cursor = conn.cursor()

        # Cria a tabela de histórico de saída
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS historico_saida (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                produto_id INTEGER,
                quantidade INTEGER,
                nome_responsavel TEXT,
                data_saida TEXT
            )
        """)

        conn.commit()
        conn.close()
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao criar tabela de histórico de saída: {e}")
