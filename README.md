# Armazenando dados de um E-Commerce na Cloud

O projeto propõe criar um banco de dados na nuvem que armazene dados de produtos, sendo possível inserir produtos com descrição, preço e imagem assim como listar todos os produtos cadastrados via browser, utilizando a biblioteca streamlit do Python.
        
Além do código, foi ensinado como criar e configurar um ambiente que permite a consulta e o acesso a um banco de dados, usando Resource Group, SQL Database e Storage Account, assim como definir as autorizações de acesso ao banco de dados.

Os dados do arquivo .env, necessários para a conexão com o banco de dados, são obtidos através dos serviços da Azure

Bibliotecas requeridas:

- streamlit (para exibir a interface web)
- azure-storage-blob (para interagir com o armazenamento de blobs da Azure)
- pymssql (para interagir com o banco de dados)
- dotenv (para que o programa principal possa ler o arquivo .env e carregar suas configurações).

Interface gráfica final:

![Alt text](interface_gráfica.png?raw=true "Interface Gráfica")

