import streamlit as st
import time
import random
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Check-in Cognitivo", layout="centered")

st.title("🧠 Check-in Cognitivo de Segurança")
st.write("Teste rápido de atenção (≈2 minutos)")

nome = st.text_input("Digite seu nome ou matrícula")

if st.button("Iniciar Teste"):

    tempos = []

    for i in range(5):
        st.write(f"Rodada {i+1}/5 - Aguarde a tela ficar VERDE")

        delay = random.uniform(2,5)
        time.sleep(delay)

        st.markdown("<h1 style='color:green;'>APERTE ENTER AGORA!</h1>", unsafe_allow_html=True)

        start_time = time.time()
        input("Pressione ENTER")
        reaction_time = (time.time() - start_time) * 1000

        tempos.append(reaction_time)
        st.success(f"Tempo: {int(reaction_time)} ms")

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
