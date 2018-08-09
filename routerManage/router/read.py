#-*- coding=utf-8 -*-
import xlrd
def open_excel(file= 'file.xls'):
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception as e:
        print(str(e))

def excel_table_byname(file= u'../static/txt.xls',colnameindex=0,by_name=u'Sheet1'):#修改自己路径
    data = open_excel(file)
    table = data.sheet_by_name(by_name) #获得表格
    nrows = table.nrows  # 拿到总共行数
    colnames = table.row_values(colnameindex)  # 某一行数据 ['姓名', '用户名', '联系方式', '密码']

    list = []
    for rownum in range(5, nrows): #也就是从Excel第二行开始，第一行表头不算
        print('行数----'+str(rownum)) #行数
        row = table.row_values(rownum)
        # print(row) #该行的内容
        # print(row[0])
        if len(row[0].split('.')[-1]) > 0 and len(row[0].split('.')[-1])< 4 :
            if int(row[0].split('.')[-1])<31 and int(row[0].split('.')[0]) == 222: #vlan1
                print(row)
                for i in range(len(row)):
                    print(str(i+1)+str(row[i]))
                    print('vlan621')
            elif int(row[0].split('.')[-1])<63 and int(row[0].split('.')[0]) == 222:
                    print(row)
                    for i in range(len(row)):
                        print(str(i + 1) + str(row[i]))
                        print('vlan622')
            elif int(row[0].split('.')[-1])<95 and int(row[0].split('.')[0]) == 222:
                    print(row)
                    for i in range(len(row)):
                        print(str(i + 1) + str(row[i]))
                        print('vlan623')
            elif int(row[0].split('.')[-1])<127 and int(row[0].split('.')[0]) == 222:
                    print(row)
                    for i in range(len(row)):
                        print(str(i + 1) + str(row[i]))
                        print('vlan624')
            elif int(row[0].split('.')[-1])<159 and int(row[0].split('.')[0]) == 222:
                    print(row)
                    for i in range(len(row)):
                        print(str(i + 1) + str(row[i]))
                        print('vlan625')
            elif int(row[0].split('.')[-1])<191 and int(row[0].split('.')[0]) == 222:
                    print(row)
                    for i in range(len(row)):
                        print(str(i + 1) + str(row[i]))
                        print('vlan626')
            elif int(row[0].split('.')[-1])<223 and int(row[0].split('.')[0]) == 222:
                    print(row)
                    for i in range(len(row)):
                        print(str(i + 1) + str(row[i]))
                        print('vlan627')
            elif int(row[0].split('.')[-1])<255 and int(row[0].split('.')[0]) == 222:
                    print(row)
                    for i in range(len(row)):
                        print(str(i + 1) + str(row[i]))
                        print('vlan628')




            # for i in range(len(row)): #循环遍历一行中的每一列数据
            #
            #     if i==0 and  len(row[i].split('.')[-1])>0 and len(row[i].split('.')[-1]) <4 and int(row[i].split('.')[-1])<31 :
            #         if int(row[i].split('.')[-1])<31:
            #             print('这个是vlan1')


                # print(row[i])
                # print('ip最后一位')
                # print(row[i].split('.')[-1])
                # print('长yhtb   度')
                # print (len(row[i].split('.')[-1]))

    # if row:
    #     app = {}
    #     for i in range(len(colnames)):
    #         app[colnames[i]] = row[i] #表头与数据对应
    #     list.append(app)
    return list

def main():
    tables = excel_table_byname()
    # for row in tables:
    #    print(row)
if __name__ =="__main__":
    main()