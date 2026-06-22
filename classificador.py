import pandas as pd
from groq import Groq
from dotenv import load_dotenv
import os
import json
import time

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

df = pd.read_excel("processos.xlsx")
resultados = []

for index, row in df.iterrows():
    prompt = f"""
    Você é um especialista em gestão de riscos administrativos.
    
    Regras obrigatórias de classificação:
    
    SEMPRE Alto:
    - Acesso nao autorizado ao sistema
    - Mercadoria transportada sem documentacao
    - Dado sensivel exposto em relatorio
    - Fornecedor com CNPJ irregular
    - Sistema legado sem atualizacao de seguranca
    - Multa por descumprimento contratual
    
    SEMPRE Medio:
    - Atraso em entrega de documentos
    - Contrato vencido sem renovacao
    - Declaracao fiscal entregue fora do prazo
    - Nota fiscal emitida com valor incorreto
    - Erro em calculo de tributo
    - Contrato sem assinatura digital
    - Auditoria atrasada sem justificativa
    - Processo judicial sem acompanhamento
    - Processo sem responsavel definido
    - Ausencia de servidor em periodo critico
    
    SEMPRE Baixo:
    - Pagamento registrado em duplicidade
    - Dado cadastral desatualizado
    - Equipamento sem manutencao preventiva
    - Servidor sem treinamento obrigatorio
    - Licenca de software vencida
    - Falha em backup de dados
    - Acesso de usuario desligado ainda ativo
    - Solicitacao de isencao sem documentacao
    
    Analise o processo abaixo e responda APENAS em JSON, sem mais nada:
    {{"risco": "Alto ou Medio ou Baixo", "justificativa": "uma frase curta"}}

    Processo: {row['Processo']}
    Descrição: {row['Descricao']}
    Área: {row['Area']}
    """

    resposta = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
    )

    texto_resposta = resposta.choices[0].message.content.strip()

    if texto_resposta.startswith("```"):
        texto_resposta = texto_resposta.split("```")[1]
        if texto_resposta.startswith("json"):
            texto_resposta = texto_resposta[4:]
        texto_resposta = texto_resposta.strip()

    try:
        dados = json.loads(texto_resposta)
        risco = dados.get("risco", "Indefinido")
        justificativa = dados.get("justificativa", "Sem justificativa")
    except:
        risco = "Indefinido"
        justificativa = texto_resposta.strip()

    resultados.append(
        {
            "ID": row["ID"],
            "Processo": row["Processo"],
            "Descricao": row["Descricao"],
            "Area": row["Area"],
            "Risco": risco,
            "Justificativa": justificativa,
        }
    )

    print(f"✓ {row['ID']} classificado")
    time.sleep(1)

df_resultado = pd.DataFrame(resultados)
df_resultado.to_excel("resultado_classificacao.xlsx", index=False)
print("\nArquivo salvo: resultado_classificacao.xlsx")
print(df_resultado[["ID", "Processo", "Risco", "Justificativa"]])