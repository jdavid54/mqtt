import urllib.request
#import requests
import re,time,sys
#sys.path.append("c:/python34/steve/network/")
from html.parser import HTMLParser
from urllib.parse import urlparse

import paho.mqtt.client as mqtt
from mqtt_functions import *
verbose=False
log_dir="flightlogs"
log_recs=10000
number_logs=20
keepalive=120
site="/arrivals-and-departures/"
temp=[]
url="https://"+site
broker="192.168.1.61"
base_topic="Flights" #topic for MQTT publish
client=mqtt.Client("python-flight-data")
client.connect(broker)
file_out="flightlogs"
####
record_flag=False #make copy of web pages 
get_from_disk=True #set true to read data from disk
####
scan_interval=20 #should be 60 

data_out={}
def test_string(s):
    try:
       s.strip()
       return True
    except:
        #print("not a string ")
        return False
class MyHTMLParser(HTMLParser):

    def set_flags(self):
        self.in_tr=False
        self.start_tag=""
    
    def handle_starttag(self, tag, attrs):
        tag=tag.lower()
        
        if tag=="table" and not self.in_tr:
            self.chunks=[]
            self.in_tr=True
            self.start_tag="table"
        if self.in_tr:   
            #print("tag is ",tag," attribs = ",attrs)
            #s=[tag,attrs]
            self.chunks.append(tag)
            self.chunks.append(attrs)



       
    def handle_endtag(self, tag):
        if self.in_tr:
            self.chunks.append("/"+tag)
            if tag==self.start_tag: #only add end tag matches
                self.set_flags()
                element.append(self.chunks)
                #print("tags are: ", self.chunks)

            


    def handle_data(self, data):

        if self.in_tr:
            #print("data is ",data)
            self.chunks.append(data)

def decodepage(data):
    code="utf8"
    
       
    try:
        print("trying to decode with",code)
        wpage = data.decode(code,"ignore")
        return(0,wpage) #success
    except:
        print("Error with code ",code)
    
    code="latin1"
    try:
        print("trying to decode with",code)
        wpage = data.decode(code,"ignore")
        return(0,wpage) #success
    except:
        print("Error with code ",code)
        return(-1,"") #return fail

def openpage_web(url):
    real_url=None
    ret=[]
    
    try:
        print("trying",url,"\n")

        user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'

        headers={'User-Agent':user_agent,'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',} 

        request=urllib.request.Request(url,None,headers) #The assembled request
        
        fp=urllib.request.urlopen(request)
        data = fp.read()
        
        inf=fp.info()
        code=fp.getcode()
        real_url=fp.geturl()
        if verbose:
            print("status",code)
            print("headers",inf)
        return(1,data,real_url)
    except Exception as inst:
        print("can't open file",url,"   ..skipping\n")
        #print("status",fp.getcode())
        print("error is",inst,"\n")
        return(0,"",real_url)




#########
def get_page():
    ret=openpage_web(url) #gets page and saves
    ret=decodepage(ret[1])
    if ret[0]==0:
        print("decodes ok")
        wpage=ret[1]
        return wpage

    else:
     print("need to skip can't decode file")
     return -1
     sys.exit(0) #quit


def get_data_file(file_in):
    fo=open(file_in)
    page=fo.read()
    wpage=page.strip()
    return wpage

def extract_data(wpage):
    try:
        parser.feed(wpage)
        print("parsing page")
    except Exception as e:
        print(e)
        print("parse error on page ",url,"skipping")
    count=0
    #print(element)
    rows=[]
    #print("extract data len rows",len(rows))
    t_header=[]
    td_end_flag=False
    td_flag=False
    th_flag=False
    th_end_flag=False
    for tr in element:
        process_flag=False
        l=len(tr)

        for index,line in enumerate(tr):
            #print(line)
            ret=test_string(line)
            if ret:
                line=line.strip()
                if line=="th":
                    #print(line)
                    th_flag=True
                    continue
                if line=="/th":
                    #print(t_header)
                    t_header=[]
                    th_flag=False
                    continue
                if line=="tr":
                    #print("start")
                    tr_dict=dict()
                    process_flag=True
                    td_flag=False
                    td_end_flag=False
                if line=="/tr":
                    #print("end")
                    #print(tr_dict)
                    rows.append(tr_dict)
                    process_flag=False
            if th_flag:
                t_header.append(line)

            if process_flag:
                if line=="td":
                    #print("starting td block")
                    td_flag=True
                    td_end_flag=False
                    continue
                if line== "/td":
                    td_end_flag=True
                    #print("ending td block")
                    continue
            if td_flag and not td_end_flag:
                #print("line is",line)
                if not ret: ##must be list
                    if line[0][0]=="class":
                        tr_dict[line[0][1]]=tr[index+1]
    return(rows)

def record_pages(i):
    wpage=get_page()
    if wpage!=-1:
        fileout=file_out+"/pages/"+str(i)+".html"
        f_out=open(fileout,"w")
        f_out.write(wpage)
        f_out.close()


def get_from_file(index):
    file_in=file_out+"/pages/"+str(index)+".html"
    print("reading file",file_in)
    try:
        f_in=open(file_in,"r")
    except:
        print("can't open file ",file_in)
        return -1
    wpage=f_in.read()
    f_in.close()
    return wpage
    


def get_web_page(i):
    if not get_from_disk:
        return(get_page())
    else:
        return(get_from_file(i))

##main
parser = MyHTMLParser(convert_charrefs=True)
parser.set_flags() #set initial flags
##use this code to copy pages to disk
if record_flag:
    for i in range(1,61):
        record_pages(i)
        time.sleep(60)
    raise SystemExit
##end record pages
while True:
 for i in range(1,60):
    rows=[]
    element=[] #stores all tags extracted from page
    wpage=get_web_page(i)
    if wpage!=-1:
        print("Page size read ",len(wpage))
        rows=extract_data(wpage)
    else:
        continue

    #client.publish(topic,"test")
    count=0
    pub_count=0
    pub_size=0
    #print("number of rows=",len(rows))
    #print("pubishing",i)
    for r in rows:
        count+=1
        client.loop(.001)
        
        if "fid__cell--flightNo" in r:
            flightnumber=r["fid__cell--flightNo"]
            #print(r["fid__cell--airline"]," ",r["fid__cell--flightNo"]) 
            topic=base_topic+"/"+r["fid__cell--airline"]+"/"+r["fid__cell--flightNo"]
            msg="From:"+r["fid__cell--place"]+" -Expected:"+\
         r["fid__cell--time"]+" -Status:"+r["fid__cell--details"]
            if flightnumber in data_out:
                if data_out[flightnumber]==msg:
                    #print("not publishing ",flightnumber)
                    continue #don't publish
                else:
                    pub_count+=1
                    pub_size+=len(msg)
                    data_out[flightnumber]=msg
                    client.publish(topic,msg,retain=True)

            else:
                pub_count+=1
                pub_size+=len(msg)
                data_out[flightnumber]=msg
                client.publish(topic,msg,retain=True)

    print("published ",pub_count," total bytes =",pub_size, " processed ",count)
    print("\n**********\n")
    #quit()   
    time.sleep(scan_interval) #how often to check page and output
client.disconnect
##end


