from django.shortcuts import render
from router import models
from django.http import FileResponse
import json
import os
import datetime
import xlrd
from xlwt import *
import random
import re
from django.http import HttpResponse, HttpResponseRedirect
import time
from django.core.mail import send_mail
from routerManage.settings import EMAIL_FROM

'''
ctrl + alt + L 进行代码的格式化
'''


# Create your views here.


def upload_txt(request):
    return render(request, 'upload.html')


def index(request):
    return render(request, 'index.html')


'''
文件上传接口
通过post将指定的xls格式的ip分配表上传到服务器
'''
def upload(request):
    if request.method == "POST":
        obj = request.FILES.get('IP_table', None)
        print(obj.name)
        f = open('static/IP_table.xls', 'wb')  # 保存文件
        print(obj)
        for chuck in obj.chunks():
            f.write(chuck)
        f.close()
        excel_table_byname()
        return HttpResponse('上传成功')
    re = json.dumps({
        "status": '0',
        "msg": '上传错误'
    })
    return HttpResponse(re, content_type='application/json')


'''
打开后台检测功能
'''
def start_ping(request):
    try:

        i = 0
        while 1:
            Ping()
            time.sleep(120)
            i = i + 1
    except:
        return HttpResponse('网站查询失败')

'''
将上传的文件插入到数据库中，默认上传之后自动插入
接口的作用是 恢复、还原重置数据库内容
'''
def start_insert(request):
    re = excel_table_byname()
    return HttpResponse(re, content_type='application/json')


'''
将数据库内容进行全部导出
'''
def excel_export(request):
    list_obj = models.IP.objects.all()
    if list_obj:
        # 创建工作薄
        ws = Workbook(encoding='utf-8')
        w = ws.add_sheet(u"数据报表第一页")
        w.write(0, 0, u"Vlan")  # 添加表头数据
        w.write(0, 1, u"主机IP")
        w.write(0, 2, u"是否运行")
        w.write(0, 3, u"单位|组织")
        w.write(0, 4, u"主机用途")
        w.write(0, 5, u"域名")
        w.write(0, 6, u"负责人")
        w.write(0, 7, u"联系电话")
        w.write(0, 8, u"管理员")
        w.write(0, 9, u"联系电话")
        w.write(0, 10, u"系统类型")
        w.write(0, 11, u"Cpu")
        w.write(0, 12, u"内存")
        w.write(0, 13, u"存储")
        w.write(0, 14, u"远程协助")
        w.write(0, 15, u"SSH")
        w.write(0, 16, u"Telnet")
        w.write(0, 17, u"主机用户")
        w.write(0, 18, u"主机密码")
        w.write(0, 19, u"主机管理方式（托管|自营")
        w.write(0, 20, u"数据库类型")
        w.write(0, 21, u"能否开放接口")
        w.write(0, 22, u"外网开放端口")
        w.write(0, 23, u"备注")
        w.write(0, 24, u"集群")
        w.write(0, 25, u"最后修改时间")

        # 写入数据
        excel_row = 1
        for obj in list_obj:
            data_id = obj.vlan
            if obj.status == str(1):
                data_status = '当前正在运行'
            else:
                data_status = '当前停止运行'
            data_content = obj.name
            w.write(excel_row, 0, obj.vlan)
            w.write(excel_row, 1, obj.host)
            w.write(excel_row, 2, data_status)
            w.write(excel_row, 3, obj.name)
            w.write(excel_row, 4, obj.thing)
            w.write(excel_row, 5, obj.domain)
            w.write(excel_row, 6, obj.person_name)
            w.write(excel_row, 7, obj.person_tel)
            w.write(excel_row, 8, obj.admin_name)
            w.write(excel_row, 9, obj.admin_tel)
            w.write(excel_row, 10, obj.system_type)
            w.write(excel_row, 11, obj.cpu)
            w.write(excel_row, 12, obj.momory)
            w.write(excel_row, 13, obj.storage)
            w.write(excel_row, 14, obj.assistance)
            w.write(excel_row, 15, obj.ssh)
            w.write(excel_row, 16, obj.telnet)
            w.write(excel_row, 17, obj.host_user)
            w.write(excel_row, 18, obj.host_password)
            w.write(excel_row, 19, obj.host_manage_type)
            w.write(excel_row, 20, obj.sql_type)
            w.write(excel_row, 21, obj.is_post)
            w.write(excel_row, 22, obj.post)
            w.write(excel_row, 23, obj.remark)
            w.write(excel_row, 24, obj.colony)
            w.write(excel_row, 25, obj.times)
            excel_row += 1
        # 检测文件是够存在
        # 方框中代码是保存本地文件使用，如不需要请删除该代码
        exist_file = os.path.exists("test.xls")
        if exist_file:
            os.remove(r"test.xls")
        ws.save("test.xls")
        file = open('test.xls', 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="IP.xls"'
        return response


'''
用户的登录
'''
def login(request):
    print('aa')
    if request.method == "POST":
        user_number = request.POST.get('user_number', None)
        user_password = request.POST.get('user_password', None)
        if models.User.objects.filter(user_number=user_number):
            userlist = models.User.objects.get(user_number=user_number)
            if str(user_password) == str(userlist.user_password):
                print('用户登录成功')
                re = json.dumps({
                    'status': '1',
                    'msg': '登录成功'
                })
                res = HttpResponse(re, content_type='application/json')
                res.set_cookie('user_number', user_number)  # 将用户编号设置为cookie
                request.session['user_number'] = user_number
                request.session['user_password'] = user_password
                return res
            else:
                re = json.dumps({
                    'status': '0',
                    'msg': '密码错误'
                })
                return HttpResponse(re, content_type='application/json')
        else:
            re = json.dumps({
                'status': '0',
                'msg': '用户名不存在'
            })
            return HttpResponse(re, content_type='application')


def logout(request):
    if request.session.get('user_number') == None:
        re = json.dumps({
            'status': '1',
            'msg': '清楚session失败，咩有可清楚的session'
        })
    else:
        request.session.clear()
        re = json.dumps({
            'status': '0',
            'msg': '清楚session成功'
        })
    return HttpResponse(re, content_type='application/json')


'''
返回所有的ip信息
'''


def get_all_data(request):
    if request.method == "GET":
        all_data = models.IP.objects.all()  # 返回一个列表
        all = []  # 要返回的最终列表
        # child ={} #每一个all的元素
        for i in range(len(all_data)):
            child = {}  # 每一个all的元素
            child['vlan'] = all_data[i].vlan
            child['host'] = all_data[i].host
            child['name'] = all_data[i].name
            child['thing'] = all_data[i].thing
            child['domain'] = all_data[i].domain
            child['person_name'] = all_data[i].person_name
            child['person_tel'] = all_data[i].person_tel
            child['admin_name'] = all_data[i].admin_name
            child['admin_tel'] = all_data[i].admin_tel
            child['system_type'] = all_data[i].system_type
            child['cpu'] = all_data[i].cpu
            child['momory'] = all_data[i].momory
            child['storage'] = all_data[i].storage
            child['assistance'] = all_data[i].assistance
            child['ssh'] = all_data[i].ssh
            child['telnet'] = all_data[i].telnet
            child['host_user'] = all_data[i].host_user
            child['host_password'] = all_data[i].host_password
            child['host_manage_type'] = all_data[i].host_manage_type
            child['sql_type'] = all_data[i].sql_type
            child['is_post'] = all_data[i].is_post
            child['post'] = all_data[i].post
            child['remark'] = all_data[i].remark
            child['colony'] = all_data[i].colony
            child['status'] = all_data[i].status
            child['times'] = all_data[i].times
            child['ms'] = all_data[i].ms
            all.append(child)
        re = json.dumps({
            'status': '0',
            'msg': '成功',
            'data': all
        })
        return HttpResponse(re, content_type='application/json')


'''
获取所有可以分配的ip
'''


def get_all_allot(request):
    if request.method == "GET":
        print('ll')
        all_data = models.IP.objects.filter(name='').all()
        print(all_data)
        all = []
        for i in range(len(all_data)):
            child = {}
            child['host'] = all_data[i].host
            all.append(child)
        print(all)

        re = json.dumps({
            'status': '0',
            'msg': '查询成功',
            'data': all
        })
        return HttpResponse(re, content_type='application/json')


'''
参数：vlan = vlan621
方式：get
返回：ip 一个可以分配的ip
根据前端的参数vlan自动生成一个可以使用的ip
随机生成一个可以分配的ip
'''


def get_one_ip(request):
    if request.method == "GET":
        vlan = request.GET.get('vlan', None)  # 获取用户选择的vlan
        vlans = ['vlan621', 'vlan622', 'vlan623', 'vlan624', 'vlan625', 'vlan626', 'vlan627', 'vlan628']
        if vlan != None and (vlan in vlans):
            all_data = list(models.IP.objects.filter(vlan=vlan, name='').all())
            if len(all_data) == 0:
                re = json.dumps({
                    'status': '0',
                    'msg': '此vlan已经没有可以分配的ip'
                })
                return HttpResponse(re, content_type='application/json')
            else:
                j = random.randint(0, len(all_data) - 1)
                ip = all_data[j].host
                re = json.dumps({
                    'status': '1',
                    'msg': '已经产生随机的可分配的ip',
                    'data': ip
                })
                return HttpResponse(re, content_type='application/json')
        else:
            re = json.dumps({
                'status': '0',
                'msg': '咩有这个vlan'
            })
            return HttpResponse(re, content_type='application/json')


'''
分配ip
参数 23个
根据前端的参数，将数据写入对应的位置
'''


def set_one_ip(request):
    if request.method == 'POST':
        host = request.POST.get('host', None)
        name = request.POST.get('name', None)
        thing = request.POST.get('thing', None)
        domain = request.POST.get('domain', None)
        person_name = request.POST.get('person_name', None)
        person_tel = request.POST.get('person_tel', None)
        admin_name = request.POST.get('admin_name', None)
        admin_tel = request.POST.get('admin_tel', None)
        system_type = request.POST.get('system_type', None)
        cpu = request.POST.get('cpu', None)
        momory = request.POST.get('momory', None)
        storage = request.POST.get('storage', None)
        assistance = request.POST.get('assistance', None)
        ssh = request.POST.get('ssh', None)
        telnet = request.POST.get('telnet', None)
        host_user = request.POST.get('host_user', None)
        host_password = request.POST.get('host_password', None)
        host_manage_type = request.POST.get('host_manage_type', None)
        sql_type = request.POST.get('sql_type', None)
        is_post = request.POST.get('is_post', None)
        post = request.POST.get('post', None)
        remark = request.POST.get('remark', None)
        colony = request.POST.get('colony', None)
        tim = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if host != None and name != None and models.IP.objects.filter(host=host, name=''):  # ip和单位不为空,并且主机所对应的name字段为空
            models.IP.objects.filter(host=host).update(  # 找到ip对应的信息，更新这条信息
                name=name,
                thing=thing,
                domain=domain,
                person_name=person_name,
                person_tel=person_tel,
                admin_name=admin_name,
                admin_tel=admin_tel,
                system_type=system_type,
                cpu=cpu,
                momory=momory,
                storage=storage,
                assistance=assistance,
                ssh=ssh,
                telnet=telnet,
                host_user=host_user,
                host_password=host_password,
                host_manage_type=host_manage_type,
                sql_type=sql_type,
                is_post=is_post,
                post=post,
                remark=remark,
                colony=colony,
                times=tim
            )
            re = json.dumps({
                'status': '1',
                'msg': 'ip分配成功'
            })
            return HttpResponse(re, content_type='application/json')

        else:
            re = json.dumps({
                'status': '0',
                'msg': 'ip不可以被分配,重新选择ip',
            })
            return HttpResponse(re, content_type='application/json')


'''
修改信息的接口
'''


def change_one_ip(request):
    if request.method == 'POST':
        host = request.POST.get('host', None)
        name = request.POST.get('name', None)
        thing = request.POST.get('thing', None)
        domain = request.POST.get('domain', None)
        person_name = request.POST.get('person_name', None)
        person_tel = request.POST.get('person_tel', None)
        admin_name = request.POST.get('admin_name', None)
        admin_tel = request.POST.get('admin_tel', None)
        system_type = request.POST.get('system_type', None)
        cpu = request.POST.get('cpu', None)
        momory = request.POST.get('momory', None)
        storage = request.POST.get('storage', None)
        assistance = request.POST.get('assistance', None)
        ssh = request.POST.get('ssh', None)
        telnet = request.POST.get('telnet', None)
        host_user = request.POST.get('host_user', None)
        host_password = request.POST.get('host_password', None)
        host_manage_type = request.POST.get('host_manage_type', None)
        sql_type = request.POST.get('sql_type', None)
        is_post = request.POST.get('is_post', None)
        post = request.POST.get('post', None)
        remark = request.POST.get('remark', None)
        colony = request.POST.get('colony', None)
        tim = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if host != None and name != None and models.IP.objects.filter(
                host=host):  # ip和单位不为空,并且主机所对应的name字段不空
            models.IP.objects.filter(host=host).update(  # 找到ip对应的信息，更新这条信息
                name=name,
                thing=thing,
                domain=domain,
                person_name=person_name,
                person_tel=person_tel,
                admin_name=admin_name,
                admin_tel=admin_tel,
                system_type=system_type,
                cpu=cpu,
                momory=momory,
                storage=storage,
                assistance=assistance,
                ssh=ssh,
                telnet=telnet,
                host_user=host_user,
                host_password=host_password,
                host_manage_type=host_manage_type,
                sql_type=sql_type,
                is_post=is_post,
                post=post,
                remark=remark,
                colony=colony,
                times=tim
            )
            re = json.dumps({
                'status': '1',
                'msg': 'ip分配成功'
            })
            return HttpResponse(re, content_type='application/json')

        else:
            re = json.dumps({
                'status': '0',
                'msg': 'ip不可以被分配,重新选择ip',
            })
            return HttpResponse(re, content_type='application/json')


'''
删除数据（只平清空数据，不删除数据）
'''


def del_host(request):
    if request.method == 'POST':
        host = request.POST.get('host', None)  # 获取要删除的主机ip
        tim = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if models.IP.objects.filter(host=host):
            models.IP.objects.filter(host=host).update(  # 找到ip对应的信息，更新这条信息
                name='',
                thing='',
                domain='',
                person_name='',
                person_tel='',
                admin_name='',
                admin_tel='',
                system_type='',
                cpu='',
                momory='',
                storage='',
                assistance='',
                ssh='',
                telnet='',
                host_user='',
                host_password='',
                host_manage_type='',
                sql_type='',
                is_post='',
                post='',
                remark='',
                colony='',
                times=tim,
                status='',
                ms=''

            )
            re = json.dumps({
                'status': '1',
                'msg': '主机重置成功'
            })
            return HttpResponse(re, content_type='application/json')

        else:
            re = json.dumps({
                'status': '0',
                'msg': 'ip不可以被重置,重新选择ip',
            })
            return HttpResponse(re, content_type='application/json')


'''
修改信息
参数 host
返回 此ip的所有信息
根据host（ip）来查询具体的信息
'''


def get_by_ip(request):
    if request.method == 'GET':
        host = request.GET.get('host', None)
        if host != None:
            all_data = models.IP.objects.filter(host=host).all()
            all = []
            for i in range(len(all_data)):
                child = {}  # 每一个all的元素
                child['vlan'] = all_data[i].vlan
                child['host'] = all_data[i].host
                child['name'] = all_data[i].name
                child['thing'] = all_data[i].thing
                child['domain'] = all_data[i].domain
                child['person_name'] = all_data[i].person_name
                child['person_tel'] = all_data[i].person_tel
                child['admin_name'] = all_data[i].admin_name
                child['admin_tel'] = all_data[i].admin_tel
                child['system_type'] = all_data[i].system_type
                child['cpu'] = all_data[i].cpu
                child['momory'] = all_data[i].momory
                child['storage'] = all_data[i].storage
                child['assistance'] = all_data[i].assistance
                child['ssh'] = all_data[i].ssh
                child['telnet'] = all_data[i].telnet
                child['host_user'] = all_data[i].host_user
                child['host_password'] = all_data[i].host_password
                child['host_manage_type'] = all_data[i].host_manage_type
                child['sql_type'] = all_data[i].sql_type
                child['is_post'] = all_data[i].is_post
                child['post'] = all_data[i].post
                child['remark'] = all_data[i].remark
                child['colony'] = all_data[i].colony
                child['status'] = all_data[i].status
                child['times'] = all_data[i].times
                child['ms'] = all_data[i].ms
                all.append(child)
            re = json.dumps({
                'status': '0',
                'msg': '成功',
                'data': all
            })
            return HttpResponse(re, content_type='application/json')


'''
获取此vlan的所有数据信息
参数 vlan_id
 
'''


def get_all_data_by_vlan_id(request):
    if request.method == "GET":
        vlan_id = request.GET.get('vlan', None)
        all_data = models.IP.objects.filter(vlan=vlan_id).all()  # 根据vlan的不同查询不同的数据
        if all_data:
            all = []
            for i in range(len(all_data)):
                child = {}  # 每一个all的元素
                child['vlan'] = all_data[i].vlan
                child['host'] = all_data[i].host
                child['name'] = all_data[i].name
                child['thing'] = all_data[i].thing
                child['domain'] = all_data[i].domain
                child['person_name'] = all_data[i].person_name
                child['person_tel'] = all_data[i].person_tel
                child['admin_name'] = all_data[i].admin_name
                child['admin_tel'] = all_data[i].admin_tel
                child['system_type'] = all_data[i].system_type
                child['cpu'] = all_data[i].cpu
                child['momory'] = all_data[i].momory
                child['storage'] = all_data[i].storage
                child['assistance'] = all_data[i].assistance
                child['ssh'] = all_data[i].ssh
                child['telnet'] = all_data[i].telnet
                child['host_user'] = all_data[i].host_user
                child['host_password'] = all_data[i].host_password
                child['host_manage_type'] = all_data[i].host_manage_type
                child['sql_type'] = all_data[i].sql_type
                child['is_post'] = all_data[i].is_post
                child['post'] = all_data[i].post
                child['remark'] = all_data[i].remark
                child['colony'] = all_data[i].colony
                child['status'] = all_data[i].status
                child['times'] = all_data[i].times
                child['ms'] = all_data[i].ms
                all.append(child)

            # 组织 ip 是否被分配的信息--------------
            vlan0 = models.IP.objects.filter(name='', vlan=vlan_id).count()  # 可以被分配的ip
            vlan1 = models.IP.objects.filter(vlan=vlan_id).count() - vlan0  # 已经被分配的ip
            vlan = {}  # 返回vlan信息
            vlan['vlan0'] = vlan0
            vlan['vlan1'] = vlan1

            # 阻止 ip 是否可用的信息--------------

            ip0 = models.IP.objects.exclude(name='').filter(vlan=vlan_id, status='1').count()
            ip1 = models.IP.objects.exclude(name='').filter(vlan=vlan_id, status='0').count()  # 0表示可以ping通
            print('aaa')
            print(ip0)
            print(ip1)
            ip = {}
            ip[0] = ip0
            ip[1] = ip1

            # 组织返回的数据------------
            data = {}  # 返回的所有数据
            data['all_data'] = all
            data['vlan'] = vlan
            data['ip'] = ip
            print(data)
            re = json.dumps({
                'status': '0',
                'msg': '成功',
                'data': data

            })
            return HttpResponse(re, content_type='application/json')


'''
获取错误信息的接口
'''


def getError(request):
    if request.method=="POST":
        error_status1 = models.Error.objects.all().order_by('-error_id') #已分配，未运行
        # error_status0 = models.Error.objects.filter(status='0').all().order_by('-error_id') #未分配，在运行
        error1 = []
        # error0 = []
        for i in range(len(error_status1)):
            e={}
            if int(error_status1[i].host.split('.')[-1]) < 31:
                e['vlan'] ='vlan621'
            elif int(error_status1[i].host.split('.')[-1]) < 63:
                e['vlan'] = 'vlan622'
            elif int(error_status1[i].host.split('.')[-1]) < 95:
                e['vlan'] = 'vlan623'
            elif int(error_status1[i].host.split('.')[-1]) < 127:
                e['vlan'] = 'vlan624'
            elif int(error_status1[i].host.split('.')[-1]) < 159:
                e['vlan'] = 'vlan625'
            elif int(error_status1[i].host.split('.')[-1]) < 191:
                e['vlan'] = 'vlan626'
            elif int(error_status1[i].host.split('.')[-1]) < 223:
                e['vlan'] = 'vlan627'
            elif int(error_status1[i].host.split('.')[-1]) < 255:
                e['vlan'] = 'vlan628'

            e['host']=error_status1[i].host
            e['time']=error_status1[i].time
            e['text']=error_status1[i].text
            e['status']=error_status1[i].status
            error1.append(e)

        re = json.dumps({
            'status':'1',
            'msg':'',
            'data':{
                'error1':error1,
                # 'error0':error0
            }
        })
        return HttpResponse(re,content_type='application/json')


'''
用户注册的接口
'''

def setUser(request):
    if request.method=="POST":
        name = request.POST.get('name',None)
        password = request.POST.get('password',None)
        mail = request.POST.get('mail',None)
        if models.User.objects.filter(user_number=name):
            re = json.dumps({
                'status':'0',
                'msg':'用户名重复',
            })
            return HttpResponse(re,content_type='application/json')
        else:
            models.User.objects.create(
                user_number = name,
                user_password = password,
                user_mail = mail
            )
            re = json.dumps({
                'status':'1',
                "msg":'注册成功',
            })
            return  HttpResponse(re,content_type='application/json')

'''
检测是否监控的接口
根据请求的时间返回是否在监控
'''

def monitor(request):
    now = int(time.time())  #获取当前时间的时间戳
    print(now)
    tim = models.Time.objects.last() #获取最近的一条记录
    print(tim.times)
    x = now - int(tim.times)  #当前时间和最后一次数据库存储的时间的差值---1800  半个小时
    if x> 1800: #时间相隔差30分钟以上，说明后台进程停掉了
        re = json.dumps({
            'status':'0',
            'msg':'检测进程消失'
        })
        return HttpResponse(re,content_type='application/json')
    else:
        re = json.dumps({
            'status':'1',
            'msg':'检测进程正常运行'
        })
        return HttpResponse(re,content_type='application/json')


'''
获得近期系统运行的数据信息
返回一定时间内的主机的运行情况，
时间 运行中个数 未运行个数  共100条  

'''


def getWorkData(request):
    all = list(models.Time.objects.all().order_by('-time_id')[0:99])
    print(len(all))
    data = []
    lens = len(all)
    for i in range(100):
        if i<lens:
            d ={}
            d['number'] = 99-i
            d['time'] = str(all[i].time)
            d['count1'] = all[i].count1
            d['count0'] = all[i].count0
        else:
            d={}
            d['number'] = 99-i
            d['time'] = '0'
            d['count0'] = '0'
            d['count1'] = '0'
        data.append(d)
    print(data)
    data.reverse()
    re =json.dumps({
        'status':'1',
        'msg':'',
        'data':data
    })
    return  HttpResponse(re,content_type='application/json')










'''
发送邮件接口
参数 ：
email_title 标题
email_body  主要内容
email_to  接收人的邮箱列表

'''


def sendmail(email_title, email_body):
    print('准备发送')
    email_list = list(models.User.objects.exclude(user_mail='None').values('user_mail'))
    email_to = []
    for i in range(len(email_list)):
        a = email_list[i].get('user_mail')
        if a:
            res = re.search('@qq.com$', a)
            if res:
                email_to.append(a)
            else:
                pass
    print(email_to)
    send_status = send_mail(email_title, email_body, "1027908281@qq.com", email_to, fail_silently=False)
    send_status=True
    if send_status:
        print('发送成功')
        return 1
    else:
        return 0


'''
ping主机，将成功和失败的主机ip保存在数据库中，然后记录下ping的具体时间
'''


def Ping():
    import time
    start_Time = int(time.time())
    # ip_True = open('static/ip/ip_True.txt', 'w+')
    # ip_False = open('static/ip/ip_False.txt', 'w+')
    IPhost = []
    # IPbegin = (input(u'请输入起始查询IP： '))
    # IPend = input(u'请输入终止查询IP： ')
    IPbegin = '222.24.62.1'
    IPend = '222.24.62.255'
    IP1 = IPbegin.split('.')[0]
    IP2 = IPbegin.split('.')[1]
    IP3 = IPbegin.split('.')[2]
    IP4 = IPbegin.split('.')[-1]
    IPend_last = IPend.split('.')[-1]
    count_True, count_False = 0, 0

    list1 = []  # 保存可以ping同的网站
    list0 = []  # 保存ping不同的网站
    for i in range(int(IP4) - 1, int(IPend_last)):
        ip = str(IP1 + '.' + IP2 + '.' + IP3 + '.' + IP4)
        int_IP4 = int(IP4)
        int_IP4 += 1
        IP4 = str(int_IP4)
        op = os.popen('ping -c 1 -w 1 %s' % ip)  # 让系统去执行ping命令-----------在ubuntu环境下使用ping -c 1 -w 1
        res = op.read()
        p1 = re.compile('\d+%')
        a1 = str(p1.findall(res)[0])  # 根据a1的值来判断网站是不是可以访问，100%表示不可以访问，
        if a1 == '100%':
            # print('网站ping不通')---------------------主机不在运行
            if models.IP.objects.filter(host=ip):  # 将情况保存在ip表中
                models.IP.objects.filter(host=ip).update(
                    status='0',  # 网站ping不同的情况
                    ms='0'
                )
                list0.append(ip)
                count_False += 1

            if models.IP.objects.exclude(name='').filter(host=ip):  # 主机不在运行，但是主机被分配-------------->异常
                if models.Error.objects.filter(host=ip):  # 如果error表中已经有数据就不重复添加
                    pass
                else:
                    _op = os.popen('ping -c 1 -w 1 %s' % ip)
                    _res = _op.read()
                    _p1 = re.compile('\d+%')
                    _a1 = str(_p1.findall(_res)[0])  # 根据a1的值来判断网站是不是可以访问，100%表示不可以访问，
                    if _a1 == '100%':  # 再次确认一遍，然后将错误记录下来

                        tim = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 当前时间
                        models.Error.objects.create(
                            host=ip,
                            text='已分配，未运行',
                            time=tim
                        )
                        email_title = '警告' + str(ip) + str(tim)
                        email_body = str(ip) + '已分配，未运行'

                        ret = sendmail(email_title, email_body)
                        if ret == 1:
                            print('邮件发送完成')
                        else:
                            print('邮件发送失败')

                            # email_to = ['1027908281@qq.com','1968618449@qq.com','363748101@qq.com','2915681468@qq.com']
                            # 调用发邮件函数
            else:  # 主机不在运行，同时主机也没有被分配  -->此主机正常  -->查看error表中是否有此条记录，有的话就删除掉
                if models.Error.objects.filter(host=ip):
                    models.Error.objects.filter(host=ip).delete()

        else:

            if models.IP.objects.filter(host=ip):
                # print('网站能ping通')--------------------------主机在运行
                p = re.compile('\d+ms')
                a = p.findall(res)[0]  # a 保存的是ping的延迟大小
                pp = re.compile('\d+')  # 只匹配数字
                aa = pp.findall(a)[0]  # 取出延迟   获取网站的延迟
                models.IP.objects.filter(host=ip).update(
                    status='1',
                    ms=aa
                )
                list1.append(ip)
                count_True += 1

                if models.IP.objects.filter(host=ip, name=''):  # 主机在运行，但是主机没有被分配------->异常
                    if models.Error.objects.filter(host=ip):
                        pass
                    else:
                        tim = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        models.Error.objects.create(
                            host=ip,
                            time=tim,
                            text='未分配，在运行',
                            status='0'
                        )
                        # 调用发邮件函数
                        email_title = '警告' + "-" + str(ip) + "-" + str(tim)
                        email_body = str(ip) + '未分配，在运行'
                        # email_to = ['1027908281@qq.com','1968618449@qq.com','363748101@qq.com','2915681468@qq.com']
                        # 调用发邮件函数
                        _op = os.popen('ping -c 1 -w 1 %s' % ip)
                        _res = _op.read()
                        _p1 = re.compile('\d+%')
                        _a1 = str(_p1.findall(_res)[0])  # 根据a1的值来判断网站是不是可以访问，100%表示不可以访问，
                        if _a1 != '100%':
                            ret = sendmail(email_title, email_body)
                            if ret == 1:
                                print('邮件发送完成')
                            else:
                                print('邮件发送失败')
                else:  # 主机在运行，但是主机没有被分配--->此主机正常  ---->查看error表中是否有此主机的记录，有的话就可以删除掉
                    if models.Error.objects.filter(host=ip):
                        models.Error.objects.filter(host=ip).delete()

    print(list0)  # 可以ping通的网站的列表
    print(list1)  # ping不通的网站的列表

    #保存 当前时间的时间戳  ---
    tim = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 记录一次ping的时间
    now = int(time.time())  #->时间戳
    models.Time.objects.create(
        time =tim,
        times=now,
        list1=list1,
        list0=list0,
        count1=count_False,
        count0=count_True
    )
    end_Time = int(time.time())
    print("time(秒)：", end_Time - start_Time, "s")
    print("ping通的ip数：", count_True, "   ping不通的ip数：", count_False)


'''
刷新error表中的数据
如果用户进行了更改，将会刷新error表中的数据
'''

def reError(request):
    if request.method=="POST":
        all = list(models.Error.objects.all())
        print(all)
        for i in range(len(all)):
            ip = all[i].host #获取到error中的ip
            if models.IP.objects.filter(host=ip,name=''): #未分配
                if all[i].status=='1': #未运行
                    models.Error.objects.filter(host=ip).delete()  #将这条error信息删除掉
            else:  #已分配
                if all[i].status=='0': #在运行
                    models.Error.objects.filter(host=ip).delete()
        re = json.dumps({
            'status':'1',
            'msg':'刷新成功',
        })
        return HttpResponse(re,content_type='application/json')





# 打开excel表格
def open_excel(file='file.xls'):
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception as e:
        print(str(e))


# 将数据保存在数据库中
def excel_table_byname(file=u'static/IP_table.xls', colnameindex=0, by_name=u'Sheet1'):  # 修改自己路径

    if models.IP.objects.count() != 0:  # 将之前的数据删除掉
        models.IP.objects.all().delete()
    data = open_excel(file)
    table = data.sheet_by_name(by_name)  # 获得表格
    nrows = table.nrows  # 拿到总共行数
    colnames = table.row_values(colnameindex)  # 某一行数据 ['姓名', '用户名', '联系方式', '密码']
    for rownum in range(5, nrows):  # 也就是从Excel第二行开始，第一行表头不算
        print('行数----' + str(rownum))  # 行数
        row = table.row_values(rownum)

        if len(row[0].split('.')[-1]) > 0 and len(row[0].split('.')[-1]) < 4:  # 判断录取的信息是不是ip
            vlan = {
                'vlan621': 31,
                'vlan622': 63,
                'vlan623': 95,
                'vlan624': 127,
                'vlan625': 159,
                'vlan626': 191,
                'vlan627': 223,
                'vlan628': 255,
            }

            if int(row[0].split('.')[-1]) < int(vlan.get('vlan621')) and int(row[0].split('.')[0]) == 222:  # vlan1
                insert('vlan621', row)
            elif int(row[0].split('.')[-1]) < int(vlan.get('vlan622')) and int(row[0].split('.')[0]) == 222:  # vlan1
                insert('vlan622', row)
            elif int(row[0].split('.')[-1]) < int(vlan.get('vlan623')) and int(row[0].split('.')[0]) == 222:  # vlan1
                insert('vlan623', row)
            elif int(row[0].split('.')[-1]) < int(vlan.get('vlan624')) and int(row[0].split('.')[0]) == 222:  # vlan1
                insert('vlan624', row)
            elif int(row[0].split('.')[-1]) < int(vlan.get('vlan625')) and int(row[0].split('.')[0]) == 222:  # vlan1
                insert('vlan625', row)
            elif int(row[0].split('.')[-1]) < int(vlan.get('vlan626')) and int(row[0].split('.')[0]) == 222:  # vlan1
                insert('vlan626', row)
            elif int(row[0].split('.')[-1]) < int(vlan.get('vlan627')) and int(row[0].split('.')[0]) == 222:  # vlan1
                insert('vlan627', row)
            elif int(row[0].split('.')[-1]) < int(vlan.get('vlan628')) and int(row[0].split('.')[0]) == 222:  # vlan1
                insert('vlan628', row)

    re = json.dumps({
        'status': '1',
        'msg': '录入成功'
    })
    return re


# 数据库插入接口
def insert(val, row):
    tim = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    models.IP.objects.create(
        vlan=val,
        host=row[0],
        name=row[1],
        thing=row[2],
        domain=row[3],
        person_name=row[4],
        person_tel=row[5],
        admin_name=row[6],
        admin_tel=row[7],
        bbs_admin_name=row[8],
        bbs_admin_tel=row[9],
        blj_user=row[10],
        blj_password=row[11],
        system_type=row[12],
        cpu=row[13],
        momory=row[14],
        storage=row[15],
        assistance=row[16],
        ssh=row[17],
        telnet=row[18],
        host_user=row[19],
        host_password=row[20],
        host_manage_type=row[21],
        sql_type=row[22],
        is_post=row[23],
        post=row[24],
        remark=row[25],
        colony=row[26],
        times=tim
    )
    return 'ok'



def user_list(res):
    user_result = list(models.User.objects.all().values())
    print(user_result)
    re =json.dumps({
        'status':True,
        'msg':'',
        'data': user_result
    })
    return  HttpResponse(re,content_type='application/json')


def user_typechange(req):
    try:
        user_id = req.GET.get('user_id', None)
        value = req.GET.get('value', None)
        models.User.objects.filter(user_id=user_id).update(user_type=value)

        re =json.dumps({
            'status':True,
            'msg':'',
            'data': ''
        })
        return  HttpResponse(re,content_type='application/json')

    except:
        re =json.dumps({
            'status':False,
            'msg':'',
            'data': ''
        })
        return  HttpResponse(re,content_type='application/json')


def user_del(req):
    try:
        user_id = req.GET.get('user_id', None)
        models.User.objects.filter(user_id=user_id).delete()

        re = json.dumps({
            'status': True,
            'msg': '',
            'data': ''
        })
        return HttpResponse(re, content_type='application/json')
    except:
        re = json.dumps({
            'status': False,
            'msg': '',
            'data': ''
        })
        return HttpResponse(re, content_type='application/json')


def ip_info(req):
    try:
        res = list(models.IpWhiteList.objects.values("ip_id", "host","des"))
        print(res)
        re = json.dumps({
            'status': True,
            'msg': '',
            'data': res
        })
        return HttpResponse(re, content_type='application/json')
    except Exception as e:
        print(e)
        re = json.dumps({
            'status': False,
            'msg': '',
            'data': ''
        })
        return HttpResponse(re, content_type='application/json')


def ip_add(request):
    try:
        models.IpWhiteList.objects.create(
            host=request.POST.get('host', None),
            des=request.POST.get('des', None),
        )
        re = json.dumps({
            'status': True,
            'msg': '',
            'data': ''
        })
        return HttpResponse(re, content_type='application/json')
    except:
        re = json.dumps({
            'status': False,
            'msg': '',
            'data': ''
        })
        return HttpResponse(re, content_type='application/json')

def ip_del(request):
    try:
        ip_id = request.GET.get('ip_id', None)

        models.IpWhiteList.objects.filter(ip_id=ip_id).delete()
        re = json.dumps({
            'status': True,
            'msg': '',
            'data': ''
        })
        return HttpResponse(re, content_type='application/json')
    except:
        re = json.dumps({
            'status': False,
            'msg': '',
            'data': ''
        })
        return HttpResponse(re, content_type='application/json')