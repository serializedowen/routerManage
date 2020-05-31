"""routerManage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from router import views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^upload/text$',views.upload_txt), #文件上传页面
    url(r'^excel/upload$',views.upload),#文件上传接口
    url(r'^start/ping$',views.start_ping), #开启ping
    url(r'^start/insert$',views.start_insert), #数据库数据插入excel_export（默认上传文件是=时调用）
    url(r'^excel/export$',views.excel_export), #导出 excel表
    url(r'^$',views.index), #用户登录
    url(r'^login$',views.login), #用户登录
    # url(r'^user/login$',views.user_login), #导出 excel表
    url(r'^logout$',views.logout), #登出
    url(r'^getAllData$',views.get_all_data), #胡获取数据
    url(r'^getAllAllot$',views.get_all_allot), #登出
    url(r'^getOneIp$',views.get_one_ip), #随机获取一个可分配的ip
    url(r'^setOneIp$',views.set_one_ip), #设置ip
    url(r'^changeOneIp$',views.change_one_ip), #设置ip
    url(r'^getByIp$',views.get_by_ip), #设置ip
    url(r'^delHost$',views.del_host), #删除
    url(r'^getAllDataByVlanId$',views.get_all_data_by_vlan_id), #根据vlanid查找所有数据sendmail
    url(r'^send/mail$',views.sendmail), #根据vlanid查找所有数据sendmail
    url(r'^getError$',views.getError), #获取错误信息的接口
    url(r'^setUser$',views.setUser), #注册用户
    url(r'^reError$',views.reError), #刷新error
    url(r'^monitor$',views.monitor), #监控接口
    url(r'^getWorkData',views.getWorkData), #监控数据
    # url(r'^getAllDataByVlanId$',views.get_all_data_by_vlan_id), #根据vlanid查找所有数据
    url(r'^user/list$', views.user_list),  # 用户列表
    url(r'^user/typechange$', views.user_typechange),  # 用户类型更改
    url(r'^user/del', views.user_del),  # 删除ip白名单
    url(r'^ip/info', views.ip_info),  # 获取ip白名单
    url(r'^ip/add', views.ip_add),  # 添加ip白名单
    url(r'^ip/del', views.ip_del),  # 删除ip白名单

]
