import streamlit as st
import pandas as pd
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="", #insira sua senha
    database="brascolor"
)

cursor = conn.cursor()

#Funções de manipulação de dados (backend)
def insert_os(data):
    query = f"INSERT INTO Ordem_servico(cliente_id_os, logistica_cpf_os, produto_id_os, data_hora_consulta, data_hora_emissao) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(query, data)
    conn.commit()
    st.success(f'Ordem de serviço gerada.')

def select_os():
    query = "SELECT * FROM ordem_servico"
    cursor.execute(query)
    query_result = cursor.fetchall()
    return query_result

def select_os_id(data):
    query = f"SELECT * FROM ordem_servico WHERE id = {data}"
    cursor.execute(query)
    query_result = cursor.fetchall()
    return query_result

def select_os_cli(data):
    query = f"SELECT * FROM ordem_servico WHERE cliente_id_os = {data}"
    cursor.execute(query)
    query_result = cursor.fetchall()
    return query_result

def select_os_prod(data):
    query = f"SELECT * FROM ordem_servico WHERE produto_id_os = {data}"
    cursor.execute(query)
    query_result = cursor.fetchall()
    return query_result

def select_os_dt_emissao(data):
    query = f"SELECT * FROM ordem_servico WHERE data_hora_emissao = {data}"
    cursor.execute(query)
    query_result = cursor.fetchall()
    return query_result

def select_os_dt_consulta(data):
    query = f"SELECT * FROM ordem_servico WHERE data_hora_consulta = {data}"
    cursor.execute(query)
    query_result = cursor.fetchall()
    return query_result

def filter_os():
    query = f"SELECT calcular_creditos({data});"
    cursor.execute(query)
    query_result = cursor.fetchall()
    return query_result

def delete_eq(data):
    query = f"DELETE FROM equipamento WHERE id = {data}"
    cursor.execute(query)
    conn.commit()
    st.success(f'Ordem de serviço apagada.')

#Interface
st.title("Gráfica e Editora Brascolor")
operation = st.sidebar.selectbox("Selecione o que deseja fazer", ("Gerar Ordem de Serviço", "Visualizar Ordem(ns) de Serviço", "Apagar Ordem(ns) de Serviço", "Atualizar Ordem(ns) de Serviço"))
if operation == "Gerar Ordem de Serviço":
    cliente = st.number_input("Registro do cliente", value=1, format="%d")
    cpf = st.text_input("CPF de quem gerou")
    produto = st.number_input("Registro do Produto", value=1, format="%d")
    qtd_produto = st.number_input("Quantidade de produtos", value=1, format="%d")
    data_consulta = st.text_input("Data da consulta")
    data_emissao = st.text_input("Data da emissão")
    if st.button("Gerar"):
        insert_os((cliente, cpf, produto, qtd_produto, data_consulta, data_emissao))


if operation == "Visualizar Ordem(ns) de Serviço":
    op_filter = st.sidebar.selectbox("Filtrar por", ("Ver todos", "Cliente", "Produto", "Data de Emissão", "Data de Consulta"))
    if op_filter == "Ver todos":
        data = select_os()
        st.write("Ordens de Serviço:")
        df = pd.DataFrame(data, columns=["ID", "Cliente", "CPF de quem gerou", "Produto", "Quantidade dos produtos", "Data da consulta", "Data da emissão"])
        st.dataframe(df.set_index('ID'), width=800)
    elif op_filter == "ID da Ordem de Serviço":
        id_os = st.number_input("ID da Ordem de Serviço", value=1, format="%d")
        data = select_os_id(id_os)
        st.write("Ordens de Serviço:")
        df = pd.DataFrame(data, columns=["ID", "Cliente", "CPF de quem gerou", "Produto", "Quantidade dos produtos", "Data da consulta", "Data da emissão"])
        st.dataframe(df.set_index('ID'), width=800)
    elif op_filter == "Cliente":
        client = st.number_input("ID do cliente", value=1, format="%d")
        data = select_os_cli(client)
        st.write("Ordens de Serviço:")
        df = pd.DataFrame(data, columns=["ID", "Cliente", "CPF de quem gerou", "Produto", "Quantidade dos produtos", "Data da consulta", "Data da emissão"])
        st.dataframe(df.set_index('ID'), width=800)
    elif op_filter == "Produto":
        product = st.number_input("ID do produto", value=1, format="%d")
        data = select_os_prod(product)
        st.write("Ordens de Serviço:")
        df = pd.DataFrame(data, columns=["ID", "Cliente", "CPF de quem gerou", "Produto", "Quantidade dos produtos", "Data da consulta", "Data da emissão"])
        st.dataframe(df.set_index('ID'), width=800)
    elif op_filter == "Data de Emissão":
        em_dt = st.text_input("Data de emissão")
        data = select_os_dt_emissao(em_dt)
        st.write("Ordens de Serviço:")
        df = pd.DataFrame(data, columns=["ID", "Cliente", "CPF de quem gerou", "Produto", "Quantidade dos produtos", "Data da consulta", "Data da emissão"])
        st.dataframe(df.set_index('ID'), width=800)
    elif op_filter == "Data de Consulta":
        cons_dt = st.text_input("Data de consulta")
        data = select_os_dt_consulta(cons_dt)
        st.write("Ordens de Serviço:")
        df = pd.DataFrame(data, columns=["ID", "Cliente", "CPF de quem gerou", "Produto", "Quantidade dos produtos", "Data da consulta", "Data da emissão"])
        st.dataframe(df.set_index('ID'), width=800)


if operation == "Apagar Ordem de Serviço":
    if st.button("Apagar"):
        delete_eq()


if operation == "Atualizar Ordem de Serviço":
    cliente = st.number_input("Registro do cliente", value=1, format="%d")
    cpf = st.text_input("CPF de quem gerou")
    produto = st.number_input("Registro do Produto", value=1, format="%d")
    data_consulta = st.date_input("Data da consulta")
    data_emissao = st.date_input("Data da emissão")
    if st.button("Atualizar"):
        update_os(id, cliente, cpf, produto, data_consulta, data_emissao)
# table = st.sidebar.selectbox("Selecione a tabela", ("Ordem de Serviço", "Cliente", "pessoa", "professor", "disciplina", "turma", "ministra", "aluno", "aluno_turma", "prova", "monitoria", "busca - créditos totais"))

#Operações

    # if table == 'busca - créditos totais':
    #     matricula_aluno = st.number_input("Matrícula do aluno", min_value=1010)
    #     if st.button("Buscar"):
    #         result = select_data(matricula_aluno)
    #         st.write(f"Total de créditos do aluno: {result}")

cursor.close()
conn.close()

# if __name__ == '__main__':
#     app()