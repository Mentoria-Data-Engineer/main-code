# ETL Automatizado com Airflow: Dummy API para Data Lake AWS

Este projeto demonstra uma pipeline de ETL automatizada que utiliza uma Dummy API para coletar dados, realiza tratamentos nesses dados e os envia para um Data Lake na AWS. O processo é gerenciado pelo Apache Airflow e o código-fonte está disponível neste repositório do GitHub.

Esse projeto foi desenvolvido em conjunto com a mentora [Larissa Rocha](https://www.linkedin.com/in/larissa-m-h-rocha).

## Descrição do Projeto

### Funcionalidades Principais

- Coleta de dados de uma Dummy API.
- Processamento e tratamento dos dados.
- Envio dos dados processados para o Amazon S3 na AWS.
- Agendamento e monitoramento do fluxo de trabalho com o Apache Airflow.

### Estrutura do Projeto

O projeto está organizado da seguinte forma:


- `/dags`: Inclui os DAGs do Apache Airflow para a execução da pipeline de ETL.
   - `/Scripts`: Scripts de coleta, transformação e carga dos dados.
- `/data`: Dados resultantes da ETL
- `docker-compose.yaml`: Arquivo Docker Compose para configuração do ambiente.

## Como Usar

Siga as etapas abaixo para configurar e executar este projeto em seu ambiente:

1. **Clone o Repositório**

~~~bash
git clone git@github.com:nayyarabernardo/pipeline_ETL_airflow_dummy_API_AWS.git
cd pipeline_ETL_airflow_dummy_API_AWS
~~~


2. **Configure as Credenciais da AWS**

Certifique-se de ter as credenciais adequadas da AWS configuradas no ambiente.

3. **Configure as Variáveis de Ambiente**

Defina as variáveis de ambiente necessárias para o projeto, como as credenciais da API Dummy e as configurações do Amazon S3 da AWS.

4 **Execute o Apache Airflow**

Configure e inicie o Apache Airflow para agendar e monitorar a pipeline de ETL. Certifique-se de configurar os DAGs apropriados.

5. **Execute a Pipeline de ETL**

Execute a pipeline de ETL para coletar, transformar e enviar os dados para o Data Lake AWS.

6. **Monitore o Progresso**

Acompanhe o progresso da pipeline de ETL por meio do painel do Apache Airflow e verifique os logs para solucionar problemas, se necessário.

## Contribuições


Este projeto é aberto a contribuições. Se você deseja melhorar ou adicionar recursos, sinta-se à vontade para criar uma solicitação pull ou entrar em [contato](https://www.linkedin.com/in/nayyarabernardo).
## Licença

Este projeto é distribuído sob a licença MIT. Consulte o arquivo `LICENSE` para obter detalhes.

---


