# Classificador de Risco em Processos Administrativos com IA

Projeto desenvolvido para automatizar a classificação de risco de processos administrativos. Em vez de analisar linha por linha manualmente, o sistema lê uma planilha, analisa cada processo e retorna o nível de risco (Alto, Médio ou Baixo) com a justificativa. O objetivo é reduzir o tempo gasto em triagem manual e permitir que o analista foque nos casos mais críticos

## O que o projeto faz

- Lê um arquivo Excel com processos administrativos
- Envia cada processo para um modelo de linguagem (LLM) via API
- Recebe a classificação de risco e a justificativa
- Salva o resultado em uma nova planilha Excel

## Como funciona

É como uma linha de montagem: o Pandas lê os dados da planilha, 
envia cada processo para a IA analisar, e o resultado é salvo 
em uma nova planilha Excel.

- **Python** — linguagem principal
- **Pandas** — lê e organiza os dados da planilha de entrada
- **Groq API** — processa cada processo com IA e retorna a classificação
- **OpenPyXL** — salva o resultado em uma nova planilha Excel

## Como usar

1. Clone o repositório
2. Crie um arquivo `.env` com sua chave: `GROQ_API_KEY=sua_chave`
3. Instale as dependências: `pip install -r requirements.txt`
4. Adicione seus processos no arquivo `processos.xlsx`
5. Execute: `python classificador.py`
6. O resultado será salvo em `resultado_classificacao.xlsx`

## Exemplo de saída

| ID | Processo | Risco | Justificativa |
|---|---|---|---|
| P001 | Atraso em entrega de documentos | Alto | Pode gerar multas e penalidades |
| P003 | Pagamento em duplicidade | Baixo | Erro facilmente identificável |

## Aplicações práticas

Este sistema pode ser adaptado para triagem de ocorrências fiscais, priorização de processos em órgãos públicos e classificação de demandas em qualquer área administrativa.

## Autor

Jhonattaw Barreto