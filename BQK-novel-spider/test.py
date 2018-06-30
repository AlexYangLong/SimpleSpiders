import requests
from lxml import etree

url = 'http://www.biqukan.net/book/85167/25666333.html'
resp = requests.get(url)

html = etree.HTML(resp.text.encode('iso-8859-1').decode('gbk'))
content = html.xpath('//div[@id="htmlContent"]/text()')
try:
    html.xpath('//div[@id="htmlContent"]/p')
    next = html.xpath('//*[@id="linkNext"]/@href')
    resp2 = requests.get(next[0])
    html2 = etree.HTML(resp2.text.encode('iso-8859-1').decode('gbk'))
    content2 = html2.xpath('//div[@id="htmlContent"]/text()')
    content3 = content + content2
except:
    pass
cons = ''.join(content3)  # [con.replace('\xa0', '') for con in content3]
print(cons)
