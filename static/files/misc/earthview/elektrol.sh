#!/bin/bash

resolution="1920x1080"
monitor=0
data_dir="./"
de="xfce"

usage=\
"Usage: $(basename $0) [-d <pictures dir>] [-r <resolution>] [-m <monitor>] [-e <desktop environment>]\n\
\tscript updates XFCE wallpaper on specified monitro\n
params:\n
\tpictures dir\t  - directory where images are downloaded (default value: $HOME/.local/share/electrol/)\n\
\tresolution\t\t - resolution to which image is beeing resized (default value: 1920x1080)\n\
\tmonitor\t\t    - number of monitor (default value: 0)\n
\tdesktop environment\t - desktop environment, supported values are kde, xfce (default)"

while getopts "hr:m:d:e:" opt; do
  case $opt in
    h)
    echo $usage
    exit 1
    ;;  
    r)
    resolution=$OPTARG      
    ;;
    m)
      monitor=$OPTARG     
      ;;
    d)
      data_dir=$OPTARG
      ;;
    e)
      de=$OPTARG
      ;;
    \?)
      echo $usage
      exit
      ;;
  esac
done

export LC_ALL=en_US.UTF-8 
# ELEKTRO-L server
ftp_site=ftp://electro:electro@ftp.ntsomz.ru/ELECTRO_L_2
# generating date information
year=`date +%Y`
year00=`date +%y`
month=`date +%B`
month00=`date +%m`
day=`date +%d`
hour=`date +%H -d "25 min ago"`
minute=`date +%M -d "25 min ago"`
# minutes can be only only 00 or 30
if [ $minute -ge 30 ]; then
   minute="30"
else
   minute="00"
fi

# generate file name
file_name=$year00$month00$day"_"$hour$minute"_original_RGB.jpg"
# generate url of image
image_url=$ftp_site/$year/$month/$day/$hour$minute/$file_name
# download image
background="$year00$month00$day$hour$minute.jpg"
echo $background
wget $image_url -O $file_name
# add time and resize
if [ ! -s "$background" ]; then
  convert -font Courier $file_name -pointsize 200 -draw "gravity SouthWest fill grey text 0,0 '$hour:$minute $day.$month00.$year' " -resize $resolution $background
fi
