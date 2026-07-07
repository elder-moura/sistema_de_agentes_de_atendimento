import json
from datetime import datetime
from langchain_groq import ChatGroq

def gerar_alerta_sistema(mensagem_cliente: str, motivo: str):
    """Simula uma Tool que salva um alerta crítico no banco de dados para os humanos."""
    alerta = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "nivel_criticidade": "MAXIMA",
        "motivo_detectado": motivo,
        "mensagem_original": mensagem_cliente,
        "status_atendimento": "AGUARDANDO_HUMANO_URGENTE"
    }
    
    # Salva um arquivo JSON simulando um webhook ou inserção no banco
    with open("alertas_criticos.json", "a", encoding="utf-8") as f:
        f.write(json.dumps(alerta, ensure_ascii=False) + "\n")
    print("\n🚨 [SISTEMA] Alerta de crise gerado e salvo em 'alertas_criticos.json'!")

def responder_crise(mensagem_cliente: str, justificativa_triagem: str) -> str:
    # 1. Aciona a ferramenta de infraestrutura para registrar o alerta
    gerar_alerta_sistema(mensagem_cliente, justificativa_triagem)
    
    # 2. Usa a IA para gerar uma resposta acolhedora de contenção
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.5)
    
    prompt = f"""
    Você é o Agente de Gerenciamento de Crises do SAC. Um cliente muito insatisfeito mandou a mensagem abaixo.
    Sua única função é dar uma resposta extremamente empática, pedir desculpas em nome da empresa,
    e avisar que um gerente humano especializado já foi acionado e entrará em contato prioritário nas próximas horas.
    Não tente resolver o problema técnico você mesmo. Foque no acolhimento.
    
    MENSAGEM DO CLIENTE:
    "{mensagem_cliente}"
    
    RESPOSTA DE CONTENÇÃO:
    """
    
    resposta = llm.invoke(prompt)
    return resposta.content

# --- ÁREA DE TESTE DO SEU SCRIPT ---
if __name__ == "__main__":
    teste_reclamacao = "Meu produto veio quebrado, paguei caro e quero meu dinheiro de volta agora!"
    justificativa_ficticia = "Cliente exigindo estorno por produto danificado."
    
    print("--- PROCESSANDO ROTA DE CRISE ---")
    print(responder_crise(teste_reclamacao, justificativa_ficticia))