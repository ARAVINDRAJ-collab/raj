import sys
import  os
import requests
from bs4 import BeautifulSoup
import re
import socket




def is_downloadable(url):
    """
    Does the url contain a downloadable resource
    """
    h = requests.head(url, allow_redirects=True)
    header = h.headers
    content_type = header.get('content-type')
    if 'text' in content_type.lower():
        return False
    if 'html' in content_type.lower():
        return False
    return True


def download_latest_build(url):

    """
    Downloads the latest build
    """
   # print("indownload",run_time)
    build_list=[]
    i = 0
    check_sum=[]
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
   # print (soup.encode('utf-8'))

    for Build in soup.find_all('a', href = re.compile(r'(.*Rel.*Linux.*bin$)|(.*.gz)')):
        build_list.append(Build.text)
        #print ("\n Servers:")
      #  print ("build_text=" ,Build.text)


   # build_list.pop(build_list.index("NFM_Rel_22.0_1.1123.Linux-x86_64.bin"))
   # print("list=",*build_list)
    build_list.sort(reverse=True)
  #  for x in build_list:
  #      print ("x=" ,x)
    s = re.compile("(^AS.*)|(^NS.*)|(^XSP.*)|(^PS.*)|(^IP.*)|(XS.*)")
    build_list = list(filter(s.match, build_list))  # Note 1
  #  print("newlist=" ,build_list)
    asmode(url,build_list)

   # n = build_list.index([i for i in build_list if re.findall(r'^IP.ps.*.gz', i)][0])
    #str2 = 'IP.ps.24.0.562.ip20190906.Linux-x86_64.tar.md5sum'
   # str2 = build_list[i for i in build_list if re.findall(r'^IP.ps.*.gz', i)][0]]
    #print ("str=" ,str2)
    #newstr = " ".join((url, str2))
   # newstr = url + str2
   # print ("newstr=" ,newstr)
    s = ['^XS','^PS']
    print("s[0]=",s[0])
   # r =r'(s[0])'
   # print(r)
    n = build_list.index([i for i in build_list if re.findall((s[1]),i)][0])
    print("n=", n)

   # print("sed -i '/latest_build/c\latest_build: " + sorted(build_list)[-1].strip(".bin") + "' " + "vars.yml")
   # os.system("sed -i '/latest_build/c\latest_build: " + sorted(build_list)[-1].strip(".bin") + "' " + "vars.yml")
   # if is_downloadable(newstr):
       # file_obj = requests.get(newstr, allow_redirects=True)
        #print ("file=" ,file_obj)
       # open('demo', 'wb').write(file_obj.content)

    #f = open("demo", "r")
   # for x in f:
      #  check_sum.append(x)
      #  print(x)


    #for x in check_sum:
      #  print("check=" ,x)
   # print ("answer=" ,check_sum[0].split())
    #a = check_sum[0].split()
    #print ("check1=" ,a)
    #for x in check_sum:
       # vv = x.split()
       # print ("\nvv=" ,vv)
   # with open('str2', encoding='utf-8') as content_file:
    #    content = content_file.read()
    #    print (content)

    #if is_downloadable(url + sorted(build_list)[-1].strip("bin") + "md5sum"):
     #   file_obj = requests.get(url+sorted(build_list)[-1], allow_redirects=True)
      #  open("/var/tmp/" + sorted(build_list)[-1].strip("bin")+ "md5sum", 'wb').write(file_obj.content)

def asmode(url,build_list):
   #  print("asmode=",url,build_list)
     server=['^PS.*.bin','^IP.ps.*.gz','^NS.*.bin','^IP.ns.*.gz','^XS.*.bin','^IP.xs.*.gz','^XSP.*.bin','^IP.xsp.*.gz',]
     server_map=['.*xs-ps.*','.*xs-ns.*','.*xs-xs.*','.*xs-xsp.*']
     hostname = 'che-bw3-xs-ps1'
   # m = server_map.index([i for i in server_map if re.match(i,(hostname))])
     for i in server_map:
         print(i)
         if re.match(i, (hostname)):
             m = i;
             print("n=", m)
             m = server_map.index(m)
             print("serverindex=", m)
     print("m=",m)
     if m==0:
         m=-1
     k=1;
     print("m=", m)
     for j in range(m+1,m+3):
            print("j=",j)
            n = build_list.index([i for i in build_list if re.findall((server[j]), i)][0])
            print("build",build_list[n])
            if is_downloadable(url + build_list[n]):
                file_obj = requests.get(url + build_list[n], allow_redirects=True, stream=True)
                try:
                    print("downloading",build_list[n])
                    with open("/var/lib/awx/" + build_list[n], 'wb') as fp:
                        for chunk in file_obj.iter_content(chunk_size=1024):
                            if chunk:
                                fp.write(chunk)
                except StopIteration:
                    break
            print ("DOwnloaded",build_list[n])


def download_specific_build(url,  buildname):


    """
    Downloads the Specific build
    """

    if is_downloadable(url + buildname + ".bin"):
        file_obj = requests.get(url+buildname, allow_redirects=True)
        open("/var/tmp/" + buildname + ".bin", 'wb').write(file_obj.content)

    if is_downloadable(url + buildname + ".md5sum"):
        file_obj = requests.get(url+buildname, allow_redirects=True)
        open("/var/tmp/" + buildname + ".md5sum", 'wb').write(file_obj.content)


if __name__ == "__main__":

    url = 'http://10.8.7.33/Linux/x86_64/releases_rhel6/'
    run_time =[]
    for eachArg in sys.argv:
        print(eachArg)
        run_time.append(eachArg)
    print("length=",len(sys.argv))
  #  print ("run=",*run_time)
    if  run_time[1] == 'latest' :
        download_latest_build(url)
   # else:
    #    download_specific_build(run_time[3])

