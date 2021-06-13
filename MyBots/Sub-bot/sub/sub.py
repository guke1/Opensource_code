import opencc
import pysubs2
def subs(file,c):
	_json = ['s2t.json', 't2s.json', 's2tw.json', 'tw2s.json', 't2jp.json', 'jp2t.json']
	c_list = ['简转繁', '繁转简', '简转台湾', '台湾转简', '繁转日文', '日文转繁']
	c = str(c)
	i = c_list.index(c)
	c = _json[i]
	try:
		sub = pysubs2.load(file)
		for line in sub:
			converter = opencc.OpenCC(c)  # 转换文件编码
			line.text = converter.convert(line.text)
		print("转换成功，文件名为:",file)
		sub.save(file)
		return True
	except IOError:
		return False