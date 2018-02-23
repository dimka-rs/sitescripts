#!/bin/sh
HTML=~/public_html/rf/index.html
DATE=`date +%Y-%m-%d\ %H:%M | tr '\n' ' '`
CURFILE=~/public_html/rf/raiffeisen_cur.log
PAIFILE=~/public_html/rf/raiffeisen_pai.log

EURS=$(tail -n4 $CURFILE |grep "group: 0"|awk '{print $6}'|tr -d ,)
EURB=$(tail -n4 $CURFILE |grep "group: 1"|awk '{print $6}'|tr -d ,)
USDS=$(tail -n4 $CURFILE |grep "group: 2"|awk '{print $6}'|tr -d ,)
USDB=$(tail -n4 $CURFILE |grep "group: 3"|awk '{print $6}'|tr -d ,)

PAIV=$(tail -n2 $PAIFILE |grep "group: 10"|awk '{print $6}'|tr -d ,)
PAID=$(tail -n2 $PAIFILE |grep "group: 11"|awk '{print $6}'|tr -d ,)

##genpage
cat << EOF > $HTML
<html>
<head>
<script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/vis/4.18.1/vis.min.js"></script>
<link href="https://cdnjs.cloudflare.com/ajax/libs/vis/4.18.1/vis.min.css" rel="stylesheet">
<link rel="icon" href="/rf/trend.ico" type="image/x-icon">
<link rel="shortcut icon" href="/rf/trend.ico" type="image/x-icon"> 
<meta charset="UTF-8"><META HTTP-EQUIV="REFRESH" CONTENT="1800">
</head><body>
<p>Updated at $DATE</p>
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
    content: "Value $PAIV"
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
    legend: {
        enabled: true,
	right: {
	    position: 'top-left'
	    }
        },
    drawPoints: false,
    yAxisOrientation: 'right'
  };
  var graph2d = new vis.Graph2d(container, CurItems, groups, options);
  var graph2d = new vis.Graph2d(container, PaiItems, groups, options);
</script>
</body>
</html>
EOF


