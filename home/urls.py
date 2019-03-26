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
	path('apply_adopt/<int:id>',views.apply_adopt,name='apply_adopt'),
	path('login/',views.login,name='login'),
	path('register/',views.register,name='register'),
	path('do_apply_adopt/',views.do_apply_adopt,name='do_apply_adopt'),
	path('new_detail/<int:id>',views.new_detail,name='new_detail'),
	path('volunteer/',views.volunteer,name='volunteer'),
	path('do_volunteer/',views.do_volunter,name='do_volunteer'),
]
