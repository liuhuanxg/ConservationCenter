from django.urls import path,include
from . import views
urlpatterns = [
	path('',views.index,name='index'),
	path('adopt/',views.adopt,name='adopt'),
	path('adopt_center/',views.adopt_center,name='adopt_center'),
	path('map/',views.map,name='map'),
	path('about_us/',views.about_us,name='about_us'),
	path('news/',views.news,name='news'),
	path('goods/',views.goods,name='goods'),
	path('contribute/',views.contribute,name='contribute'),
	path('detail/<int:id>',views.detail,name='detail'),
	path('goods_detail/<int:id>',views.goods_detail,name='goods_detail'),
	path('apply_adopt/',views.apply_adopt,name='apply_adopt'),
]
