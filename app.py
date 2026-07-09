import streamlit as st
import time

# Importando os nossos módulos (MVC)
from model.trello_api import buscar_cards, buscar_listas, concluir_card, criar_card
from model.game_state import iniciar_estado_jogo, ganhar_xp
from views.ui import desenhar_cabecalho, desenhar_status_heroi, analisar_monstro, desenhar_historico

# Configuração Base
st.set_page_config(page_title="TDAH Quest", page_icon="⚔️", layout="wide")
iniciar_estado_jogo()

# Autenticação Segura via Sidebar
st.sidebar.header("🔐 Cofre de Credenciais")
TOKEN = st.sidebar.text_input("Seu Token do Trello:", type="password")
ID_DO_QUADRO = st.sidebar.text_input("ID do Quadro:", value="qF36LXf1")

if not TOKEN:
    st.info("👋 Bem-vindo ao TDAH Quest! Por favor, insira o seu Token do Trello no menu lateral esquerdo para carregar a sua arena.")
    st.stop()

# Renderizando a Tela
desenhar_cabecalho()
col_esq, col_dir = st.columns([2, 1])

# --- CONTROLADOR: ÁREA DOS MONSTROS ---
with col_esq:
    st.write("### 👹 Monstros na Arena")
    cards = buscar_cards(TOKEN, ID_DO_QUADRO)
    
    if not cards:
        st.info("⚔️ A arena está limpa!")
        
    for card in cards:
        nome, tipo, recompensa, sprite, dificuldade = analisar_monstro(card)
        
        with st.expander(f"{tipo} -> {nome[:50]}...", expanded=True):
            c1, c2 = st.columns([1, 3])
            c1.code(sprite, language="text")
            c2.markdown(f"**Quest:** {nome}\n\n💎 **Recompensa:** +{recompensa} XP")
            
            if c2.button(f"⚔️ Derrotar Monstro", key=f"btn_{card['id']}"):
                if concluir_card(TOKEN, card['id']):
                    st.toast("💥 Ataque Crítico!", icon="💥")
                    subiu_de_nivel = ganhar_xp(recompensa, nome, dificuldade)
                    if subiu_de_nivel:
                        st.toast("🌟 SUBISTE DE NÍVEL!", icon="🎉")
                    st.balloons()
                    time.sleep(1.5)
                    st.rerun()

    desenhar_historico()

# --- CONTROLADOR: PAINEL DIREITO ---
with col_dir:
    desenhar_status_heroi()
    
    st.write("### ➕ Invocador de Quests")
    colunas_trello = buscar_listas(TOKEN, ID_DO_QUADRO)
    
    with st.form("form_criar_card", clear_on_submit=True):
        nova_tarefa = st.text_input("Nome da Missão:")
        prioridade = st.selectbox("Nível do Inimigo:", ["Fácil", "Média", "Urgente"])
        
        id_lista_final = None
        if colunas_trello:
            coluna_escolhida = st.selectbox("Invoque em qual Coluna?", list(colunas_trello.keys()))
            id_lista_final = colunas_trello[coluna_escolhida]
            
        if st.form_submit_button("✨ Invocar"):
            if not nova_tarefa or not id_lista_final:
                st.warning("Preencha o nome e selecione uma coluna válida.")
            else:
                cor_label = "red" if prioridade == "Urgente" else "yellow" if prioridade == "Média" else "green"
                if criar_card(TOKEN, id_lista_final, nova_tarefa, cor_label):
                    st.success(f"Monstro '{nova_tarefa}' criado!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Falha ao criar o cartão na API.")