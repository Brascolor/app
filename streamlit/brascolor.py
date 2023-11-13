import streamlit as st
import pandas as pd
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="MaMaE!0!0", #inserir a senha!
    database="brascolor"
)

cursor = conn.cursor()

# Define CRUD functions
def insert_os(data):
    query = f"INSERT INTO Ordem_servico VALUES ({', '.join(['%s']*len(data))})"
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

# Define Streamlit app
#interface
st.title("Gráfica e Editora Brascolor")
operation = st.sidebar.selectbox("Selecione o que deseja fazer", ("Gerar Ordem de Serviço", "Apagar", "Atualizar Ordem de Serviço", "Visualizar Ordem de Serviço"))
table = st.sidebar.selectbox("Selecione a tabela", ("Ordem de Serviço", "Cliente", "pessoa", "professor", "disciplina", "turma", "ministra", "aluno", "aluno_turma", "prova", "monitoria", "busca - créditos totais"))

if operation == 'Visualizar Ordem de Serviço':
    if table == "Ordem de Serviço":
        data = select_os()
        st.write("Ordens de Serviço:")
        df = pd.DataFrame(data, columns=["ID", "Cliente", "CPF de quem gerou", "Produto", "Data da consulta", "Data da emissão"])
        st.dataframe(df.set_index('ID'), width=800)
    # if table == 'busca - créditos totais':
    #     matricula_aluno = st.number_input("Matrícula do aluno", min_value=1010)
    #     if st.button("Buscar"):
    #         result = select_data(matricula_aluno)
    #         st.write(f"Total de créditos do aluno: {result}")

cursor.close()
conn.close()

# if __name__ == '__main__':
#     app()