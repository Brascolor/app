CREATE DATABASE BRASCOLOR;
use brascolor;

CREATE TABLE Material(
id int AUTO_INCREMENT PRIMARY KEY,
nome varchar(50),
quantidade int
);

CREATE TABLE Tipo(
codigo smallint AUTO_INCREMENT PRIMARY KEY,
nome varchar(30)
);

CREATE TABLE Produto(
id int AUTO_INCREMENT PRIMARY KEY,
quantidade int,
descricao varchar(50),
tipo_codigo_prod smallint,
CONSTRAINT fk_Tipo_prod FOREIGN KEY (tipo_codigo_prod) REFERENCES Tipo (codigo)
);

CREATE TABLE Cliente (
id int AUTO_INCREMENT PRIMARY KEY,
nome varchar(50),
cidade varchar(30),
numero int,
rua varchar(50),
estado varchar(30),
bairro varchar(30)
)

CREATE TABLE Email_cliente (
cliente_id_em int PRIMARY KEY,
email varchar(50),
CONSTRAINT fk_Cliente_em FOREIGN KEY (cliente_id_em) REFERENCES Cliente(id)
);

CREATE TABLE Telefone_cliente (
cliente_id_tel int PRIMARY KEY,
telefone varchar(20),
CONSTRAINT fk_Cliente_tel FOREIGN KEY (cliente_id_tel) REFERENCES Cliente(id)
);

CREATE TABLE Veiculo (
placa varchar(10) PRIMARY KEY,
marca varchar(30),
modelo varchar(30),
ano int
);

CREATE TABLE entrega (
produto_id_ent int,
veiculo_placa_ent varchar(10),
cliente_id_ent int,
CONSTRAINT fk_Produto_ent FOREIGN KEY (produto_id_ent) REFERENCES Produto(id),
CONSTRAINT fk_Veiculo_ent FOREIGN KEY (veiculo_placa_ent) REFERENCES Veiculo(placa),
CONSTRAINT fk_Cliente_ent FOREIGN KEY (cliente_id_ent) REFERENCES Cliente(id)
);

CREATE TABLE Funcionario (
cpf varchar(15) PRIMARY KEY,
nome varchar (50),
data_nascimento date,
turno varchar(10),
carga_horaria int,
email_inst varchar(50) CHECK (email_inst LIKE '%@brascolor.com'),
gerente varchar(15),
CONSTRAINT fk_gerente_cpf FOREIGN KEY (gerente) REFERENCES Funcionario(cpf)
);

CREATE TABLE Email_funcionario (
funcionario_cpf_em varchar(15) PRIMARY KEY,
email varchar(50),
CONSTRAINT fk_Funcionario_em FOREIGN KEY (funcionario_cpf_em) REFERENCES Funcionario(cpf)
);

CREATE TABLE Celular_funcionario (
funcionario_cpf_cel varchar(15) PRIMARY KEY,
celular varchar(20),
CONSTRAINT fk_Funcionario_cel FOREIGN KEY (funcionario_cpf_cel) REFERENCES Funcionario(cpf)
);

CREATE TABLE Setor (
id smallint AUTO_INCREMENT PRIMARY KEY,
nome varchar(30),
descricao varchar(100)
);

CREATE TABLE Logistica (
funcionario_cpf_log varchar(15),
setor_id_log smallint,
CONSTRAINT fk_Funcionario_log FOREIGN KEY (funcionario_cpf_log) REFERENCES Funcionario(cpf),
CONSTRAINT fk_Setor_log FOREIGN KEY (setor_id_log) REFERENCES Setor(id)
);

CREATE TABLE Equipamento (
id int AUTO_INCREMENT PRIMARY KEY,
nome varchar(50),
descricao varchar(100)
);

CREATE TABLE Operador (
funcionario_cpf_op varchar(15),
equipamento_id_op int,
CONSTRAINT fk_Funcionario_op FOREIGN KEY (funcionario_cpf_op) REFERENCES Funcionario(cpf),
CONSTRAINT fk_Equipamento_op FOREIGN KEY (equipamento_id_op) REFERENCES Equipamento(id)
);

CREATE TABLE Ordem_servico (
id int AUTO_INCREMENT PRIMARY KEY,
cliente_id_os int,
logistica_cpf_os varchar(15),
produto_id_os int,
data_hora_consulta datetime,
data_hora_emissao datetime,
CONSTRAINT fk_Cliente_os FOREIGN KEY (cliente_id_os) REFERENCES Cliente(id),
CONSTRAINT fk_Logistica_os FOREIGN KEY (logistica_cpf_os) REFERENCES Logistica(funcionario_cpf_log),
CONSTRAINT fk_Produto_os FOREIGN KEY (produto_id_os) REFERENCES Produto (id)
);

CREATE TABLE Endereco (
os_id_end int,
cidade varchar(30),
numero int,
rua varchar(50),
estado varchar(30),
bairro varchar(30),
CONSTRAINT fk_OS_end FOREIGN KEY (os_id_end) REFERENCES Ordem_servico(id)
);

CREATE TABLE tem (
equipamento_id_tem int,
os_id_tem int,
PRIMARY KEY(equipamento_id_tem, os_id_tem),
CONSTRAINT fk_Equipamento_tem FOREIGN KEY (equipamento_id_tem) REFERENCES Equipamento(id),
CONSTRAINT fk_OS_tem FOREIGN KEY (os_id_tem) REFERENCES Ordem_servico (id)
);

CREATE TABLE contem (
material_id_cont int,
os_id_cont int,
PRIMARY KEY (material_id_cont, os_id_cont),
CONSTRAINT fk_Material_cont FOREIGN KEY (material_id_cont) REFERENCES Material(id),
CONSTRAINT fk_OS_cont FOREIGN KEY (os_id_cont) REFERENCES Ordem_servico(id)
);
