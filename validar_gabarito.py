import pandas as pd
from groq import Groq
from dotenv import load_dotenv
import os
import json
import time
import unicodedata

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Antes do loop — fixo, não muda a cada processo
SYSTEM_PROMPT = """
Você é um auditor especialista em gestão de riscos administrativos.
Sua função é triar processos para que a equipe humana foque nos casos mais críticos.

Classifique o nível de risco considerando o contexto e o impacto descrito:

Alto: impacto imediato e grave — acesso indevido, vazamento, invasão, serviço crítico parado, prejuízo financeiro relevante ou risco legal iminente.
Médio: requer atenção em prazo curto — pode escalar para Alto se não tratado, situação recorrente ou pendência relevante.
Baixo: rotineiro e controlável — solicitação comum ou erro isolado sem impacto operacional.
REVISAR: use quando o caso estiver genuinamente na fronteira entre dois níveis e exigir julgamento humano.

EXEMPLOS:

Processo: Licença de firewall vencida sem renovação iniciada
Descrição: Licença do servidor de firewall expirou expondo toda a rede corporativa a acessos não autorizados.
Área: TI
Resposta: {"risco": "Alto", "justificativa": "Exposição imediata da rede a invasões sem proteção ativa."}

Processo: Contribuinte solicita restituição por pagamento em duplicidade
Descrição: Contribuinte efetuou dois pagamentos da mesma guia e solicita devolução do valor pago a mais.
Área: Fiscal
Resposta: {"risco": "Baixo", "justificativa": "Situação rotineira sem impacto operacional, tratamento simples e controlável."}

Responda APENAS com JSON válido, sem markdown, sem texto adicional:
{"risco": "Alto, Medio, Baixo ou REVISAR", "justificativa": "uma frase curta"}
"""

def normalizar(texto):
    texto = str(texto).strip().lower()
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    return texto

def classificar_processo(dados_processo, max_tentativas=3):
    for tentativa in range(max_tentativas):
        try:
            resposta = client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": dados_processo}
                ],
                temperature=0,
            )

            texto = resposta.choices[0].message.content.strip()
            texto = texto.replace("```json", "").replace("```", "").strip()

            return json.loads(texto)

        except json.JSONDecodeError:
            print(f"  ⚠ Tentativa {tentativa + 1}: JSON inválido. Retentando...")
            time.sleep(2)
        except Exception as e:
            print(f"  ⚠ Tentativa {tentativa + 1}: Erro na API ({e}). Retentando...")
            time.sleep(2)

    return {"risco": "Indefinido", "justificativa": "Falha após múltiplas tentativas"}


df = pd.read_excel("gabarito_30.xlsx")
resultados = []

for index, row in df.iterrows():
    dados_processo = f"Processo: {row['Processo']}\nDescrição: {row['Descricao']}\nÁrea: {row['Area']}"

    resultado = classificar_processo(dados_processo)

    risco = resultado.get("risco", "Indefinido")
    justificativa = resultado.get("justificativa", "Sem justificativa")

    if normalizar(risco) == "revisar":
        acertou = "Revisar"
    elif normalizar(risco) == normalizar(str(row["Risco_Esperado"])):
        acertou = "Sim"
    else:
        acertou = "Não"

    resultados.append({
        "ID": row["ID"],
        "Processo": row["Processo"],
        "Descricao": row["Descricao"],
        "Area": row["Area"],
        "Risco_Esperado": row["Risco_Esperado"],
        "Risco_IA": risco,
        "Justificativa_IA": justificativa,
        "Acertou": acertou,
    })

    if acertou == "Sim":
        marca = "✓"
    elif acertou == "Revisar":
        marca = "⚠"
    else:
        marca = "✗"

    print(f"{marca} {row['ID']} | Esperado: {row['Risco_Esperado']} | IA: {risco}")
    time.sleep(1)

df_resultado = pd.DataFrame(resultados)

total = len(df_resultado)
acertos = df_resultado[df_resultado["Acertou"] == "Sim"].shape[0]
erros = df_resultado[df_resultado["Acertou"] == "Não"].shape[0]
revisar = df_resultado[df_resultado["Acertou"] == "Revisar"].shape[0]

classificados = acertos + erros
assertividade = round((acertos / classificados) * 100, 1) if classificados > 0 else 0

print(f"\n{'='*50}")
print(f"Total de processos: {total}")
print(f"Classificados com confiança: {classificados}")
print(f"  - Acertos: {acertos}")
print(f"  - Erros: {erros}")
print(f"Enviados para revisão humana: {revisar}")
print(f"\nAssertividade nos classificados: {assertividade}%")
print(f"{'='*50}")

df_resultado.to_excel("gabarito_30_resultado.xlsx", index=False)
print("Arquivo salvo: gabarito_30_resultado.xlsx")
