#!/usr/bin/env python
import urllib
import json
import bs4
from time import strftime, localtime

gogurl_start="https://www.gog.com/games/ajax/filtered?mediaType=game&page="
gogurl_end="&price=discounted&sort=popularity"
cpage=1
gogurl=gogurl_start+str(cpage)+gogurl_end
outfile="/home/d/dimkasorg/public_html/gog/index.html"

try:
    list=urllib.urlopen(gogurl)
except Exception as err:
    print(str(err))
    exit()

try:
    list=list.read()
except Exception as err:
    print(str(err))
    exit()

if len(list) < 1 :
    print("No data!")
    exit()

try:
    listj  = json.loads(list)
except Exception as err:
    print(str(err))
    exit()

tpages=listj['totalPages']
#print "page 1 of "+str(tpages)

listjpall=listj['products']

while cpage < tpages:
    cpage += 1
    #print "pages "+str(cpage)+" of "+str(tpages)
    gogurl = gogurl_start+str(cpage)+gogurl_end
    list=urllib.urlopen(gogurl)
    list=list.read()
    try:
        listj=json.loads(list)
        listjp=listj['products']
        listjpall += listjp
    except ValueError, error:
        exit()

listjpalls=sorted(listjpall, key=lambda b: b['price']['discountPercentage'] )
listjpalls.reverse()
#print "total entries "+qty

f = open(outfile,'w')
f.write('<!DOCTYPE html>\n')
f.write('<html><head><meta charset="utf-8"><title>GOG discounts</title><META HTTP-EQUIV="REFRESH" CONTENT="3600">')
f.write('<link rel="shortcut icon" href="/gog/favicon.png" type="image/png"></head><body><table cellpadding="5" border="0">\n')
f.write('<p><a href="https://www.gog.com">GOG</a> discounts. Updated at '+strftime("%Y-%m-%d %H:%M:%S", localtime())+'.\n')
f.write('<tr bgcolor="gray" align="center"><th>#</th><th>Image</th><th>Discount</th><th>Price</th><th>Title</th><th>Category</th><th>Linux</th></tr>\n')

i=0
for x in listjpalls:
    i = i + 1
    disc=x['price']['discountPercentage']
    if   disc == 0:
        continue
    elif disc >= 80 :
        bgc="#009966"
    elif disc >= 70 :
        bgc="#3CB371"
    elif disc >= 50 :
        bgc="#CCFF99"
    else :
        bgc="#C0C0C0"

    mystr='<tr bgcolor="'+bgc+'"><td>'+str(i)+'</td><td><img src="http:'+str(x['image'])+'_100.jpg"></td><td align="right">'+str(x['price']['discountPercentage'])+"%"+'</td><td align="right">'+str(x['price']['amount'])+'</td><td><a href="http://www.gog.com'+x['url'].encode("utf-8")+'">'+x['title'].encode("utf-8")+'</a></td><td>'+x['category'].encode("utf-8")+'</td><td>'+('&#10004;' if x['worksOn']['Linux'] else '')+'</td></tr>\n'
    f.write(mystr)

f.write('</table></body></html>\n')
f.close()
