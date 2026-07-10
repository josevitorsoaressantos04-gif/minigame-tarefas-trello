import streamlit as st
from model.database import save_state, save_log

def iniciar_estado_jogo():
    if "xp" not in st.session_state:
        st.session_state.xp = 0
    if "level" not in st.session_state:
        st.session_state.level = 1
    if "historico_missoes" not in st.session_state:
        st.session_state.historico_missoes = []

def ganhar_xp(recompensa, nome_missao, dificuldade):
    # 1. Atualiza na memória volátil do Streamlit
    st.session_state.xp += recompensa
    
    subiu_de_nivel = False
    # Exemplo simples de subir de nível a cada 100 XP
    if st.session_state.xp >= st.session_state.level * 100:
        st.session_state.level += 1
        subiu_de_nivel = True
        
    # 2. SALVA NO BANCO DE DADOS (Aqui a mágica acontece!)
    save_state(st.session_state.xp, st.session_state.level)
    
    # 3. GRAVA O LOG NO HISTÓRICO
    # Certifique-se de passar o nome correto: 'Logs do Sistema' ou o destino que preferir
    save_log(missao=nome_missao, dificuldade=dificuldade, xp_ganho=recompensa, destino="Trello")
    
    return subiu_de_nivel
    return True # Subiu de nível
    return False