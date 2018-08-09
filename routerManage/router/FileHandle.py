#-*- coding:utf-8 -*-
import os,django,sys
BASE_DIR =os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from router.models import IP,User,Time

import datetime
import xlwt




def BulidNewExcel(download_url,dbname):
    db_dict={
        'IP':IP
    }
    style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on')
    style1 = xlwt.easyxf(num_format_str='D-MMM-YY')
    #获取字段名(列表)
    field_name_list = []
    field_verbose_name_list = []

    # for i in models.SSHLog._meta.get_fields():
    for i in db_dict[dbname]._meta.get_fields():
        field_name_list.append(i.name)
        if db_dict[dbname] == IP:
            field_verbose_name_list.append(i.name)
        else:
            field_verbose_name_list.append(i._verbose_name)

    #Dns表中字段替换
    field_name_list = ['Domain_name_id' if x == 'Domain_name' else x for x in field_name_list]
    #config表中字段替换
    field_name_list = ['baseid_id' if x == 'baseid' else x for x in field_name_list]

    #plat、buss表字段替换
    if 'baseinfo' in field_name_list:field_name_list.remove('baseinfo')
    if 'baseinfo' in field_verbose_name_list:field_verbose_name_list.remove('baseinfo')
    #domain表字段替换
    if 'dnsinfo' in field_name_list:field_name_list.remove('dnsinfo')
    if 'dnsinfo' in field_verbose_name_list:field_verbose_name_list.remove('dnsinfo')

    #base表字段替换
    if 'configinfo' in field_name_list:field_name_list.remove('configinfo')
    if 'business_unit' in field_name_list:field_name_list.remove('business_unit')
    if 'configinfo' in field_verbose_name_list:field_verbose_name_list.remove('configinfo')
    if 'business_unit' in field_verbose_name_list:field_verbose_name_list.remove('business_unit')

    field_name_list = ['isp_id' if x == 'isp' else x for x in field_name_list]


    style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on')
    style1 = xlwt.easyxf(num_format_str='D-MMM-YY')

    wb = xlwt.Workbook()
    ws = wb.add_sheet('Sheet',cell_overwrite_ok=True)
    for i in range(len(field_verbose_name_list)):
        ws.write(0,i,field_verbose_name_list[i],style0)

    mylist=[]

    log_obj = db_dict[dbname].objects.all()


    num = 0
    for i in log_obj.values():
        mylist.append([])
        for j in range(len(field_name_list)):
            mylist[num].append(i[field_name_list[j]])
        num+=1

    for i in range(0,log_obj.count()):
        for j in range(len(field_verbose_name_list)):
            ws.write(i+1,j,mylist[i][j])
    timestr=datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    wb.save(download_url+'New-'+timestr+'.xls')
    return timestr