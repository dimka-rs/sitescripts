#!/usr/bin/env python
import urllib
import json
import bs4
from time import strftime, localtime


gogurl="https://www.gog.com/games/ajax/filtered?mediaType=game&page=1&price=discounted&sort=bestselling&limit=1000"
outfile="/home/d/dimkasorg/public_html/gog/index.html"
list=urllib.urlopen(gogurl)
list=list.read()
if len(list) < 1 :
    print("No data!")
    exit()

try:
    list  = json.loads(list)
except ValueError, error:
    exit()

list=list['products']
list2=sorted(list, key=lambda b: b['price']['discountPercentage'] )
list2.reverse()
qty=str(len(list2))

f = open(outfile,'w')
f.write('<!DOCTYPE html>\n')
f.write('<html><head><meta charset="utf-8"><title>GOG discounts</title></head><body><table cellpadding="5" border="0">\n')
f.write('<p>GOG discounts. Updated at '+strftime("%Y-%m-%d %H:%M:%S", localtime())+'. Titles: '+qty+'.</p>\n')
f.write('<tr bgcolor="gray" align="center"><th>#</th><th>Image</th><th>Disc.</th><th>Price</th><th>Title</th><th>Category</th></tr>\n')

i=0
for x in list2:
    i = i + 1
    disc=x['price']['discountPercentage']
    if   disc >= 80 :
        bgc="#009966"
    elif disc >= 70 :
        bgc="#3CB371"
    elif disc >= 50 :
        bgc="#CCFF99"
    else :
        bgc="#C0C0C0"

    mystr='<tr bgcolor="'+bgc+'"><td>'+str(i)+'</td><td><img src="http:'+str(x['image'])+'_100.jpg"></td><td align="right">'+str(x['price']['discountPercentage'])+"%"+'</td><td align="right">'+str(x['price']['amount'])+'</td><td><a href="http://www.gog.com'+x['url'].encode("utf-8")+'">'+x['title'].encode("utf-8")+'</a></td><td>'+x['category'].encode("utf-8")+'</td></tr>\n'
    f.write(mystr)

f.write('</table></body></html>\n')
f.close()

