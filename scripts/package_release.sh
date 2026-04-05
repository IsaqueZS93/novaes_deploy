#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT_DIR="$ROOT_DIR/dist"
mkdir -p "$OUT_DIR"
ARCHIVE="$OUT_DIR/novaes_ops_corporativo.tar.gz"

# Exclui diretórios pesados e internos
tar \
  --exclude='.git' \
  --exclude='dist' \
  --exclude='__pycache__' \
  --exclude='*.pyc' \
  --exclude='WebAppStreamlit' \
  -czf "$ARCHIVE" \
  -C "$ROOT_DIR" \
  .

echo "Pacote gerado em: $ARCHIVE"
