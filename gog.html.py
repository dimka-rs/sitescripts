#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import json
import sys
from time import strftime, localtime

gogurl_start = "https://www.gog.com/games/ajax/filtered?mediaType=game&page="
gogurl_end = "&price=discounted&sort=popularity"
#outfile="/home/d/dimkasorg/public_html/gog/index.html"
out_file_name="./index.html"
json_file_name="all_products.json"

def write_header(f, all_cats):
    f.write('<!DOCTYPE html>\n')
    f.write('<html><head><meta charset="utf-8"><title>GOG discounts</title><META HTTP-EQUIV="REFRESH" CONTENT="3600">')
    f.write('<link rel="shortcut icon" href="/gog/favicon.png" type="image/png"></head><body><table cellpadding="5" border="0">\n')
    f.write('<p><a href="https://www.gog.com">GOG</a> discounts. Updated at '+strftime("%Y-%m-%d %H:%M:%S", localtime())+'.</p>\n')
    f.write('<script language="javascript">\n')
    f.write('function filter_change() {\n')
    f.write('        var c = document.getElementById("category").value;\n')
    f.write('        var p = document.getElementById("platform").value;\n')
    f.write('        var list = document.getElementsByClassName("ALL");\n')
    f.write('        console.log("CT: " + c + ", PL: "+p);\n')
    f.write('        for (var i = 0; i < list.length; i++)\n')
    f.write('        {\n')
    f.write('            console.log(i + ": " + list.item(i).classList );\n')
    f.write('            if ( (p == "plt-ALL" || list.item(i).classList.contains(p)) && (c == "cat-ALL" || list.item(i).classList.contains(c)) )\n')
    f.write('            {\n')
    f.write('               list.item(i).style.display = "table-row";\n')
    f.write('            } else {\n')
    f.write('               list.item(i).style.display = "none";\n')
    f.write('            }\n')
    f.write('        }\n')
    f.write('    } </script>\n')
    f.write('<p>\n')
    f.write('Category: <select name="category" id="category" onchange="filter_change();">\n')
    f.write('    <option value="cat-ALL">ALL</option>\n')

    for k,v in all_cats.items():
        f.write('    <option value="cat-'+k.replace(" ", "")+'">'+k+' ('+str(v)+')</option>\n')

    f.write('</select>\n')
    f.write('Paltform: <select name="platform" id="platform" onchange="filter_change();">\n')
    f.write('    <option value="plt-ALL">ALL</option>\n')
    f.write('    <option value="plt-lin">Linux</option>\n')
    f.write('    <option value="plt-win">Windows</option>\n')
    f.write('    <option value="plt-mac">Mac</option>\n')
    f.write('</select>\n')
    f.write('</p>\n')
    f.write('<tr bgcolor="gray" align="center"><th>#</th><th>Image</th><th>Discount</th><th>Price</th><th>Title</th><th>Category</th><th>Platform</th></tr>\n')


def write_line(f, bg_color, idx, img, discount, price, url, title, category, win, lin, mac):
    plt_win = 'plt-win' if len(win) > 0 else ''
    plt_lin = 'plt-lin' if len(lin) > 0 else ''
    plt_mac = 'plt-mac' if len(mac) > 0 else ''

    mystr = '<tr bgcolor="'+bg_color+'" class="ALL cat-'+category.replace(" ", "")+' '+plt_win+' '+plt_lin+' '+plt_mac+'"><td>'+idx+'</td><td><img src="http:'+img+'_100.jpg"></td><td align="right">'+discount+"%"+'</td><td align="right">'+price+'</td><td><a href="http://www.gog.com'+url+'">'+title+'</a></td><td>'+category+'</td><td>'+win+' '+lin+' '+mac+'</td></tr>\n'
    f.write(mystr)


def write_footer(f):
    f.write('</table></body></html>\n')


def get_json_from_url(url):
    try:
        body = urllib.urlopen(url)
    except Exception as err:
        print(str(err))
        exit()

    try:
        body = body.read()
    except Exception as err:
        print(str(err))
        exit()

    if len(body) < 1 :
        print("No data!")
        exit()

    try:
        body = json.loads(body)
    except Exception as err:
        print(str(err))
        exit()

    return body


def fetch_data_from_file(in_file):
    try:
        with open(in_file) as f:
            all_products = json.load(f)
    except Exception as err:
        print(str(err))
        exit()

    return all_products


def fetch_data_from_url(url_start, url_end):
    page_num = 1
    url = url_start + str(page_num) + url_end
    list_json = get_json_from_url(url)

    total_pages = list_json['totalPages']
    #print "page 1 of "+str(tpages)

    all_products = list_json['products']

    while page_num < total_pages:
        page_num += 1
        #print "pages "+str(page_num)+" of "+str(total_pages)
        url = url_start+str(page_num)+url_end
        all_products += get_json_from_url(url)['products']

    all_products = sorted(all_products, key=lambda b: b['price']['discountPercentage'] )
    all_products.reverse()
    #print "total entries "+qty

    return all_products

def generate_page_from_json(all_products, out_file):
    ## get cats stats
    all_cats = {}
    for x in all_products:
        k = x['category'].encode("utf-8")
        all_cats[k] = all_cats.get(k, 0) + 1

    #for k,v in all_cats.items():
    #    print k + ":" + str(v)

    f = open(out_file,'w')

    write_header(f, all_cats)

    idx = 0
    for x in all_products:
        idx = idx + 1
        discount = x['price']['discountPercentage']
        if discount == 0:
            continue
        elif discount >= 80 :
            bg_color="#009966"
        elif discount >= 70 :
            bg_color="#3CB371"
        elif discount >= 50 :
            bg_color="#CCFF99"
        else :
            bg_color="#C0C0C0"

        image = str(x['image'])
        idx_str = str(idx)
        discount = str(x['price']['discountPercentage'])
        price = str(x['price']['amount'])
        url = x['url'].encode("utf-8")
        title = x['title'].encode("utf-8")
        category = x['category'].encode("utf-8")
        win = 'windows' if x['worksOn']['Windows'] else ''
        lin = 'linux' if x['worksOn']['Linux'] else ''
        mac = 'mac' if x['worksOn']['Mac'] else ''

        write_line(f, bg_color, idx_str, image, discount, price, url, title, category, win, lin, mac)
        ### FIXME:
        if idx > 200:
            break

    write_footer(f)
    f.close()


if ( __name__ == '__main__'):
    if len(sys.argv) > 1:
        # file given
        all_products = fetch_data_from_file(sys.argv[1])
    else:
        # from url
        all_products = fetch_data_from_url(gogurl_start, gogurl_end)

    ### dump JSON
    with open(json_file_name, 'w') as f:
        json.dump(all_products, f)

    generate_page_from_json(all_products, out_file_name)
