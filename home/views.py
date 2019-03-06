from django.shortcuts import render
from  .models import Animals,Goods

# Create your views here.
#首页
def index(request):
	animal_list=Animals.objects.all().exclude(is_activate=1)
	if len(animal_list)>5:
		animal_list=animal_list[0:5]
	goods_list = Goods.objects.all().exclude(is_activate=1)
	if len(goods_list) > 5:
		goods_list = goods_list[0:5]
	print(goods_list)
	return render(request,'common/index.html',{'animal_list':animal_list,
	                                           'goods_list':goods_list})

#领养要求
def adopt(request):
	return render(request,'common/adopt.html')

#领养中心
def adopt_center(request):
	return render(request, 'common/adopt_center.html')

#救助中心
def map(request):
	return render(request,'common/map.html')

#关于我们
def about_us(request):
	return render(request,'common/about_us.html')

#新闻动态
def news(request):
	return render(request, 'common/news.html')

#线上义卖
def goods(request):
	return render(request,'common/goods.html')

#我要捐献
def contribute(request):
	return render(request,'common/contribute.html')

from django.http import Http404
def detail(request,id):
	animal=Animals.objects.filter(id=id,is_activate=0)
	if animal.exists():
		animal=animal[0]
		return render(request, 'common/animal_detail.html', {'animal':animal})
	else:
		raise Http404

def goods_detail(request,id):
	goods = Goods.objects.filter(id=id, is_activate=0)
	if goods.exists():
		goods = goods[0]
		return render(request, 'common/goods_detail.html', {'goods': goods})
	else:
		raise Http404


def apply_adopt(request):
	return render(request,'common/apply_adopt.html')