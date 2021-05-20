# -*- coding: utf-8 -*-
import pandas as pd
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
	csv.to_csv(r'Desktop\exercise\task1_1.csv',index=False,header=True,encoding='gbk')#生成文件
def ulti_total(file,primary_key,data_key,data2_key):
	csv = pd.read_csv(file,encoding='gbk')
	data ={}
	for x,y,z in csv[[primary_key,data_key,data2_key]].values:
		if data.get(x):#存在主类
			if data[x].get(y):
				if data[x][y].get(z):#存在小类，在原本出现基础上+1
					data[x][y][z]['num']+=1
				else:
					data[x][y][z]={'num':1}
			else:#不存在小类，则新建
				data[x][y]={}
				data[x][y][z]={'num':1}
		else:#如果没有主类，则初始化主类，小类
			data[x]={}
			data[x][y]={}
			data[x][y][z]={'num':1}
	print(data.items())
def compare(file,primary_key,data_key):#统计相同数据，重复出现次数
	df = pd.read_csv(file, encoding='gbk')
	dic={}
	for p_key, u_key in df[[primary_key, data_key]].values:
		if ret_dict.get(p_key):
			if ret_dict[p_key].get(u_key):
				ret_dict[p_key][u_key]['num'] += 1
			else:
				ret_dict[p_key][u_key] = {'num': 1}
		else:
			ret_dict[p_key] = {}
			ret_dict[p_key][u_key] = {'num': 1}
def add(file,primary_key,data_key):#task1_2
	csv = pd.read_csv(file,encoding='gbk')
	data = csv.groupby(primary_key).sum()
	data.rename(columns={data_key:data_key+'总和'},inplace=True)
	data = data[data_key+'总和']
	data.to_csv(r'Desktop\exercise\task1_2.csv', header=True, encoding='gbk')
def discount(file,primary_key,data_key,key1,key2,val1,val2):#task1_3,task1_4,task1_5
	csv = pd.read_csv(file,encoding='gbk')
	print(csv[data_key].value_counts(dropna=False))
	csv_yes = csv.loc[csv[data_key] == key1,:]
	csv_no = csv.loc[csv[data_key] == key2,:]
	data_yes = csv_yes.groupby(primary_key).sum()
	data_yes.rename(columns={'销售金额':val1},inplace=True)
	csv_yes = data_yes[val1]
	data_no = csv_no.groupby(primary_key).sum()
	data_no.rename(columns={'销售金额':val2},inplace=True)
	csv_no = data_no[val2]
	csv = pd.merge(csv_yes, csv_no, how='left', left_on=primary_key,right_on=primary_key)#合并两个
	return csv
def customer():
	pass
if __name__ == '__main__':
	file=r'D:\迅雷下载\泰迪杯\泰迪杯\第2届泰迪杯材料\A题\附件.csv'#初始数据
	print('清洗完成')
	FinalPath=r'C:\Users\Administrator\Desktop\exercise\task1_1.csv'#清洗后数据
	# refined(FinalPath)#task1_1,清洗数据
	# print(dic)#问题数据检索
	# add(FinalPath,'大类名称','销售金额')#task1_2
	csv=discount(FinalPath,'中类名称','是否促销','是','否','促销销售金额总和','非促销销售金额总和')#task1_3
	csv.to_csv(r'Desktop\exercise\task1_3.csv',encoding='gbk')