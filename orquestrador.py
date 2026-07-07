from typing import TypedDict
from langgraph.graph import StateGraph, END
from triagem import triagem_cliente
from resolucao import responder_duvida
from crise import responder_crise

# 1. Definir o Estado do Grafo 
class EstadoSAC(TypedDict):
    mensagem_cliente: str
    categoria_detectada: str
    justificativa_triagem: str
    resposta_final: str

# 2. Criar os Nós (Nodes) do Grafo, envelopando as funções
def no_triagem(estado: EstadoSAC):
    print("\n[Grafo] 🧠 Iniciando Nó de Triagem...")
    resultado = triagem_cliente(estado["mensagem_cliente"])
    return {
        "categoria_detectada": resultado.categoria,
        "justificativa_triagem": resultado.justificativa
    }

def no_resolucao(estado: EstadoSAC):
    print("\n[Grafo] 🔍 Redirecionado para o Nó de Resolução (Dúvida)...")
    resposta = responder_duvida(estado["mensagem_cliente"])
    return {"resposta_final": resposta}

def no_crise(estado: EstadoSAC):
    print("\n[Grafo] 🚨 Redirecionado para o Nó de Crise...")
    resposta = responder_crise(estado["mensagem_cliente"], estado["justificativa_triagem"])
    return {"resposta_final": resposta}

def no_elogio(estado: EstadoSAC):
    print("\n[Grafo] ✨ Redirecionado para o Nó de Elogios...")
    return {"resposta_final": "Muito obrigado pelo seu feedback positivo! Ficamos extremamente felizes em ajudar. 🥰"}

# 3. A Função Roteadora (Conditional Edge)
# Lê o estado atual e diz para qual nó o fluxo deve ir
def rotear_mensagem(estado: EstadoSAC):
    categoria = estado["categoria_detectada"]
    if categoria == "DUVIDA":
        return "ir_para_resolucao"
    elif categoria == "CRISE":
        return "ir_para_crise"
    else:
        return "ir_para_elogio"

# 4. Construindo a Estrutura do Grafo
workflow = StateGraph(EstadoSAC)

# Adiciona os nós no mapa
workflow.add_node("triagem", no_triagem)
workflow.add_node("resolucao", no_resolucao)
workflow.add_node("crise", no_crise)
workflow.add_node("elogio", no_elogio)

# Define o ponto de partida
workflow.set_entry_point("triagem")

# Adiciona a aresta condicional
workflow.add_conditional_edges(
    "triagem",
    rotear_mensagem,
    {
        "ir_para_resolucao": "resolucao",
        "ir_para_crise": "crise",
        "ir_para_elogio": "elogio"
    }
)

# Liga os nós de resposta ao ponto final do grafo
workflow.add_edge("resolucao", END)
workflow.add_edge("crise", END)
workflow.add_edge("elogio", END)

# Compila o grafo para deixá-lo pronto para execução
app_sac = workflow.compile()

# --- ÁREA DE TESTE DO ECOSSISTEMA COMPLETO ---
if __name__ == "__main__":
    # Primeiro teste: Uma dúvida que precisa ler o FAQ
    entrada_usuario = {"mensagem_cliente": "O atendimento de vocês é péssimo, vou cancelar!"}
    
    print("=== INICIANDO ORQUESTRADOR DE AGENTES ===")
    resultado_final = app_sac.invoke(entrada_usuario)
    
    print("\n=== RESPOSTA ENTREGUE PELO GRAFO ===")
    print(resultado_final["resposta_final"])