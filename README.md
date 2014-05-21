web_spider
==========

简单的网页爬虫。 测试网站为bj.597rcw.com，抓取该网站的发布招聘信息的公司及联系方式，包存到文本中.


用到的开源项目：

pytesser：

https://code.google.com/p/pytesser/

修改pytesser.py在调用tesseract的时候加了'nobatch', 'digits'2个参数，以便识别数字(手机号)。

Tesseract engine：

https://code.google.com/p/tesseract-ocr/

PIL：

http://www.pythonware.com/products/pil/


