from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from scripts.elt import *


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 3, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'dummy_api_etl',
    default_args=default_args,
    description='Uma DAG de com funções do ETL',
    schedule_interval=timedelta(days=1),
)

t1 = PythonOperator(
    task_id='extract_users',
    python_callable=extract_users,
    op_kwargs={'url': 'https://dummyapi.io/data/v1/user', 'app_id': '63eecdb28d3fc51cbfc2d4ab'},
    dag=dag,
)

t2 = PythonOperator(
    task_id='extract_user_details',
    python_callable=extract_user_details,
    op_kwargs={
        'user_id': "{{ task_instance.xcom_pull(task_ids='extract_users', key='user_id') }}",
        'url': base_url_users,
        'app_id': app_id
    },
    dag=dag
)


t3 = PythonOperator(
    task_id='transform_users',
    python_callable=transform_users,
    op_kwargs={'users': '{{ ti.xcom_pull(task_ids="extract_users") }}'},
    dag=dag,
)


t4 = PythonOperator(
    task_id='save_users',
    python_callable=salvar_users,
    op_kwargs={'df': '{{ ti.xcom_pull(task_ids="transform_users") }}',
               'path': '/home/nay/Downloads/engdados/github/main-code/data/processed/users-1.csv'},
    dag=dag,
)

t1 >> t2 >> t3 >> t4
