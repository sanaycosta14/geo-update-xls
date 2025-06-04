
# Atualizador de Latitude/Longitude

Este projeto é uma interface web para processar arquivos XSL/XSLX com informações de coordenadas e atualizar um banco PostgreSQL.

## Como usar

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

