#!/bin/sh

# Código para reduzir tamanho das imagens para o jogo carregar mais rápido
# `sh min.sh 128x128 *.png` vai fazer as imagens ir para 128x128
# Usa o imagemagick

size=$1

shift $($1)
echo "Aplying resize: $size"
echo

for i in $*
do
	convert $i -resize $size $i.min;
	echo "convert $i"
done
