import pandas as pd
import requests
import json
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
    df = pd.DataFrame(transformed_users)
    df['Genero'] = df['Genero'].replace({'male': 'homem', 'female': 'mulher'})
    return df

def salvar_users(df, path):
    today = datetime.date.today().strftime('%Y-%m-%d')
    filename = f'user{today}.csv'
    df.to_csv(path + filename, index=False)


if __name__ == '__main__':

    url = f"{base_url_users}?limit={limit}"
    users = extract_users(url, app_id)

    # Faz o request para o detalhamento de cada usuário individualmente
    for user in users:
        user_details = extract_user_details(user['id'], base_url_users, app_id)
        user.update(user_details)
    
    # Transforma os dados dos usuários
    transformed_users = transform_users(users)

    path = 'C:/Users/nayya/Downloads/ESTUDO/projetos/main-code/airflow/dags/dados/'
    salvar_users(transformed_users, path)
