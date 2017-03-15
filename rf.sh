#!/bin/sh
HTML=~/public_html/rf/index.html
CURFILE=~/public_html/rf/raiffeisen_cur.log
CURIMG=~/public_html/rf/raiffeisen_cur.png
CURTMP=/tmp/raiffeisen_cur.tmp
CURURL=https://connect.raiffeisen.ru/rba/show-rates.do
PAIFILE=~/public_html/rf/raiffeisen_pai.log
PAIIMG=~/public_html/rf/raiffeisen_pai.png
PAITMP=/tmp/raiffeisen_pai.tmp
PAIURL=http://www.raiffeisen-capital.ru/
DATE=`date +%Y-%m-%d\ %H:%M | tr '\n' ' '`


getcur() {
  ##currency
  for i in `seq 5`; do
    wget $CURURL -q -O - | grep --binary-files=text 'rates\[.*RateBean' > $CURTMP
    [ -s $CURTMP ] && break
  done
  USDB=$(cat $CURTMP |grep USD | awk -F\' '{print $6}')
  USDS=$(cat $CURTMP |grep USD | awk -F\' '{print $8}')
  EURB=$(cat $CURTMP |grep EUR | awk -F\' '{print $6}')
  EURS=$(cat $CURTMP |grep EUR | awk -F\' '{print $8}')

  if [ -z "$EURB" ]; then
    echo "No data! ($EURB, $EURS, $USDB, $USDS)"
    exit 1
  fi
  ##  {x: '2014-06-13 01:12:13', y: 30, group: 0},
  echo "{x: '$DATE', y: $EURB, group: 1}," >> $CURFILE
  echo "{x: '$DATE', y: $EURS, group: 0}," >> $CURFILE
  echo "{x: '$DATE', y: $USDB, group: 3}," >> $CURFILE
  echo "{x: '$DATE', y: $USDS, group: 2}," >> $CURFILE
  rm $CURTMP
}

getpai() {
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

}

truncate() {
  ## remove old entries
  FILE=$1
  LINES=$2
  [ -z "$FILE" ] || [ -z "$LINES" ] && return
  tail -n $LINES $FILE > $FILE.tmp
  mv $FILE.tmp $FILE
}

## update data
getcur
truncate $CURFILE 5760 ## 2 record/hour * 24h * 4 lines/record * 30 days = 5760
getpai
truncate $PAIFILE 2880 ## 2 record/hour * 24h * 2 lines/record * 30 days = 2880

##genpage
cat << EOF > $HTML
<html>
<head>
<script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/vis/4.18.1/vis.min.js"></script>
<link href="https://cdnjs.cloudflare.com/ajax/libs/vis/4.18.1/vis.min.css" rel="stylesheet">
<link rel="icon" href="/rf/favicon.ico" type="image/x-icon">
<link rel="shortcut icon" href="/rf/favicon.ico" type="image/x-icon"> 
<meta charset="UTF-8"><META HTTP-EQUIV="REFRESH" CONTENT="900">
</head><body>
<div id="visualization"></div>
<script type="text/javascript">
  var groups = new vis.DataSet();
  groups.add({
    id: 0,
    content: "EURS $EURS"
    });
  groups.add({
    id: 1,
    content: "EURB $EURB"
    });
  groups.add({
    id: 2,
    content: "USDS $USDS"
    });
  groups.add({
    id: 3,
    content: "USDB $USDB"
    });
  groups.add({
    id: 10,
    content: "Value $PAIVAL"
    });
  groups.add({
    id: 11,
    content: "Paid $PAID"
    });

var container = document.getElementById('visualization');
var CurItems = [
EOF
cat $CURFILE >> $HTML
cat << EOF >> $HTML
  ];
var PaiItems = [
EOF
cat $PAIFILE >> $HTML
cat << EOF >> $HTML
  ];

  var CurDataset = new vis.DataSet(CurItems);
  var PaiDataset = new vis.DataSet(PaiItems);

  var options = {
    moveable: false,
    zoomable: false,
    legend: true
  };
  var graph2d = new vis.Graph2d(container, CurItems, groups, options);
  var graph2d = new vis.Graph2d(container, PaiItems, groups, options);
</script>
</body>
</html>
EOF

