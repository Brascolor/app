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
);

CREATE TABLE Email_cliente (
cliente_id_em int,
email varchar(50),
CONSTRAINT fk_Cliente_em FOREIGN KEY (cliente_id_em) REFERENCES Cliente(id)
);

CREATE TABLE Telefone_cliente (
cliente_id_tel int,
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
funcionario_cpf_em varchar(15),
email varchar(50),
CONSTRAINT fk_Funcionario_em FOREIGN KEY (funcionario_cpf_em) REFERENCES Funcionario(cpf)
);

CREATE TABLE Celular_funcionario (
funcionario_cpf_cel varchar(15),
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
qtd_produto int,
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
qtd_material int,
PRIMARY KEY (material_id_cont, os_id_cont),
CONSTRAINT fk_Material_cont FOREIGN KEY (material_id_cont) REFERENCES Material(id),
CONSTRAINT fk_OS_cont FOREIGN KEY (os_id_cont) REFERENCES Ordem_servico(id)
);

CREATE TABLE OS_log(
id int PRIMARY KEY,
cliente_id int,
data_hora_consulta datetime,
data_hora_emissao datetime,
logistica_cpf varchar(15),
produto_id int,
quantidade int
);

CREATE TABLE tem_log(
equipamento_id int,
os_id int,
PRIMARY KEY (equipamento_id, os_id)
);

CREATE TABLE contem_log(
material_id int,
os_id int,
quantidade int,
PRIMARY KEY (material_id, os_id)
);

CREATE TABLE Endereco_log(
os_id int PRIMARY KEY,
cidade varchar(30),
numero int,
rua varchar(50),
estado varchar(30),
bairro varchar(30)
);

DELIMITER $$
CREATE TRIGGER tr_delete_tem
BEFORE DELETE ON tem
FOR EACH ROW
BEGIN
    INSERT INTO tem_log values(OLD.equipamento_id_tem, OLD.os_id_tem);
END $$

CREATE TRIGGER tr_delete_contem
BEFORE DELETE ON contem
FOR EACH ROW
BEGIN
    INSERT INTO contem_log values(OLD.material_id_cont, OLD.os_id_cont, OLD.qtd_material);
END $$

CREATE TRIGGER tr_delete_endereco
BEFORE DELETE ON Endereco
FOR EACH ROW
BEGIN
    INSERT INTO endereco_log values(OLD.os_id_end, OLD.cidade, OLD.numero, OLD.rua, OLD.estado, OLD.bairro);
END $$

CREATE TRIGGER tr_delete_os
BEFORE DELETE ON Ordem_servico
FOR EACH ROW
BEGIN
    INSERT INTO OS_log values(OLD.id, OLD.cliente_id_os, OLD.data_hora_consulta, OLD.data_hora_emissao, OLD.logistica_cpf_os, OLD.produto_id_os, OLD.qtd_produto);
    DELETE FROM Endereco WHERE os_id_end = OLD.id;
    DELETE FROM tem WHERE os_id_tem = OLD.id;
    DELETE FROM contem WHERE os_id_cont = OLD.id;
END $$
DELIMITER ;

INSERT INTO Material values(1, 'couché brilho', 2000);
INSERT INTO Material values(2, 'duplex', 5000);
INSERT INTO Material values(3, 'jornal', 25000);
INSERT INTO Material values(4, 'tinta amarela', 5000);
INSERT INTO Material values(5, 'tinta ciano', 5000);
INSERT INTO Material values(6, 'tinta magenta', 5000);
INSERT INTO Material values(7, 'tinta preta', 10000);
INSERT INTO Material values(8, 'kraft', 10000);
INSERT INTO Material values(9, 'sufite', 20000);

INSERT INTO Tipo values(1, 'sacola');
INSERT INTO Tipo values(2, 'panfleto');
INSERT INTO Tipo values(3, 'jornal');
INSERT INTO Tipo values(4, 'agenda');
INSERT INTO Tipo values(5, 'cinta');
INSERT INTO Tipo values(6, 'embalagem semirrigida');

INSERT INTO Produto values(1, 'sacolas de papel com impressão frente', 1);
INSERT INTO Produto values(2, 'tablóides com impressão frente e verso', 2);
INSERT INTO Produto values(3, 'jornal com impressão frente e verso', 3);
INSERT INTO Produto values(4, 'tablóides com impressão frente e verso', 2);

INSERT INTO Cliente values(1, 'Duda Cakes', 'Recife', 30, 'Av. Agamenon Magalhaes', 'Pernambuco', 'Ilha do Leite');
INSERT INTO Cliente values(2, 'Novo Atacarejo', 'Recife', 1400, 'Av. da Recuperação', 'Pernambuco', 'Dois Irmãos');
INSERT INTO Cliente values(3, 'Diário de Pernambuco', 'São Paulo', 255, 'Rua Barão de Itapetinga', 'São Paulo', 'Centro');
INSERT INTO Cliente values(4, 'Grupo Pão de Açúcar', 'Recife', 261, 'Rua Desembargador Góis', 'Recife', 'Parnamirim');

INSERT INTO Email_cliente values(1, 'dudacakes@gmail.com');
INSERT INTO Email_cliente values(2, 'novoatacarejo@gmail.com');
INSERT INTO Email_cliente values(3, 'diariodepernambuco@gmail.com');
INSERT INTO Email_cliente values(3, 'DDP@gmail.com');
INSERT INTO Email_cliente values(4, 'GPA@gmail.com');
INSERT INTO Email_cliente values(4, 'grupopaodeacucar@gmail.com');

INSERT INTO Telefone_cliente values(1, '8127117364');
INSERT INTO Telefone_cliente values(1, '8136831379');
INSERT INTO Telefone_cliente values(2, '8132552514');
INSERT INTO Telefone_cliente values(3, '1433171561');
INSERT INTO Telefone_cliente values(4, '8125853221');

INSERT INTO Veiculo values('KKL9693', 'Fiat', 'Palio', 2009);
INSERT INTO Veiculo values('KJG9343', 'Fiat', 'Fiorino', 2013);
INSERT INTO Veiculo values('KGP2212', 'Mercedes', 'Accelo', 2023);
INSERT INTO Veiculo values('KHS7339', 'Honda', 'Titan', 2016);

#funcionarios do financeiro

INSERT INTO Funcionario values('29076685010', 'Diogmar Brunetti', '1975-08-30', 'MT', 8, 'diogobrunetti@brascolor.com', '29076685010');
INSERT INTO Funcionario values('30634196057', 'Marcos Tulio', '1980-03-14', 'M', 4, 'marcostulio@brascolor.com', '29076685010');
INSERT INTO Funcionario values('50392216060', 'Michelle Obama', '1990-12-10', 'TN', 8, 'MichelleO@brascolor.com', '29076685010');
INSERT INTO Funcionario values('61853409090', 'Raphael Carvalho', '1987-04-01', 'T', 4, 'raphaelc@brascolor.com', '29076685010');

#funcionarios do comercial


INSERT INTO Funcionario values('23790097080', 'Edmilson Santos', '1978-11-12', 'MT', 8, 'edmilsonsantos@brascolor.com', '29076685010');
INSERT INTO Funcionario values('46522890062', 'Edjane Santos', '1978-11-12', 'MT', 8, 'edjanesantos@brascolor.com', '29076685010');
INSERT INTO Funcionario values('17291974003', 'Andrea Lacerda', '1983-08-23', 'MT', 8, 'andrea123@brascolor.com', '29076685010');

#funcionarios da produção

INSERT INTO Funcionario values('86649025003', 'Euller Freitas', '1972-05-28', 'MT', 8, 'eullerfreitas@brascolor.com', '86649025003');
INSERT INTO Funcionario values('68098378098', 'Zilda Cunha', '1970-03-03', 'T', 4, 'zilda03@brascolor.com', '86649025003');
INSERT INTO Funcionario values('88922891017', 'Eldencleiton Umberto', '1989-02-28', 'N', 4, 'Eldencleiton@brascolor.com', '86649025003');

INSERT INTO Celular_funcionario values('29076685010', '87992117371');
INSERT INTO Celular_funcionario values('30634196057', '81998641872');
INSERT INTO Celular_funcionario values('50392216060', '81973355247');
INSERT INTO Celular_funcionario values('61853409090', '87973325801');
INSERT INTO Celular_funcionario values('23790097080', '81998135478');
INSERT INTO Celular_funcionario values('46522890062', '81975377858');
INSERT INTO Celular_funcionario values('17291974003', '81969575715');
INSERT INTO Celular_funcionario values('86649025003', '87999765226');
INSERT INTO Celular_funcionario values('68098378098', '87980655413');
INSERT INTO Celular_funcionario values('88922891017', '87975495468');

INSERT INTO Setor values(1, 'financeiro', 'setor encarregado de gerenciar custos e cobranças da empresa, além de monitorar as vendas.');
INSERT INTO Setor values(2, 'comercial', 'setor encarregado de vender os produtos e lançar ordens de serviço para iniciar sua produção.');

#funcionarios financeiro

INSERT INTO Logistica values('29076685010', 1);
INSERT INTO Logistica values('30634196057', 1);
INSERT INTO Logistica values('50392216060', 1);
INSERT INTO Logistica values('61853409090', 1);

#funcionarios comercial

INSERT INTO Logistica values('23790097080', 2);
INSERT INTO Logistica values('46522890062', 2);
INSERT INTO Logistica values('17291974003', 2);

INSERT INTO Equipamento values(1, 'SM-74', 'maquinário de impressão de médio porte que trabalha com folha inteira.');
INSERT INTO Equipamento values(2, 'CD-120', 'maquinário de impressão de médio porte que trabalha com meia folha, não imprime em frente e verso.');
INSERT INTO Equipamento values(3, 'Rotativa-01', 'maquinário de impressão de grande porte, trabalha com bobinas');

INSERT INTO Operador values('86649025003', 3);
INSERT INTO Operador values('68098378098', 2);
INSERT INTO Operador values('88922891017', 1);

INSERT INTO Ordem_servico (cliente_id_os, logistica_cpf_os, produto_id_os, qtd_produto, data_hora_consulta, data_hora_emissao) values(1, '23790097080', 1, 250, NOW(), NOW());
INSERT INTO Ordem_servico (cliente_id_os, logistica_cpf_os, produto_id_os, qtd_produto, data_hora_consulta, data_hora_emissao) values(2, '46522890062', 2, 12000, NOW(), NOW());
INSERT INTO Ordem_servico (cliente_id_os, logistica_cpf_os, produto_id_os, qtd_produto, data_hora_consulta, data_hora_emissao) values(3, '17291974003', 3, 10000000, NOW(), NOW());
INSERT INTO Ordem_servico (cliente_id_os, logistica_cpf_os, produto_id_os, qtd_produto, data_hora_consulta, data_hora_emissao) values(4, '17291974003', 4, 24000, NOW(), NOW());

INSERT INTO Endereco values(1, 'Recife', 30, 'Av. Agamenon Magalhaes', 'Pernambuco', 'Ilha do Leite');
INSERT INTO Endereco values(2, 'Recife', 1400, 'Av. da Recuperação', 'Pernambuco', 'Dois Irmãos');
INSERT INTO Endereco values(3, 'São Paulo', 255, 'Rua Barão de Itapetinga', 'São Paulo', 'Centro');
INSERT INTO Endereco values(4, 'Recife', 261, 'Rua Desembargador Góis', 'Recife', 'Parnamirim');

INSERT INTO tem values(1, 1);
INSERT INTO tem values(2, 2);
INSERT INTO tem values(3, 3);
INSERT INTO tem values(2, 4);

INSERT INTO contem values(8, 1, 20);

INSERT INTO contem values(9, 2, 30);
INSERT INTO contem values(4, 2, 1);
INSERT INTO contem values(5, 2, 1);
INSERT INTO contem values(6, 2, 1);
INSERT INTO contem values(7, 2, 1);

INSERT INTO contem values(3, 3, 100);
INSERT INTO contem values(4, 3, 10);
INSERT INTO contem values(5, 3, 10);
INSERT INTO contem values(6, 3, 10);
INSERT INTO contem values(7, 3, 10);

INSERT INTO contem values(9, 4, 30);
INSERT INTO contem values(4, 4, 1);
INSERT INTO contem values(5, 4, 1);
INSERT INTO contem values(6, 4, 1);
INSERT INTO contem values(7, 4, 1);