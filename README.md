# TJCase

Gerenciador de casos de testes.

## Funcionalidades

- Cadastro de usuários;
- Cadastro e gerenciamento de casos de testes.

## Tecnologias Usadas

- **Flask**: Framework web Python.
- **SQLAlchemy**: ORM para interação com o banco de dados.
- **Bootstrap**: Framework CSS para design responsivo.
- **JavaScript**: Scripts interativos no front-end.

## Como Rodar o Projeto

### Pré-requisitos

1. **Python 3.13.2**
2. **pip** para gerenciar pacotes

### Instalação

1. Clone o repositório:

2. Crie um ambiente virtual:
    ```bash
    python -m venv venv
    ```

3. Ative o ambiente virtual:

    - **Windows**:
    ```bash
    .\venv\Scripts\activate
    ```

    - **Mac/Linux**:
    ```bash
    source venv/bin/activate
    ```

4. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

5. Defina as variáveis de ambiente necessárias (exemplo de variáveis de ambiente para o Flask):
    ```bash
    export FLASK_APP=app.py
    export FLASK_ENV=development
    ```

6. Rode o servidor:
    ```bash
    flask run
    ```

Agora você pode acessar o projeto em `http://127.0.0.1:5000/`.


