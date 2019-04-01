from django.contrib import admin

# Register your models here.
from .models import Animals,Goods,News,Adoption,Volunteer,User,Orders

@admin.register(Animals)
class AnimalsAdmin(admin.ModelAdmin):
	list_display = ('name','type','age','sex','colored_status')
	search_fields = ('name','type','age','sex')
	list_display_links = ('name', 'colored_status')
	exclude = ('image',)
	ordering = ('is_activate',)
	def get_readonly_fields(self, request, obj=None):
		if obj:
			if obj.is_activate == 0:
				return ['is_activate']
			else:
				return ['name','age','sex','type','message','is_activate']
		else:
			return []


@admin.register(Goods)
class GoodsAdmin(admin.ModelAdmin):
	list_display = ('name','price','colored_status')
	search_fields = ('name','is_activate')
	list_display_links = ('name', 'colored_status')
	ordering = ('is_activate','price')
	def get_readonly_fields(self, request, obj=None):
		if obj:
			if obj.is_activate == 0:
				return ['is_activate']
			else:
				return ['name','price','address','message','is_activate']
		else:
			return []

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
	list_display = ('title','modify_time')
	search_fields = ('title','modify_time')

@admin.register(Adoption)
class AdoptionAdmin(admin.ModelAdmin):
	list_display = ('name','sex','phone','address','animal','colored_status')
	search_fields = ('name','sex','phone','address')
	list_display_links = ('name', 'colored_status')
	def get_readonly_fields(self, request, obj=None):
		if obj:
			if obj.is_sure == 0:
				return ['name','sex','phone','emal','address','reason','reason_time','animal']
			else:
				return ['name', 'sex', 'phone', 'emal', 'address', 'reason', 'reason_time', 'animal','is_sure']
		else:
			return []

	def save_model(self, request, obj, form, change):
		super().save_model(request, obj, form, change)
		if obj.is_sure==1:
			Animals.objects.filter(id=obj.animal_id).update(is_activate=1)
		else:
			Animals.objects.filter(id=obj.animal_id).update(is_activate=0)

@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
	list_display = ('name','phone','order','colored_status','colored','pay','add_time')
	search_fields = ('name','order','phone','address')
	ordering = ('is_pay','is_send','is_save','-add_time')
	list_display_links = ('name', 'colored_status','colored','pay')
	def get_readonly_fields(self, request, obj=None):
		if obj:
			if obj.is_send == 0 :
				return ['name','phone','order','add_time','user','goods','is_pay','is_save','address']
			else:
				return ['name', 'phone', 'order', 'add_time', 'user', 'goods', 'is_pay', 'is_save', 'address','is_send']
		else:
			return []

	def save_model(self, request, obj, form, change):
		super().save_model(request, obj, form, change)
		if obj.is_save==1:
			Goods.objects.filter(id=obj.goods_id).update(is_activate=1)
		else:
			Goods.objects.filter(id=obj.goods_id).update(is_activate=0)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
	list_display = ('id','name')
	search_fields = ('id','name')
	def get_readonly_fields(self, request, obj=None):
		if obj:
			return ['name','password']
		else:
			return []

@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
	list_display = ('name','sex','phone','time','address','colored_status')
	search_fields = ('name','sex','phone','address')
	list_display_links = ('name','colored_status')
	def get_readonly_fields(self, request, obj=None):
		if obj:
			return ['name','sex','phone','time','address','reason']
		else:
			return []

admin.site.site_header='小动物保护中心'
admin.site.site_title='小动物保护中心'