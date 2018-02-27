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

## HTTP Status Code
> 200 （成功） 服务器已成功处理了请求。通常，这表示服务器提供了请求的网页。
>
> 201 （已创建） 请求成功并且服务器创建了新的资源。
>
> 400 （错误请求） 服务器不理解请求的语法。
>
> 403 （禁止） 服务器拒绝请求，权限不够
>
> 404 （未找到） 服务器找不到请求的网页。
>
> 500 （服务器内部错误） 服务器遇到错误，无法完成请求。数据库错误。


## 与中间件交互说明

操作对象：部分功能待商议，确定扩展中间件接口还是直接查库

* Objects
  * 校园卡
    * 充值
      * 微信(前端发起)--下订单:向中间件发缴费信息
      * 翼支付(门户发起)--缴费订单：中间件推送缴费信息
    * 余额查询
    * 挂失
    * 申办
    * 充值记录查询
  * 学生
    * 学生信息查询
    * 一卡通变更记录查询
    * 一卡通状态查询
    * 一卡通变更记录查询
