import streamlit as st
from azure.storage.blob import BlobServiceClient
import os
import pymssql 
import uuid
from dotenv import load_dotenv


load_dotenv()

#configurações do Azure storage do arquivo .env
BlobConnectionString = os.getenv("BLOB_CONNECTION_STRING")
blobContainerName = os.getenv("BLOB_CONTAINER_NAME")
blobAccountName = os.getenv("BLOB_ACCOUNT_NAME")

#configurações do Azure SQL server
SQL_SERVER = os.getenv("SQL_SERVER")
SQL_DATABASE = os.getenv("SQL_DATABASE")
SQL_USER = os.getenv("SQL_USER")
SQL_PASSWORD = os.getenv("SQL_PASSWORD")

#título da aplicação
st.title("Cadastro de produtos")


#formulário de cadastro de produtos
product_name = st.text_input("Nome do produto")
product_price = st.number_input("Preço do produto", min_value=0.0, format='%.2f')
product_description = st.text_area("Descrição do produto")
product_image = st.file_uploader("Imagem do produto", type=['jpg', 'png', 'jpeg'])


#função que envia imagem para o Azure Blob Storage e retorna a url da imagem 

def upload_blob(file):
    try:
        blob_service_client = BlobServiceClient.from_connection_string(BlobConnectionString)
        container_client = blob_service_client.get_container_client(blobContainerName)
        blob_name = str(uuid.uuid4()) + file.name 
        blob_client = container_client.get_blob_client(blob_name)
        blob_client.upload_blob(file.read(), overwrite=True) 
        image_url = f"https://{blobAccountName.strip()}.blob.core.windows.net/{blobContainerName}/{blob_name}"
        return image_url
    except Exception as e:
        st.error(f"Falha ao enviar a imagem")
        return None

#função que insere os dados do produto no Azure SQL server

def insert_product(product_name, product_price, product_description, product_image):
    try:
        if product_name=="" or product_description == "" or product_price is None or product_image is None:
            st.warning("Preencha os campos obrigatórios")
            return
        image_url = upload_blob(product_image)
        conn = pymssql.connect(server=SQL_SERVER, user=SQL_USER, password=SQL_PASSWORD, database=SQL_DATABASE)
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO Produtos (nome, descricao, preco, imagem_url) VALUES ('{product_name}', '{product_description}', '{product_price}', '{image_url}')")
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Erro ao inserir o produto: {e}")

#função que recupera a lista de produtos do Azure SQL server e os retorna em formato de lista de tuplas
def list_products():
    try:
        conn = pymssql.connect(server=SQL_SERVER, user=SQL_USER, password=SQL_PASSWORD, database=SQL_DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Produtos")
        rows = cursor.fetchall()
        conn.close()
        return rows
    except Exception as e:
        st.error(f"Erro ao listar produtos: {e}")
        return []

#função que lista na página os produtos organizados em linhas e colunas
def list_products_screen():
    products = list_products()
    if products:
        #define o número de cards por linha
        cards_por_linha = 3
        #Cria as colunas iniciais
        cols = st.columns(cards_por_linha)
        for i, product in enumerate(products):
            col = cols[i % cards_por_linha]
            with col:
                st.markdown(f"### {product[1]}")
                st.write(f"**Descrição:** {product[2]}")
                st.write(f"**Preço:** R$ {product[3]:.2f}")
                if product[4]:
                    html_img = f'<img src="{product[4]}" width="200" height="200" alt="imagem de produto">'
                    st.markdown(html_img, unsafe_allow_html=True)
                st.markdown("---")
            # A cada 'cards por linha' produtos, se ainda houver produtos, cria novas colunas   
            if (i + 1) % cards_por_linha == 0 and (i + 1) < len(products):
                cols = st.columns(cards_por_linha)
    else:
        st.info("Nenhum produto encontrado")


#Botão para cadastro do produto
if st.button("Salvar produto"):
    if insert_product(product_name, product_price, product_description, product_image):
        st.success("Produto salvo com sucesso")
        list_products_screen()
    else:
        st.error("Erro ao cadastrar produto")


st.header("Produtos cadastrados")

#Botão que lista os produtos cadastrados
if st.button("Listar produtos"):
    try:
        list_products_screen()
        st.success("Produtos listados com sucesso")
    except Exception as e:
        st.error("Falha em exibir os produtos")
