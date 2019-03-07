from django.contrib import admin

# Register your models here.
from .models import Animals,Goods,News,Adoption

@admin.register(Animals)
class AnimalsAdmin(admin.ModelAdmin):
	list_display = ('name','type','age','sex')
	search_fields = ('name','type','age','sex')

@admin.register(Goods)
class GoodsAdmin(admin.ModelAdmin):
	list_display = ('name','price','is_activate')
	search_fields = ('name','is_activate','is_activate')

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
	list_display = ('title','modify_time')
	search_fields = ('title','modify_time')

@admin.register(Adoption)
class AdoptionAdmin(admin.ModelAdmin):
	list_display = ('name','sex','phone','address')
	search_fields = ('name','sex','phone','address')

admin.site.site_header='小动物保护中心'
admin.site.site_title='小动物保护中心'