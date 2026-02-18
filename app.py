import streamlit as st
import time
import random
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Check-in Cognitivo", layout="centered")

st.title("🧠 Check-in Cognitivo de Segurança")
st.write("Teste rápido de atenção (≈2 minutos)")

nome = st.text_input("Digite seu nome ou matrícula")

# estados da sessão
if "rodada" not in st.session_state:
    st.session_state.rodada = 0
    st.session_state.tempos = []
    st.session_state.iniciado = False
    st.session_state.start_time = 0

# botão iniciar
if st.button("Iniciar Teste"):
    st.session_state.iniciado = True
    st.session_state.rodada = 1
    st.session_state.tempos = []

# lógica das rodadas
if st.session_state.iniciado and st.session_state.rodada <= 5:

    st.write(f"Rodada {st.session_state.rodada}/5")

    # esperar tempo aleatório
    delay = random.uniform(2,5)
    time.sleep(delay)

    # registrar início
    st.session_state.start_time = time.time()

    if st.button("CLIQUE RÁPIDO AGORA!"):
        reaction_time = (time.time() - st.session_state.start_time) * 1000
        st.session_state.tempos.append(reaction_time)
        st.success(f"Tempo: {int(reaction_time)} ms")
        st.session_state.rodada += 1
        st.rerun()

# resultado final
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

# CLASSIFICAÇÃO TEMPO
if media <= 280:
    status_tempo = "bom"
elif media <= 350:
    status_tempo = "normal"
elif media <= 450:
    status_tempo = "ruim"
else:
    status_tempo = "critico"

# CLASSIFICAÇÃO VARIABILIDADE
if desvio <= 40:
    status_var = "estavel"
elif desvio <= 70:
    status_var = "medio"
else:
    status_var = "instavel"

# STATUS FINAL
if status_tempo == "bom" and status_var == "estavel":
    st.success("🟢 PRONTIDÃO IDEAL")
elif status_tempo in ["normal","ruim"] or status_var == "medio":
    st.warning("🟡 ATENÇÃO – atenção moderada")
else:
    st.error("🔴 RISCO – baixa prontidão cognitiva")

    st.success("Teste concluído!")
