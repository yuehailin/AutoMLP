# Create your views here.
from __future__ import print_function
from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import models
from .forms import UserForm, RegisterForm ,FileFieldForm
import hashlib
import yaml
import collections
import csv
import logging
import os
import datetime
import SimpleITK as sitk

import radiomics
import pandas as pd
from radiomics import featureextractor



def index(request):
    task = models.Task.objects.all()
    pass
    return render(request, 'upload/index.html',{"task_list": task})

def login(request):
    if request.session.get('is_login', None):
        return redirect("/index/")
    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.User.objects.get(name=username)
                if user.password == hash_code(password):  # 哈希值和数据库内的值进行比对
                    print("ojbk")
                    request.session['is_login'] = True
                    request.session['user_id'] = user.user_id
                    request.session['user_name'] = user.name
                    request.session['user_email'] = user.email
                    print("ojbk01")

                    return redirect('/index/')
                else:
                    message = "密码不正确！"
            except:

                message = "用户不存在！"
        return render(request, 'login/finlogin.html', locals())

    login_form = UserForm()
    return render(request, 'login/finlogin.html', locals())
def register(request):
    # if request.session.get('is_login', None):
    #     # 登录状态不允许注册。你可以修改这条原则！
    #     return redirect("/index/")
    if request.method == "POST":

            username = request.POST.get("username01",None)
            password1 = request.POST.get("password1",None)
            password2 = request.POST.get("password2",None)
            email = request.POST.get("email",None)
            print(username)
            print(password1)
            print(password2)
            print(email)
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'login/finregister.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'

                    return render(request, 'login/finregister.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:  # 邮箱地址唯一
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request, 'login/finregister.html', locals())

                # 当一切都OK的情况下，创建新用户
                print("创建用户")
                models.User.objects.create(name=username,password=hash_code(password1),email=email,c_time=datetime.datetime.now())
                return redirect('/login/')  # 自动跳转到登录页面
    return render(request, 'login/finregister.html', locals())
def add_kind(request):
    if request.method == "POST":
        # new_id = request.POST.get("id", None)
        pickind = request.POST.get("pickind",None)
        des = request.POST.get("des",None)
        new_filename = request.POST.get("filename",None)
        models.Kind.objects.create(kind=pickind,describe=des,filename=new_filename,filecreatetime=datetime.datetime.now())
    return render(request, "upload/newkind01.html")
def publisher_list(request):
    ret = models.Publisher.objects.all().order_by("id")
    return  render(request,"publish/publisher_list.html", {"publisher_list": ret})

def delete_publisher(request):
    del_id = request.GET.get("id",None)
    del_name = request.GET.get("name",None)
    print("删除ID为{0}，名称为{1}的数据".format(del_id,del_name))
    if del_id:
        del_obj = models.Publisher.objects.get(id=del_id)
        del_obj.delete()
        return  redirect("/publisher_list/")
    else:
        return HttpResponse("error,检查数据后再试")
#增加数据（增）

def add_publisher(request):#第一次请求页面的时候，返回一个页面，页面有两个填写框
    error_msg = ""
    if request.method == "POST":
        new_id  = request.POST.get("publisher_id",None)
        new_name = request.POST.get("publisher_name",None)# print(new_name)
        print("你添加的出版社名称为：{0}".format(new_name))
        models.Publisher.objects.create(id=new_id,name=new_name)#数据库中新创建一条数据行
        return redirect("/publisher_list/") # redirect返回方法 HttpResponse返回字符串
    else:
        error_msg = "出版社名称不能为空"
    return render(request, "publish/add_publisher.html", {"error":error_msg})#render完成HTML界面替换

#编辑出版社(更新操作)（改）
def edit_publisher(request):
    if request.method == "POST":
        print(request.POST)
        edit_id = request.POST.get("publisher_id")
        new_name = request.POST.get("publisher_name")
        edit_publisher = models.Publisher.objects.get(id=edit_id)
        edit_publisher.name = new_name
        edit_publisher.save()  # 把修改提交到数据库
        #跳转到出版社列表页，查看是否修改
        return redirect("/publisher_list/")
    edit_id = request.GET.get("id")
    if edit_id:
        publisher_obj = models.Publisher.objects.get(id=edit_id)#获取到数据内的这条记录，
        # 在html界面的替换语句那里加上.name表示，获取这条记录中的name值（套路）
        return render(request,"publish/edit_publisher.html", {"publisher": publisher_obj})
# 退出登录
def logout(request):
    if not request.session.get('is_login',None):
        return redirect('/index/')
    request.session.flush()

    return redirect('/login/')

def hash_code(s, salt='mysite_login'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()
# 文件的上传
def handle_uploaded_file(f,path):

    savepath = "E:\\upload\\"+path
    if not os.path.exists(savepath):
        os.mkdir(savepath)

    with open(os.path.join(savepath,str(f)), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    destination.close()

def upload_file(request):
    global inputpa,outputpa,catalog,catalog01 ,stringcode,filename
    global task
    count =0
    number = 0
    ID = []
    Image = []
    Mask = []
    stringcode=""
    if request.method == "POST":    # 请求方法为POST时，进行处理
        form = FileFieldForm(request.POST,request.FILES)
        files = request.FILES.getlist("myfile")
        myLabel = request.FILES.getlist("mylabel")
        for k in myLabel:
            stringcode = str(k)

        for i in stringcode:
            if i != '.':
                count = count + 1
            else:
                break


        for f  in files:
            handle_uploaded_file(f,stringcode[0:count])
            number =  number+1
            ID.append(str(f))
            filepath = "E:\\upload\\"+stringcode[0:count]+"\\"+str(f)
            Image.append(filepath)
        for h  in myLabel:
            handle_uploaded_file(h,stringcode[0:count])
            for i in range(number):
                labelpath = "E:\\upload\\"+stringcode[0:count]+"\\"+str(h)
                Mask.append(labelpath)
        df = pd.DataFrame({'ID': ID, 'Image': Image, 'Mask': Mask})
        df.to_csv('{}.csv'.format("E:\\upload\\"+stringcode[0:count]+"\\"+stringcode[0:count]), index=False)
        inputpa = "E:\\upload\\"+stringcode[0:count]+"\\"+stringcode[0:count]+".csv"
        outputpa = "E:\\upload\\"+stringcode[0:count]+"\\"+stringcode[0:count]+"feather.csv"
        print(inputpa)
        print(outputpa)
        catalog = "E:\\upload\\"+stringcode[0:count]+"\\"+stringcode[0:count]+".yaml"
        catalog01 = "E:\\upload\\"+stringcode[0:count]+"\\"
        filename = stringcode[0:count]+'.yaml'
        models.Task.objects.create(user_id=1,csv_path=inputpa,yaml_path=catalog,up_time=datetime.datetime.now())
        # inputpa = savepathin+".csv"
        # outputpa=savepathin+"_Feather.csv"
        task = models.Task.objects.all()
        for ii in task:
            print(ii.task_id)
            print(ii.csv_path)
            print(ii.user_id)
        return render(request, "upload/index01.html")

# 显示上传的页面
def showpages(request):
    return render(request, "upload/newkind01.html")
# 提取特征的方法
def coll_feathers(csv_input,yaml_input):
  print("执行到这里啦，很开心")
  global inputpa,outputpa
  print(inputpa)
  print(outputpa)
  outPath = r''

  inputCSV = os.path.join(outPath,csv_input)

  outputFilepath = os.path.join(outPath,outputpa)
  progress_filename = os.path.join(outPath, 'pyrad_log.txt')
  params = os.path.join(outPath,yaml_input)

  # Configure logging
  rLogger =logging.getLogger('radiomics')

  # Set logging level
  # rLogger.setLevel(logging.INFO)  # Not needed, default log level of logger is INFO

  # Create handler for writing to log file
  handler = logging.FileHandler(filename=progress_filename, mode='w')
  handler.setFormatter(logging.Formatter('%(levelname)s:%(name)s: %(message)s'))
  rLogger.addHandler(handler)

  # Initialize logging for batch log messages
  logger = rLogger.getChild('batch')

  # Set verbosity level for output to stderr (default level = WARNING)
  radiomics.setVerbosity(logging.INFO)

  logger.info('pyradiomics version: %s', radiomics.__version__)
  logger.info('Loading CSV')

  flists = []
  try:
    with open(inputCSV, 'r') as inFile:
      cr = csv.DictReader(inFile, lineterminator='\n')
      flists = [row for row in cr]
  except Exception:
    logger.error('CSV READ FAILED', exc_info=True)

  logger.info('Loading Done')
  logger.info('Patients: %d', len(flists))

  if os.path.isfile(params):
    extractor = featureextractor.RadiomicsFeatureExtractor(params)
  else:  # Parameter file not found, use hardcoded settings instead
    settings = {}
    settings['binWidth'] = 25
    settings['resampledPixelSpacing'] = None  # [3,3,3]
    settings['interpolator'] = sitk.sitkBSpline
    settings['enableCExtensions'] = True

    extractor = featureextractor.RadiomicsFeatureExtractor(**settings)
    # extractor.enableInputImages(wavelet= {'level': 2})

  logger.info('Enabled input images types: %s', extractor.enabledImagetypes)
  logger.info('Enabled features: %s', extractor.enabledFeatures)
  logger.info('Current settings: %s', extractor.settings)

  headers = None

  for idx, entry in enumerate(flists, start=1):

    logger.info("(%d/%d) Processing Patient (Image: %s, Mask: %s)", idx, len(flists), entry['Image'], entry['Mask'])

    imageFilepath = entry['Image']
    maskFilepath = entry['Mask']
    label = entry.get('Label', None)

    if str(label).isdigit():
      label = int(label)
    else:
      label = None

    if (imageFilepath is not None) and (maskFilepath is not None):
      featureVector = collections.OrderedDict(entry)
      featureVector['Image'] = os.path.basename(imageFilepath)
      featureVector['Mask'] = os.path.basename(maskFilepath)

      try:
        featureVector.update(extractor.execute(imageFilepath, maskFilepath, label))

        with open(outputFilepath, 'a') as outputFile:
          writer = csv.writer(outputFile, lineterminator='\n')
          if headers is None:
            headers = list(featureVector.keys())
            writer.writerow(headers)

          row = []
          for h in headers:
            row.append(featureVector.get(h, "N/A"))
          writer.writerow(row)
      except Exception:
        logger.error('FEATURE EXTRACTION FAILED', exc_info=True)
# 生成yaml的配置文件
def getresult(request):
    global catalog,catalog01,stringcode,filename

    if request.method == 'POST':
        dir={}
        check_box_list = request.POST.getlist("check_box_list")
        # 将获取到的多选按钮存到字典中
        for i in check_box_list:

            dir[i]=None;
        for i in dir.keys():
            print(i)
        create_list = {

            'imageType': {'Original': {}, 'LoG': {'sigma': [1.0, 2.0, 3.0, 4.0, 5.0]},
                          'Wavelet': {}
                          },
            'setting': {'padDistance': 10, 'binWidth': 25,
                        'voxelArrayShift': 100, 'label': 1, 'resampledPixelSpacing': [1, 1, 1]
                        },
            'featureClass':dir


        }


        createyaml = os.path.join(catalog01,filename)
        # 写入到yaml文件
        print(catalog01)
        print(filename)
        with open(createyaml, "w", encoding="utf-8") as f:
            yaml.dump(create_list, f)
    return render(request, "upload/index02.html",{"task_list": task})  # render完成HTML界面替换


def getfeather(request):
        print("*/*/*/*/*/*/*/*/*/*/*/*/*")
        csv_path=""
        yaml_path=""

        fea_id = request.GET.get("id", None)
        print("*************"+fea_id)
        if fea_id:
            fea_obj = models.Task.objects.get(task_id=fea_id)
            csv_path = fea_obj.csv_path
            yaml_path = fea_obj.yaml_path
            print("***************"+csv_path)
            print("***************"+yaml_path)
        coll_feathers(csv_path,yaml_path)


