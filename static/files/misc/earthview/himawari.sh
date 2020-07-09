#!/bin/sh

json=$(wget http://himawari8-dl.nict.go.jp/himawari8/img/D531106/latest.json -O - )

url=$(echo "$json" | sed -e s/^.........// -e 's/\".*$//' -e s/-/'\/'/g  -e s/\ /'\/'/g -e s/://g)

base="http://himawari8-dl.nict.go.jp/himawari8/img/D531106/1d/550/"

suff="_0_0.png"

url=$base$url$suff

echo $url
