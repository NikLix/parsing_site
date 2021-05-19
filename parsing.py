# -*- coding: utf-8 -*-

import mysql.connector as conn
import time
import requests
from bs4 import BeautifulSoup


def get_html(url,page=''):
    """
    Get запрос по url и
    Вывод запрошенной страницы
    :url url запрашиваемого сайта 
    :page страница добавляемая к url
    """
    r = requests.get(str(url+"/"+str(page))) 
    return BeautifulSoup(r.text, 'html.parser')

def connect_db(sql):
    """
    Соединение с базой данных и выполнение запроса к ней
    :sql Запрос добавления данных о организации     
    """
    db = conn.connect(host="localhost", user="root", password="mysql", db="db", charset='utf8')
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()     
    cursor.close()
    db.close()


def search_okpo(url_id_company):
    """
    Поиск номера ОКПО организации через url
    :url_id_company url организации у который ищем ОКПО 
    """
    soup = get_html(url_id_company)
    okpo = soup.find('span', {'id': 'clip_okpo'}) 
    return okpo.text.strip() if okpo else 'null'
    

def pars (company):
    """
    Парсинг страницы https://www.rusprofile.ru/codes/* 
    Собираем данные:
    Название организации,
    ОРГН,
    Статус организации
    Дата регистрации,
    Уставный капитал
     
    :company Страница с get Запроса

    return
     :url url организации 
     :Список собираемых данных  
    """
    name = 'null'
    ogrn = 'null'
    date_reg = 'null'
    us_capital = 'null'
    
    find_name = company.find('div', class_='company-item__title')
    name=find_name.find('a').text.strip()
    #Собираем url компании для того чтобы определить их ОКПО
    url_id_company = 'https://www.rusprofile.ru'+find_name.find('a').get('href')
    
    find_status = company.find('div', class_='company-item-status')
    status = find_status.text.strip() if find_status else 'Действующая организация'
    
    info = company.find_all('div', class_='company-item-info')
    info_dl = info[1].find_all('dl')
    for col in info_dl:
        if col.find('dt').text.strip() == 'ОГРН':
            ogrn = col.find('dd').text.strip()
        elif col.find('dt').text.strip() == 'Дата регистрации':
            date_reg = col.find('dd').text.strip()
        elif col.find('dt').text.strip() == 'Уставный капитал':
            us_capital = col.find('dd').text.strip()
    
    return url_id_company,[name,ogrn,status,date_reg,us_capital]

def main(soup):
    """ 
    :soup Страница с get Запроса 
    """
    company = soup.find_all('div', class_='company-item') 
    list_url = []
    list_okpo = []
    list_items = []
    sql = '''
    INSERT company(
        name
        ,ogrn
        ,status
        ,date_reg
        ,us_capital
        ,okpo
        )
        VALUES
    '''
    # Формируем список URL организаций и 
    # Список собираемых данных об организации
    for items in company:      
        url,items = pars(items)
        list_url.append(url)
        list_items.append(items) 
        break
    # Проходимся по всем организациям извлекая из них ОКПО
    for url in list_url:
        list_okpo.append(search_okpo(url)) 
        # Замедляем чтобы не было подозрительной активности
        time.sleep(3)
    
    # Формируем sql запрос из собранных данных
    for i in range(0,len(list_url)):
        sql += '''('{}',{},'{}','{}','{}',{}),'''.format(
        list_items[i][0], # name
        list_items[i][1], # ОГРН
        list_items[i][2], # Статус организации
        list_items[i][3], # Дата регистрации
        list_items[i][4], # Уставный капитал
        list_okpo[i]      # ОКПО
        )
    
    connect_db(sql[:-1]+';')


# Страницы для парсинга
url_429110 = 'https://www.rusprofile.ru/codes/429110'
url_89220 = 'https://www.rusprofile.ru/codes/89220'

main(get_html(url_89220))
for i in range(1,3):
    main(get_html(url_429110,i))
