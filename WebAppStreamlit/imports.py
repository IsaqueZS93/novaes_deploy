import os
import sys

# Define o diretório base
base_path = r"C:\Users\Novaes Engenharia\WebAppStreamlit"

# Caminha por todos os subdiretórios do base_path e adiciona ao sys.path
for root, dirs, files in os.walk(base_path):
    if root not in sys.path:
        sys.path.append(root)
