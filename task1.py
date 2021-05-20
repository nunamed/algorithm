# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import model
dic={}
def new_round(f):#为round保留两位小数添加四舍五入功能
	if isinstance(f,float):
		if str(f)[-1] == '5':
			return(round(float(str(f)[:-1]+'6'),2))
		else:
			return(round(f,2))
def sor(file,by='顾客编号',ascending=False):#以默认顾客编号进行从低到高排序
	csv = pd.read_csv(file,encoding='gbk')
	csv=csv.sort_values(by,ascending)
	print('排序完成')
	return csv
def check(file):#检查数据是否存在空值
	data=[]
	csv=pd.read_csv(file,encoding='gbk')
	for i in csv.index.values:
		if True in csv.loc[i].isnull().values:
			data.append(i+2)
	dic['数据存在空值索引']=data
	return csv
def refined(file,sort=False):#默认不进行排序，对数据进行清理
	csv=pd.read_csv(file,encoding='gbk')
	if sort:
		csv=sor(file)
	data=[]#负或零销售数量，销售金额，商品单价索引
	data2=[]#未促销，销售数量*商品单价不等于销售金额索引
	data3=[]#是否促销列存在脏数据索引
	data4=[]#数据存在空值索引
	i=0
	csv.drop(['销售月份'], axis=1, inplace=True)#删除多余
	csv.loc[:,'销售日期'] = pd.to_datetime(csv.loc[:,'销售日期'].astype(str), format='%Y-%m-%d', errors='coerce')#修改销售日期格式
	for num,sale,amo,discount in csv[['销售数量','销售金额','商品单价','是否促销']].values:
		if True in csv.loc[i].isnull().values:#检查数据是否存在空值
			data4.append(i+2)
			dic['数据存在空值索引']=data4
			csv.drop(i,inplace=True)
			i+=1
			continue
		if not discount in ['是','否']:#对脏数据进行删除
			data3.append(i+2)
			dic['是否促销列存在脏数据索引']=data3
			csv.drop(i,inplace=True)
		elif num<=0 or sale<=0 or amo<=0:#对负销售数量，销售金额，商品单价记录进行删除
			data.append(i+2)
			dic['存在负或零销售数量，销售金额，商品单价索引']=data
			csv.drop(i,inplace=True)
		else:
			if amo*num!=sale:#对未促销，销售数量*商品单价不等于销售金额的，进行记录，并改正
				if new_round(round(amo,3)*round(num,3))!=sale:
					if discount!='是':
						data2.append(i+2)
						dic['未促销，销售数量*商品单价不等于销售金额索引']=data2
						csv.loc[i,'销售金额']=new_round(round(amo,3)*round(num,3))
		i+=1
	csv.to_csv(r'Desktop\task1_1.csv',index=False,header=True,encoding='gbk')
if __name__ == '__main__':
	Path= r'D:\迅雷下载\泰迪杯\泰迪杯\第2届泰迪杯材料\A题\附件.csv'
	refined(Path)
	print(dic)
	print('数据已修正')
	print('已处理负值')