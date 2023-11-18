SELECT * 
FROM Ordem_servico 
WHERE id IN (SELECT id 
			 FROM Cliente c 
			 Where c.nome LIKE '%atacarejo%');

DELETE FROM ordem_servico WHERE id = 9;

SELECT OS.id, C.nome AS nome_cliente, f.nome, os.produto_id_os, os.qtd_produto, t.equipamento_id_tem, c2.material_id_cont, c2.qtd_material, os.data_hora_consulta, os.data_hora_emissao 
FROM Ordem_servico OS
JOIN Cliente C ON OS.cliente_id_os = C.id 
join funcionario f on os.logistica_cpf_os = f.cpf
join tem t on os.id = t.os_id_tem 
join contem c2 on os.id = c2.os_id_cont 
WHERE C.nome LIKE '%novo%';

delete from equipamento where id=2;

SELECT material_id_cont, qtd_material FROM contem WHERE os_id_cont = 2;

select * from endereco;

select * from tem;

select * from contem;

select * from ordem_servico;