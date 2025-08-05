#!/bin/bash

# Script de build pour Vercel
echo "🚀 Démarrage du build Vercel..."

# Installation des dépendances
echo "📦 Installation des dépendances Python..."
pip install -r requirements.txt

# Vérification de la structure
echo "🔍 Vérification de la structure du projet..."
if [ ! -f "app.py" ]; then
    echo "❌ app.py non trouvé"
    exit 1
fi

if [ ! -d "templates" ]; then
    echo "❌ Dossier templates non trouvé"
    exit 1
fi

if [ ! -d "static" ]; then
    echo "❌ Dossier static non trouvé"
    exit 1
fi

# Création des dossiers nécessaires
echo "📁 Création des dossiers nécessaires..."
mkdir -p static/images

# Optimisation des fichiers statiques
echo "⚡ Optimisation des fichiers statiques..."
if [ -f "static/css/style.css" ]; then
    echo "✅ CSS trouvé"
fi

if [ -f "static/js/script.js" ]; then
    echo "✅ JavaScript trouvé"
fi

# Vérification des fichiers SEO
echo "🔍 Vérification des fichiers SEO..."
if [ -f "static/sitemap.xml" ]; then
    echo "✅ Sitemap trouvé"
else
    echo "⚠️ Sitemap manquant"
fi

if [ -f "static/robots.txt" ]; then
    echo "✅ Robots.txt trouvé"
else
    echo "⚠️ Robots.txt manquant"
fi

echo "✅ Build terminé avec succès!" 