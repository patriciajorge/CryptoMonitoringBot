## CryptoMonitoringBot

É um bot Python projetado para monitorar criptomoedas e fornecer relatórios sobre suas variações de preços. O bot realiza consultas regulares a uma API de criptomoedas, analisa os dados recebidos e envia relatórios por e-mail. O processo é automatizado para execução a cada 10 minutos.

## Funcionalidades
- Consulta à API: Obtém dados atualizados sobre preços de criptomoedas de uma API externa.
- Análise de Dados: Processa e analisa os dados de preços das criptomoedas.
- Envio de Relatórios: Envia relatórios por e-mail com informações sobre as criptomoedas monitoradas e análises.
- Automatização: Executa o processo automaticamente a cada 10 minutos.

## Tecnologias Utilizadas

- Python: Linguagem de programação utilizada para desenvolver o bot.
- Requests: Biblioteca para fazer requisições HTTP à API de criptomoedas.
- Python-dotenv: Biblioteca para carregar variáveis de ambiente a partir de um arquivo .env.
- Schedule: Biblioteca para agendar a execução do bot a cada 10 minutos.
- Smtplib e Email: Bibliotecas para enviar e-mails com os relatórios gerados.

## Pré-requisitos

Antes de executar o projeto, certifique-se de que o Python 3.6 ou superior está instalado no seu sistema.

## Uso

- Instale as dependências:

bash
Copiar código
pip install -r requirements.txt

- Execute o bot:

bash
Copiar código
python app.py

- Automatização:

O bot está configurado para rodar a cada 10 minutos automaticamente. A lógica de agendamento está implementada usando a biblioteca schedule.