#!/bin/sh
#echo "`date +%F_%T`" >> ./clean_camera.log
find ./public_html/camera/ -type d -name '201*' -mtime +30 -exec rm -r {} \; 2>/dev/null

