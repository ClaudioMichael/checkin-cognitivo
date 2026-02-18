import streamlit as st
import time
import random
import pandas as pd

st.set_page_config(page_title="Check-in Cognitivo", layout="centered")

st.title("🧠 Check-in Cognitivo de Segurança")
st.write("Quando aparecer VERDE, pressione a tecla ESPAÇO rapidamente")

nome = st.text_input("Nome ou matrícula")

if "rodada" not in st.session_state:
    st.session_state.rodada = 0
    st.session_state.tempos = []
    st.session_state.inicio = 0
    st.session_state.ativo = False

if st.button("Iniciar Teste"):
    st.session_state.rodada = 1
    st.session_state.tempos = []
    st.session_state.ativo = True

if st.session_state.ativo and st.session_state.rodada <= 5:

    st.write(f"Rodada {st.session_state.rodada}/5")
    st.info("Aguarde a tela ficar verde...")

    delay = random.uniform(2,5)
    time.sleep(delay)

    st.success("PRESSIONE ESPAÇO AGORA!")
    st.session_state.inicio = time.time()

    tecla = st.text_input("Pressione ESPAÇO e ENTER")

    if tecla:
        tempo = (time.time() - st.session_state.inicio) * 1000
        st.session_state.tempos.append(tempo)
        st.write(f"Tempo: {int(tempo)} ms")

        st.session_state.rodada += 1
        st.rerun()

if st.session_state.rodada > 5:

    media = sum(st.session_state.tempos)/len(st.session_state.tempos)
    desvio = pd.Series(st.session_state.tempos).std()

    st.subheader("Resultado")
    st.write(f"Tempo médio: {int(media)} ms")
    st.write(f"Variabilidade: {int(desvio)}")

    if media <= 350 and desvio <= 80:
        st.success("🟢 PRONTIDÃO IDEAL")
    elif media <= 600 and desvio <= 150:
        st.warning("🟡 ATENÇÃO")
    else:
        st.error("🔴 RISCO")
