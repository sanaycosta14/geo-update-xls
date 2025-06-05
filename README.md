
# Atualizador de Latitude/Longitude

Este projeto é uma interface web para processar arquivos XSL/XSLX com informações de coordenadas e atualizar um banco PostgreSQL.

## Como usar para usuários de Docker

1️⃣ Construa a imagem Docker:

```bash
docker build -t atualizador-xml-app .
```

2️⃣ Rode o container diretamente:

use o docker-compose:

```bash
docker-compose up --build -d
```

3️⃣ Acesse [http://localhost:8501](http://localhost:8501) e use a interface para subir seu XML e atualizar o banco!

-------------------------------------------------------------------------------------------------------------------------------------

OBS: temos arquivo .env para que consiga usar variáveis de ambiente sem precisar usar o docker.

## Como usar para os não usuários de docker

1️⃣ O que precisa instalar:

✅ Python 3.11 (ou a versão que está no projeto)
✅ Bibliotecas do projeto (listadas no requirements.txt)
✅ Banco de dados já acessível (o Postgres rodando e configurado, via .env)
✅ O arquivo .env com as variáveis de ambiente certinhas

2️⃣ Passos para rodar localmente:

- crie e ative o ambiente virtual

```bash
python3 -m venv venv
source venv/bin/activate   # no Linux/Mac
# ou
venv\Scripts\activate.bat  # no Windows
```

- Instale as dependências:

```bash
pip install -r requirements.txt
```

- Carregue as variáveis do .env no ambiente (opcional, porém recomendado):

Linux
```bash
export $(cat .env | xargs)
```

Windows (Power shell)
```bash
setx DB_NAME "seu-banco"
setx DB_USER "nome-banco"
setx DB_PASSWORD "senha-banco"
setx DB_HOST "localhost"
setx DB_PORT "5432" #se sua porta for padrão
```

Execute o app do streamlit
```bash
streamlit run app.py
```

Retorno exemplo
```bash
Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
```

🚀 Pronto!
A aplicação vai subir localmente, usando as variáveis do .env para acessar o banco.