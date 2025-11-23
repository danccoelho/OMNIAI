# =====================================================================
# IMPORTS – Importações necessárias
# =====================================================================

import streamlit as st
from groq import Groq

# =====================================================================
# SYSTEM PROMPT – Define o comportamento base do assistente
# =====================================================================

SYSTEM_PROMPT = """
Você é um Assistente Especialista em Machine Learning, Deep Learning, MLOps, LLMs e Explicabilidade de Modelos (XAI).

Seu papel é ajudar usuários a entender e aplicar:
- Algoritmos de Machine Learning
- Hiperparâmetros
- Métricas de avaliação
- Técnicas de pré-processamento
- Feature engineering
- Análise de resultados
- Escolha de modelos
- Explicabilidade (SHAP, LIME, Feature Importance)
- Boas práticas de modelagem
- Arquitetura de projetos de dados e MLOps
- LLMs, embeddings, vetores e técnicas de RAG
- Estratégias avançadas de prompting

(Regras omitidas para reduzir o espaço…)
"""

# =====================================================================
# Função para validar a API Key fornecida pelo usuário
# =====================================================================

def validar_api_key(api_key: str):
    """
    Valida uma API Key da Groq chamando o endpoint de listagem de modelos.
    Retorna:
        (bool, str): (status_da_api, mensagem)
    """

    # Verifica se o campo está vazio
    if not api_key or api_key.strip() == "":
        return False, "API Key vazia. Insira uma para continuar."

    try:
        # Testa a chave chamando qualquer endpoint simples
        client = Groq(api_key=api_key)
        client.models.list()
        return True, "API Key válida!"
    except Exception:
        # Falha na autenticação ou na chamada
        return False, "API Key inválida ou não foi possível validar."

# =====================================================================
# Configurações gerais da página Streamlit
# =====================================================================

st.set_page_config(
    page_icon="⚡",
    page_title="AI Expert",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================================
# Inicialização do estado da sessão
# =====================================================================

if "show_sidebar" not in st.session_state:
    st.session_state.show_sidebar = True

if "api_valida" not in st.session_state:
    st.session_state.api_valida = False

if "messages" not in st.session_state:
    st.session_state.messages = []

# =====================================================================
# Sidebar – Configurações, API Key, limpeza de sessão
# =====================================================================

with st.sidebar:
    if st.session_state.show_sidebar:

        st.title("⚙️ Configurações")
        st.subheader("🔑 API")

        # Campo para o usuário inserir a chave da Groq
        groq_api_key = st.text_input(
            "Groq API Key",
            type="password",
            placeholder="Digite sua API Key..."
        )

        # Validação automática quando o usuário digita a chave
        if groq_api_key:
            valida, msg = validar_api_key(groq_api_key)
            if valida:
                st.success(msg)
                st.session_state.api_valida = True
            else:
                st.error(msg)
                st.session_state.api_valida = False
        else:
            st.warning("Digite sua API Key para continuar.")

        # Botão para limpar o histórico da conversa
        st.subheader("🧹 Sessão")
        if st.button("Limpar Conversa"):
            st.session_state["messages"] = []
            st.success("Conversa apagada!")

        # Créditos e footer
        st.markdown("---")
        st.caption("**ML Expert Chat** — Tudo sobre o mundo da IA.")
        st.caption("Desenvolvido por Daniel Coelho 🚀")

# =====================================================================
# Header estilizado do conteúdo principal
# =====================================================================

st.markdown("""
<div style="
    padding: 20px;
    background-color: #ffffffcc;
    backdrop-filter: blur(4px);
    border-radius: 12px;
    margin-bottom: 20px;
    border: 1px solid #e5e5e5;
">
    <h2>🧠 ML Expert Chat</h2>
    <p>Chat especializado em Machine Learning, Deep Learning, XAI e LLMs.</p>
</div>
""", unsafe_allow_html=True)

# =====================================================================
# Renderização das mensagens já enviadas
# =====================================================================

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# =====================================================================
# Bloqueia o chat enquanto não houver API Key válida
# =====================================================================

if not st.session_state.api_valida:
    st.warning("🔒 Insira sua API Key na barra lateral para liberar o chat.")
    st.stop()  # Impede execução do restante da página

# =====================================================================
# Inicializa o cliente Groq com a chave informada
# =====================================================================

client = Groq(api_key=groq_api_key)

# =====================================================================
# Entrada do usuário via st.chat_input()
# =====================================================================

if prompt := st.chat_input():

    # Salva a mensagem do usuário no histórico
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Renderiza visualmente a mensagem do usuário
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepara o histórico completo + system prompt
    message_api_key = [{"role": "system", "content": SYSTEM_PROMPT}]
    for msg in st.session_state.messages:
        message_api_key.append(msg)

    # Resposta do assistente
    with st.chat_message("assistant"):
        with st.spinner("⏳Pensando..."):
            try:
                # Chamada ao modelo da Groq
                chat_completion = client.chat.completions.create(
                    messages=message_api_key,
                    model="openai/gpt-oss-20b",
                    temperature=0.7,
                    max_tokens=2048,
                )

                # Extrai resposta da API
                response = chat_completion.choices[0].message.content

                # Exibe no chat
                st.markdown(response)

                # Armazena no histórico
                st.session_state.messages.append(
                    {"role": "assistant", "content": response}
                )

            except Exception as e:
                st.error(f"Erro na API: {e}")
