import streamlit as st
import pandas as pd
import mysql.connector

#rodar com:  streamlit run "C:\Users\marib\OneDrive\Área de Trabalho\farmacia\farmacia-bd/main.py"

#conexão com o banco
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="", #inserir a senha!
    database="universidade"
)

cursor = conn.cursor()

#insert
def insert_data(table, data):
    query = f"INSERT INTO {table} VALUES ({', '.join(['%s']*len(data))})"
    cursor.execute(query, data)
    conn.commit()
    st.success(f'Dados inseridos em {table}.')

#delete
def delete_data(table, condition_column, condition_value):
    query = f"DELETE FROM {table} WHERE {condition_column} = %s"
    cursor.execute(query, (condition_value,))
    conn.commit()
    st.success(f'Dados deletados de {table}.')

#update
def update_data(table, set_column, set_value, condition_column, condition_value):
    query = f"UPDATE {table} SET {set_column} = %s WHERE {condition_column} = %s"
    cursor.execute(query, (set_value, condition_value))
    conn.commit()
    st.success(f'Dados atualizados em {table}.')

#select
def select_data(table):
    query = f"SELECT * FROM {table}"           
    cursor.execute(query)
    data = cursor.fetchall()
    return data

# def select_data(data):
#     query = f"SELECT calcular_creditos({data});"
#     cursor.execute(query)
#     query_result = cursor.fetchone()
#     valor = query_result[0]
#     return valor

#interface
st.title("Aplicação de Gerenciamento de Dados")
operation = st.sidebar.selectbox("Selecione a operação", ("Inserir", "Deletar", "Atualizar", "Select"))
table = st.sidebar.selectbox("Selecione a tabela", ("curso", "projeto", "pessoa", "professor", "disciplina", "turma", "ministra", "aluno", "aluno_turma", "prova", "monitoria", "busca - créditos totais"))

if operation == "Inserir":
    if table == "curso":
        codigo_curso = st.number_input("Código do Curso", min_value=0)
        nome_curso = st.text_input("Nome do Curso")
        if st.button("Inserir"):
            insert_data(table, (codigo_curso, nome_curso))
elif operation == "Deletar":
    if table == "curso":
        codigo_curso = st.number_input("Código do Curso a ser deletado", min_value=0)
        if st.button("Deletar"):
            delete_data(table, "codigo_curso", codigo_curso)
elif operation == "Atualizar":
    if table == "curso":
        codigo_curso = st.number_input("Código do Curso a ser atualizado", min_value=0)
        novo_nome = st.text_input("Novo Nome do Curso")
        if st.button("Atualizar"):
            update_data(table, "nome", novo_nome, "codigo_curso", codigo_curso)
elif operation == 'Select':
    if table == "curso":
        data = select_data(table)
        st.write("Dados da tabela Curso:")
        df = pd.DataFrame(data, columns=["Código do Curso", "Nome do Curso"])
        st.dataframe(df.set_index('Código do Curso'), width=800)
    if table == 'aluno':
        data = select_data(table)
        st.write("Dados da tabela Aluno:")
        df = pd.DataFrame(data, columns=["Matrícula do aluno", "Nota do vestibular", "Codigo do curso"])
        st.dataframe(df.set_index('Matrícula do aluno'), width=800)
    if table == 'busca - créditos totais':
        matricula_aluno = st.number_input("Matrícula do aluno", min_value=1010)
        if st.button("Buscar"):
            result = select_data(matricula_aluno)
            st.write(f"Total de créditos do aluno: {result}")

cursor.close()
conn.close()