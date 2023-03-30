from etl import *


   # Faz o request para os  usuários
url = f"{base_url_users}?limit={limit}"
users = extract_users(url, app_id)

    # Faz o request para o detalhamento de cada usuário individualmente
for user in users:
    user_details = extract_user_details(user['id'], base_url_users, app_id)
    user.update(user_details)
    
    # Transforma os dados dos usuários
transformed_users = transform_users(users)


#     #Validação dos dados 
# validate_data(transformed_users)
    
    
    # Salva os dados em formato CSV
output_path = '/home/nay/Downloads/engdados/github/main-code/data/processed/users-9.csv'
salvar_users(transformed_users, output_path)