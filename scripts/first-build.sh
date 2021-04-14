#!/usr/bin/sh

# echo "Validando diretório pai..."
# if ! [ $(basename $(dirname "$PWD")) = "app" ]; then
#   echo  "Diretório pai deve ser = app/" >&2
#   exit 1
# fi

# echo "Validando diretório pai..."
# if ! [ $(basename $"$PWD") = "src" ]; then
#   echo  "Diretório deve ser = app/src" >&2
#   exit 1
# fi

echo 
echo "Diretório atual: $(pwd)"
echo "Data atual: $(date)"
echo "Verificando dependências..."

if ! [ -x "$(command -v docker)" ]; then
  echo  "Instalar o docker.io !" >&2
  exit 1
fi

if ! [ -x "$(command -v docker-compose)" ]; then
  echo  "Instalar docker-compose !" >&2
  exit 1
fi
echo "Dependências OK."

echo "Criando diretórios e arquivos necessários"
mkdir -p ../../mail
mkdir -p ../../job
mkdir -p ../../upload
mkdir -p ../../logs
mkdir -p ../../database
touch ../backend/.env

echo "------------------------------"
echo "Iniciando build dos containers"
echo ">docker-compose build" 
docker-compose build
echo "containers construidos com sucesso!"
# docker-compose up
