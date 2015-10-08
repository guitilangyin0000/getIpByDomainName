import re
import urllib.request
import urllib
import sys,socket

from collections import deque
#使用队列存放url 
queue = deque()
#使用一个列表保存提取到的url结果
ans_url = []

#使用visited防止重复爬同一页面
visited = set()
 
url = 'http://www.baidu.com'  # 入口页面, 可以换成别的
 #入队最初的页面
#queue.append(url)
cnt = 0
input_data = open(r'c:\Users\skl\Desktop\input.txt','r')
for each_line in input_data:
  queue.append(each_line)
print(queue)

while queue:
  url = queue.popleft()  # 队首元素出队
  visited |= {url}  # 标记为已访问
 
  print('已经抓取: ' + str(cnt) + '   正在抓取 <---  ' + url)
  cnt += 1
  #抓取页面
  urlop = urllib.request.urlopen(url)
  #判断是否为html页面
  if 'html' not in urlop.getheader('Content-Type'):
    continue
 
  # 避免程序异常中止, 用try..catch处理异常
  try:
   #转换为utf-8码
    data = urlop.read().decode('utf-8')
  except:
    continue
 
  # 正则表达式提取页面中所有队列, 并判断是否已经访问过, 然后加入待爬队列
  linkre = re.compile("https?://.{2,10}\.com")
  for x in linkre.findall(data):##返回所有有匹配的列表
    if 'http' in x and x not in visited:##判断是否为http协议链接，并判断是否抓取过
      ans_url.append(x)
no_multipul_url = set(ans_url)

infor=[]
for str in no_multipul_url:
  str1=str.split("//")
  str2=str1[1]
  infor.append(str2)
#print(infor)
dns={}
for str in infor:
  ipadd=socket.getaddrinfo(str,None)
  dns[str]=ipadd[0][4][0]
  f = open(r'c:\Users\skl\Desktop\DNS.txt','a')
  f.write(str+"  "+dns[str]+'\n')
f.close()
print(dns)


