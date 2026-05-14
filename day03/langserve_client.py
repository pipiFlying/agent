import requests

def chat():
    responses = requests.post(
        url='http://192.168.3.10:8000/translate/invoke',
        json={"input":{"content":"我来自中国","language":"英语"},"config":{}}
    )
    return responses

if __name__ == '__main__':
    res = chat()

    if res.status_code == 200:
        res_json = res.json()
        if 'output' in res_json:
            print(res_json['output'])
    elif res.status_code == 500:
        print('server error')
    elif res.status_code == 404:
        print('404')
