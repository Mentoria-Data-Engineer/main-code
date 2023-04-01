import requests

base_url = "https://dummyapi.io/data/v1/user?limit=10" 
app_id = "63eecdb28d3fc51cbfc2d4ab"

headers = {'Content-Type': 'application/json', 'app-id': app_id}


def appel_data(data, limite):
    url = '{}{}?limit={}'.format(base_url, data, limite)
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return 'erreur {}'.format(response.status_code)


# Chama a função para obter os dados
dados = appel_data('users', 10)

# Exibe os dados no console
print(dados)
