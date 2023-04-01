from airflow import DAG
from airflow.models import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from scripts.etl import *


default_args = {
    'start_date': datetime(year=2023, month=3, day=30)
}


base_url_users = 'https://dummyapi.io/data/v1/user'
app_id = '63eecdb28d3fc51cbfc2d4ab'
pages = 5
limit = 100

with DAG(
    dag_id='dummy_api_etl',
    default_args=default_args,
    schedule_interval='@daily'
) as dag:

    t1 = PythonOperator(
        task_id='extract_users',
        python_callable=extract_users,
        op_kwargs={'url': base_url_users, 'app_id': app_id}
    )

    t2 = PythonOperator(
        task_id='extract_user_details',
        python_callable=extract_user_details,
        op_kwargs={
            'user_id': "{{ task_instance.xcom_pull(task_ids='extract_users', key='user_id') }}",
            'url': base_url_users,
            'app_id': app_id}
    )

    t3 = PythonOperator(
         task_id='transform_users',
         python_callable=transform_users,
         op_kwargs={'user_details': '{{ ti.xcom_pull(task_ids="extract_user_details") }}'}
    )


    t4 = PythonOperator(
        task_id='salvar_users',
        python_callable=salvar_users,
        op_kwargs={'df': '{{ ti.xcom_pull(task_ids="salvar_users") }}',
                'path': 'C:/Users/nayya/Downloads/ESTUDO/projetos/projetorescue/ingestao/airflow/dags/dados/'}
    )

    t1 >> t2
    t2 >> t3
    t3 >> t4

