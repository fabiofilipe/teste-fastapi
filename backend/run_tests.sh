#!/bin/bash
# Script para executar testes com coverage

echo "🧪 Executando testes..."
pytest tests/ -v --cov=app --cov-report=html --cov-report=term-missing

echo ""
echo "✅ Testes concluídos!"
echo "📊 Relatório HTML disponível em: htmlcov/index.html"
