from django.db import models

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

class News(models.Model):
	class Meta:
		verbose_name='新闻中心'
		verbose_name_plural='新闻中心'
	title=models.CharField(max_length=30,verbose_name='标题')
	image=models.ImageField(upload_to='news',verbose_name='图片')
	content=models.TextField(verbose_name='内容')
	modify_time = models.DateTimeField(auto_now_add=True, verbose_name=('添加时间'))
	def __str__(self):
		return self.title