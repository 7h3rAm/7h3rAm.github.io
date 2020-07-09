#!/usr/bin/env bash

declare -a dates=("May/27" "May/28" "May/29" "May/30" "May/31" "June/01" "June/02")
declare -a dates=("May/31" "June/01" "June/02")
declare -a timestamps=("0000" "0030" "0100" "0130" "0200" "0230" "0300" "0330" "0400" "0430" "0500" "0530" "0600" "0630" "0700" "0730" "0800" "1030" "1100" "1130" "1200" "1230" "1300" "1330" "1400" "1430" "1500" "1530" "1600" "1630" "1700")

for d in "${dates[@]}";do
  for t in "${timestamps[@]}";do
   curl -O -u electro:electro "ftp://ntsomz.gptl.ru:2121/ELECTRO_L_2/2020/${d}/${t}/200602_${t}_RGB.jpg"
  done
done
