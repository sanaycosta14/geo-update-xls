# 🚀 Atualizador de Latitude/Longitude

Uma aplicação Streamlit para atualizar coordenadas geográficas (latitude/longitude) no banco de dados a partir de um arquivo XLS.

## 📋 Pré-requisitos

- Python 3.8+
- PostgreSQL
- Arquivo `.env` com as configurações do banco de dados

## 🔧 Instalação

1️⃣ Clone o repositório:
```bash
git clone [URL_DO_REPOSITORIO]
cd geo-update-xls
```

2️⃣ Crie um ambiente virtual e ative-o:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate  # Windows
```

3️⃣ Instale as dependências:
```bash
pip install -r requirements.txt
```

4️⃣ Configure o arquivo `.env`:
```env
DB_NAME=seu_banco
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_HOST=localhost
DB_PORT=5432
```

## 🚀 Uso

1️⃣ Ative o ambiente virtual (se ainda não estiver ativo)  
2️⃣ Execute a aplicação:
```bash
streamlit run app.py
```

3️⃣ Acesse a aplicação no navegador (geralmente [http://localhost:8501](http://localhost:8501))

## 📁 Estrutura do Projeto

```
.
├── src/                # Código do projeto
│   ├── config/         # Configurações gerais
│   ├── database/       # Conexão e queries do banco de dados
│   ├── utils/          # Funções utilitárias
│   └── views/          # Interface do usuário
├── .env                # Variáveis de ambiente (não versionado)
├── app.py              # Ponto de entrada da aplicação
├── requirements.txt    # Dependências do projeto
├── Dockerfile          # Dockerfile para build da imagem
└── docker-compose.yml  # Orquestração do serviço
```

## 📝 Formato do Arquivo XLS

O arquivo XLS deve conter as seguintes colunas:
- Codigo_Propriedade
- Latitude
- Longitude (sim, está escrito assim mesmo)

## 🐳 Subir o App com Docker

O projeto já possui os arquivos necessários para subir com Docker:

- `Dockerfile`: Instruções para build da imagem.
- `requirements.txt`: Dependências do Python.
- `docker-compose.yml`: Orquestração do serviço.

### 🟢 Subir o serviço com docker-compose

1️⃣ Certifique-se de ter o arquivo `.env` configurado na raiz do projeto com as variáveis corretas.

2️⃣ No terminal, na raiz do projeto, rode:
```bash
docker-compose up -d
```

✅ Isso vai:
- Buildar a imagem (`Dockerfile`)
- Rodar o container
- Expor o app em: [http://localhost:8501](http://localhost:8501)

### 🔴 Parar o container
```bash
docker-compose down
```

💡 Para rebuildar a imagem após alterações no código:
```bash
docker-compose up -d --build
```