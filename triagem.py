import os
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq

# 1. Definir a estrutura exata que queremos que a IA responda.

class DecisaoTriagem(BaseModel):
    categoria: str = Field(
        description="A categoria da mensagem. Deve ser estritamente: 'DUVIDA', 'CRISE' ou 'ELOGIO'."
    )
    justificativa: str = Field(
        description="Uma breve explicação do porquê a mensagem foi classificada nessa categoria."
    )

# 2. Inicializa o modelo da Groq (garanta que sua GROQ_API_KEY está configurada no ambiente)
# Usamos uma temperatura baixa (0.0) para que a IA seja o mais lógica e menos "criativa" possível
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.0)

# 3. Forçar a LLM a responder seguindo a nossa classe Pydantic
classificador = llm.with_structured_output(DecisaoTriagem)

def triagem_cliente(mensagem_usuario: str):
    prompt = f"""
    Você é o Agente de Triagem de uma grande empresa. Sua única função é analisar a mensagem do cliente
    e categorizá-la corretamente para o direcionamento do suporte.
    
    Mensagem do Cliente: "{mensagem_usuario}"
    """
    
    # Executa a chamada
    resposta = classificador.invoke(prompt)
    return resposta

# --- ÁREA DE TESTE DO SCRIPT ---
if __name__ == "__main__":
    # Teste 1:
    teste_crise = "Quero cancelar minha assinatura agora! Meu produto veio quebrado e ninguém me atende!"
    resultado = triagem_cliente(teste_crise)
    
    print("--- RESULTADO DA TRIAGEM ---")
    print(f"Categoria Detectada: {resultado.categoria}")
    print(f"Justificativa da IA: {resultado.justificativa}")