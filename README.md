# Gerenciador de Estoque

Este é um sistema simples de gerenciamento de estoque desenvolvido em Python com interface gráfica (Tkinter) e banco de dados SQLite.

## Funcionalidades

- **Adicionar Produtos ao Estoque:** Adicionar novos produtos ou aumentar a quantidade de produtos já existentes.
- **Registrar Saída de Produtos:** Registrar a saída de produtos, incluindo o nome da pessoa responsável e a data da movimentação.
- **Exibir Histórico de Movimentações:** Consultar um histórico completo de entradas e saídas de produtos.
- **Controle Manual:** Controle manual para corrigir registros errados diretamente no banco de dados.

## Tecnologias Utilizadas
- Python 3
- Tkinter (Interface Gráfica)
- SQLite (Banco de Dados)

## Requisitos
- Python 3.x instalado

## Como Executar o Projeto

1. Clone o repositório:
   ```bash
   git clone https://github.com/Ppvinny/gerenciador-estoque.git
   ```
2. Acesse o diretório do projeto:
   ```bash
   cd gerenciador-estoque
   ```
3. Execute o arquivo `gerenciador-estoque.py`:
   ```bash
   python gerenciador-estoque.py
   ```

## Estrutura do Projeto

```
├── gerenciador-estoque.py  # Arquivo principal do sistema
├── estoque.db              # Banco de dados SQLite
├── README.md               # Este arquivo de documentação
```

## Melhorias Futuras
- Implementar alertas visuais para baixo estoque.
- Adicionar funcionalidade de exclusão de registros diretamente pela interface.

## Contribuições
Contribuições são bem-vindas! Sinta-se à vontade para fazer um fork e enviar um pull request.

