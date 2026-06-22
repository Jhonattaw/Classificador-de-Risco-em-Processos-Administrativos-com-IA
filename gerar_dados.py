import pandas as pd
import random

processos = [
    ("Atraso em entrega de documentos", "Fiscal", [
        "Contribuinte nao entregou declaracao fiscal dentro do prazo estipulado pela legislacao",
        "Empresa deixou de protocolar documentacao exigida ate a data limite fixada em edital",
        "Documentos solicitados pelo fisco nao foram apresentados no prazo de 10 dias uteis",
    ]),
    ("Solicitacao de isencao sem documentacao", "Fiscal", [
        "Empresa solicitou isencao de ICMS sem anexar os documentos comprobatorios obrigatorios",
        "Pedido de isencao tributaria protocolado sem laudo tecnico e certidoes exigidas",
        "Contribuinte requereu beneficio fiscal sem apresentar documentacao de habilitacao",
    ]),
    ("Pagamento registrado em duplicidade", "Financeiro", [
        "Fornecedor registrou o mesmo pagamento duas vezes no sistema financeiro",
        "Ordem de pagamento emitida em duplicidade para o mesmo fornecedor e competencia",
        "Sistema processou dois lancamentos identicos para a mesma nota fiscal do fornecedor",
    ]),
    ("Acesso nao autorizado ao sistema", "TI", [
        "Usuario tentou acessar modulo restrito sem possuir permissao de acesso",
        "Tentativa de acesso a base de dados sigilosa registrada por perfil sem autorizacao",
        "Log do sistema registrou acesso indevido a painel administrativo por usuario comum",
    ]),
    ("Contrato vencido sem renovacao", "Juridico", [
        "Contrato com fornecedor expirou sem que o processo de renovacao fosse iniciado",
        "Instrumento contratual encerrou vigencia sem aditivo ou novo processo licitatorio",
        "Fornecedor continuou prestando servico apos vencimento contratual sem formalizacao",
    ]),
    ("Erro em calculo de tributo", "Fiscal", [
        "Calculo de ICMS gerou valor incorreto devido a parametro desatualizado no sistema",
        "Aliquota aplicada na apuracao diverge da tabela vigente publicada em diario oficial",
        "Sistema calculou base de reducao de forma equivocada gerando recolhimento a menor",
    ]),
    ("Ausencia de servidor em periodo critico", "RH", [
        "Servidor responsavel pela entrega ausentou sem designar substituto para o periodo",
        "Colaborador chave entrou em licenca durante prazo legal sem formalizar substituicao",
        "Equipe ficou sem responsavel tecnico durante auditoria externa por ausencia nao planejada",
    ]),
    ("Dado cadastral desatualizado", "Fiscal", [
        "CPF do contribuinte possui endereco incorreto gerando retorno de correspondencias oficiais",
        "Razao social do fornecedor no cadastro diverge do registro atual na Receita Federal",
        "Dados bancarios do beneficiario estao desatualizados causando falha no pagamento",
    ]),
    ("Falha em backup de dados", "TI", [
        "Rotina de backup nao foi executada por tres dias consecutivos sem registro de erro",
        "Job agendado de copia de seguranca falhou silenciosamente sem gerar alerta",
        "Backup do banco de dados nao foi validado apos execucao resultando em arquivo corrompido",
    ]),
    ("Processo sem responsavel definido", "Gestao", [
        "Demanda foi aberta ha mais de 30 dias sem atribuicao de responsavel no sistema",
        "Chamado critico permanece sem dono apos redistribuicao de equipe nao comunicada",
        "Solicitacao de area de negocio aguarda tratamento sem designacao formal de responsavel",
    ]),
    ("Nota fiscal emitida com valor incorreto", "Fiscal", [
        "Nota fiscal emitida com valor divergente do contrato firmado entre as partes",
        "NF-e emitida com CFOP incorreto alterando a classificacao fiscal da operacao",
        "Valor unitario informado na nota fiscal diverge da tabela de precos homologada",
    ]),
    ("Mercadoria transportada sem documentacao", "Fiscal", [
        "Veiculo interceptado na divisa transportando mercadoria sem nota fiscal ou manifesto",
        "Carga retida em posto fiscal por ausencia de DANFE e conhecimento de transporte",
        "Transportadora realizou entrega sem documentacao fiscal habilitadora do transito",
    ]),
    ("Acesso de usuario desligado ainda ativo", "TI", [
        "Colaborador desligado ha 15 dias ainda possui credencial de acesso ativa no sistema",
        "Conta de ex-funcionario nao foi desativada apos rescisao contratual registrada no RH",
        "Login de prestador encerrado continua com permissao de leitura em repositorio interno",
    ]),
    ("Contrato sem assinatura digital", "Juridico", [
        "Contrato enviado para fornecedor aguarda assinatura digital ha mais de 20 dias",
        "Instrumento juridico nao foi assinado eletronicamente dentro do prazo regimental",
        "Aditivo contratual encontra-se pendente de assinatura digital por ambas as partes",
    ]),
    ("Servidor sem treinamento obrigatorio", "RH", [
        "Colaborador nao realizou treinamento de seguranca da informacao dentro do prazo exigido",
        "Servidor publico nao concluiu capacitacao obrigatoria de compliance no ciclo vigente",
        "Funcionario em funcao critica nao possui certificacao interna de privacidade de dados",
    ]),
    ("Sistema legado sem atualizacao de seguranca", "TI", [
        "Sistema critico operando com versao desatualizada exposta a vulnerabilidades conhecidas",
        "Aplicacao legada nao recebeu patch de seguranca em mais de seis meses de operacao",
        "Servidor de aplicacao roda versao obsoleta com CVE critico sem plano de correcao",
    ]),
    ("Auditoria atrasada sem justificativa", "Gestao", [
        "Ciclo de auditoria interna nao foi realizado no prazo previsto sem registro de justificativa",
        "Revisao periodica de controles internos esta atrasada sem comunicacao formal ao gestor",
        "Auditoria de conformidade nao ocorreu no trimestre previsto sem abertura de excecao",
    ]),
    ("Fornecedor com CNPJ irregular", "Juridico", [
        "Fornecedor ativo no cadastro possui CNPJ com situacao irregular junto a Receita Federal",
        "Empresa contratada apresenta restricoes cadastrais em consulta ao portal da RFB",
        "CNPJ do prestador consta como suspenso no momento da emissao da ordem de servico",
    ]),
    ("Declaracao fiscal entregue fora do prazo", "Fiscal", [
        "Empresa entregou declaracao de apuracao fiscal apos o encerramento do prazo legal",
        "SPED Fiscal transmitido com atraso de cinco dias em relacao a data limite obrigatoria",
        "Contribuinte protocolou GIA apos vencimento sujeitando-se a multa por atraso",
    ]),
    ("Equipamento sem manutencao preventiva", "TI", [
        "Servidor fisico nao recebeu manutencao preventiva dentro do cronograma estabelecido",
        "Nobreak do datacenter esta fora do ciclo de revisao preventiva ha dois trimestres",
        "Desktop de uso critico nao passou por checagem tecnica no periodo recomendado pelo fabricante",
    ]),
    ("Divergencia entre estoque e sistema", "Financeiro", [
        "Quantidade registrada no sistema diverge do estoque fisico verificado na contagem",
        "Inventario identificou sobra de 12 unidades nao registradas no modulo de almoxarifado",
        "Saldo contabil de materiais de consumo nao bate com levantamento fisico realizado",
    ]),
    ("Processo judicial sem acompanhamento", "Juridico", [
        "Acao judicial em andamento sem movimentacao registrada ha mais de 60 dias",
        "Processo na vara fiscal nao possui advogado responsavel designado para acompanhamento",
        "Prazo processual em risco por falta de monitoramento ativo das movimentacoes do caso",
    ]),
    ("Dado sensivel exposto em relatorio", "TI", [
        "Relatorio gerado pelo sistema expos dados pessoais sensiveis sem mascara de protecao",
        "Exportacao de planilha incluiu CPFs e rendimentos de contribuintes sem anonimizacao",
        "Dashboard compartilhado externamente continha informacoes medicas de servidores",
    ]),
    ("Licenca de software vencida", "TI", [
        "Software critico operando com licenca expirada colocando o orgao em risco de penalidade",
        "Suite de escritorio com licenciamento vencido em uso por setor administrativo ha 45 dias",
        "Ferramenta de monitoramento de rede expirou contrato de suporte sem renovacao aprovada",
    ]),
    ("Multa por descumprimento contratual", "Juridico", [
        "Fornecedor descumpriu clausula contratual sujeitando o orgao a pagamento de multa",
        "Entrega realizada fora do prazo contratual gerou incidencia de penalidade pecuniaria",
        "Inadimplemento de obrigacao acessoria pelo contratado resultou em aplicacao de multa",
    ]),
]

dados = []
for i in range(1, 201):
    processo, area, descricoes = random.choice(processos)
    dados.append({
        "ID": f"P{i:03d}",
        "Processo": processo,
        "Descricao": random.choice(descricoes),
        "Area": area
    })

df = pd.DataFrame(dados)
df.to_excel("processos.xlsx", index=False)
print(f"Gerado: {len(df)} processos em processos.xlsx")