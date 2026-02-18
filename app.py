import streamlit as st
import time
import random
import pandas as pd

st.set_page_config(page_title="Check-in Cognitivo", layout="centered")

st.title("🧠 Check-in Cognitivo de Segurança")
st.write("Teste rápido de atenção (≈2 minutos)")

nome = st.text_input("Digite seu nome ou matrícula")

# estados
if "rodada" not in st.session_state:
    st.session_state.rodada = 0
    st.session_state.tempos = []
    st.session_state.mostrar_botao = False
    st.session_state.inicio = 0

# iniciar teste
if st.button("Iniciar Teste"):
    st.session_state.rodada = 1
    st.session_state.tempos = []
    st.session_state.mostrar_botao = False

# rodadas
if st.session_state.rodada >= 1 and st.session_state.rodada <= 5:

    st.write(f"Rodada {st.session_state.rodada}/5")

if not st.session_state.mostrar_botao:
    st.info("Aguarde aparecer o botão...")
    delay = random.uniform(2,5)
    time.sleep(delay)
    st.session_state.mostrar_botao = True
    st.session_state.inicio = time.time()
    st.rerun()

if st.session_state.mostrar_botao:
    if st.button("CLIQUE AGORA!"):
        tempo = (time.time() - st.session_state.inicio) * 1000
        st.session_state.tempos.append(tempo)
        st.success(f"Tempo: {int(tempo)} ms")

        st.session_state.rodada += 1
        st.session_state.mostrar_botao = False
        st.rerun()

# resultado final
if st.session_state.rodada > 5:

    tempos = st.session_state.tempos
    media = sum(tempos)/len(tempos)
    desvio = pd.Series(tempos).std()

    st.subheader("Resultado")
    st.write(f"Tempo médio: {int(media)} ms")
    st.write(f"Variabilidade: {int(desvio)}")

    if media <= 280 and desvio <= 40:
        st.success("🟢 PRONTIDÃO IDEAL")
    elif media <= 350 and desvio <= 70:
        st.warning("🟡 ATENÇÃO")
    else:
        st.error("🔴 RISCO")
