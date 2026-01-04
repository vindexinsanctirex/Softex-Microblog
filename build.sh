#!/usr/bin/env bash
# build.sh - Script de build para o Render

set -o errexit
set -o pipefail

echo "🔨 Iniciando processo de build..."

# Atualizar pip
echo "1. 📦 Atualizando pip..."
pip install --upgrade pip

# Instalar dependências
echo "2. 📚 Instalando dependências..."
pip install -r requirements.txt

# Verificar instalação
echo "3. ✅ Verificando instalações..."
python -c "import django; print(f'Django {django.__version__} instalado')" || echo "❌ Django não instalado"
python -c "import gunicorn; print('Gunicorn instalado')" || echo "❌ Gunicorn não instalado"

echo "🎉 Build concluído com sucesso!"