# 🚀 Atualizador de Latitude/Longitude

Uma aplicação Streamlit para atualizar coordenadas geográficas (latitude/longitude) no banco de dados a partir de um arquivo Excel.

## 📋 Pré-requisitos

- Python 3.8+
- PostgreSQL
- Arquivo .env com as configurações do banco de dados

## 🔧 Instalação

1. Clone o repositório:
```bash
git clone [URL_DO_REPOSITORIO]
cd geo-update-xls
```

2. Crie um ambiente virtual e ative-o:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate  # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure o arquivo .env:
```env
DB_NAME=seu_banco
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_HOST=localhost
DB_PORT=5432
```

## 🚀 Uso

1. Ative o ambiente virtual (se ainda não estiver ativo)
2. Execute a aplicação:
```bash
streamlit run app.py
```

3. Acesse a aplicação no navegador (geralmente http://localhost:8501)

## 📁 Estrutura do Projeto

```
.
├── src/
│   ├── config/         # Configurações do projeto
│   ├── database/       # Conexão e queries do banco de dados
│   ├── utils/          # Funções utilitárias
│   └── views/          # Interface do usuário
├── .env               # Variáveis de ambiente (não versionado)
├── app.py            # Ponto de entrada da aplicação
└── requirements.txt  # Dependências do projeto
```

## 📝 Formato do Arquivo Excel

O arquivo Excel deve conter as seguintes colunas:
- Codigo_Propriedade
- Latitude
- Longitude (sim, está escrito assim mesmo)