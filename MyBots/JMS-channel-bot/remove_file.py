import os

with open("./remove_path.txt","r") as f:
	fileList = f.readlines()

def get_filesize(path):
	"""获取文件的大小,结果保留两位小数，单位为MB"""
	fsize = os.path.getsize(path)
	fsize = fsize/float(1024*1024)
	return round(fsize,2)

for path in fileList:
	if os.path.isfile(path):
		fsize = get_filesize(path)
		if int(fsize)>2: # 移除大于2MB的文件
			os.remove(path)