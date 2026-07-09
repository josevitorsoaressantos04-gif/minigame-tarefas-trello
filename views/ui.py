import streamlit as st
import pandas as pd

def desenhar_cabecalho():
    st.title("⚔️ TDAH Quest: Arena do Quadro")
    st.caption("Transforme obrigações do Trello em batalhas reais de RPG por dopamina!")

def desenhar_status_heroi():
    st.write("### 📊 Status do Herói")
    st.metric(label="Nível Atual", value=f"LVL {st.session_state.level}")
    st.metric(label="Dopamina XP", value=f"{st.session_state.xp} XP")
    st.progress(min((st.session_state.xp % 100) / 100.0, 1.0))
    st.markdown("---")

def analisar_monstro(card):
    nome_tarefa = card.get("name")
    if not nome_tarefa and "data" in card:
        nome_tarefa = card["data"].get("card", {}).get("name")
    nome_tarefa = nome_tarefa or "⚔️ Missão Secreta"

    labels = card.get("labels", [])
    cor_etiqueta = labels[0]["color"] if labels else "green"
    
    if cor_etiqueta == "red":
        return nome_tarefa, "👹 CHEFÃO URGENTE", 50, "┌( 🔴_🔴 )┐\n  └──(⚔️)──┘", "Urgente"
    elif cor_etiqueta == "yellow":
        return nome_tarefa, "👾 Monstro de Elite", 30, " ⎧[☉_☉]⎫\n  └──(⚡)──┘", "Média"
    else:
        return nome_tarefa, "🐛 Inseto de Rotina", 15, "  (•_•)\n <)   )⚡\n  /   \\", "Fácil"

def desenhar_historico():
    st.write("### 📜 Log de Aventuras (Histórico)")
    if st.session_state.historico_missoes:
        st.dataframe(pd.DataFrame(st.session_state.historico_missoes), use_container_width=True)
    else:
        st.info("Nenhuma missão concluída nesta sessão ainda.")