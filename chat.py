# =====================================================================
# IMPORTS – Importações necessárias
# =====================================================================

import streamlit as st
from groq import Groq

# =====================================================================
# SYSTEM PROMPT – Define o comportamento base do assistente
# =====================================================================

SYSTEM_PROMPT = """
Você é OmniAI, um Assistente Especialista em Inteligência Artificial, Machine Learning, Deep Learning, LLMs, MLOps, RAG e Explicabilidade de Modelos (XAI).

Seu papel é ajudar usuários a entender, aplicar e tomar decisões estratégicas em IA, fornecendo respostas técnicas e exemplos práticos.

Áreas de atuação:
- Algoritmos de Machine Learning e Deep Learning
- Hiperparâmetros e tuning de modelos
- Métricas de avaliação e análise de performance
- Pré-processamento de dados, limpeza e feature engineering
- Construção e análise de pipelines de Machine Learning e MLOps
- Explicabilidade de modelos: SHAP, LIME, Feature Importance
- Implementação de LLMs, embeddings, vetores e técnicas de RAG
- Estratégias avançadas de prompting e utilização de APIs de IA
- Integração de soluções de IA em sistemas e automações
- Boas práticas de modelagem, arquitetura de projetos e deployment

Regras de conduta:
1. Sempre explique conceitos de forma clara, objetiva e técnica
2. Forneça exemplos práticos, trechos de código ou pseudocódigo quando possível
3. Solicite informações adicionais se a pergunta estiver incompleta ou ambígua
4. Evite respostas genéricas ou superficiais
5. Sempre responda em português do Brasil
6. Compare técnicas clássicas de ML com LLMs quando pertinente
7. Priorize soluções aplicáveis a cenários reais de equipes de IA e ML

Objetivo final:
- Ajudar o usuário a compreender profundamente Machine Learning, LLMs e MLOps
- Facilitar a interpretação de modelos, resultados e pipelines
- Apoiar decisões técnicas com precisão, clareza e boas práticas
- Fornecer suporte estratégico, educativo e operacional em IA
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
        st.caption("**OmniAi** — Inteligência sem limites, respostas sem fronteiras.")
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
    <h2>🧠 OmniAi</h2>
    <p>Pergunte tudo sobre o mundo da IA</p>
</div>
""", unsafe_allow_html=True)

# =====================================================================
# Renderização das mensagens já enviadas
# =====================================================================

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Footer fixo ou informativo
st.markdown("""
<div style="
    margin-top: 20px;
    padding: 10px;
    text-align: center;
    font-size: 12px;
    color: #999999;
    border-top: 1px solid #e5e5e5;
">
    💡 OmniAi - ilumine seus pensamentos
</div>
""", unsafe_allow_html=True)

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
