import streamlit as st
from orquestrador import app_sac

# Configuração da página do Streamlit
st.set_page_config(page_title="SAC Inteligente - IA", page_icon="🤖", layout="centered")

st.title("🤖 Sistema de Agentes de Atendimento (SAC)")
st.markdown("---")
st.markdown("""
    Este sistema utiliza **LangGraph** e **Multi-Agentes** para fazer a triagem e 
    resolução automática de chamados de clientes em tempo real.
""")

# Inicializa o histórico de chat na sessão se não existir
if "historico_chat" not in st.session_state:
    st.session_state.historico_chat = []

# Exibe as mensagens anteriores do chat
for mensagem in st.session_state.historico_chat:
    with st.chat_message(mensagem["role"]):
        st.markdown(mensagem["content"])

# Campo de entrada do usuário na parte inferior (estilo chat moderno)
if prompt_usuario := st.chat_input("Digite sua mensagem para o suporte da empresa..."):
    
    # 1. Mostra a mensagem do usuário na tela
    with st.chat_message("user"):
        st.markdown(prompt_usuario)
    st.session_state.historico_chat.append({"role": "user", "content": prompt_usuario})
    
    # 2. Roda o nosso Orquestrador de Agentes em segundo plano
    with st.spinner("🤖 Agentes processando e roteando seu chamado..."):
        # Montamos o estado inicial para passar para o grafo compilado
        estado_inicial = {"mensagem_cliente": prompt_usuario}
        
        # Invocamos o grafo completo!
        resultado_grafo = app_sac.invoke(estado_inicial)
        
        resposta_final = resultado_grafo["resposta_final"]
        categoria = resultado_grafo.get("categoria_detectada", "ELOGIO")

    # 3. Define um ícone e cor baseado na categoria para dar um feedback visual
    icones = {"DUVIDA": "🔍", "CRISE": "🚨", "ELOGIO": "✨"}
    icone_atual = icones.get(categoria, "🤖")
    
    # 4. Mostra a resposta do agente na tela
    with st.chat_message("assistant", avatar=icone_atual):
        st.markdown(f"**[Agente de {categoria.title()}]**\n\n{resposta_final}")
        
        if categoria == "CRISE":
            st.error("🚨 Um alerta crítico de insatisfação foi gerado e enviado para o time humano no backend!")
            
    st.session_state.historico_chat.append({
        "role": "assistant", 
        "content": f"**[Agente de {categoria.title()}]**\n\n{resposta_final}"
    })