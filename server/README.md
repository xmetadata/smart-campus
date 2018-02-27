# Smart Campus Server

## Install
+ gedit config.py
+ python migrate.py db init
+ python migrate.py db migrate
+ python migrate.py db upgrade

## Running
> Nginx + Gunicorn/Supervisor + Flask-RESTful
>
> /usr/bin/gunicorn -w 4 -b 0.0.0.0:5000 app:app

seg1：与中间件交互说明
操作对象：部分功能待商议，确定扩展中间件接口还是直接查库
Objects--校园卡:功能
       |       |-充值--微信(前端发起)--下订单:向中间件发缴费信息
       |       |      |-翼支付(门户发起)--缴费订单：中间件推送缴费信息
       |       |
       |       |-余额查询
       |       |-挂失
       |       |-申办
       |       |-充值记录查询
       |
       |-学生：功能
             |-学生信息查询
             |-一卡通变更记录查询
             |-一卡通状态查询
             |-一卡通变更记录查询
