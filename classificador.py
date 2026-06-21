import pandas as pd
from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

df = pd.read_excel("processos.xlsx")
resultados = []

for index, row in df.iterrows():
    prompt = f"""
    Você é um especialista em gestão de riscos administrativos.
    Analise o processo abaixo e responda APENAS em JSON, sem mais nada:
    {{"risco": "Alto ou Medio ou Baixo", "justificativa": "uma frase curta"}}

    Processo: {row['Processo']}
    Descrição: {row['Descricao']}
    Área: {row['Area']}
    """

    resposta = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
    )

    texto_resposta = resposta.choices[0].message.content

    dados = json.loads(texto_resposta)

    resultados.append(
        {
            "ID": row["ID"],
            "Processo": row["Processo"],
            "Descricao": row["Descricao"],
            "Area": row["Area"],
            "Risco": dados["risco"],
            "Justificativa": dados["justificativa"],
        }
    )

    print(f"✓ {row['ID']} classificado")

df_resultado = pd.DataFrame(resultados)
df_resultado.to_excel("resultado_classificacao.xlsx", index=False)
print("\nArquivo salvo: resultado_classificacao.xlsx")
print(df_resultado[["ID", "Processo", "Risco", "Justificativa"]])
