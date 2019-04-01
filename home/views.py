from django.shortcuts import render
from  .models import Animals,Goods,News,Adoption,User,Volunteer,Orders
from django.http import Http404,HttpResponse,HttpResponseRedirect
import time
from django.shortcuts import reverse ,HttpResponseRedirect
from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
from alipay.aop.api.domain.AlipayTradePagePayModel import AlipayTradePagePayModel
from alipay.aop.api.request.AlipayTradePagePayRequest import AlipayTradePagePayRequest
from PIL import Image,ImageDraw,ImageFont
from io import BytesIO
import json
import random
import hashlib
from django.core.paginator import Paginator

#加密
def encryption(pwd):
	md=hashlib.md5()
	md.update(pwd.encode('utf-8'))
	md5_pwd=md.hexdigest()
	return md5_pwd

#检测用户有没有登录
def check_user(func):
	def inner(request,*args,**kwargs):
		if request.session.get('name'):
			return func(request,*args,**kwargs)
		else:
			return HttpResponseRedirect(reverse('login'))
	return inner

def page(r,data,pagenum,path,**kwargs):
	paginator = Paginator(data, pagenum)
	p = int(r.GET.get('p', 1))
	pagedata = paginator.page(p)
	pagecount = paginator.num_pages
	pagerange = paginator.page_range
	if p < 1:
		p = 1
	if p > pagecount:
		p = pagecount
	if p <= 5:
		page_list = pagerange[:10]
	elif p + 5 > pagecount:
		page_list = pagerange[-10:]
	else:
		page_list = pagerange[p - 5:p + 4]
	return render(r, path, {'pagedata': pagedata, 'page_list': page_list, 'p': p})

#首页
def index(request):
	animal_list=Animals.objects.all().exclude(is_activate=1)
	if len(animal_list)>5:
		animal_list=animal_list[0:5]
	goods_list = Goods.objects.all().exclude(is_activate=1)
	if len(goods_list) > 5:
		goods_list = goods_list[0:5]
	news_list = News.objects.all()
	return render(request,'common/index.html',{'animal_list':animal_list,
											   'goods_list':goods_list,
											   'news_list':news_list})

#领养要求
def adopt(request):
	return render(request,'common/adopt.html')

#领养中心
def adopt_center(request):
	animal_list = Animals.objects.all().exclude(is_activate=1)
	return render(request, 'common/adopt_center.html',{'animal_list':animal_list})

#救助中心
def map(request):
	return render(request,'common/map.html')

#关于我们
def about_us(request):
	return render(request,'common/about_us.html')

#新闻动态
def news(request):
	news_list=News.objects.all()
	# return render(request, 'common/news.html',{'news_list':news_list})
	return page(request,news_list,1,'common/news.html')

#线上义卖
def goods(request):
	goods_list = Goods.objects.all().exclude(is_activate=1)
	return render(request,'common/goods.html',{'goods_list':goods_list})

#我要捐献
def contribute(request):
	return render(request,'common/contribute.html')

#动物细节
def detail(request,id):
	animal=Animals.objects.filter(id=id,is_activate=0)
	if animal.exists():
		animal=animal[0]
		return render(request, 'common/animal_detail.html', {'animal':animal})
	else:
		raise Http404

#商品细节
def goods_detail(request,id):
	goods = Goods.objects.filter(id=id, is_activate=0)
	if goods.exists():
		goods = goods[0]
		return render(request, 'common/goods_detail.html', {'goods': goods})
	else:
		raise Http404

#领养申请
@check_user
def apply_adopt(request,id):
	id=request.session['id']
	return render(request,'common/apply_adopt.html',{'id':id})


#新闻细节
def new_detail(request,id):
	new_list = News.objects.filter(id=id)
	if new_list.exists():
		news = new_list[0]
		return render(request, 'common/news_detail.html',{'news':news})
	else:
		raise Http404

#登陆页面
def login(request):
	if request.method=='POST':
		name = request.POST.get('name')
		password = request.POST.get('password')
		password = encryption(password)
		u=User.objects.filter(name=name,password=password)
		if u.exists():
			u=u[0]
			request.session['id']=u.id
			request.session['name']=u.name
			next=request.GET.get('next')
			if next:
				return HttpResponseRedirect(next)
			return HttpResponseRedirect('/')
	return render(request,'common/login.html')

#注册页面
def register(request):
	if request.method=='POST':
		name=request.POST.get('name')
		password=request.POST.get('password')
		password=encryption(password)
		try:
			u=User(name=name,password=password)
			u.save()
			return HttpResponseRedirect('/login')
		except:
			raise Http404
	return render(request,'common/register.html')

#申请领养信息提交
@check_user
def do_apply_adopt(request):
	if request.method=='POST':
		id=request.POST.get('id')
		animal=Animals.objects.filter(id=id,is_activate=1)
		if animal.exists():
			return HttpResponse('抱歉，该动物已被领养。')
		name=request.POST.get('name')
		sex=request.POST.get('sex')
		phone=request.POST.get('phone')
		emal=request.POST.get('emal')
		address=request.POST.get('address')
		reason=request.POST.get('reason')
		adopt=Adoption(name=name,sex=sex,phone=phone,emal=emal,address=address,reason=reason,animal_id=id)
		adopt.save()
		return HttpResponseRedirect('/')
	else:
		return HttpResponse('Please send by post！')

#志愿者申请
def volunteer(request):
	return render(request,'common/volunteer.html')

def do_volunter(request):
	name = request.POST.get('name')
	sex = request.POST.get('sex')
	phone = request.POST.get('phone')
	time = request.POST.get('time')
	address = request.POST.get('address')
	reason = request.POST.get('reason')
	v = Volunteer(name=name, sex=sex, phone=phone, time=time, address=address, reason=reason)
	v.save()
	return HttpResponseRedirect('/')

@check_user
def pay_goods(request):
	g_id=request.GET.get('g_id')
	return render(request,'common/pay_goods.html',{'g_id':g_id})

@check_user
def do_pay_goods(request):
	user_id=request.session.get('id')
	id=request.POST.get('id')
	name=request.POST.get('name')
	phone=request.POST.get('phone')
	address=request.POST.get('address')
	t = str(time.time()).split('.')
	order = t[0] + t[1]
	goods=Goods.objects.filter(id=id,is_activate=0)
	if not goods.exists():
		return HttpResponse('该商品已被购买。')
	goods=goods[0]
	goods.is_activate=1
	goods.save()
	o=Orders(order=order,address=address,phone=phone,name=name,goods_id=id,user_id=user_id)
	o.save()
	money=goods.price
	alipay_client_config = AlipayClientConfig()
	alipay_client_config.server_url = 'https://openapi.alipaydev.com/gateway.do'
	alipay_client_config.app_id = '2016092100561600'
	alipay_client_config.app_private_key = 'MIIEpQIBAAKCAQEAxr2mbz2s8RigfJPxqYFht3hjtbEY9k/7C5BNvATGJRXSpI+9XmSCHG58OnYoZvYLgQoSLKRrE/z7ZeDL8gCVRuLWmEUHRYGEeBQ3IraaHqfHewP39yyoZ3M0Z9gIoK+yRIsgMcK4vdYwQGaw+MRypIEmqIC+AUeWOStYVDzK/TtcJPq8NZN+Gc2hzm94NE4F1fE+OFXVDPmoKJyljRsD2NYRz2iV6nuvRZ4inU31lpy6wNWwgqAZi6tIKMr1ElOFWH59ReCtkTyY0N2u4Z2TopiZgpCnZ3tQAoSEOslyefIH4w/I/dm2zxH3FF7bRuEp5jkueem5gfzmarGRClNp0wIDAQABAoIBABTfaDJ4tMghgQF0fEYEK6IcR8SWU/vSjJg7UJ61laXhc90Kp6XZQnz/8ZYmQLoHj0+/IgeEQSa5RCIACQtimkr2mfkmDsxy/Nmrrdq8eNVNY7r8wLc5/nnW9KMPYmCV81AVmI0BWWu+qhSpdF68Kxox4kCCPPJfdVyNu9olBGCyAtPKp2J/+lD/qCG9uxo7ltT5L4nsoR9gciLqce4B4VImHroUatDcOrDeMniRhNHkNa2YRkV4ddncAHtexAjA8yesTO1bO1D/TyLOHRnNElTBSDJbJaVzifgHM0OmcJUhgdbjJhGEUh+/atMjHLmMiZxEwoUsn4Ctcb8/NT541CECgYEA8Ao8+LIYzydlmaV4ns7GmclkfDXp3ZzVUeoQLCPGQtVeSZjiwIeB4G0bcO3d4JA0c1g5dfYJUA7YhOaOcQzMkkUnJu7oMBX2STYohX2012AdZPUz1/UWnckt5zvZoRYK0KjVQ06zLo2gWuk+dr+KVYQB1XRh777QxLhXK19V8LECgYEA0/RzoZ/+KvMTrFDEFiJep/I3avk6kohx8JUJyJQlus0cxnUdBv3rp3RkElJYCnvvtwhILWRuMovRTKxgUU7fXGIZY3HH7Zw0V3wpsOzPefNsVHCsg9kmpHqIEbabdJKAtnNIginMgEs0l5K2LKPbRK1CETRG3GwRcsoCdFV7A8MCgYEAyWB9eFLJd3jgxr7Ia8qjWL9ZOs9sLMx3Nip8eNtmaAli+bF2gfjs36AJRnt4Cf5Q0newdSL8+xoJUa2u0G7hbNDxILuLNVQnc5Io+pzUS1/KKTmAzetClwsBJJ3UXU0Fs7oAeGAc+LA+WCaXjb3xSv7dHvttclmOAYt5LdzkV3ECgYEAqkr6aH4yaPGZ+dV+ZkZBBPDAA8uwerDz0pb8IFKfKcHIf87yfn6eypDiIjJUmD/Rbp5R116chzH8/Hx2en1DSmdq/JIbTtY026Ffoc3yOIoSnJlWkixzNq1YC9tKdVOL5IslU6cfrmg+HhX7FkykTD5kGYyF7m1Ja4/QfwV6658CgYEAq/YNAIzrLkQxQeyS26bbCf7+FT6jLGmKgxyReODIOPKk7S+vaZWbyHX14AW9cDBeOfsiIQobfkIHMRJtVqe5TC49lHh08zAX610SvXSzIkpeTIMfUVKwhr0xfOqCMSEHKNG6mGbTie0AvhGCHYl2ptAWZot9ugNcgwdTu43Nyag='
	alipay_client_config.alipay_public_key ='MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA8OsmAJsaykPLzLIN//XnymU4s13kPE95EyOvZFq8TMPKJtsQ/f7eQB72wYAi3NarGT7RwebfJoAyeaM0KJsYNFqAodVHwpPRSemj8mwBtzEGGSyOT4Ilbv4KOz+HAsOkaLuQQ2ZGD1m7CCrgZCtxJDVqbd4xigSgMwrTFZYywoT0Sswv0oPV2TMl1tg+F7VUuvQpEvIn6qCQfzXa15eX9/P8OknvP9NSl3jOvDcpMliC2KvbfkNF9Qx9FEgtRlfnZdDItgmUj34VmBph+LUrAyV3lZjLpbFMhKlTBUeAbH72JPUKifXTXKsmbAl0n6cPaJQgb3zd+cfW7equoMhIEQIDAQAB'
	client = DefaultAlipayClient(alipay_client_config=alipay_client_config)

	model = AlipayTradePagePayModel()
	model.out_trade_no = o.order
	model.total_amount = money
	model.subject = "小动物保护网站-" + goods.name
	model.body = goods.name
	model.product_code = "FAST_INSTANT_TRADE_PAY"
	request = AlipayTradePagePayRequest(biz_model=model)
	request.return_url = 'http://39.105.195.67:8000/return_url'
	print('request:',request)
	# 得到构造的请求，如果http_method是GET，则是一个带完成请求参数的url，如果http_method是POST，则是一段HTML表单片段
	response = client.page_execute(request, http_method="GET")
	print('response:',response)
	return HttpResponseRedirect(response)

def return_url(request):
	order=request.GET.get('out_trade_no')
	result=Orders.objects.filter(order=order).update(is_pay=1)
	print('result:',result)
	return HttpResponseRedirect('/')

# 验证码
def verify_code(request):
	#1、创建画板（画布） 2、创建画笔   3、画相应的图片   4、保存图片并退出
	img_color= (random.randint(0,255),random.randint(0,150),random.randint(0,255))
	img = Image.new('RGB',(120,30),img_color)
	draw=ImageDraw.Draw(img)
	str='ABC1D2EF3GH4IJ5KL6MN70PQ8RS9TUV0WXYZ'  #候选字符串
	font=ImageFont.truetype('simkai.ttf',28)   #字体字号
	x,y=0,0
	font_str=''
	#生成验证码
	for i in range(0,5):
		#字体颜色
		one_str=str[random.randint(0,len(str)-1)]
		font_str+=one_str
		color=(random.randint(0,255),random.randint(150,255),random.randint(0,255))
		#横纵坐标   内容   颜色   字号
		draw.text((x,y),one_str,fill=color,font=font)
		x+=20

	#画干扰点
	for z in range(0,200):
		point_color=(random.randint(0,255),random.randint(0,255),random.randint(0,255))
		draw.point((random.randint(0,100),random.randint(0,25)),fill=point_color)

	#画干扰线
	draw.line(((20,15),(90,18)),fill=(0,0,0))
	draw.line(((15,5),(100,22)),fill=(0,0,0))

	io=BytesIO()
	img.save(io,'png')   #保存图片
	request.session['verify_code']=font_str.lower()    #将验证码存入session用于验证用户输入
	return HttpResponse(io.getvalue(),'image/png')


#检查验证码是否正确
def checked_code(request):
	verify_code=request.POST.get('verify_code','')
	verify_code=verify_code.lower()
	loca_code=request.session['verify_code']
	data={}
	# 判断验证码
	if len(verify_code) != 5:
		data['msg'] = '验证码错误'
		data['status'] = 0
		return HttpResponse(json.dumps(data))
	if  loca_code !=verify_code:
		data['msg']='验证码错误！'
		data['status']=0
		return HttpResponse(json.dumps(data))
	else:
		data['msg']='验证码正确！'
		data['status']=1
		return HttpResponse(json.dumps(data))
