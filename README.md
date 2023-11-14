# CarRent-Platform-
线上画er diagram的web
https://app.diagrams.net/
在这个网页上可以打开new_er.drawio 这个是最终的ER diagram.

数据库启动：
打开manager—osx 
在manage servers里 ：
make MySQL and Apache Web Server as RUNNING

这个时候，在网页打开： http://localhost/dashboard/，点击phpMyAdmin
数据库是rentCar
如果没有rentCar, 创建rentCar（查看tutorial）
复制database.sql 文件内容到sql里，点击go
创建成功。
run flaskbolg.py      （spyder)
在网页中打开http://127.0.0.1:5000/
