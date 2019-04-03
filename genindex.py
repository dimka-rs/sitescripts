# encoding: utf-8
'''genindex.py'''
import pickle
import datetime
import os.path
# import subprocess
### base data ###
newdatafile='/home/d/dimkasorg/public_html/env/sensors.data'
olddatafile='/home/d/dimkasorg/public_html/env/sensors.data.old'
res={
'inet-p-img':'img/internet.png',  'inet-p-head':'Интернет',      'inet-p-text':'Пинг: _val_ мс',            'inet-p-url':'https://thingspeak.com/channels/306596',
'elec-u-img':'img/voltage.png',   'elec-u-head':'Электричество', 'elec-u-text':'Напряжение: _val_ В',       'elec-u-url':'https://thingspeak.com/channels/71570',
'hwat-t-img':'img/hotwater.png',  'hwat-t-head':'Горячая вода',  'hwat-t-text':'Температура: _val_ &deg;C', 'hwat-t-url':'https://thingspeak.com/channels/64404',
'cwat-p-img':'img/coldwater.png', 'cwat-p-head':'Холодная вода', 'cwat-p-text':'Давление: _val_ кПа',       'cwat-p-url':'https://thingspeak.com/channels/145269',
'env-b-img' :'img/barometer.png', 'env-b-head' :'Барометр',      'env-b-text' :'Давление: _val_ мм рт. ст.','env-b-url':'https://thingspeak.com/channels/96563',
'env-t-img':'img/temperature.png', 'env-t-head':'Температура',   'env-t-text' :'В комнате _val_ &deg;C',    'env-t-url':'https://thingspeak.com/channels/96563'
}
## These keys will be shown, cam1-p excluded
keys=('inet-p', 'elec-u', 'cwat-p', 'hwat-t', 'env-b', 'env-t')

def printhead():
    print '<html><head><link rel="shortcut icon" href="favicon.png" type="image/png">'
    print '<style type="text/css">'
    print '.tbl { border: 2px solid black; padding: 5px; width: 400px;}'
    print '.hd { font-size: 20; text-align: left; }'
    print '.nt { font-size: 15; text-align: right; }'
    print '.blue { background-color: blue; }'
    print '.green { background-color: forestgreen; }'
    print '.yellow { background-color: gold; }'
    print '.red { background-color: red; }'
    print '.orange { background-color: orange; }'
    print '.gray { background-color: darkgray; }'
    print '</style><meta charset="UTF-8"><META HTTP-EQUIV="REFRESH" CONTENT="900"></head><body><center>'

def printtail():
    from datetime import datetime
    print '<p>Обновлено:', str(datetime.now().replace(microsecond=0)), '</p>'
    print '</center></body></html>'
        
def printdata(img, head, text, color, url=''):
    if url :
        url1='<a href="'+url+'">'
        url2='</a>'
    else:
        url1=''
        url2=''
    print '<table class="tbl" cols="3" frame="border" cellpadding="5"><tr>'
    print '<td class="'+color+'" width="5">&nbsp;</td><td width="64">'+url1+'<img src="'+img+'">'+url2+'</td>'
    print '<td><p class="hd">'+head+'</p><p class="nt">'+text+'</p></td>'
    print '</tr></table><br>'

def roundFloat(flt):
    return str(int(round(float(flt))))
        
def parseData(key, val):
    val=roundFloat(val)
    vali=int(val)
    ## get trend
    trend=''
    if key in olddata and len(olddata[key]):
        if vali > int(olddata[key]):
            trend='&#8593;' ## 8593 - arrow up, 8599 - arrow up-right
        elif vali < int(olddata[key]):
            trend='&#8595;' ## 8595 - arrow down, 8560 - arrrow down-right
        else:
            trend=''
    ## get color
    if key == 'inet-p' or key == 'cam1-p':
        if vali >= 0 and vali < 20:
            return 'green', val, trend
        else:
            return 'red', val, trend
    elif key == 'elec-u':
        if vali > 210 and vali < 240:
            return 'green', val, trend
        else:
            return 'red', val, trend
    elif key == 'hwat-t':
        if vali > 44 and vali < 80:
            return 'green', val, trend
        else:
            return 'red', val, trend
    elif key == 'env-b':
        if vali > 740 and vali < 770:
            return 'green', val, trend
        else:
            return 'red', val, trend
    elif key == 'cwat-p':
        if vali > 260 and vali < 360:
            return 'green', val, trend
        else:
            return 'red', val, trend
    elif key == 'env-t':
        if vali < 22:
            return 'blue', val, trend
        elif vali < 28:
            return 'green', val, trend
        else:
            return 'orange', val, trend
            
    else:
        ## this should draw attention to unknown key
        return 'gray', val, trend

def getData(file):
    data = {}
    if os.path.isfile(file):
        with open(file,'rb') as f:
            ## TODO: check if load ok
            data=pickle.load(f)
    return data             

def sendNotify(sensor, failed):
    if falied:
        #rc=subprocess.call(['curl', '-X', 'POST', failurl])
        rc=datetime.now()
    else:
        #rc=subprocess.call(['curl', '-X', 'POST', okurl])
        rc=datetime.now()
    return

''' ### Main ### '''
data=getData(newdatafile)
olddata=getData(olddatafile)
printhead()

''' ## parse list '''
for k in keys:
    if k in data:
        ## if new data arrived - update page and olddata
        val=data[k]
        color,val,tail=parseData(k, val)
        ## check if notify needed
        if k+'-failed' in olddata:
            if k+'-failed' == True:
                olddata[k+'-failed']=False
                sendNotify(k, False)
        ## save data
        olddata[k]=val
        olddata[k+'-age']=datetime.datetime.now().replace(microsecond=0)
        olddata[k+'-failed']=False
    else:
        color='gray'
        if k in olddata and k+'-age' in olddata:
            ## if we have old data - use it and show age at tail
            val=olddata[k]
            tail='('+str(datetime.datetime.now().replace(microsecond=0) - olddata[k+'-age'])+')'
            ## send notify
            if k+'-failed' in olddata:
                if k+'-failed' == False:
                    olddata[k+'-failed']=True
                    sendNotify(k, True)
        else:
            ''' ## else - show question marks '''
            val='no data'
            tail='no age'
    ''' ## finally, print data '''
    img=res[k+'-img']
    head=res[k+'-head']
    text=res[k+'-text'].replace('_val_', val)+'&nbsp;'+tail
    if k+'-url' in res :
        url=res[k+'-url']
    else:
        url=''
    printdata(img, head, text, color, url)

printtail()
## save old data
f=open(olddatafile,'wb')
pickle.dump(olddata, f)
f.close()
## remove used data
#if os.path.isfile(newdatafile):
    #os.remove(newdatafile)

## end

