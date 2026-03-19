# Auto Haki Observation

Bot automatique pour détecter l'activation du Haki dans Roblox et appuyer automatiquement sur la touche H.

## Fonctionnalités

- Détection automatique de l'image Haki à l'écran
- Vérification que Roblox est la fenêtre active avant d'agir
- Interface graphique overlay (transparente, toujours au premier plan)
- Raccourci personnalisable (F6 par défaut)

## Installation

### 1. Prérequis

Installer Python 3.11+ depuis [python.org](https://www.python.org/)

### 2. Installer les dépendances

```bash
pip install pyautogui pydirectinput customtkinter keyboard pillow pygetwindow pyinstaller
```

### 3. Lancer le script

```bash
python sailorpiece.py
```

## Utilisation

1. Lancer le jeu Roblox
2. Lancer `Auto Haki Observation.exe` ou `python sailorpiece.py`
3. Clique sur le bouton "▶ Démarrer" ou appuyez sur F6
4. Le bot détectera automatiquement l'image Haki et appuiera sur H

### Commandes

- **F6** : Démarrer/Arrêter le bot
- **Cliquer sur le texte du raccourci** : Changer le raccourci

## Compilation en .exe

### Option 1 : Commandes manuelles

```bash
# Installer PyInstaller si besoin
pip install pyinstaller

# Compiler
python -m PyInstaller --onefile --add-data "image.png;." --icon=logo.ico --name "Auto Haki Observation" --noconsole sailorpiece.py
```

Le .exe sera dans le dossier `dist/`

### Option 2 : GitHub Actions (Automatique)

1. Push le code sur GitHub
2. Créer un tag de version :
```bash
git tag v1.0.0
git push origin v1.0.0
```
3. GitHub Actions compilera automatiquement et créera une release

## Fichiers requis

- `sailorpiece.py` - Code source principal
- `image.png` - Image à détecter (doit être dans le même dossier que l'exe)
- `logo.ico` - Icône de l'application (optionnel)

## Dépannage

### Le bot ne détecte pas l'image
- Vérifier que `image.png` est dans le même dossier que l'exe
- Ajuster la valeur `confidence=0.6` dans le code si nécessaire

### Le bot appuie sur H n'importe quand
- La vérification de fenêtre Roblox peut nécessiter un ajustement selon votre configuration

### Erreur "pyinstaller n'est pas reconnu"
- Utiliser `python -m PyInstaller` au lieu de `pyinstaller`
