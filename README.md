# mysite_login
项目部署：
数据库：mysql
Django2.0
文件夹介绍：
mysite_login是配置文件之类的文件夹
Medical文件夹是项目的主文件夹，之后我们还可以根据需求增加类似的模块
Static是静态资源文件夹
requirements.txt是项目的依赖包

数据库说明：
Django中数据库表不需要自己创建，Django会根据model模块自动生成数据库表。

部署步骤
1:项目导入
2:修改配置文件，在mysite_login的settings中，修改数据库用户名和密码
3:创建数据库，首先创建一个名为django的数据库，然后在终端执行下面两条指令：
	python manage.py makemigrations
 
	python manage.py migrate
这两条命令是自动生成数据库文件的命令。
4:生成数据库之后，打开navicat，将数据库表中以medical开头的数据库的主键都设置为自增的。
