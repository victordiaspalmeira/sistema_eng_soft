import requests
url_user = 'http://127.0.0.1:5000/auth/register_user'
url_inst = 'http://127.0.0.1:5000/auth/register_inst'
url_test = 'http://127.0.0.1:5000/auth/test'
url_login = 'http://127.0.0.1:5000/auth/login'
if __name__ == '__main__':
    obj = {
        'username': 'master3',
        'password': 'master3',
        'INST_ID':  0,
        'INST_TYPE': 0,
        'NOME': 'master',
        'SOBRENOME': 'SYS',
        'CARGO': 'master',
        'EMAIL':'master@master.com',
        'TELEFONE': '0'
    }

    #Tentativa de criar usuário
    print('=== TENTATIVA DE CRIAR USUÁRIO SEM ESTAR LOGADO ===')
    x = requests.post(url_user, data = obj)
    print(x.text)

    #Tentativa de logar
    print('=== TENTATIVA DE LOGAR ===')
    obj = {
        'username': 'master3',
        'password': 'master3',
    }

    x = requests.post(url_login, data = obj)
    c = x.cookies
    print(x.text)

    #Tentativa de acessar uma página que requer usuário logado
    print('=== TENTATIVA LOGIN REQUIRED ===')
    x = requests.post(url_test, data = obj, cookies=c)
    print(x.text)

    print('=== TENTATIVA DE REGISTRAR INST LOGADO ===')
    x = requests.post(url_inst, data = obj, cookies=c)
    print(x.text)