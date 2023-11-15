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

#Funções de manipulação de dados
def insert_os(data):
    query = f"INSERT INTO Ordem_servico(cliente_id_os, logistica_cpf_os, produto_id_os, data_hora_consulta, data_hora_emissao) VALUES (%d, %s, %d, %s, %s)"
    cursor.execute(query, data)
    conn.commit()
    st.success(f'Ordem de serviço gerada.')

def select_os():
    query = "SELECT * FROM ordem_servico"
    cursor.execute(query)
    query_result = cursor.fetchall()
    return query_result

def filter_os():
    query = f"SELECT calcular_creditos({data});"
    cursor.execute(query)
    query_result = cursor.fetchall()
    return query_result

#Interface
st.title("Gráfica e Editora Brascolor")
operation = st.sidebar.selectbox("Selecione o que deseja fazer", ("Gerar Ordem de Serviço", "Registrar Consulta", "Ver Consulta", "Atualizar Ordem de Serviço", "Visualizar Ordem de Serviço"))
if operation == "Gerar Ordem de Serviço":
    cliente = st.number_input("Registro do cliente", value=1, format="%d")
    cpf = st.text_input("CPF de quem gerou")
    produto = st.number_input("Registro do Produto", value=1, format="%d")
    data_consulta = st.date_input("Data da consulta")
    data_emissao = st.date_input("Data da emissão")
    if st.button("Gerar"):
        insert_os((cliente, cpf, produto, data_consulta, data_emissao))
if operation == "Ver Consulta":
    op_filter = st.sidebar.selectbox("Filtrar por", ("Cliente", "Data de Consulta"))
    if op_filter == "Cliente":
        data = select_os()
        st.write("Consultas:")
        df = pd.DataFrame(data, columns=["ID", "Cliente", "CPF de quem gerou", "Data da consulta"])
        st.dataframe(df.set_index('ID'), width=800)
    if op_filter == "Data de Consulta":
        data = select_os()
        st.write("Consultas:")
        df = pd.DataFrame(data, columns=["ID", "Cliente", "CPF de quem gerou", "Data da consulta"])
        st.dataframe(df.set_index('ID'), width=800)
if operation == "Visualizar Ordem de Serviço":
    op_filter = st.sidebar.selectbox("Filtrar por", ("Ordem de Serviço", "Cliente", "Produto", "Data de Emissão", "Data de Consulta"))
    if op_filter == "Ordem de Serviço":
        data = select_os()
        st.write("Ordens de Serviço:")
        df = pd.DataFrame(data, columns=["ID", "Cliente", "CPF de quem gerou", "Produto", "Data da consulta", "Data da emissão"])
        st.dataframe(df.set_index('ID'), width=800)
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