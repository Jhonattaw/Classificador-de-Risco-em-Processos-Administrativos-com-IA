# Classificador de Risco em Processos Administrativos com IA

Sistema que lê uma planilha com processos administrativos e usa inteligência artificial para classificar automaticamente o nível de risco de cada um como Alto, Médio ou Baixo.

## O que o projeto faz

- Lê um arquivo Excel com processos administrativos
- Envia cada processo para um modelo de linguagem (LLM) via API
- Recebe a classificação de risco e a justificativa
- Salva o resultado em uma nova planilha Excel

## Tecnologias utilizadas

- Python
- Pandas
- Groq API (LLM llama-3.3-70b-versatile)
- OpenPyXL

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