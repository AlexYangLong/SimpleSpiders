import requests

url = 'http://fm.shiyunjj.com/2018/1334/3iu7.jpg'

headers = {
    'Referer': 'http://www.mmjpg.com/mm/1334',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'''
}

resp = requests.get(url=url, headers=headers)

print(resp.content)
