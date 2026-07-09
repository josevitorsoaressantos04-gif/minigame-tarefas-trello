import streamlit as st

def iniciar_estado_jogo():
    if "xp" not in st.session_state:
        st.session_state.xp = 0
    if "level" not in st.session_state:
        st.session_state.level = 1
    if "historico_missoes" not in st.session_state:
        st.session_state.historico_missoes = []

def ganhar_xp(recompensa, nome_tarefa, dif_texto):
    st.session_state.historico_missoes.append({
        "Missão": nome_tarefa,
        "Dificuldade": dif_texto,
        "XP Ganho": recompensa,
        "Status": "Concluído"
    })
    
    st.session_state.xp += recompensa
    if st.session_state.xp >= st.session_state.level * 100:
        st.session_state.level += 1
        return True # Subiu de nível
    return False