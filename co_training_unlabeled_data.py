# -*- coding: utf-8 -*-
"""
Modify the sample crawler to get the desired data as needed
"""
import requests
from bs4 import BeautifulSoup
import mysql.connector

flag = 0  #0 for high, 1 for low
config={'host':'127.0.0.1',
        'user':'root',
        'password':'root',
        'port':3306 ,
        'database':'paper',
        'charset':'utf8'
        }
config1={'host':'127.0.0.1',
        'user':'root',
        'password':'root',
        'port':3306 ,
        'database':'paper',
        'charset':'utf8'
        }
try:
  conn=mysql.connector.connect(**config)
except mysql.connector.Error as e:
  print 'connect fails!{}'.format(e) 
  if '1045' in format(e):
      try:
          conn=mysql.connector.connect(**config1)
      except mysql.connector.Error as e:
          print 'connect fails!{}'.format(e)

cursor = conn.cursor()

if flag == 0:
    sql0 = "INSERT INTO co_training_unlabeled_data (URL, 回复内容, 问题, 提问时间, 回答时间) VALUES (%s, %s, %s, %s, %s)"
elif flag == 1:
    sql0 = "INSERT INTO co_training_unlabeled_data (URL, 回复内容, 问题, 提问时间, 回答时间) VALUES (%s, %s, %s, %s, %s)"
    
def get_session():
    s = requests.Session()
    s.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36'
    return s
s = get_session()
r = s.get('http://www.haodf.com/sitemap-zx/20160326_1/')
soup = BeautifulSoup(r.content)
print soup.select('div.p_bar > a.page_turn_a')[-1].text.strip()
total_pages = soup.select('div.p_bar > a.page_turn_a')[-1].text.strip()
total_questions_links = []
for tp in xrange(1, int(total_pages)+1):
    print 'pages:', tp
    r1 = s.get('http://www.haodf.com/sitemap-zx/20160326_%d/' % tp)
    soup1 = BeautifulSoup(r1.content)
    for tql in xrange(len(soup1.select('div.map_all > div > li > a'))):
        total_questions_links.append(soup1.select('div.map_all > div > li > a')[tql].get('href').strip())
    print 'num_of_questions_one_page:', len(total_questions_links)
print 'num_of_questions_all_page:', len(total_questions_links)

que_cnt = 0
for input_url1 in total_questions_links:
    que_cnt += 1
    print 'total_questions:', len(total_questions_links)
    print 'que_cnt:', que_cnt
    url = input_url1
    print 'url', url
    if 'http' in input_url1:
        r2 = s.get(input_url1)
    else:
        r2 = s.get('http://' + input_url1)
    soup2 = BeautifulSoup(r2.content)
    if len(soup2.select('div.h_s_time')) < 2:continue
    if '：' in soup2.select('div.h_s_time')[0].text.strip().split('发表于')[-1]:
        continue
    que_time = soup2.select('div.h_s_time')[0].text.strip().split('发表于')[-1].strip()
    print 'que_time:', que_time
    if len(soup2.select('div.h_s_info_cons > p')) < 3:continue
    if '希望提供的帮助：' not in soup2.select('div.h_s_info_cons > p')[1].text.strip() or '疾病：' not in soup2.select('div.h_s_info_cons > p')[0].text.strip():
        continue
    que = soup2.select('div.h_s_info_cons > h2')[0].text.strip() + '，' + soup2.select('div.h_s_info_cons > p')[1].text.strip().split('希望提供的帮助：')[1].strip()
    print 'que:', que
    if len(soup2.select('div.h_s_cons_docs')) == 0:continue
    if '此对话涉及隐私内容仅患者本人和医生可见' in soup2.select('div.h_s_cons_docs')[0].encode('utf8'):
        continue
    if len(soup2.select('div.h_s_cons_docs > h3')[0].text.strip()) < 15:continue
    ans = soup2.select('div.h_s_cons_docs > h3')[0].text.strip()
    print 'ans:', ans
    ans_time = soup2.select('div.h_s_time')[1].text.strip().split('发表于')[-1].lstrip('：')
    print 'ans_time:', ans_time
    print
    cursor.execute(sql0, (url, ans, que, que_time, ans_time))
    conn.commit()     
    
cursor.close()
conn.close()







































































































































































