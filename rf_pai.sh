#!/bin/sh
PAIFILE=~/public_html/rf/raiffeisen_pai.log
PAITMP=/tmp/raiffeisen_pai.tmp
PAIURL=http://www.raiffeisen-capital.ru/
DATE=`date +%Y-%m-%d\ %H:%M | tr '\n' ' '`
LINES=360 ## 1 record/day * 2 lines * 180 days = 360

  ## pai
  PAIQ=2.71663
  PAID=23000
  wget $PAIURL -q -O - > $PAITMP
  LINE=`cat $PAITMP |grep --binary-files=text -n 'openfonds/mmvb/graphics'|tail -n 2|head -n 1|awk '{print $1}'|sed 's/://'`
  LINE=$(( LINE + 7 ))
  PAIPRICE=`cat $PAITMP |head -n $LINE |tail -n 1 | sed -e 's/<[^>]*>//g' | awk '{print $1 $2}'`
  PAIVAL=$(expr $PAIPRICE*$PAIQ|bc)
  #PAIAVG=$(expr $PAID/$PAIQ|bc)
  #DIFF=$(expr $PAIPRICE-$PAIAVG|bc)
  ###
  if [ -z "$PAIVAL" ]; then
    echo "No data!"
    exit 1
  fi
  echo "{x: '$DATE', y: $PAIVAL, group: 10}," >> $PAIFILE
  echo "{x: '$DATE', y: $PAID, group: 11}," >> $PAIFILE

  tail -n $LINES $PAIFILE > $PAIFILE.tmp
  mv $PAIFILE.tmp $PAIFILE


