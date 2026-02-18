import streamlit as st
import time
import random
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Check-in Cognitivo", layout="centered")

st.title("🧠 Check-in Cognitivo de Segurança")
st.write("Teste rápido de atenção (≈2 minutos)")

nome = st.text_input("Digite seu nome ou matrícula")

# estados
if "fase" not in st.session_state:
st.session_state.fase = "inicio"
st.session_state.rodada = 0
st.session_state.tempos = []
st.session_state.inicio_estimulo = 0

# iniciar teste
if st.button("Iniciar Teste"):
st.session_state.rodada = 1
st.session_state.tempos = []
st.session_state.fase = "espera"
st.rerun()

# FASE ESPERA (tela cinza)
if st.session_state.fase == "espera":

st.write(f"Rodada {st.session_state.rodada}/5")
st.info("Aguarde a tela ficar VERDE...")

delay = random.uniform(2,5)
time.sleep(delay)

st.session_state.fase = "estimulo"
st.session_state.inicio_estimulo = time.time()
st.rerun()

# FASE ESTÍMULO (tempo começa aqui)
if st.session_state.fase == "estimulo":

st.success("CLIQUE RÁPIDO AGORA!")

if st.button("CLIQUE!"):
tempo = (time.time() - st.session_state.inicio_estimulo) * 1000
st.session_state.tempos.append(tempo)

st.write(f"Tempo: {int(tempo)} ms")

if st.session_state.rodada < 5:
st.session_state.rodada += 1
st.session_state.fase = "espera"
else:
st.session_state.fase = "resultado"

st.rerun()

# RESULTADO FINAL
if st.session_state.fase == "resultado":

tempos = st.session_state.tempos
media = sum(tempos)/len(tempos)
desvio = pd.Series(tempos).std()

st.subheader("Resultado")
st.write(f"Tempo médio: {int(media)} ms")
st.write(f"Variabilidade: {int(desvio)}")

# classificação real
if media <= 280 and desvio <= 40:
st.success("🟢 PRONTIDÃO IDEAL")
elif media <= 350 and desvio <= 70:
st.warning("🟡 ATENÇÃO")
else:
st.error("🔴 RISCO")
