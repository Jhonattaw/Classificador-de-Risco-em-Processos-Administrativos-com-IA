# Classificador de Risco em Processos Administrativos com IA

Desenvolvi esse projeto para automatizar a triagem de processos 
administrativos por nível de risco. Em vez de analisar centenas 
de registros um por um, o sistema lê uma planilha, analisa cada 
processo e retorna se o risco é Alto, Médio ou Baixo com uma 
justificativa. O analista para de ler tudo e passa a focar onde 
o risco é maior.

## Como funciona

O Pandas lê os dados da planilha e envia cada processo para um 
modelo de linguagem via API. O modelo analisa o contexto, 
classifica o risco e devolve a justificativa. O resultado é 
salvo automaticamente em uma nova planilha Excel.

A escolha foi usar LLM via API em vez de machine learning 
tradicional. O problema envolve interpretação de contexto e 
critérios subjetivos de risco, o que torna essa abordagem mais 
ágil para um MVP, sem precisar de uma base histórica grande 
para treinar.

## Stack

- Python
- Pandas
- Groq API (modelo openai/gpt-oss-120b)
- OpenPyXL
- python-dotenv

## Como usar

1. Clone o repositório
2. Crie um arquivo `.env` com sua chave: `GROQ_API_KEY=sua_chave`
3. Instale as dependências: `pip install -r requirements.txt`
4. Adicione seus processos no arquivo `processos.xlsx`
5. Execute: `python classificador.py`
6. O resultado será salvo em `resultado_classificacao.xlsx`

## Validação

Para medir se o classificador funciona, criei uma base separada 
de 30 processos com a resposta esperada definida antes de rodar 
(o gabarito). Rodei o classificador nesses 30, comparei com o 
gabarito e medi o resultado.

**27 acertos em 30 casos. 90% de concordância.**

As 3 divergências foram todas adjacentes (Médio classificado 
como Alto ou vice-versa). Nenhuma divergência crítica entre 
extremos (Alto classificado como Baixo ou o contrário).

## Sobre a base de dados

Os processos usados nesse projeto são fictícios, gerados para 
demonstração e validação do classificador. A distribuição de 
risco não representa uma operação real. Em produção, o esperado 
é que a maioria dos processos seja de baixo risco, com menor 
incidência de casos críticos. As regras de classificação são 
configuráveis no prompt conforme a necessidade de cada operação.

## Exemplo de saída

| ID | Processo | Risco | Justificativa |
|---|---|---|---|
| P001 | Sistema legado sem atualização de segurança | Alto | Servidor com CVE crítico expõe o ambiente a ataques sem mitigação |
| P004 | Acesso de usuário desligado ainda ativo | Alto | Credencial ativa permite acesso não autorizado e risco de vazamento |
| P029 | Divergência entre estoque e sistema | Baixo | Diferença isolada sem impacto operacional, tratamento simples |

## Autor

Jhonattaw Barreto