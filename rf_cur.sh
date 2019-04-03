#!/bin/sh
CURFILE=~/public_html/rf/raiffeisen_cur.log
CURTMP=/tmp/raiffeisen_cur.tmp
CURURL=https://www.raiffeisen.ru/
DATE=`date +%Y-%m-%d\ %H:%M | tr '\n' ' '`
LINES=6912 ## 6 record/hr * 4 lines/rec * 24 h * 12 d = 6912

  ##currency
  for i in `seq 5`; do
    wget $CURURL -q -O $CURTMP
    #grep --binary-files=text rates $CURTMP > ${CURTMP}2
    grep --binary-files=text cn-data $CURTMP | sed -e 's/<[^>]*>//g'|sed -e 's/\ *//g'|sed -e 's/<.*//g' > ${CURTMP}2
    mv ${CURTMP}2 $CURTMP
    [ -s $CURTMP ] && break
  done
  USDB=$( head -n 1 $CURTMP | tail -n 1 )
  USDS=$( head -n 3 $CURTMP | tail -n 1 )
  EURB=$( head -n 2 $CURTMP | tail -n 1 )
  EURS=$( head -n 4 $CURTMP | tail -n 1 )
  #echo "$USDB . $USDS . $EURB . $EURS"
  #exit 0

  ## rewrite! now we have json
  #USDB=$(cat $CURTMP|grep --binary-files=text \'rates\' | awk -F\" '{print $10}')
  #USDS=$(cat $CURTMP|grep --binary-files=text \'rates\' | awk -F\" '{print $14}')
  #EURB=$(cat $CURTMP|grep --binary-files=text \'rates\' | awk -F\" '{print $28}')
  #EURS=$(cat $CURTMP|grep --binary-files=text \'rates\' | awk -F\" '{print $32}')

  if [ -z "$EURB" ]; then
    #echo "No data! ($EURB, $EURS, $USDB, $USDS)"
    #grep EUR $CURTMP
    exit 1
  fi
  ##  {x: '2014-06-13 01:12:13', y: 30, group: 0},
  echo "{x: '$DATE', y: $EURB, group: 1}," >> $CURFILE
  echo "{x: '$DATE', y: $EURS, group: 0}," >> $CURFILE
  echo "{x: '$DATE', y: $USDB, group: 3}," >> $CURFILE
  echo "{x: '$DATE', y: $USDS, group: 2}," >> $CURFILE
  rm $CURTMP

  ## remove old entries
  tail -n $LINES $CURFILE > $CURFILE.tmp
  mv $CURFILE.tmp $CURFILE


