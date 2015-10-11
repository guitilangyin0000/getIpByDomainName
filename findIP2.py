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

cnt = 0
input_data = open(r'./input.txt','r')
for each_line in input_data:
  each_line = each_line.strip('\n')
  queue.append(each_line)
  visited |= {str(each_line)}
  #print(len(each_line))
#print(queue)

#生成正则表达式
linkre = re.compile("https?://.{2,18}\.com")
#linkre = re.compile("https?://[^/]+")
times = 1
while times>0:
  while queue:
    url = queue.popleft()  # 队首元素出队
    print('已经抓取: ' + str(cnt) + '   正在抓取 <---  ' + url)
    cnt += 1

    # 避免程序异常中止, 用try..catch处理异常
    try:
    #抓取页面
      urlop = urllib.request.urlopen(url)
    except:
      print("can not get " + url + "'s content'")
      continue
    #判断是否为html页面
    if 'html' not in urlop.getheader('Content-Type'):
      continue

    try:
    #转换为utf-8码
      data = urlop.read().decode('utf-8')
    except:
      continue

    for x in linkre.findall(data):##返回所有有匹配的列表
      #if 'http' in x and x not in visited:##判断是否为http协议链接，并判断是否抓取过
      if x not in visited:
        if x.endswith("baidu.com"):
          visited |= {str(x)}  # 标记为已存在
          ans_url.append(x)
  times-=1
  for y in ans_url:
    queue.append(y)

no_multipul_url = set(ans_url)

infor=[]
for str in no_multipul_url:
  str1=str.split("//")
  str2=str1[1]
  infor.append(str2)
#print(infor)
dns={}
f = open(r'./DNS.txt','a+')
for str in infor:
  try:
    ipadd=socket.getaddrinfo(str,None)
  except:
    continue
  dns[str]=ipadd[0][4][0]
  f.write(str+"  "+dns[str]+'\n')
f.close()
print(dns)


