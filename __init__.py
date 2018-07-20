import requests
import time
import math
from bs4 import BeautifulSoup

#获取当前Cookie
def getCookie(url):
    session = requests.Session()
    response = session.get(url)
    cookie = session.cookies.get_dict()
    cookie_str = []
    for key, value in cookie.items():
        cookie_str.append(key+"="+value)
    cookie_str = ';'.join(cookie_str)
    return cookie_str
    
#使用Cookie，用户名，密码访问指定网址
def login(url, cookie, username, password):
    url = url+"/login.asp"
    payload = {
        'password': password,
        'select1': '',
        'submit1.x': 26,
        'submit1.y': 7,
        'username': username
    }
    headers = {
        'origin': url,
        'upgrade-insecure-requests': "1",
        'content-type': "application/x-www-form-urlencoded",
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
        'x-devtools-emulate-network-conditions-client-id': "(CF6CFF68993929AC46BF7384FDAD3C18)",
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        'dnt': "1",
        'referer': url+"/default.asp",
        'accept-encoding': "gzip, deflate",
        'accept-language': "zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7",
        'cookie': cookie
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    return response.content.decode("gb18030",'ignore')

#使用Cookie，获取指定页面的内容
def getPage(url, cookie):
    headers = {
        'origin': url,
        'upgrade-insecure-requests': "1",
        'content-type': "application/x-www-form-urlencoded",
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
        'x-devtools-emulate-network-conditions-client-id': "(CF6CFF68993929AC46BF7384FDAD3C18)",
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        'dnt': "1",
        'referer': url+"/default.asp",
        'accept-encoding': "gzip, deflate",
        'accept-language': "zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7",
        'cookie': cookie
    }
    response = requests.request("GET", url, headers=headers)
    contents = response.content.decode("gb18030",'ignore')
    return contents

#根据网页结构摘取学生姓名和学号
def getStuinfo(stuinfo):
    index = stuinfo.find('</b>')
    trimstuinfo = stuinfo[index+4:]
    index1 = trimstuinfo.find('　')
    index2 = trimstuinfo.find('<')
    result = '';
    if(index1<index2):
        result = trimstuinfo[0:index1]
    else:
        result = trimstuinfo[0:index2]
    result = result+','
    index = trimstuinfo.find('</b>')
    trimstuinfo = trimstuinfo[index+4:]
    index1 = trimstuinfo.find('　')
    index2 = trimstuinfo.find('<')
    if(index1<index2):
        result = result + trimstuinfo[0:index1]
    else:
        result = result + trimstuinfo[0:index2]
    return result
    
#访问的目标地址
url = {
    'login': 'http://oldjw.cqu.edu.cn:8088/',
    #学生总成绩查询
    'sumscore': 'http://oldjw.cqu.edu.cn:8088/score/sel_score/sum_score_sel.asp'
}

#获取当前页面的cookie
cookie = getCookie(url['login'])

#从当前目录下的input.txt读入文件，用户名占一行，密码占一行，以此类推
inpath ='input.txt'
infile = open(inpath,'r')

#按次读取用户名和密码
username = infile.readline()
password = infile.readline()

#去除读取数据末尾的换行符
username = username.strip('\n')
password = password.strip('\n')

#计数
cnt = 1;

#循环执行，直到没有数据可供读取
while (username != ''):

    #使用设置好的cookie，用户名和密码登录
    login_res = login(url['login'], cookie, username, password)
    
    #获取所需页面的信息
    get_res = getPage(url['sumscore'], cookie)
    
    #开始文件解析
    soup = BeautifulSoup(get_res)
    stuinfo=''
    
    #根据表单结构，<p>第1次出现用于显示标题，第2次用于显示学生信息
    #若登录失败则无法打开此界面，<p>将不出现，需要处理异常
    try:
        stuinfo = str(soup.findAll('p')[1])
    except IndexError as e:
        print ('Analyze sid '+str(username)+', password '+str(password)+' failed, case '+str(cnt))
        #报错输出至日志
        outpath = 'fail.log'
        f = open (outpath,'a',encoding='gb2312',errors='ignore');
        print ('Analyze sid '+str(username)+', password '+str(password)+' failed, case '+str(cnt),file = f)
        f.close()
        pass
        
    #学生信息正常显示
    if (stuinfo!=''):
        #获取学生信息
        stuinfostr = getStuinfo(stuinfo)
        #根据表单结构找到所在行
        stugrade = soup.findAll('tr')[1]
        stugrade = stugrade.findAll('tr')
        #解析数据生成逗号表
        for idx, tr in enumerate(stugrade):
            if idx > 0:
                stuline = stuinfostr
                tds = tr.findAll('td')
                for iny, td in enumerate(tds):
                    if iny > 0:
                        stuline = stuline + ',' +(td.contents[0]).replace('\n','').replace('\r','').replace('\t','').replace(' ','')
                outpath = 'output.csv'
                f = open (outpath,'a',encoding='gb2312',errors='ignore');
                print (stuline,file = f)
                f.close()
        print ('Analyze sid '+str(username)+', password '+str(password)+' successful, case '+str(cnt))
        
    #计数器自增
    cnt = cnt + 1
    
    #反爬虫休眠
    time.sleep(3)
    
    #读取下一组数据
    username = infile.readline()
    password = infile.readline()
    username = username.strip('\n')
    password = password.strip('\n')
