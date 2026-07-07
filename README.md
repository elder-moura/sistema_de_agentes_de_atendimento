# 🤖 Sistema Multi-Agente de Atendimento ao Cliente (SAC Inteligente)

Este é um projeto corporativo de ponta a ponta que implementa um ecossistema de **Multi-Agentes de IA** utilizando uma arquitetura de **Grafo de Estados Dirigido** para triagem, roteamento e resolução automatizada de chamados de suporte em tempo real.

O objetivo principal é simular um ambiente de produção que reduz custos operacionais de SAC, garantindo respostas rápidas para dúvidas comuns e alertas imediatos para casos críticos.

---

## 🏗️ Arquitetura do Sistema e Fluxo de Trabalho

O sistema utiliza o **LangGraph** para orquestrar a tomada de decisão através de 4 nós principais:

1. **Nó de Triagem (Classificador):** Utiliza uma LLM com **Structured Outputs (Pydantic)** para garantir resiliência, classificando a intenção do cliente estritamente em `DUVIDA`, `CRISE` ou `ELOGIO`.
2. **Nó de Resolução (RAG):** Roteado automaticamente quando o cliente tem uma dúvida. Realiza uma busca indexada em uma base de conhecimento local (`faq_empresa.txt`) e responde estritamente baseado nas regras de negócio.
3. **Nó de Gerenciamento de Crise:** Roteado quando há ameaça de cancelamento ou alta insatisfação. Dispara de forma assíncrona um log estruturado em JSON (`alertas_criticos.json`) para a equipe humana e gera uma resposta de contenção altamente empática.
4. **Nó de Elogio:** Rota de feedback positivo para encerramento do fluxo de forma amigável.

---

## 🛠️ Tecnologias Utilizadas

* **Python 3.12+**
* **LangGraph:** Orquestração do Grafo de Estados e roteamento condicional.
* **LangChain & ChatGroq:** Integração e consumo do modelo de última geração `llama-3.3-70b-versatile`.
* **Pydantic:** Garantia de tipagem e validação de outputs estruturados da LLM.
* **Streamlit:** Interface web moderna e reativa simulando um chat de atendimento real.

---

## 🚀 Como Executar o Projeto

### 1. Clonar o repositório
```bash
git clone [https://github.com/seu-usuario/sac-agente-inteligente.git](https://github.com/seu-usuario/sac-agente-inteligente.git)
cd sac-agente-inteligente 

### 2. Instalar as dependências
pip install pandas langchain-groq pydantic langgraph streamlit

### 3. Configurar a Chave de API da Groq

### 4. Rodar a Interface Web
python -m streamlit run app.py


