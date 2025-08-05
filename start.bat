@echo off
echo ========================================
echo   AutoResume LinkedIn - Lancement
echo ========================================
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Python n'est pas installé ou n'est pas dans le PATH
    echo Veuillez installer Python depuis https://python.org
    pause
    exit /b 1
)

echo Python detecte avec succes!
echo.

REM Vérifier si l'environnement virtuel existe
if not exist "venv" (
    echo Creation de l'environnement virtuel...
    python -m venv venv
    if errorlevel 1 (
        echo ERREUR: Impossible de créer l'environnement virtuel
        pause
        exit /b 1
    )
    echo Environnement virtuel créé avec succès!
)

REM Activer l'environnement virtuel
echo Activation de l'environnement virtuel...
call venv\Scripts\activate.bat

REM Installer les dépendances si nécessaire
if not exist "venv\Lib\site-packages\flask" (
    echo Installation des dépendances...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERREUR: Impossible d'installer les dépendances
        pause
        exit /b 1
    )
    echo Dépendances installées avec succès!
)

echo.
echo ========================================
echo   Lancement de l'application...
echo ========================================
echo.
echo L'application sera accessible à l'adresse:
echo http://localhost:5000
echo.
echo Appuyez sur Ctrl+C pour arrêter le serveur
echo.

REM Lancer l'application
python app.py

pause 