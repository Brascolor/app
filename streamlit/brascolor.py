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
    query = f"INSERT INTO Ordem_servico(cliente_id_os, logistica_cpf_os, produto_id_os, data_hora_consulta, data_hora_emissao) VALUES (%s, %s, %s, %s, %s, %s);"
    cursor.execute(query, data)
    conn.commit()
    st.success(f'Ordem de serviço gerada.')

def insert_prod(data):
    query = f"INSERT INTO Produto(descricao, tipo_codigo_prod) values(%s, (SELECT codigo FROM Tipo WHERE nome = %s));"
    cursor.execute(query, data)
    conn.commit()
    st.success(f'Produto adicionado.')

def insert_tem(data):
    query = f"INSERT INTO tem values((SELECT id FROM Equipamento WHERE nome = %s), %s);"
    cursor.execute(query, data)
    conn.commit()
    st.success(f'Equipamento adicionado à ordem de serviço.')

def insert_contem(data):
    query = f"INSERT INTO contem values(%s, %s, %s);"
    cursor.execute(query, data)
    conn.commit()
    st.success(f'Material adicionado à ordem de serviço.')

def select_os():
    query = "SELECT OS.id, C.nome AS nome_cliente, f.nome, os.produto_id_os, os.qtd_produto, os.data_hora_consulta, os.data_hora_emissao FROM Ordem_servico OS JOIN Cliente C ON OS.cliente_id_os = C.id join funcionario f on os.logistica_cpf_os = f.cpf;"
    cursor.execute(query)
    query_result = cursor.fetchall()
    return query_result

def select_os_id(data):
    query = f"SELECT OS.id, C.nome AS nome_cliente, f.nome, os.produto_id_os, os.qtd_produto, os.data_hora_consulta, os.data_hora_emissao FROM Ordem_servico OS JOIN Cliente C ON OS.cliente_id_os = C.id join funcionario f on os.logistica_cpf_os = f.cpf WHERE os.id = {data};"
    cursor.execute(query)
    query_result = cursor.fetchall()
    return query_result

def select_os_cli(data):
    query = f"SELECT OS.id, C.nome AS nome_cliente, f.nome, os.produto_id_os, os.qtd_produto, os.data_hora_consulta, os.data_hora_emissao FROM Ordem_servico OS JOIN Cliente C ON OS.cliente_id_os = C.id join funcionario f on os.logistica_cpf_os = f.cpf WHERE C.nome LIKE '%{data}%';"
    cursor.execute(query)
    query_result = cursor.fetchall()
    return query_result

def select_os_prod(data):
    query = f"SELECT OS.id, C.nome AS nome_cliente, f.nome, os.produto_id_os, os.qtd_produto, os.data_hora_consulta, os.data_hora_emissao FROM Ordem_servico OS JOIN Cliente C ON OS.cliente_id_os = C.id join funcionario f on os.logistica_cpf_os = f.cpf WHERE produto_id_os IN (SELECT id FROM Produto p Where p.descricao LIKE '%{data}%');"
    cursor.execute(query)
    query_result = cursor.fetchall()
    return query_result

def select_mat():
    query = "SELECT * FROM material;"
    cursor.execute(query)
    query_result = cursor.fetchall()
    return query_result

def select_mat_id(data):
    query = f"SELECT * FROM material WHERE id = {data};"
    cursor.execute(query)
    query_result = cursor.fetchall()
    return query_result

def select_mat_nome(data):
    query = f"SELECT * FROM material WHERE nome LIKE '%{data}%';"
    cursor.execute(query)
    query_result = cursor.fetchall()
    return query_result

def select_mat_os(data):
    query = f"SELECT material_id_cont, qtd_material FROM contem WHERE os_id_cont = {data};"
    cursor.execute(query)
    query_result = cursor.fetchall()
    return query_result

def select_eq():
    query = "SELECT * FROM equipamento;"
    cursor.execute(query)
    query_result = cursor.fetchall()
    return query_result

def select_eq_id(data):
    query = f"SELECT * FROM equipamento WHERE id = {data};"
    cursor.execute(query)
    query_result = cursor.fetchall()
    return query_result

def select_eq_nome(data):
    query = f"SELECT * FROM equipamento WHERE nome = '{data}';"
    cursor.execute(query)
    query_result = cursor.fetchall()
    return query_result

def select_eq_os(data):
    query = f"SELECT * FROM Equipamento WHERE id IN (SELECT equipamento_id_tem FROM tem WHERE os_id_tem = {data});"
    cursor.execute(query)
    query_result = cursor.fetchall()
    return query_result

def delete_eq(data):
    query = f"DELETE FROM ordem_servico WHERE id = %s;"
    cursor.execute(query, (data,))
    conn.commit()
    st.success(f'Ordem de serviço apagada.')

def update_material(qty, name):
    query = f"UPDATE material SET quantidade = {qty} WHERE nome = '{name}';"
    cursor.execute(query)
    conn.commit()
    st.success(f'Material atualizado.')

#Interface
st.title("Gráfica e Editora Brascolor")
operation = st.sidebar.selectbox("Selecione o que deseja fazer", ("Gerar Ordem de Serviço", "Adicionar Novo Produto", "Adicionar Material(is) à Ordem de Serviço", "Adicionar Equipamento(s) à Ordem de Serviço", "Visualizar Ordem(ns) de Serviço", "Visualizar Material(is)", "Visualizar Equipamento(s)", "Apagar Ordem(ns) de Serviço", "Atualizar Material(is)"))
if operation == "Gerar Ordem de Serviço":
    st.subheader("Gerar Ordem de Serviço")
    cliente = st.number_input("Registro do cliente", value=1, format="%d")
    cpf = st.text_input("CPF de quem gerou")
    produto = st.number_input("Registro do Produto", value=1, format="%d")
    qtd_produto = st.number_input("Quantidade de produtos", value=1, format="%d")
    data_consulta = st.text_input("Data da consulta")
    data_emissao = st.text_input("Data da emissão")
    if st.button("Gerar"):
        insert_os((cliente, cpf, produto, qtd_produto, data_consulta, data_emissao))

if operation == "Adicionar Novo Produto":
    st.subheader("Adicionar Novo Produto")
    desc = st.text_input("Descrição do Produto")
    tipo = st.text_input("Tipo do produto")
    if st.button("Adicionar"):
        print(desc, tipo)
        insert_prod((desc, tipo))

if operation == "Adicionar Material(is) à Ordem de Serviço":
    st.subheader("Adicionar Material(is) à Ordem de Serviço")
    id_mat = st.number_input("ID do Material", value=1, format="%d")
    id_os = st.number_input("ID da Ordem de Serviço", value=1, format="%d")
    qty_mat = st.number_input("Quantidade do Material", value=1, format="%d")
    if st.button("Adicionar"):
        insert_contem((id_mat, id_os, qty_mat))

if operation == "Adicionar Equipamento(s) à Ordem de Serviço":
    st.subheader("Adicionar Equipamento(s) à Ordem de Serviço")
    id_os = st.number_input("ID da Ordem de Serviço", value=1, format="%d")
    nome_eq = st.text_input("Nome do Equipamento")
    if st.button("Adicionar"):
        insert_tem((nome_eq, id_os))

if operation == "Visualizar Material(is)":
    st.subheader("Visualizar Materiais")
    op_filter = st.sidebar.selectbox("Filtrar por", ("Ver todos", "ID do Material", "Nome", "Ordem de Serviço"))
    if op_filter == "Ver todos":
        data = select_mat()
        st.write("Materiais:")
        df = pd.DataFrame(data, columns=["ID", "Nome", "Quantidade no Estoque"])
        st.dataframe(df.set_index('ID'), width=800)
    elif op_filter == "ID do Material":
        id_mat = st.number_input("ID do Material", value=1, format="%d")
        data = select_mat_id(id_mat)
        st.write("Materiais:")
        df = pd.DataFrame(data, columns=["ID", "Nome", "Quantidade no Estoque"])
        st.dataframe(df.set_index('ID'), width=800)
    elif op_filter == "Nome":
        desc = st.text_input("Nome do Material")
        data = select_mat_nome(desc)
        st.write("Materiais:")
        df = pd.DataFrame(data, columns=["ID", "Nome", "Quantidade no Estoque"])
        st.dataframe(df.set_index('ID'), width=800)
    elif op_filter == "Ordem de Serviço":
        id_os = st.number_input("ID da Ordem de Serviço", value=1, format="%d")
        data = select_mat_os(id_os)
        st.write("Materiais:")
        df = pd.DataFrame(data, columns=["ID", "Quantidade"])
        st.dataframe(df.set_index('ID'), width=1000)

if operation == "Visualizar Equipamento(s)":
    st.subheader("Visualizar Equipamento(s)")
    op_filter = st.sidebar.selectbox("Filtrar por", ("Ver todos", "ID do Equipamento", "Nome", "Ordem de Serviço"))
    if op_filter == "Ver todos":
        data = select_eq()
        st.write("Equipamentos:")
        df = pd.DataFrame(data, columns=["ID", "Nome", "Descrição"])
        st.dataframe(df.set_index('ID'), width=800)
    if op_filter == "ID do Equipamento":
        id_eq = st.number_input("ID do Equipamento", value=1, format="%d")
        data = select_eq_id(id_eq)
        st.write("Equipamentos:")
        df = pd.DataFrame(data, columns=["ID", "Nome", "Descrição"])
        st.dataframe(df.set_index('ID'), width=800)
    if op_filter == "Nome":
        nome = st.text_input("Nome do Equipamento")
        data = select_eq_nome(nome)
        st.write("Equipamentos:")
        df = pd.DataFrame(data, columns=["ID", "Nome", "Descrição"])
        st.dataframe(df.set_index('ID'), width=800)
    if op_filter == "Ordem de Serviço":
        id_os = st.number_input("ID da Ordem de Serviço", value=1, format="%d")
        data = select_eq_os(id_os)
        st.write("Equipamentos:")
        df = pd.DataFrame(data, columns=["ID", "Nome", "Descricao"])
        st.dataframe(df.set_index('ID'), width=800)

if operation == "Visualizar Ordem(ns) de Serviço":
    st.subheader("Visualizar Ordem(ns) de Serviço")
    op_filter = st.sidebar.selectbox("Filtrar por", ("Ver todos", "ID da Ordem de Serviço","Cliente", "Produto"))
    if op_filter == "Ver todos":
        data = select_os()
        st.write("Ordens de Serviço:")
        df = pd.DataFrame(data, columns=["ID", "Cliente", "Funcionário Emissor", "Produto", "Quantidade dos produtos", "Data da consulta", "Data da emissão"])
        st.dataframe(df.set_index('ID'), width=800)
    elif op_filter == "ID da Ordem de Serviço":
        id_os = st.number_input("ID da Ordem de Serviço", value=1, format="%d")
        data = select_os_id(id_os)
        st.write("Ordens de Serviço:")
        df = pd.DataFrame(data, columns=["ID", "Cliente", "Funcionário Emissor", "Produto", "Quantidade dos produtos", "Data da consulta", "Data da emissão"])
        st.dataframe(df.set_index('ID'), width=800)
    elif op_filter == "Cliente":
        client = st.text_input("Nome do cliente")
        data = select_os_cli(client)
        st.write("Ordens de Serviço:")
        df = pd.DataFrame(data, columns=["ID", "Cliente", "Funcionário Emissor", "Produto", "Quantidade dos produtos", "Data da consulta", "Data da emissão"])
        st.dataframe(df.set_index('ID'), width=800)
    elif op_filter == "Produto":
        product = st.text_input("Descrição do produto")
        data = select_os_prod(product)
        st.write("Ordens de Serviço:")
        df = pd.DataFrame(data, columns=["ID", "Cliente", "Funcionário Emissor", "Produto", "Quantidade dos produtos", "Data da consulta", "Data da emissão"])
        st.dataframe(df.set_index('ID'), width=800)


if operation == "Apagar Ordem(ns) de Serviço":
    st.subheader("Apagar Ordem de Serviço")
    id_os = st.number_input("ID da Ordem de Serviço que deseja apagar", value=1, format="%d")
    if st.button("Apagar"):
        delete_eq(id_os)


if operation == "Atualizar Material(is)":
    st.subheader("Atualizar Material(is)")
    qty = st.number_input("Nova quantidade de material no estoque", value=1, format="%d")
    name = st.text_input("Nome do material que deseja substituir a quantidade")
    if st.button("Atualizar"):
        update_material(qty, name)

cursor.close()
conn.close()

# if __name__ == '__main__':
#     app()