INSERT INTO Ordem_servico(cliente_id_os, logistica_cpf_os, produto_id_os, qtd_produto, data_hora_consulta, data_hora_emissao) VALUES (%s, %s, %s, %s, %s, %s);

INSERT INTO Produto(descricao, tipo_codigo_prod) values(%s, (SELECT codigo FROM Tipo WHERE nome = %s));

INSERT INTO tem values((SELECT id FROM Equipamento WHERE nome = %s), %s);

INSERT INTO contem values(%s, %s, %s);

INSERT INTO endereco values(%s, %s, %s, %s, %s, %s);

SELECT OS.id, C.nome AS nome_cliente, f.nome, os.produto_id_os, os.qtd_produto, os.data_hora_consulta, os.data_hora_emissao 
FROM Ordem_servico OS 
JOIN Cliente C ON OS.cliente_id_os = C.id 
join funcionario f on os.logistica_cpf_os = f.cpf
order by id asc;

SELECT OS.id, C.nome AS nome_cliente, f.nome, os.produto_id_os, os.qtd_produto, os.data_hora_consulta, os.data_hora_emissao 
FROM Ordem_servico OS 
JOIN Cliente C ON OS.cliente_id_os = C.id 
join funcionario f on os.logistica_cpf_os = f.cpf 
WHERE os.id = {data};

SELECT OS.id, C.nome AS nome_cliente, f.nome, os.produto_id_os, os.qtd_produto, os.data_hora_consulta, os.data_hora_emissao 
FROM Ordem_servico OS 
JOIN Cliente C ON OS.cliente_id_os = C.id 
join funcionario f on os.logistica_cpf_os = f.cpf 
WHERE C.nome LIKE '%{data}%'
order by id asc;

SELECT OS.id, C.nome AS nome_cliente, f.nome, os.produto_id_os, os.qtd_produto, os.data_hora_consulta, os.data_hora_emissao 
FROM Ordem_servico OS 
JOIN Cliente C ON OS.cliente_id_os = C.id 
join funcionario f on os.logistica_cpf_os = f.cpf 
WHERE produto_id_os IN (SELECT id 
						FROM Produto p 
						Where p.descricao LIKE '%{data}%')
order by id asc;
					
SELECT * FROM produto order by id asc;

SELECT * FROM produto WHERE id = {data};

SELECT * FROM produto WHERE descricao LIKE '%{data}%' order by id asc;

SELECT * FROM produto WHERE tipo_codigo_prod = (SELECT codigo FROM tipo WHERE nome = '{data}') order by id asc;
						
SELECT * FROM material order by id asc;

SELECT * FROM material WHERE id = {data};

SELECT * FROM material WHERE nome LIKE '%{data}%' order by id asc;

SELECT material_id_cont, qtd_material 
FROM contem 
WHERE os_id_cont = {data}
order by id asc;

SELECT * FROM equipamento order by id asc;

SELECT * FROM equipamento WHERE id = {data};

SELECT * FROM equipamento WHERE nome = '{data}' order by id asc;

SELECT * FROM Equipamento WHERE id IN (SELECT equipamento_id_tem FROM tem WHERE os_id_tem = {data}) order by id asc;

SELECT * FROM endereco order by id asc;

SELECT * FROM endereco WHERE os_id_end = {data};

SELECT * FROM endereco WHERE cidade LIKE '%{data}%' order by id asc;

SELECT * FROM endereco WHERE estado = '{data}' order by id asc;

DELETE FROM ordem_servico WHERE id = %s;

UPDATE material SET quantidade = {qty} WHERE nome = '{name}';

SELECT Ano, Mes, TotalOrdens
FROM (
    SELECT 
        YEAR(data_hora_emissao) AS Ano,
        MONTH(data_hora_emissao) AS Mes,
        COUNT(*) AS TotalOrdens
    FROM Ordem_servico
    GROUP BY YEAR(data_hora_emissao), MONTH(data_hora_emissao)
) AS MesesOrdens
WHERE TotalOrdens = (
    SELECT MAX(TotalOrdens)
    FROM (
        SELECT 
            COUNT(*) AS TotalOrdens
        FROM Ordem_servico
        GROUP BY YEAR(data_hora_emissao), MONTH(data_hora_emissao)
    ) AS MaxOrdens
);

SELECT * FROM Ordem_servico
WHERE qtd_produto = (SELECT MAX(qtd_produto) FROM Ordem_servico);