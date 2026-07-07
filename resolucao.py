import os
from langchain_groq import ChatGroq

def buscar_no_faq(termo_busca: str) -> str:
    """Função simples que simula uma busca na base de conhecimento da empresa."""
    if not os.path.exists("faq_empresa.txt"):
        return "Base de conhecimento indisponível no momento."
        
    with open("faq_empresa.txt", "r", encoding="utf-8") as f:
        linhas = f.readlines()
    
    # Filtra as linhas do FAQ que contêm palavras relacionadas à busca do cliente
    contexto = [linha.strip() for linha in linhas if termo_busca.lower() in linha.lower()]
    
    if contexto:
        return "\n".join(contexto)
    return "Nenhuma regra específica encontrada no FAQ para este termo."

def responder_duvida(mensagem_cliente: str) -> str:
    # 1. Extrair uma palavra-chave simples da mensagem para buscar no FAQ
    
    palavras = mensagem_cliente.lower().split()
    contexto_encontrado = ""
    
    # Busca por palavras-chaves comuns como 'prazo', 'devolução', 'suporte', 'premium'
    for palavra in ['prazo', 'devolução', 'suporte', 'premium', 'entrega', 'custo']:
        if palavra in mensagem_cliente.lower():
            contexto_encontrado = buscar_no_faq(palavra)
            break
            
    if not contexto_encontrado:
        contexto_encontrado = "Use as regras gerais de bom atendimento da empresa."

    # 2. Inicializa o modelo para responder com base no contexto
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.2)
    
    prompt = f"""
    Você é o Agente de Resolução do SAC. Sua função é responder à dúvida do cliente de forma educada,
    utilizando ESTRITAMENTE as regras da empresa fornecidas no contexto abaixo.
    Se a informação não estiver no contexto, diga polidamente que não possui essa informação e peça para aguardar um atendente humano.
    
    CONTEXTO DA EMPRESA:
    {contexto_encontrado}
    
    MENSAGEM DO CLIENTE:
    "{mensagem_cliente}"
    
    RESPOSTA AO CLIENTE:
    """
    
    resposta = llm.invoke(prompt)
    return resposta.content

# --- ÁREA DE TESTE DO SCRIPT ---
if __name__ == "__main__":
    teste_duvida = "Qual é o prazo de entrega para quem mora no interior?"
    print("--- PROCESSANDO RESPOSTA DE DÚVIDA ---")
    print(responder_duvida(teste_duvida))