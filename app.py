import streamlit as st
import time
import random
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Check-in Cognitivo", layout="centered")

st.title("🧠 Check-in Cognitivo de Segurança")
st.write("Teste rápido de atenção (≈2 minutos)")

nome = st.text_input("Digite seu nome ou matrícula")

if "rodada" not in st.session_state:
    st.session_state.rodada = 0
    st.session_state.tempos = []
    st.session_state.iniciado = False

if st.button("Iniciar Teste"):
    st.session_state.iniciado = True
    st.session_state.rodada = 1
    st.session_state.tempos = []

if st.session_state.iniciado and st.session_state.rodada <= 5:

    st.write(f"Rodada {st.session_state.rodada}/5")

    delay = random.uniform(2,5)
    time.sleep(delay)

    start_time = time.time()
    if st.button("CLIQUE RÁPIDO AGORA!"):
        reaction_time = (time.time() - start_time) * 1000
        st.session_state.tempos.append(reaction_time)
        st.success(f"Tempo: {int(reaction_time)} ms")
        st.session_state.rodada += 1
        st.experimental_rerun()

if st.session_state.rodada > 5:

    tempos = st.session_state.tempos
    media = sum(tempos)/len(tempos)
    desvio = pd.Series(tempos).std()
    indice = 1/(media*desvio)

    df = pd.DataFrame([{
        "nome": nome,
        "data": datetime.now(),
        "media_ms": media,
        "desvio": desvio,
        "indice": indice
    }])

    df.to_csv("resultados.csv", mode="a", header=False, index=False)

    st.subheader("Resultado")
    st.write(f"Tempo médio: {int(media)} ms")
    st.write(f"Variabilidade: {int(desvio)}")
    st.write(f"Índice de Atenção: {round(indice,6)}")

    st.success("Teste concluído!")
