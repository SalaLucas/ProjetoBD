Requisitos:
Linux
Python 3.7+

Crie um .venv:
python3 -m venv .venv

Ative o projeto com o comando:
. .venv/bin/activate

Após isso instale o flask com o comando:
pip install flask

Arrume as configurações do flask:
export FLASK_APP=app

Inicie o banco de dados:
python init_db.py

Rode o projeto na porta padrão (127.0.0.1:5000):
flask run