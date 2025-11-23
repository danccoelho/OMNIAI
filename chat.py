import streamlit as st
from groq import Groq

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

REGRAS IMPORTANTES:
1. Explique conceitos de forma clara, objetiva e técnica.
2. Sempre forneça exemplos práticos ou trechos de código relevantes.
3. Quando o usuário pedir análise de um modelo, pipeline ou dataset, solicite as informações necessárias.
4. Evite respostas genéricas: responda com profundidade e raciocínio estruturado.
5. Se a pergunta for incompleta, peça esclarecimentos antes de responder.
6. Mantenha tom profissional, didático e acessível.
7. Ao explicar algoritmos, detalhe:
   - Objetivo
   - Como funciona
   - Vantagens
   - Limitações
   - Hiperparâmetros essenciais
8. Ao explicar métricas, sempre forneça um exemplo numérico simples.
9. Não invente bibliotecas, funções ou sintaxes inexistentes.
10. Responda sempre em português do Brasil.
11. Priorize exemplos reais encontrados em equipes de Machine Learning no mercado.

ORIENTAÇÃO ADICIONAL:
- Quando apropriado, ofereça comparações entre ML clássico e LLMs.
- Mostre quando embeddings, RAG ou LLMs podem substituir ou complementar técnicas tradicionais.

OBJETIVO FINAL:
Ajudar o usuário a compreender profundamenteMachine Learning, Deep Learning, MLOps e LLMs, interpretar modelos, tomar melhores decisões técnicas e aprimorar soluções de IA com precisão, clareza e boas práticas.
"""

def validar_api_key(api_key: str):
    if not api_key or api_key.strip() == "":
        return False, "API Key vazia. Insira uma para continuar."

    try:
        client = Groq(api_key=api_key)
        client.models.list()    
        return True, "API Key válida!"
    except Exception:
        return False, "API Key inválida ou não foi possível validar."


st.set_page_config(
    page_icon= "⚡",
    page_title= "AI Expert",
    layout= "wide",
    initial_sidebar_state="expanded"
)

if "show_sidebar" not in st.session_state:
    st.session_state.show_sidebar = True

if "api_valida" not in st.session_state:
    st.session_state.api_valida = False

if "messages" not in st.session_state:
  st.session_state.messages = []


with st.sidebar:

  if st.session_state.show_sidebar:
    st.title("⚙️ Configurações")
    st.subheader("🔑 API")
    groq_api_key = st.text_input(
            "Groq API Key",
            type="password",
            placeholder="Digite sua API Key..."
    )
    
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

    st.subheader("🧹 Sessão")
    if st.button("Limpar Conversa"):
        st.session_state["messages"] = []
        st.success("Conversa apagada!")

    st.markdown("---")
    st.caption("**AI Expert Chat** — Assistente especializado em Machine Learning, XAI e LLMs.")
    st.caption("Desenvolvido por Daniel Coelho 🚀")


st.title("IA Expert chat")

for message in st.session_state.messages:
  with st.chat_message(message["role"]):
    st.markdown(message["content"])

if not st.session_state.api_valida:
    st.warning("🔒 Insira sua API Key na barra lateral para liberar o chat.")
    st.stop()

client = Groq(api_key=groq_api_key)

if prompt := st.chat_input():
  st.session_state.messages.append({"role": "user", "content": prompt})

  with st.chat_message("user"):
    st.markdown(prompt)
  
  message_api_key = [{"role": "system", "content": SYSTEM_PROMPT}]
  for msg in st.session_state.messages:
    message_api_key.append(msg)

  with st.chat_message("assistant"):
    with st.spinner("⏳Pensando..."):
            try:
              chat_completion = client.chat.completions.create(
                messages = message_api_key,
                model = "openai/gpt-oss-20b",
                temperature = 0.7,
                max_tokens = 204,
              )
              response =  chat_completion.choices[0].message.content
              st.markdown(response)
              st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
              st.error(f"Erro na API: {e}")
