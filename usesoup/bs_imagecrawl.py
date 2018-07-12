import urllib.request
import requests
from bs4 import BeautifulSoup
import json
import os


################### 이미지 크롤링 함수 ####################


def imgdown(url,name,count):


	print(url)

	try:
		req = urllib.request.Request(url)
		data = urllib.request.urlopen(req).read()


		bs = BeautifulSoup(data,'html.parser')
		img = bs.find_all('img')
		imgurl = []

		for ele in img:
			val = ele.get('class')
			if val!=None and len(val)>1 and val[1]=='h-flex-auto': #전체가 h-image-img h-flex-auto responsive이며 두번째 파라미터로 구분
				base_url = ele.get("src")
				imgurl.append(base_url)


		imgpath= "C:/IMGcrawl/" + name + "/"
		if not os.path.isdir(imgpath):
			os.makedirs(imgpath)

		imgpath_org = imgpath + 'oringinal/'
		if not os.path.isdir(imgpath_org):
			os.makedirs(imgpath_org)

		imgpath_model = imgpath + 'model/'
		if not os.path.isdir(imgpath_model):
			os.makedirs(imgpath_model)
		imgname = str(count) + ".png"

		urllib.request.urlretrieve(imgurl[-1],imgpath_org+imgname)
		urllib.request.urlretrieve(imgurl[0],imgpath_model+imgname)

	except:
		return -1



################### 상세페이지 URL 따는 파트 ####################

f = open("siteinfo.txt.",'r')
lines = f.read().split('\n')
print(lines)

for line in lines:
	data = line.split(',')
	name = data[0]
	url = data[1]
	size = data[2]



	urllist = []
	for i in range(1,int(size)): #페이지 개수 만큼 

		urlstr = url + str(i)
		response = requests.get(urlstr)

		html = response.text
		patternc = '![CDATA[{"total'	#cdata로 들어가잇는 데이터들을 찾음

		cdata = html[html.find(patternc)+8:]
		findnum = cdata.find("}]]")	
		cdata = cdata[:findnum+1]
		#print(cdata)

		cjson = json.loads(cdata)
		clothlist = cjson["articles"] #옷들 정보를 리스트로 저장 -> dictionary 화

		for item in clothlist:	
			urllist.append("https://www.zalando.co.uk/" + item["url_key"]+ ".html") #url_key에 url이 저장되어있음


	f = open("test2.txt","a")
	count = 0
	for item in urllist:
		f.write(item)
		f.write('\n')
		if(imgdown(item,name,count)==-1):
			print("\n\n*ERROR*\n\n")
		else:
			count = count+1
	f.close()






#print(cjson["articles"])

'''
req = urllib.request.Request('https://www.zalando.co.uk/mens-clothing-shirts/?activation_date=0-7')
data = urllib.request.urlopen(req).read()

soup = BeautifulSoup(data)
for x in soup.find_all('item'):
	print(x.print)
    print( re.sub('\!\[CDATA\]', '', x.string))

data.decode('utf-8')
patternc = '\<\!\[CDATA\['
print(type(data))
#print(data.find(patternc))



#for x in soup.find_all('item'):
 #   print(re.sub('[\[CDATA\]]', '', x.string))

'''
'''
for ele in alist:
	print(ele)
	print("\n")
	val = ele.get('class')
	if val != None and val[0] == "cat_imageLink-OPGGa":
		base_url = ele.get("href")
		print(base_url)
		print("###")

'''