
from tkinter import messagebox
import urllib.request
import json
import datetime
import numpy as np
import pandas as pd
from tkinter import *

client_id = 	"Vn6Ao_YuYaL2VvScfEhv"
client_secret = "2pEG8Ry0nf"

# 클라이언트가 서버에 요청할 URL 정보 생성

encText = urllib.parse.quote("애플")
url = 'https://openapi.naver.com/v1/search/shop.json?query=' + encText


# URL 정보로 서버에게 요청과 응답
request = urllib.request.Request(url)      # 요청
request.add_header("X-Naver-Client-Id", client_id)
request.add_header("X-Naver-Client-Secret", client_secret)
response = urllib.request.urlopen(request) # 응답

# 응답을 제대로 받았는지 확인
rescode = response.getcode()
#print(rescode)

if(rescode==200):
    response_body = response.read()
    #print(response_body.decode('utf-8'))
else:
    print("Error Code:" + rescode)


def gen_search_url(api_node,search_text,start_num,disp_num):
    base = 'https://openapi.naver.com/v1/search'
    node = '/' + api_node + '.json'
    param_query = '?query=' + urllib.parse.quote(search_text)
    param_start = '&start=' + str(start_num)
    param_disp = '&display=' + str(disp_num)
    return base + node + param_query + param_disp + param_start

def get_result_onpage(url):
    request = urllib.request.Request(url)
    request.add_header('X-Naver-Client-Id', client_id)
    request.add_header('X-Naver-Client-Secret', client_secret)
    response = urllib.request.urlopen(request)
    print(f'{datetime.datetime.now()} Url Request Success')
    return json.loads(response.read().decode('utf-8'))

def delete_tag(input_str):
    input_str = input_str.replace('<b>', '')
    input_str = input_str.replace('</b>', '')
    input_str = input_str.replace('\xa0', '')
    return input_str


def get_fields(json_data):
    title = [delete_tag(each['title']) for each in json_data['items']]
    link = [each['link'] for each in json_data['items']]
    lprice = [each['lprice'] for each in json_data['items']]
    mall_name = [each['mallName'] for each in json_data['items']]
    now_date = datetime.datetime.now().strftime("%m-%d")
    result = pd.DataFrame({
        'title': title,
        'link': link,
        'lprice': lprice,
        'mall_name': mall_name,
        'now_date': now_date,
    }, columns=['title','lprice','mall_name','link','now_date'])
    print(result)
    return result

def validate_and_process():
    encTextInput = labEnt1.get()
    encNumInput = labEnt2.get()

    # 숫자인지 확인
    if not encNumInput.isdecimal():
        messagebox.showerror("오류", "숫자를 입력해주세요")
        return
    encNum = int(encNumInput)

    # 숫자 범위 확인
    if encNum > 1000:
        messagebox.showerror("오류", "1000까지만 가능합니다")
        return
    
    get_search_results(encTextInput, encNum)


def get_search_results(encTextInput, encNum):
    result_datas = []
    for n in range(1, int(encNum), 100): #가운데 파라미터가 최대 개수를 설정하는것이다.   
        url = gen_search_url('shop', encTextInput, n, min(100, encNum))
        json_result = get_result_onpage(url)
        result = get_fields(json_result)

        if not result.empty:
            result_datas.append(result)
    
    if result_datas:
        # 리스트로 저장된 데이터셋을 concat 함수로 모두 병합해주고, reset_index로 인덱스를 초기화해 0부터 정렬되도록 하자.
        result_datas_concat = pd.concat(result_datas)
        result_datas_concat.reset_index(drop=True, inplace=True)
        try:
            result_datas_concat['lprice'] = result_datas_concat['lprice'].astype(np.float64)
            result_datas_concat.to_csv('./web_sc_result/Naver_shopping.csv', sep=',', encoding="utf-8")
            print("CSV 파일이 성공적으로 저장되었습니다.")
        except Exception as e:
            print(f'Error during file saving: {e}')

# tkinter gui
tk = Tk()
tk.title('빠른 스크랩퍼')
tk.geometry('400x400')

lab1 = Label(tk, text='(!문자)스크래핑할 검색어를 입력해주세요:')
lab1.pack()
labEnt1 = Entry(tk, width=30)
labEnt1.pack()

lab2 = Label(tk,text='(!숫자)최대 크롤링할 개수를 입력해주세요:')
lab2.pack()
labEnt2 = Entry(tk, width=30)
labEnt2.pack()

labBtn = Button(tk, text='확인',width=300,height=3, bg='blue', fg='white', command=validate_and_process)
labBtn.pack(side='bottom')

tk.mainloop()