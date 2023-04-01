import pandas as pd
import requests
import json
import pandera as pa
from pandera import Column, Check
import datetime


base_url_users = 'https://dummyapi.io/data/v1/user'
app_id = '63eecdb28d3fc51cbfc2d4ab'
pages = 5
limit = 100


def extract_users(url: str, app_id: str) -> list:
    headers = {'Content-Type': 'application/json', 'app-id': app_id}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        users = response.json()['data']
        return users
    else:
        print(f"Error {response.status_code}")
        return []

def extract_user_details(user_id: str, url: str, app_id: str) -> dict:
    headers = {'Content-Type': 'application/json', 'app-id': app_id}
    response = requests.get(f"{url}/{user_id}", headers=headers)
    if response.status_code == 200:
        user_details = response.json()
        return user_details
    else:
        print(f"Error {response.status_code}")
        return {}
    

def transform_users(user_details):
    transformed_users = []
    for user in users:
        user_details = extract_user_details(user['id'], base_url_users, app_id)
        transformed_users.append({
            'ID': user['id'],
            'Nome': user['firstName'] + ' ' + user['lastName'],
            'Email': user_details['email'],
            'Genero': user_details['gender'],
            'Data_aniverario': pd.to_datetime(user_details['dateOfBirth']).date(),
            'Data_registro': pd.to_datetime(user_details['registerDate']).date(),
            'Telefone': user_details['phone'],
            'País': f"{user_details['location']['country']}",
            'Cidade': f"{user_details['location']['city']}"
        })

    # Transforma a lista em um DataFrame
    df = pd.DataFrame(transformed_users)

    # Transforma a coluna 'Genero'
    df['Genero'] = df['Genero'].replace({'male': 'homem', 'female': 'mulher'})

    return df

def salvar_users(df, path):
    # Obter a data atual
    today = datetime.date.today().strftime('%Y-%m-%d')
    
    # Adicionar a data ao nome do arquivo
    filename = f'user{today}.csv'
    
    # Salvar o arquivo
    df.to_csv(path + filename, index=False)


if __name__ == '__main__':

    # Faz o request para os  usuários
    url = f"{base_url_users}?limit={limit}"
    users = extract_users(url, app_id)

    # Faz o request para o detalhamento de cada usuário individualmente
    for user in users:
        user_details = extract_user_details(user['id'], base_url_users, app_id)
        user.update(user_details)
    
    # Transforma os dados dos usuários
    transformed_users = transform_users(users)

    # #Validação dos dados 
    # validate_data(transformed_users)
    
    
     # Salva os dados em formato CSV
    path = '/Users/nayya/Downloads/ESTUDO/projetos/projetorescue/ingestao/airflow/dags/dados/'

    salvar_users(transformed_users, path)


'''
Fazer graficos com Idade, Região, Homem mulher 

criar as dags e puxar a função de dentro do arquivo scrits/extracao.py

extração de dados e transferir para formato parket
 - Salva os dados em formato Parquet
    df.to_parquet("users.parquet")

enviar o arquivo dessa extração para aws
'''
