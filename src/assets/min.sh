#!/bin/sh

# Código para reduzir tamanho das imagens para o jogo carregar mais rápido
# `sh min.sh 128x128 *.png` vai fazer as imagens ir para 128x128
# Usa o imagemagick

size=$1

shift
echo "Aplying resize: $size"
echo

mkdir -p Min
for i in $*; do
    i=${i%.png}
    convert $i.png -resize $size Min/$i.min.png &&
        echo "convert $i"
done
