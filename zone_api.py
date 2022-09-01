# -*- coding:utf-8 -*-
import requests,re,json
import os,sys
import openpyxl
import time
from tqdm import tqdm
import configparser

def extract_element_from_json(obj, path):
    def extract(obj, path, ind, arr):
        key = path[ind]
        if ind + 1 < len(path):
            if isinstance(obj, dict):
                if key in obj.keys():
                    extract(obj.get(key), path, ind + 1, arr)
                else:
                    arr.append(None)
            elif isinstance(obj, list):
                if not obj:
                    arr.append(None)
                else:
                    for item in obj:
                        extract(item, path, ind, arr)
            else:
                arr.append(None)
        if ind + 1 == len(path):
            if isinstance(obj, list):
                if not obj:
                    arr.append(None)
                else:
                    for item in obj:
                        arr.append(item.get(key, None))
            elif isinstance(obj, dict):
                arr.append(obj.get(key, None))
            else:
                arr.append(None)
        return arr
    if isinstance(obj, dict):
        return extract(obj, path, 0, [])
    elif isinstance(obj, list):
        outer_arr = []
        for item in obj:
            outer_arr.append(extract(item, path, 0, []))
        return outer_arr

def zone_information(search,page,api):
    information_url= 'https://0.zone/api/data/'
    print('[-] 开始提取数据')
    for pg in tqdm(range(1,int(page))):
        time.sleep(2)
        url_data={"title":f"{search}", "title_type":"site", "page":f"{str(pg)}", "pagesize":"40", "zone_key_id":f"{api}"}

        r= requests.post(url=information_url,data=url_data)
        pp=r.content.decode('utf-8')
        jp=json.loads(pp)
        if jp['code'] == 1:
            print('[-] '+jp['message'])
            sys.exit()
        ips=extract_element_from_json(jp,["data","ip"])
        if ips==[None]:
            print('[+] 数据全部提取完毕提前结束')
            break
        urls=extract_element_from_json(jp,["data","url"])
        titles=extract_element_from_json(jp,["data","title"])
        status_codes=extract_element_from_json(jp,["data","status_code"])
        groups=extract_element_from_json(jp,["data","group"])
        operators=extract_element_from_json(jp,["data","operator"])
        CMS=extract_element_from_json(jp,["data","cms"])
        data_len=len(urls)
        for i in range(data_len):
            p = list(map(str,[ips[i]]))
            p.append(str(urls[i]))
            p.append(str(titles[i]))
            p.append(str(status_codes[i]))
            p.append(str(groups[i]))
            p.append(str(operators[i]))
            p.append(str(CMS[i]))
            sb_data.append(p)

def zone_email(search,page,api):
    url = 'https://0.zone/api/data/'
    print('[-] 开始提取数据')
    for pg in tqdm(range(1,int(page))):
        time.sleep(2)
        url_data = {"title": f"{search}", "title_type": "email", "page": f"{str(pg)}", "pagesize": "40",
                    "zone_key_id": f"{api}"}

        r = requests.post(url=url, data=url_data)
        pp=(r.content.decode('utf-8'))
        jp = json.loads(pp)
        if jp['code']==1:
            print('[-] '+jp['message'])
            sys.exit()
        emails=extract_element_from_json(jp,["data","email"])
        if emails==[None]:
            print('[+] 数据全部提取完毕提前结束')
            break
        email_types=extract_element_from_json(jp,["data","email_type"])
        groups=extract_element_from_json(jp,["data","group"])
        data_len = len(emails)
        for i in range(data_len):
            p = list(map(str, [emails[i]]))
            p.append(str(email_types[i]))
            p.append(str(groups[i]))
            sb_data.append(p)
def zone_apk(search,page,api):
    url = 'https://0.zone/api/data/'
    for pg in tqdm(range(1,int(page))):
        time.sleep(2)
        url_data = {"title": f"{search}", "title_type": "apk", "page": f"{str(pg)}", "pagesize": "40",
                    "zone_key_id": f"{api}"}
        r = requests.post(url=url, data=url_data)
        pp=(r.content.decode('utf-8'))
        jp = json.loads(pp)
        if jp['code']==1:
            print('[-] '+jp['message'])
            sys.exit()
        titles=extract_element_from_json(jp,["data","title"])
        if titles==[None]:
            print('[+] 数据全部提取完毕提前结束')
            break
        sources=extract_element_from_json(jp,["data","source"])
        wechat_ids=[]
        iconUrls=[]
        codes=[]
        groups=extract_element_from_json(jp,["data","group"])
        data_len = len(titles)
        for j in range(data_len):
            try:
                wechat_id=jp['data'][j]['msg']['wechat_id']
                iconUrl=jp['data'][j]['msg']['iconUrl']
                code=jp['data'][j]['msg']['code']
                wechat_ids.append(wechat_id)
                iconUrls.append(iconUrl)
                codes.append(code)
            except:
                wechat_ids.append(None)
                iconUrls.append(None)
                codes.append(None)
        for i in range(data_len):
            p = list(map(str, [titles[i]]))
            p.append(str(sources[i]))
            p.append(str(wechat_ids[i]))
            p.append(str(iconUrls[i]))
            p.append(str(codes[i]))
            p.append(str(groups[i]))
            sb_data.append(p)

def zone_sd(search,page,api):
    url = 'https://0.zone/api/data/'
    for pg in tqdm(range(1,int(page))):
        time.sleep(2)
        url_data = {"title": f"{search}", "title_type": "sensitive", "page": f"{str(pg)}", "pagesize": "40",
                    "zone_key_id": f"{api}"}
        r = requests.post(url=url, data=url_data)
        pp=(r.content.decode('utf-8'))
        jp = json.loads(pp)
        if jp['code']==1:
            print('[-] '+jp['message'])
            sys.exit()
        urls = extract_element_from_json(jp, ["data", "url"])
        if urls == [None]:
            print('[+] 数据全部提取完毕提前结束')
            break
        titles=extract_element_from_json(jp, ["data", "title"])
        groups=extract_element_from_json(jp, ["data", "group"])
        device_types=extract_element_from_json(jp, ["data", "device_type"])
        data_len = len(urls)
        for i in range(data_len):
            p = list(map(str, [urls[i]]))
            p.append(str(titles[i]))
            p.append(str(groups[i]))
            p.append(str(device_types[i]))
            sb_data.append(p)

def zone_code(search,page,api):
    url = 'https://0.zone/api/data/'
    for pg in tqdm(range(1,int(page))):
        time.sleep(2)
        url_data = {"title": f"{search}", "title_type": "code", "page": f"{str(pg)}", "pagesize": "40",
                    "zone_key_id": f"{api}"}
        r = requests.post(url=url, data=url_data)
        pp=(r.content.decode('utf-8'))
        jp = json.loads(pp)
        if jp['code']==1:
            print('[-] '+jp['message'])
            sys.exit()
        code_urls = extract_element_from_json(jp, ["data", "code_url"])
        if code_urls == [None]:
            print('[+] 数据全部提取完毕提前结束')
            break
        names=extract_element_from_json(jp,["data","name"])
        keywords=extract_element_from_json(jp, ["data", "keyword"])
        sources=extract_element_from_json(jp, ["data", "source"])
        groups=extract_element_from_json(jp, ["data", "group"])
        data_len = len(code_urls)
        for i in range(data_len):
            p = list(map(str, [code_urls[i]]))
            p.append(str(names[i]))
            p.append(str(keywords[i]))
            p.append(str(sources[i]))
            p.append(str(groups[i]))
            sb_data.append(p)

def zone_member(search,page,api):
    url = 'https://0.zone/api/data/'
    for pg in tqdm(range(1,int(page))):
        time.sleep(2)
        url_data = {"title": f"{search}", "title_type": "member", "page": f"{str(pg)}", "pagesize": "40",
                    "zone_key_id": f"{api}"}
        r = requests.post(url=url, data=url_data)
        pp=(r.content.decode('utf-8'))
        jp = json.loads(pp)
        if jp['code']==1:
            print('[-] '+jp['message'])
            sys.exit()
        names = extract_element_from_json(jp, ["data", "name"])
        if names == [None]:
            print('[+] 数据全部提取完毕提前结束')
            break
        groups=extract_element_from_json(jp, ["data", "group"])
        sources=extract_element_from_json(jp, ["data", "source"])
        data_len = len(names)
        for i in range(data_len):
            p = list(map(str, [names[i]]))
            p.append(str(groups[i]))
            p.append(str(sources[i]))
            sb_data.append(p)

def excl_sheel(use):
    path = r"/Users/lemonlove7/Documents/code/py/搜索引擎/零零信安/"
    os.chdir(path)
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    timestr=''
    if use =='1':
        sheet.title = '信息系统'
        timestr = '信息系统_'+time.strftime("%Y%m%d-%H%M%S")
    if use =='2':
        sheet.title = '移动端应用'
        timestr = '移动端应用_'+time.strftime("%Y%m%d-%H%M%S")
    if use =='3':
        sheet.title='敏感目录'
        timestr = '敏感目录_' + time.strftime("%Y%m%d-%H%M%S")
    if use =='4':
        sheet.title='邮箱'
        timestr = '邮箱_' + time.strftime("%Y%m%d-%H%M%S")
    if use =='5':
        sheet.title='代码'
        timestr = '代码_' + time.strftime("%Y%m%d-%H%M%S")
    if use =='6':
        sheet.title = '人员'
        timestr = '人员_' + time.strftime("%Y%m%d-%H%M%S")
    file_name=timestr+'.xlsx'
    workbook.save(file_name)
    workbook = openpyxl.load_workbook(file_name)
    sheet = workbook.active
    if use =='1':
        sheet['A1'] = 'ip'
        sheet['B1'] = 'url'
        sheet['C1'] = 'title'
        sheet['D1'] = 'status_code'
        sheet['E1']='公司名称'
        sheet['F1']='运营商'
        sheet['G1']='CMS'
    if use =='2':
        sheet['A1'] = '名称'
        sheet['B1'] = '来源'
        sheet['C1'] = '微信公众号ID'
        sheet['D1'] = '链接'
        sheet['E1']='微信公众号二维码'
        sheet['F1']='公司'
    if use =='3':
        sheet['A1'] = '域名'
        sheet['B1'] = '标题'
        sheet['C1'] = '公司名称'
        sheet['D1'] = '设备类型'
    if use =='4':
        sheet['A1']='邮箱'
        sheet['B1'] = '邮箱类型'
        sheet['C1']='所属公司'
    if use =='5':
        sheet['A1'] = '链接'
        sheet['B1'] = '代码名称'
        sheet['C1'] = '匹配上的关键字'
        sheet['D1'] = '代码来源'
        sheet['E1']='所属公司'
    if use =='6':
        sheet['A1'] = '姓名'
        sheet['B1'] = '公司'
        sheet['C1'] = '来源'
    data=sb_data
    for row in data:
        sheet.append(row)
    workbook.save(file_name)
    print(f'[+] 写入完成,数据保存在{file_name}中')

if __name__ == '__main__':
    print('[+] author:lemonlove7\n[+] team:鹏组安全')
    config = configparser.ConfigParser()
    pwd = os.getcwd()
    if os.name == 'posix':
        path = '/config/config.ini'
    if os.name == 'nt':
        path = '\\config\\config.ini'
    pwd = os.getcwd()
    paths = pwd + '/config/config.ini'
    config.read(paths)
    page = config.get('default', 'page')
    page=int(page)+1
    api= config.get('default', 'api')

    print('[-] 查询语法参考:https://0.zone/grammarList')
    while True:
        print('[-] 查询的类型:\n[+] 1:信息系统；2:移动端应用；3:敏感目录；4:邮箱；5:代码/文档；6:人员；7:退出')
        use=input('[-] 请输入数字(1-7):')
        if use =='7':
            sys.exit()
        search=input('[-] 请输入要查询的语句:')
        sb_data = []
        if use=='1':
            zone_information(search=search,page=page,api=api)
        if use =='2':
            zone_apk(search=search,page=page,api=api)
        if use =='3':
            zone_sd(search=search,page=page,api=api)
        if use == '4':
          zone_email(search=search,page=page,api=api)
        if use =='5':
            zone_code(search=search,page=page,api=api)
        if use =='6':
            zone_member(search=search,page=page,api=api)
        excl_sheel(use=use)
