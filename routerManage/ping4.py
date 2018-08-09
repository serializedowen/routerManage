import os
import re
# -n 指只ping一次 -w只超时间隔
op = os.popen('ping -n 1 -w 1 118.126.110.182')
result = op.read()
print(result)

p1 = re.compile('\d+%')
a1 = str(p1.findall(result)[0])
if a1=='100%':
    print('网站ping不通')
else:
    p = re.compile('\d+ms')
    a = p.findall(result)[0]
    pp = re.compile('\d+')
    aa = pp.findall(a)[0]
    print('延迟'+str(aa))