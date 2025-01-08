import sqlite3
import tkinter as tk
from tkinter import messagebox
from sistema import configurar_banco, consultar_estoque, criar_tabela_historico_saida
from tkinter import ttk
from datetime import datetime

# Configurar banco de dados ao iniciar
configurar_banco()
criar_tabela_historico_saida()

# Função para cadastrar um produto
def cadastrar_produto():
    def salvar_produto():
        nome = entry_nome.get()
        descricao = entry_descricao.get()
        quantidade = entry_quantidade.get()

        if not nome or not quantidade.isdigit():
            messagebox.showerror('Erro', 'Preencha os campos corretamente!')
            return

        try:
            conn = sqlite3.connect('estoque.db')
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO produtos (nome, descricao, quantidade)
            VALUES (?, ?, ?)
            ''', (nome, descricao, int(quantidade)))
            conn.commit()
            conn.close()
            messagebox.showinfo('Sucesso', f'Produto "{nome}" cadastrado com sucesso!')
            janela_cadastro.destroy()
        except Exception as e:
            messagebox.showerror('Erro', f'Erro ao cadastrar produto: {e}')

    # Janela de cadastro
    janela_cadastro = tk.Toplevel()
    janela_cadastro.title('Cadastrar Produto')
    janela_cadastro.geometry("300x300")

    tk.Label(janela_cadastro, text='Nome do Produto').pack(pady=5)
    entry_nome = tk.Entry(janela_cadastro)
    entry_nome.pack(pady=5)

    tk.Label(janela_cadastro, text='Descrição').pack(pady=5)
    entry_descricao = tk.Entry(janela_cadastro)
    entry_descricao.pack(pady=5)

    tk.Label(janela_cadastro, text='Quantidade').pack(pady=5)
    entry_quantidade = tk.Entry(janela_cadastro)
    entry_quantidade.pack(pady=5)

    tk.Button(janela_cadastro, text='Salvar', command=salvar_produto).pack(pady=10)
    tk.Button(janela_cadastro, text='Cancelar', command=janela_cadastro.destroy).pack(pady=5)

# Função para adicionar quantidade ao estoque existente
def adicionar_estoque():
    def salvar_adicao():
        id_produto = entry_id.get()
        quantidade = entry_quantidade.get()

        if not id_produto or not quantidade.isdigit():
            messagebox.showerror('Erro', 'Preencha os campos corretamente!')
            return

        try:
            conn = sqlite3.connect('estoque.db')
            cursor = conn.cursor()
            cursor.execute('SELECT nome, quantidade FROM produtos WHERE id = ?', (id_produto,))
            resultado = cursor.fetchone()

            if resultado:
                nome_produto = resultado[0]
                nova_quantidade = resultado[1] + int(quantidade)
                cursor.execute('UPDATE produtos SET quantidade = ? WHERE id = ?', (nova_quantidade, id_produto))
                conn.commit()
                messagebox.showinfo('Sucesso', f'{quantidade} unidade(s) adicionada ao produto "{nome_produto}" de ID "{id_produto}"!')
                carregar_estoque()  # Atualiza a tabela com o novo estoque
            else:
                messagebox.showerror('Erro', 'Produto não encontrado!')
            conn.close()
            janela_adicionar.destroy()
        except Exception as e:
            messagebox.showerror('Erro', f'Erro ao adicionar quantidade: {e}')

    # Janela de adição
    janela_adicionar = tk.Toplevel()
    janela_adicionar.title('Adicionar ao Estoque')
    janela_adicionar.geometry("600x500")

    # Tabela Treeview para mostrar os produtos
    colunas = ('ID', 'Nome', 'Descrição', 'Quantidade')
    tabela = ttk.Treeview(janela_adicionar, columns=colunas, show='headings')

    # Configurar cabeçalhos
    tabela.heading('ID', text='ID')
    tabela.column('ID', width=50, anchor='center')

    tabela.heading('Nome', text='Nome')
    tabela.column('Nome', width=150, anchor='center')

    tabela.heading('Descrição', text='Descrição')
    tabela.column('Descrição', width=250, anchor='center')

    tabela.heading('Quantidade', text='Quantidade')
    tabela.column('Quantidade', width=100, anchor='center')

    tabela.pack(pady=10)

    # Campos para adicionar quantidade
    tk.Label(janela_adicionar, text="ID do Produto:").pack()
    entry_id = tk.Entry(janela_adicionar)
    entry_id.pack()

    tk.Label(janela_adicionar, text="Quantidade a Adicionar:").pack()
    entry_quantidade = tk.Entry(janela_adicionar)
    entry_quantidade.pack()

    tk.Button(janela_adicionar, text="Adicionar", command=salvar_adicao).pack(pady=10)
    tk.Button(janela_adicionar, text="Fechar", command=janela_adicionar.destroy).pack(pady=5)

    # Função para carregar os dados do estoque na tabela
    def carregar_estoque():
        try:
            conn = sqlite3.connect('estoque.db')
            cursor = conn.cursor()
            cursor.execute('SELECT id, nome, descricao, quantidade FROM produtos')
            produtos = cursor.fetchall()

            # Limpa os dados anteriores na tabela
            for item in tabela.get_children():
                tabela.delete(item)

            # Insere os dados na tabela
            for produto in produtos:
                tabela.insert('', 'end', values=produto)

            conn.close()
        except Exception as e:
            messagebox.showerror('Erro', f'Não foi possível carregar o estoque: {e}')

    # Carrega o estoque ao abrir a janela
    carregar_estoque()

# Função para consultar estoque em formato de tabela (colunas)
def consultar_estoque():
    def carregar_estoque():
        try:
            # Conexão com o banco de dados
            conn = sqlite3.connect('estoque.db')
            cursor = conn.cursor()

            # Busca os dados no banco
            cursor.execute('SELECT id, nome, descricao, quantidade FROM produtos')
            produtos = cursor.fetchall()

            # Remove os dados anteriores na tabela
            for item in tabela.get_children():
                tabela.delete(item)

            # Insere os dados na tabela
            for produto in produtos:
                tabela.insert('', 'end', values=produto)

            conn.close()
        except Exception as e:
            messagebox.showerror('Erro', f'Não foi possível carregar o estoque: {e}')

    # Janela de consulta
    janela_consulta = tk.Toplevel()
    janela_consulta.title('Consultar Estoque')
    janela_consulta.geometry("600x400")

    # Configuração do Treeview
    colunas = ('ID', 'Nome', 'Descrição', 'Quantidade')
    tabela = ttk.Treeview(janela_consulta, columns=colunas, show='headings')

    # Definir cabeçalhos e tamanhos das colunas
    tabela.heading('ID', text='ID')
    tabela.column('ID', width=50, anchor='center')

    tabela.heading('Nome', text='Nome')
    tabela.column('Nome', width=150, anchor='center')

    tabela.heading('Descrição', text='Descrição')
    tabela.column('Descrição', width=250, anchor='center')

    tabela.heading('Quantidade', text='Quantidade')
    tabela.column('Quantidade', width=100, anchor='center')

    # Posiciona a tabela na janela
    tabela.pack(fill='both', expand=True, pady=10, padx=10)

    # Botão para fechar
    tk.Button(janela_consulta, text='Fechar', command=janela_consulta.destroy).pack(pady=5)

    # Carrega os dados ao abrir a janela
    carregar_estoque()


# Função para retirada de produto com tabela
def retirar_produto():
    def carregar_estoque():
        try:
            # Conexão com o banco de dados
            conn = sqlite3.connect('estoque.db')
            cursor = conn.cursor()

            # Busca os dados no banco
            cursor.execute('SELECT id, nome, descricao, quantidade FROM produtos')
            produtos = cursor.fetchall()

            # Limpa os dados anteriores
            for item in tabela.get_children():
                tabela.delete(item)

            # Adiciona os dados na tabela
            for produto in produtos:
                tabela.insert('', 'end', values=produto)

            conn.close()
        except Exception as e:
            messagebox.showerror('Erro', f'Não foi possível carregar o estoque: {e}')

    def registrar_historico_saida(produto_id, quantidade, nome_responsavel, data_saida):
        try:
            conn = sqlite3.connect('estoque.db')
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO historico_saida (produto_id, quantidade, nome_responsavel, data_saida)
                VALUES (?, ?, ?, ?)
            """, (produto_id, quantidade, nome_responsavel, data_saida))

            conn.commit()
            conn.close()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao registrar no histórico de saída: {e}")

    def retirar():
        try:
            id_produto = entry_id.get()
            quantidade_retirada = int(entry_quantidade.get())
            nome_responsavel = entry_nome_responsavel.get()

            if not id_produto or not quantidade_retirada or not nome_responsavel:
                messagebox.showerror("Erro", "Preencha todos os campos corretamente.")
                return

            conn = sqlite3.connect('estoque.db')
            cursor = conn.cursor()

            # Verifica a quantidade atual
            cursor.execute("SELECT quantidade FROM produtos WHERE id = ?", (id_produto,))
            resultado = cursor.fetchone()

            if resultado:
                quantidade_atual = resultado[0]
                if quantidade_retirada > quantidade_atual:
                    messagebox.showerror("Erro", "Quantidade insuficiente em estoque.")
                else:
                    # Atualiza a quantidade
                    nova_quantidade = quantidade_atual - quantidade_retirada
                    cursor.execute("UPDATE produtos SET quantidade = ? WHERE id = ?", (nova_quantidade, id_produto))
                    conn.commit()

                    # Registra no histórico de saída
                    data_saida = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    registrar_historico_saida(id_produto, quantidade_retirada, nome_responsavel, data_saida)

                    messagebox.showinfo("Sucesso", "Retirada realizada com sucesso!")
                    carregar_estoque()
            else:
                messagebox.showerror("Erro", "ID do produto não encontrado.")

            conn.close()
        except Exception as e:
            messagebox.showerror('Erro', f'Erro ao realizar retirada: {e}')

    # Janela de retirada
    janela_retirada = tk.Toplevel()
    janela_retirada.title("Retirar Produto")
    janela_retirada.geometry("600x500")

    # Tabela Treeview para mostrar os produtos
    colunas = ('ID', 'Nome', 'Descrição', 'Quantidade')
    tabela = ttk.Treeview(janela_retirada, columns=colunas, show='headings')

    # Configurar cabeçalhos
    tabela.heading('ID', text='ID')
    tabela.column('ID', width=50, anchor='center')

    tabela.heading('Nome', text='Nome')
    tabela.column('Nome', width=150, anchor='center')

    tabela.heading('Descrição', text='Descrição')
    tabela.column('Descrição', width=250, anchor='center')

    tabela.heading('Quantidade', text='Quantidade')
    tabela.column('Quantidade', width=100, anchor='center')

    tabela.pack(pady=10)

    # Campos para retirada
    tk.Label(janela_retirada, text="ID do Produto:").pack()
    entry_id = tk.Entry(janela_retirada)
    entry_id.pack()

    tk.Label(janela_retirada, text="Quantidade a Retirar:").pack()
    entry_quantidade = tk.Entry(janela_retirada)
    entry_quantidade.pack()

    tk.Label(janela_retirada, text="Nome do Responsável:").pack()
    entry_nome_responsavel = tk.Entry(janela_retirada)
    entry_nome_responsavel.pack()

    tk.Button(janela_retirada, text="Retirar", command=retirar).pack(pady=10)
    tk.Button(janela_retirada, text="Fechar", command=janela_retirada.destroy).pack(pady=5)

    # Carregar estoque ao abrir a janela
    carregar_estoque()

# Função para excluir um produto pelo ID com tabela
def excluir_produto():
    def carregar_estoque():
        try:
            # Conexão com o banco de dados
            conn = sqlite3.connect('estoque.db')
            cursor = conn.cursor()

            # Busca os dados no banco
            cursor.execute('SELECT id, nome, descricao, quantidade FROM produtos')
            produtos = cursor.fetchall()

            # Limpa os dados anteriores
            for item in tabela.get_children():
                tabela.delete(item)

            # Adiciona os dados na tabela
            for produto in produtos:
                tabela.insert('', 'end', values=produto)

            conn.close()
        except Exception as e:
            messagebox.showerror('Erro', f'Não foi possível carregar o estoque: {e}')

    def excluir():
        try:
            id_produto = entry_id.get()

            if not id_produto:
                messagebox.showerror("Erro", "Preencha o ID do produto.")
                return

            conn = sqlite3.connect('estoque.db')
            cursor = conn.cursor()

            # Verifica se o produto existe
            cursor.execute("SELECT * FROM produtos WHERE id = ?", (id_produto,))
            resultado = cursor.fetchone()

            if resultado:
                # Exclui o produto
                cursor.execute("DELETE FROM produtos WHERE id = ?", (id_produto,))
                conn.commit()
                messagebox.showinfo("Sucesso", "Produto excluído com sucesso!")
                carregar_estoque()
            else:
                messagebox.showerror("Erro", "ID do produto não encontrado.")

            conn.close()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao excluir produto: {e}")

    # Janela de exclusão
    janela_exclusao = tk.Toplevel()
    janela_exclusao.title("Excluir Produto")
    janela_exclusao.geometry("600x500")

    # Tabela Treeview para mostrar os produtos
    colunas = ('ID', 'Nome', 'Descrição', 'Quantidade')
    tabela = ttk.Treeview(janela_exclusao, columns=colunas, show='headings')

    # Configurar cabeçalhos
    tabela.heading('ID', text='ID')
    tabela.column('ID', width=50, anchor='center')

    tabela.heading('Nome', text='Nome')
    tabela.column('Nome', width=150, anchor='center')

    tabela.heading('Descrição', text='Descrição')
    tabela.column('Descrição', width=250, anchor='center')

    tabela.heading('Quantidade', text='Quantidade')
    tabela.column('Quantidade', width=100, anchor='center')

    tabela.pack(pady=10)

    # Campo para informar o ID a ser excluído
    tk.Label(janela_exclusao, text="ID do Produto a Excluir:").pack()
    entry_id = tk.Entry(janela_exclusao)
    entry_id.pack(pady=5)

    # Botões
    tk.Button(janela_exclusao, text="Excluir", command=excluir).pack(pady=10)
    tk.Button(janela_exclusao, text="Fechar", command=janela_exclusao.destroy).pack(pady=5)

    # Carregar estoque ao abrir a janela
    carregar_estoque()

def reorganizar_ids():
    """Reorganiza os IDs para remover 'lacunas' após exclusões."""
    try:
        conn = sqlite3.connect('estoque.db')
        cursor = conn.cursor()

        # Reorganiza os IDs
        cursor.execute("SELECT * FROM produtos ORDER BY id")
        produtos = cursor.fetchall()

        # Zera a tabela
        cursor.execute("DELETE FROM produtos")
        conn.commit()

        # Insere novamente os produtos com IDs sequenciais
        for novo_id, produto in enumerate(produtos, start=1):
            cursor.execute(
                "INSERT INTO produtos (id, nome, descricao, quantidade) VALUES (?, ?, ?, ?)",
                (novo_id, produto[1], produto[2], produto[3])
            )

        conn.commit()
        conn.close()
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao reorganizar IDs: {e}")

# Atualiza a função excluir
def excluir_produto():
    def carregar_estoque():
        try:
            conn = sqlite3.connect('estoque.db')
            cursor = conn.cursor()

            cursor.execute('SELECT id, nome, descricao, quantidade FROM produtos')
            produtos = cursor.fetchall()

            for item in tabela.get_children():
                tabela.delete(item)

            for produto in produtos:
                tabela.insert('', 'end', values=produto)

            conn.close()
        except Exception as e:
            messagebox.showerror('Erro', f'Não foi possível carregar o estoque: {e}')

    def excluir():
        try:
            id_produto = entry_id.get()

            if not id_produto:
                messagebox.showerror("Erro", "Preencha o ID do produto.")
                return

            conn = sqlite3.connect('estoque.db')
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM produtos WHERE id = ?", (id_produto,))
            resultado = cursor.fetchone()

            if resultado:
                cursor.execute("DELETE FROM produtos WHERE id = ?", (id_produto,))
                conn.commit()
                reorganizar_ids()  # Chama a função para reorganizar os IDs
                carregar_estoque()  # Atualiza a tabela
                messagebox.showinfo("Sucesso", "Produto excluído e IDs reorganizados!")
            else:
                messagebox.showerror("Erro", "ID do produto não encontrado.")

            conn.close()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao excluir produto: {e}")

    # Janela de exclusão
    janela_exclusao = tk.Toplevel()
    janela_exclusao.title("Excluir Produto")
    janela_exclusao.geometry("600x500")

    colunas = ('ID', 'Nome', 'Descrição', 'Quantidade')
    tabela = ttk.Treeview(janela_exclusao, columns=colunas, show='headings')

    tabela.heading('ID', text='ID')
    tabela.column('ID', width=50, anchor='center')

    tabela.heading('Nome', text='Nome')
    tabela.column('Nome', width=150, anchor='center')

    tabela.heading('Descrição', text='Descrição')
    tabela.column('Descrição', width=250, anchor='center')

    tabela.heading('Quantidade', text='Quantidade')
    tabela.column('Quantidade', width=100, anchor='center')

    tabela.pack(pady=10)

    tk.Label(janela_exclusao, text="ID do Produto a Excluir:").pack()
    entry_id = tk.Entry(janela_exclusao)
    entry_id.pack(pady=5)

    tk.Button(janela_exclusao, text="Excluir", command=excluir).pack(pady=10)
    tk.Button(janela_exclusao, text="Fechar", command=janela_exclusao.destroy).pack(pady=5)

    carregar_estoque()

def visualizar_historico_saida():
    def carregar_historico():
        try:
            # Conexão com o banco de dados
            conn = sqlite3.connect('estoque.db')
            cursor = conn.cursor()

            # Busca os dados do histórico de saídas
            cursor.execute('SELECT id, quantidade, nome_responsavel, data_saida FROM historico_saida')
            historico = cursor.fetchall()

            # Limpa os dados anteriores
            for item in tabela.get_children():
                tabela.delete(item)

            # Adiciona os dados na tabela
            for registro in historico:
                tabela.insert('', 'end', values=registro)

            conn.close()
        except Exception as e:
            messagebox.showerror('Erro', f'Não foi possível carregar o histórico de saídas: {e}')

    # Janela de visualização do histórico
    janela_historico = tk.Toplevel()
    janela_historico.title("Histórico de Saídas")
    janela_historico.geometry("600x400")

    # Tabela Treeview para mostrar o histórico
    colunas = ('ID', 'Quantidade', 'Responsável', 'Data de Saída')
    tabela = ttk.Treeview(janela_historico, columns=colunas, show='headings')

    # Configurar cabeçalhos
    tabela.heading('ID', text='ID')
    tabela.column('ID', width=50, anchor='center')

    tabela.heading('Quantidade', text='Quantidade')
    tabela.column('Quantidade', width=100, anchor='center')

    tabela.heading('Responsável', text='Responsável')
    tabela.column('Responsável', width=150, anchor='center')

    tabela.heading('Data de Saída', text='Data de Saída')
    tabela.column('Data de Saída', width=150, anchor='center')

    tabela.pack(pady=10)

    # Carregar histórico ao abrir a janela
    carregar_historico()




# Menu Principal
def main():
    janela = tk.Tk()
    janela.title('Gerenciador de Estoque')
    janela.geometry('600x400')

    tk.Label(janela, text='Gerenciador de Estoque', font=('Arial', 16)).pack(pady=10)

    tk.Button(janela, text='Cadastrar Produto', command=cadastrar_produto, width=20).pack(pady=5)
    tk.Button(janela, text='Consultar Estoque', command=consultar_estoque, width=20).pack(pady=5)
    tk.Button(janela, text='Adicionar ao Estoque', command=adicionar_estoque, width=20).pack(pady=5)
    tk.Button(janela, text='Registrar Saída', command=retirar_produto, width=20).pack(pady=5)
    tk.Button(janela, text="Visualizar Histórico de Saídas", command=visualizar_historico_saida).pack(pady=10)
    # tk.Button(janela, text='Retirar Produto', command=retirar_produto, width=20).pack(pady=5)
    tk.Button(janela, text='Excluir Produto', command=excluir_produto, width=20).pack(pady=5)
    tk.Button(janela, text='Sair', command=janela.quit, width=20, bg='red', fg='white').pack(pady=5)

    janela.mainloop()

if __name__ == '__main__':
    main()
