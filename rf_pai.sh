#!/bin/bash
PAIFILE=~/public_html/rf/raiffeisen_pai.log
PAITMP=/tmp/raiffeisen_pai.tmp
PAIURL=https://www.raiffeisen-capital.ru/pifs/raiffeisen-equities/
DATE=`date +%Y-%m-%d\ %H:%M | tr '\n' ' '`
LINES=360 ## 1 record/day * 2 lines * 180 days = 360

## pai
PAIQ=1.77162 ## was 2.71663
PAID=33000 ## was 23000
#wget $PAIURL -q -O $PAITMP

PAIPRICE=`cat $PAITMP | grep Акции | sed -e 's|^.*"promo_name":"«Райффайзен - Акции»"||g' | sed -e 's|</script>.*$||' | sed -e 's|"breadcrumbsName":"Акции".*$||g' | sed -e 's|^.*calculations||g' | grep unit_value | head -c 100 | sed -e 's|^.*"unit_value":"||g' | sed -e 's|".*$||g'`

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

