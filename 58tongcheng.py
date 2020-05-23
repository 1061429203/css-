import re
import base64
from parsel import Selector
import pytesseract
import requests
from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont
import numpy
from fake_useragent import UserAgent

ua=UserAgent()



headers={

'accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
'accept-encoding': 'gzip, deflate, br',
'accept-language': 'zh-CN,zh;q=0.9',
'cache-control': 'no-cache',
'pragma': 'no-cache',
'referer': 'https://c.58cdn.com.cn/git/zp-resume/pc-resume-listpage/css/resumeList_v20200316161911.css',
'sec-fetch-dest': 'image',
'sec-fetch-mode': 'no-cors',
'sec-fetch-site': 'cross-site',
'user-agent': ua.random
}
page_response=requests.get('https://nj.58.com/searchjob/?spm=158447419645.zhaopin_baidu&utm_source=12345',headers=headers)
sel=Selector(page_response.text)
print(page_response.text)

#请求网页,保存原网页及下载字体文件
def get_url(url):
    page_response = requests.get('https://nj.58.com/searchjob/?spm=158447419645.zhaopin_baidu&utm_source=12345',
                                 headers=headers)
    with open('替换之前的.html', mode='w', encoding='utf-8') as f:
        f.write(page_response.text)
    sel = Selector(page_response.text)
    print(page_response.text)
    res = sel.xpath('//style/text()').extract()
    pattern = r'base64,(.*?) format'

    res_pattern = re.search(pattern, res[0])
    font_face = res_pattern.group(1).replace('\n', '')
    b = base64.b64decode(font_face)
    with open('Glided.ttf', 'wb')as f:
        f.write(b)
    return page_response.text

def font_convert(font_path):  # 将web下载的字体文件解析，返回其编码和汉字的对应关系
    font = TTFont(font_path)  # 打开文件
    # 字体编码（特殊的编码）
    code_list = font.getGlyphOrder()[2:]
    # 新建一张图片
    im = Image.new("RGB", (1800, 1800), (255, 255, 255))
    # print(im)
    image_draw = ImageDraw.Draw(im)
    font = ImageFont.truetype(font_path, 40)

    count = 3
    # 将需要转化的内容划分15等份
    # 等分
    array_list = numpy.array_split(code_list, count)
    # print("array_list",array_list)
    for i in range(len(array_list)):
        # print('替换之前的', array_list[i])
        # 讲js的unicode码转化为python的unicode
        new_list = [i.replace("uni", "\\u") for i in array_list[i]]
        # print('替换之后的', new_list)
        # 将列表变为字符串
        text = "".join(new_list)
        print('列表变字符串', text)
        # encode decode
        # 把文字变成二进制
        # 将字符串进行反向编码
        text = text.encode('utf-8').decode('unicode_escape')
        print('反向编码之后的', text)
        # 将文件绘制到图片
        # 指定字体进行绘制
        image_draw.text((0, 100 * i), text, font=font, fill="#000000")

    im.save("aaa.jpg")

    # im.show()
    im = Image.open("aaa.jpg")

    result = zhuanzhuan(im)
    print(result)
    print('aaa')
    result_str = result.replace(" ", "").replace("\n", "")
    # 将内容替换成网页的格式，准备去网页中进行替换
    print(code_list)
    html_code_list = [i.replace("uni", "&#x") + ";" for i in code_list]
    print(html_code_list)
    print(len(html_code_list))
    print(len(result_str))
    print(dict(zip(html_code_list, list(result_str))))
    return dict(zip(html_code_list, list(result_str)))



def zhuanzhuan(im):
    print('aaaaaa')
    result = pytesseract.image_to_string(im, lang="chi_sim")

    print(result)
    return result


if __name__=="__main__":
    url='https://nj.58.com/searchjob/?spm=158447419645.zhaopin_baidu&utm_source=12345'
    html=get_url(url)


    font_rule_map = font_convert('Glided.ttf')
    print(font_rule_map)
    for key,value in font_rule_map.items():
        key = key.lower()
        html=html.replace(key,value)
        print(key,value)
    with open('替换之后的.html', mode='w', encoding='utf-8') as f:
        f.write(html)
