from django.db import models
from django.utils.html import format_html

# Create your models here.
class Animals(models.Model):
	class Meta:
		verbose_name='动物信息'
		verbose_name_plural='动物信息'

	GENDER_CHOICES = (
		(u'男', u'男'),
		(u'女', u'女'),
	)
	name=models.CharField(max_length=30,verbose_name='姓名')
	age=models.CharField(max_length=30,verbose_name='年龄')
	sex=models.CharField(max_length=10,choices=GENDER_CHOICES,verbose_name='性别')
	image=models.ImageField(upload_to='uploads',verbose_name='动物图片')
	type = models.CharField(max_length=100, verbose_name='品种')
	message=models.TextField(verbose_name='备注信息')
	is_activate=models.BooleanField(verbose_name='是否领养',default=0)
	def __str__(self):
		return self.name

	def colored_status(self):
		if self.is_activate == 0:
			color_code = 'blue'
			return format_html(
				'<span style="color:{};">{}</span>', color_code, '尚未领养',
			)
		else:
			color_code = 'green'
			return format_html(
				'<span style="color:{};">{}</span>', color_code, '已领养',
			)
	colored_status.short_description = u'是否领养'

class Goods(models.Model):
	class Meta:
		verbose_name='义卖物品'
		verbose_name_plural='义卖物品'
	name=models.CharField(max_length=30,verbose_name='名称')
	image=models.ImageField(upload_to='goods',verbose_name='商品图片')
	price = models.CharField(max_length=100, verbose_name='价钱')
	address = models.CharField(max_length=100, verbose_name='配送地址',default='')
	message=models.TextField(verbose_name='备注信息')
	is_activate=models.BooleanField(verbose_name='是否卖出',default=0)
	def __str__(self):
		return self.name
	def colored_status(self):
		if self.is_activate == 0:
			color_code = 'blue'
			return format_html(
				'<span style="color:{};">{}</span>', color_code, '尚未卖出',
			)
		else:
			color_code = 'green'
			return format_html(
				'<span style="color:{};">{}</span>', color_code, '已卖出',
			)
	colored_status.short_description = u'是否批准'

class News(models.Model):
	class Meta:
		verbose_name='新闻动态'
		verbose_name_plural='新闻动态'
	title=models.CharField(max_length=30,verbose_name='标题')
	image=models.ImageField(upload_to='news',verbose_name='图片')
	content=models.TextField(verbose_name='内容')
	modify_time = models.DateTimeField(auto_now_add=True, verbose_name=('添加时间'))
	def __str__(self):
		return self.title

class Adoption(models.Model):
	class Meta:
		verbose_name='领养申请'
		verbose_name_plural='领养申请'
	name=models.CharField(max_length=30,verbose_name='姓名')
	sex=models.CharField(max_length=30,verbose_name='性别')
	phone=models.CharField(max_length=11,verbose_name='电话')
	emal=models.CharField(max_length=30,verbose_name='邮箱')
	address=models.CharField(max_length=100,verbose_name='现住址')
	reason=models.TextField(verbose_name='申请原因')
	reason_time = models.DateTimeField(auto_now_add=True, verbose_name=('申请时间'))
	animal=models.ForeignKey(Animals,default=1,on_delete=models.DO_NOTHING,verbose_name='动物名称')
	is_sure=models.BooleanField(default=0,verbose_name='是否批准')
	def __str__(self):
		return self.name

	def colored_status(self):
		if self.is_sure == 0:
			color_code = 'blue'
			return format_html(
				'<span style="color:{};">{}</span>', color_code, '尚未批准',
			)
		else:
			color_code = 'green'
			return format_html(
				'<span style="color:{};">{}</span>', color_code, '已批准',
			)
	colored_status.short_description = u'是否批准'


class User(models.Model):
	class Meta:
		verbose_name='用户'
		verbose_name_plural='用户'
	name=models.CharField('用户名',max_length=30,unique=True)
	password=models.CharField('密码',max_length=32)
	def __str__(self):
		return self.name

class Volunteer(models.Model):
	class Meta:
		verbose_name='志愿者申请'
		verbose_name_plural='志愿者申请'
	name=models.CharField(max_length=30,verbose_name='申请人')
	sex=models.CharField(max_length=30,verbose_name='性别')
	phone=models.CharField(max_length=11,verbose_name='电话')
	address = models.CharField(max_length=100, verbose_name='现住址')
	time=models.CharField(max_length=200,verbose_name='每周空闲时间')
	reason=models.TextField(verbose_name='申请原因')
	is_sure=models.BooleanField(default=0,verbose_name='是否批准')
	def __str__(self):
		return self.name

	def colored_status(self):
		if self.is_sure == 0:
			color_code = 'blue'
			return format_html(
				'<span style="color:{};">{}</span>', color_code, '尚未批准',
			)
		else:
			color_code = 'green'
			return format_html(
				'<span style="color:{};">{}</span>', color_code, '已批准',
			)
	colored_status.short_description = u'是否批准'

