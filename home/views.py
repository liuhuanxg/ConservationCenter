from django.shortcuts import render
from  .models import Animals,Goods,News,Adoption,User
from django.http import Http404,HttpResponse,HttpResponseRedirect


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
	print(news_list)
	return render(request, 'common/news.html',{'news_list':news_list})

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
def apply_adopt(request,id):
	try:
		user=request.session['name']
		id=request.session['id']
		print(user,id)
		return render(request,'common/apply_adopt.html',{'id':id})
	except:
		return HttpResponseRedirect('/login')

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
		try:
			u=User(name=name,password=password)
			u.save()
			return HttpResponseRedirect('/login')
		except:
			raise Http404
	return render(request,'common/register.html')

#申请领养信息提交
def do_apply_adopt(request):
	if request.method=='POST':
		try:
			user = request.session['name']
			user_id = request.session['id']
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
		except:
			return HttpResponseRedirect('/login')
	else:
		return HttpResponse('Please send by post！')