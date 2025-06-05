@echo off
echo Verificando instalacao do Python...

python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo Python ja esta instalado:
    python --version
) else (
    echo Python nao encontrado no sistema
    echo Baixando Python 3.11...
    
    :: Criar diretorio temporario
    mkdir "%TEMP%\python_install" 2>nul
    
    :: Baixar o instalador do Python
    echo Baixando Python 3.11... Por favor aguarde...
    powershell -Command "$progressPreference = 'Continue'; $webClient = New-Object Net.WebClient; $webClient.DownloadFile('https://www.python.org/ftp/python/3.11.0/python-3.11.0-amd64.exe', '%TEMP%\python_install\python_installer.exe')"
    
    echo Instalando Python 3.11...
    :: Executar o instalador silenciosamente com barra de progresso
    powershell -Command "$progressPreference = 'Continue'; Start-Process '%TEMP%\python_install\python_installer.exe' -ArgumentList '/quiet InstallAllUsers=1 PrependPath=1' -Wait"
    
    :: Limpar arquivos temporarios
    rmdir /s /q "%TEMP%\python_install"
    
    echo Instalacao concluida! Verificando...
    python --version
)

echo.
echo Verificando ambiente virtual...
if exist .venv\ (
    echo Ambiente virtual ja existe!
    call .venv\Scripts\activate.bat
) else (
    echo Ambiente virtual nao encontrado
    echo Criando novo ambiente virtual...
    python -m venv .venv
    call .venv\Scripts\activate.bat
)

echo.
echo Instalando dependencias...
pip install -r requirements.txt

echo.
echo Iniciando aplicacao...
streamlit run app.py --server.port=8501 --server.address=0.0.0.0

pause