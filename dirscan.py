# encoding: utf-8

import requests
from threading import Thread, activeCount
import Queue
import optparse
import time
import urlparse



parse=optparse.OptionParser('[*]WEB DIR SCAN tools')
parse.add_option('-u','--url',dest='url',help='[*]scan url http://www.xxx.com')
parse.add_option('-t','--thread',dest='thread',help='[*]threading num default 10',default=10)
parse.add_option('-s','--status_code',dest='code',help='[*]default status_code 200,eg:1 to 200,2 to 3xx,3 to 403,you can 1,2,output 200 and 3xx',default='1')
parse.add_option('-f','--file_ext',dest='file_ext',help='[*] scan filetype',default='php')
(opt,args)=parse.parse_args()


if opt.url == None:
    parse.print_help()
    exit()


''' url format'''

t=urlparse.urlparse(opt.url)
if t.scheme=='' or t.netloc=='':
    print '[*]url format: -u http://www.xxx.com'
    exit()

''' status code'''
file_exts=['php','asp','aspx','jsp','jspx']
dir_file='./dics/dirs.txt'

status_codes=[]
code=opt.code
try:
    if code.index(','):
        code = code.split(',')
except:
    pass
for c in code:
    if c=='1':
        status_codes.append(200)
    elif c=='2':
        b3xx=[301,302,304]
        status_codes.extend(b3xx)
    elif c=='3':
        status_codes.append(403)

if not status_codes:
    print '[*]status_code format: -s 1,eg: -s 1,2'
    exit()

queue = Queue.Queue()


def scan_url_exists(url):
    headers={
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:50.0) Gecko/20100101 Firefox/50.0',
        'Accept-Language': 'en,zh-CN;q=0.8,zh;q=0.5,en-US;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        'Referer': 'http://www.google.com'}

    try:
        req=requests.head(url.strip(),timeout=8,headers=headers)
        if req.status_code in status_codes:
            print url + ' code:' + str(req.status_code)
            open('exists_url.txt','a').write(url)
    except:
        print url+' not request'



def open_pathfile(file):
    alllines=open(file,'r').readlines()
    for line in alllines:
        if url.endswith('/'):
            if line.startswith('/'):
                queue.put(url+line[1:].replace('%EXT%', file_ext))
            else:
                queue.put(url + line.replace('%EXT%', file_ext))
        else:
            if line.startswith('/'):
                queue.put(url + line.replace('%EXT%', file_ext))
            else:
                queue.put(url + '/' + line.replace('%EXT%', file_ext))



if __name__ == '__main__':
    url=opt.url
    if not opt.file_ext in file_exts:
        print '[*]scan filetype mush asp,aspx,php,jsp,jspx'
        exit()
    file_ext=opt.file_ext
    open_pathfile(dir_file)
    while queue.qsize() > 0:
        if activeCount() <= int(opt.thread):
            Thread(target=scan_url_exists,args=(queue.get(),)).start()


