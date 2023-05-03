import json
import requests
import pandas as pd
import os
from airflow.models import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime




default_args = {
    'start_date': datetime(year=2023, month=4, day=20)
}

def extract_users(url: str, ti) -> None:
    res = requests.get(url)
    json_data = json.loads(res.content)
    ti.xcom_push(key='extracted_users', value=json_data)

def transform_users(ti) -> None:
    users = ti.xcom_pull(key='extracted_users', task_ids=['extract_users'])[0]
    transformed_users = []
    for user in users:
        transformed_users.append({
            'ID': user['id'],
            'Name': user['name'],
            'Username': user['username'],
            'Email': user['email'],
            'Address': f"{user['address']['street']}, {user['address']['suite']}, {user['address']['city']}",
            'PhoneNumber': user['phone'],
            'Company': user['company']['name']
        })
    ti.xcom_push(key='transformed_users', value=transformed_users)


def load_users(ti, **kwargs) -> None:

    execution_date = kwargs['execution_date']
    data_atual = execution_date.strftime('%d-%m-%Y')
    nome_arquivo = f'exemplo_{data_atual}.csv'
    caminho_do_arquivo = r'data'
    if not os.path.exists(caminho_do_arquivo):
        os.makedirs(caminho_do_arquivo)
    
    users = ti.xcom_pull(key='transformed_users', task_ids=['transform_users'])
    users_df = pd.DataFrame(users[0])
    users_df.to_csv(os.path.join(caminho_do_arquivo, nome_arquivo))
    print(f'O arquivo foi salvo em: {os.getcwd()}/{caminho_do_arquivo}')
   

with DAG(
    dag_id='etl_users',
    default_args=default_args,
    schedule_interval='@daily'
) as dag:


    task_extract_users = PythonOperator(
        task_id='extract_users',
        python_callable=extract_users,
        op_kwargs={'url': 'https://jsonplaceholder.typicode.com/users'}
    )


    task_transform_users = PythonOperator(
        task_id='transform_users',
        python_callable=transform_users
    )
   
    task_load_users = PythonOperator(
        task_id='load_users',
        python_callable=load_users,
        provide_context=True
    )

    task_extract_users >> task_transform_users >> task_load_users