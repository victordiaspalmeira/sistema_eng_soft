import requests
url = 'http://127.0.0.1:5000/auth/register_user'

if __name__ == '__main__':
    obj = {
        'username': 'master1',
        'password': 'master1',
        'INST_ID':  0,
        'INST_TYPE': 0,
        'NOME': 'master',
        'SOBRENOME': 'SYS',
        'CARGO': 'master',
        'EMAIL':'master@master.com',
        'TELEFONE': '0'
    }
    x = requests.post(url, data = obj)

    print(x.text)