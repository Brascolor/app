import streamlit as st
from streamlit import session_state
import pandas as pd
import mysql.connector

if 'login' not in session_state:
    session_state.login = False

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="", #insira sua senha
    database="brascolor"
)

cursor = conn.cursor()

#Funções de manipulação de dados (backend)
def login_logic(username):
    query = f"SELECT * FROM funcionario WHERE cpf='{username}';"
    cursor.execute(query)
    record = cursor.fetchone()
    if record:
        session_state.login = True
        session_state.username = username
    else:
        st.warning("Incorrect username or password")

def insert_os(data):
    query = f"INSERT INTO Ordem_servico(cliente_id_os, logistica_cpf_os, produto_id_os, qtd_produto, data_hora_consulta, data_hora_emissao) VALUES (%s, %s, %s, %s, %s, %s);"
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

def insert_add(data):
    query = f"INSERT INTO endereco values(%s, %s, %s, %s, %s, %s);"
    cursor.execute(query, data)
    conn.commit()
    st.success(f'Endereço adicionado à ordem de serviço.')

def select_os():
    query = "SELECT OS.id, C.nome AS nome_cliente, f.nome, os.produto_id_os, os.qtd_produto, os.data_hora_consulta, os.data_hora_emissao FROM Ordem_servico OS JOIN Cliente C ON OS.cliente_id_os = C.id join funcionario f on os.logistica_cpf_os = f.cpf order by id asc;"
    cursor.execute(query)
    query_result = cursor.fetchall()
    return query_result

def select_os_id(data):
    query = f"SELECT OS.id, C.nome AS nome_cliente, f.nome, os.produto_id_os, os.qtd_produto, os.data_hora_consulta, os.data_hora_emissao FROM Ordem_servico OS JOIN Cliente C ON OS.cliente_id_os = C.id join funcionario f on os.logistica_cpf_os = f.cpf WHERE os.id = {data};"
    cursor.execute(query)
    query_result = cursor.fetchall()
    return query_result

def select_os_cli(data):
    query = f"SELECT OS.id, C.nome AS nome_cliente, f.nome, os.produto_id_os, os.qtd_produto, os.data_hora_consulta, os.data_hora_emissao FROM Ordem_servico OS JOIN Cliente C ON OS.cliente_id_os = C.id join funcionario f on os.logistica_cpf_os = f.cpf WHERE C.nome LIKE '%{data}%' order by id asc;"
    cursor.execute(query)
    query_result = cursor.fetchall()
    return query_result

def select_os_prod(data):
    query = f"SELECT OS.id, C.nome AS nome_cliente, f.nome, os.produto_id_os, os.qtd_produto, os.data_hora_consulta, os.data_hora_emissao FROM Ordem_servico OS JOIN Cliente C ON OS.cliente_id_os = C.id join funcionario f on os.logistica_cpf_os = f.cpf WHERE produto_id_os IN (SELECT id FROM Produto p Where p.descricao LIKE '%{data}%') order by id asc;"
    cursor.execute(query)
    query_result = cursor.fetchall()
    return query_result

def select_prod():
    query = "SELECT * FROM produto order by id asc;"
    cursor.execute(query)
    query_result = cursor.fetchall()
    return query_result

def select_prod_id(data):
    query = f"SELECT * FROM produto WHERE id = {data};"
    cursor.execute(query)
    query_result = cursor.fetchall()
    return query_result

def select_prod_desc(data):
    query = f"SELECT * FROM produto WHERE descricao LIKE '%{data}%' order by id asc;"
    cursor.execute(query)
    query_result = cursor.fetchall()
    return query_result

def select_prod_tipo(data):
    query = f"SELECT * FROM produto WHERE tipo_codigo_prod = (SELECT codigo FROM tipo WHERE nome = '{data}') order by id asc;"
    cursor.execute(query)
    query_result = cursor.fetchall()
    return query_result

def select_mat():
    query = "SELECT * FROM material order by id asc;"
    cursor.execute(query)
    query_result = cursor.fetchall()
    return query_result

def select_mat_id(data):
    query = f"SELECT * FROM material WHERE id = {data};"
    cursor.execute(query)
    query_result = cursor.fetchall()
    return query_result

def select_mat_nome(data):
    query = f"SELECT * FROM material WHERE nome LIKE '%{data}%' order by id asc;"
    cursor.execute(query)
    query_result = cursor.fetchall()
    return query_result

def select_mat_os(data):
    query = f"SELECT material_id_cont, qtd_material FROM contem WHERE os_id_cont = {data} order by id asc;"
    cursor.execute(query)
    query_result = cursor.fetchall()
    return query_result

def select_eq():
    query = "SELECT * FROM equipamento order by id asc;"
    cursor.execute(query)
    query_result = cursor.fetchall()
    return query_result

def select_eq_id(data):
    query = f"SELECT * FROM equipamento WHERE id = {data};"
    cursor.execute(query)
    query_result = cursor.fetchall()
    return query_result

def select_eq_nome(data):
    query = f"SELECT * FROM equipamento WHERE nome = '{data}' order by id asc;"
    cursor.execute(query)
    query_result = cursor.fetchall()
    return query_result

def select_eq_os(data):
    query = f"SELECT * FROM Equipamento WHERE id IN (SELECT equipamento_id_tem FROM tem WHERE os_id_tem = {data}) order by id asc;"
    cursor.execute(query)
    query_result = cursor.fetchall()
    return query_result

def select_end():
    query = "SELECT * FROM endereco order by id asc;"
    cursor.execute(query)
    query_result = cursor.fetchall()
    return query_result

def select_end_id(data):
    query = f"SELECT * FROM endereco WHERE os_id_end = {data};"
    cursor.execute(query)
    query_result = cursor.fetchall()
    return query_result

def select_end_cidade(data):
    query = f"SELECT * FROM endereco WHERE cidade LIKE '%{data}%' order by id asc;"
    cursor.execute(query)
    query_result = cursor.fetchall()
    return query_result

def select_end_estado(data):
    query = f"SELECT * FROM endereco WHERE estado = '{data}' order by id asc;"
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

def mes_mais_os():
    query = "SELECT Ano, Mes, TotalOrdens FROM (SELECT YEAR(data_hora_emissao) AS Ano, MONTH(data_hora_emissao) AS Mes, COUNT(*) AS TotalOrdens FROM Ordem_servico GROUP BY YEAR(data_hora_emissao), MONTH(data_hora_emissao)) AS MesesOrdens WHERE TotalOrdens = (SELECT MAX(TotalOrdens) FROM (SELECT COUNT(*) AS TotalOrdens FROM Ordem_servico GROUP BY YEAR(data_hora_emissao), MONTH(data_hora_emissao)) AS MaxOrdens);"
    cursor.execute(query)
    query_result = cursor.fetchall()
    return query_result

def os_mais_produtos():
    query = "SELECT * FROM Ordem_servico WHERE qtd_produto = (SELECT MAX(qtd_produto) FROM Ordem_servico);"
    cursor.execute(query)
    query_result = cursor.fetchall()
    return query_result

#Interface
st.title("Gráfica e Editora Brascolor")
if session_state.login == False:
    with st.sidebar:
        username = st.text_input("Digite seu CPF")

        if st.button("Login"):
            login_logic(username)
else:
    operation = st.sidebar.selectbox("Selecione o que deseja fazer", ("Gerar Ordem de Serviço", "Adicionar Novo Produto", "Adicionar Material(is) à Ordem de Serviço", "Adicionar Equipamento(s) à Ordem de Serviço", "Adicionar Endereço(s) à Ordem de Serviço", "Visualizar Ordem(ns) de Serviço", "Visualizar Produto(s)", "Visualizar Material(is)", "Visualizar Equipamento(s)", "Visualizar Endereço(s)", "Apagar Ordem(ns) de Serviço", "Atualizar Material(is)", "Visualizar Relatórios"))
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

    if operation == "Adicionar Endereço(s) à Ordem de Serviço":
        st.subheader("Adicionar Endereço(s) à Ordem de Serviço")
        id_os = st.number_input("ID da Ordem de Serviço", value=1, format="%d")
        cidade = st.text_input("Cidade")
        numero = st.number_input("Número", value=1, format="%d")
        rua = st.text_input("Rua")
        estado = st.text_input("Estado")
        bairro = st.text_input("Bairro")
        if st.button("Adicionar"):
            insert_add((id_os, cidade, numero, rua, estado, bairro))

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

    if operation == "Visualizar Produto(s)":
        st.subheader("Visualizar Produto(s)")
        op_filter = st.sidebar.selectbox("Filtrar por", ("Ver todos", "ID do Produto", "Descrição", "Tipo"))
        if op_filter == "Ver todos":
            data = select_prod()
            st.write("Produtos:")
            df = pd.DataFrame(data, columns=["ID", "Descrição", "Tipo"])
            st.dataframe(df.set_index('ID'), width=800)
        elif op_filter == "ID do Produto":
            id_prod = st.number_input("ID do Produto", value=1, format="%d")
            data = select_prod_id(id_prod)
            st.write("Produtos:")
            df = pd.DataFrame(data, columns=["ID", "Descrição", "Tipo"])
            st.dataframe(df.set_index('ID'), width=800)
        elif op_filter == "Descrição":
            desc = st.text_input("Descrição do Produto")
            data = select_prod_desc(desc)
            st.write("Produtos:")
            df = pd.DataFrame(data, columns=["ID", "Descrição", "Tipo"])
            st.dataframe(df.set_index('ID'), width=800)
        elif op_filter == "Tipo":
            tipo = st.text_input("Tipo do Produto")
            data = select_prod_tipo(tipo)
            st.write("Produtos:")
            df = pd.DataFrame(data, columns=["ID", "Descrição", "Tipo"])
            st.dataframe(df.set_index('ID'), width=800)

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

    if operation == "Visualizar Endereço(s)":
        st.subheader("Visualizar Endereço(s)")
        op_filter = st.sidebar.selectbox("Filtrar por", ("Ver todos", "ID da Ordem de Serviço", "Cidade", "Estado"))
        if op_filter == "Ver todos":
            data = select_end()
            st.write("Endereços:")
            df = pd.DataFrame(data, columns=["ID", "Cidade", "Número", "Rua", "Estado", "Bairro"])
            st.dataframe(df.set_index('ID'), width=800)
        elif op_filter == "ID da Ordem de Serviço":
            id_os = st.number_input("ID da Ordem de Serviço", value=1, format="%d")
            data = select_end_id(id_os)
            st.write("Endereços:")
            df = pd.DataFrame(data, columns=["ID", "Cidade", "Número", "Rua", "Estado", "Bairro"])
            st.dataframe(df.set_index('ID'), width=800)
        elif op_filter == "Cidade":
            cidade = st.text_input("Cidade")
            data = select_end_cidade(cidade)
            st.write("Endereços:")
            df = pd.DataFrame(data, columns=["ID", "Cidade", "Número", "Rua", "Estado", "Bairro"])
            st.dataframe(df.set_index('ID'), width=800)
        elif op_filter == "Estado":
            estado = st.text_input("Estado")
            data = select_end_estado(estado)
            st.write("Endereços:")
            df = pd.DataFrame(data, columns=["ID", "Cidade", "Número", "Rua", "Estado", "Bairro"])
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
        
    if operation == "Visualizar Relatórios":
        st.subheader("Visualizar Relatórios")
        op_filter = st.sidebar.selectbox("Tipo", ("Mês com mais Ordens de Serviço", "Ordem(ns) de Serviço com maior quantidade de produtos"))
        if op_filter == "Mês com mais Ordens de Serviço":
            data = mes_mais_os()
            st.write("Ano, Mês e Total de Ordens de Serviço:")
            df = pd.DataFrame(data, columns=["Ano", "Mês", "Ordens de Serviço"])
            st.dataframe(df.set_index('Mês'), width=800)
        elif op_filter == "Ordem(ns) de Serviço com maior quantidade de produtos":
            data = os_mais_produtos()
            st.write("Ordens de Serviço com maior quantidade de produtos:")
            df = pd.DataFrame(data, columns=["ID", "Cliente", "Funcionário Emissor", "Produto", "Quantidade dos produtos", "Data da consulta", "Data da emissão"])
            st.dataframe(df.set_index('ID'), width=800)

cursor.close()
conn.close()

# if __name__ == '__main__':
#     app()