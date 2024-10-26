#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 20:19:08 2024

@author: franciscotafur
"""

# dudo_app.py

import streamlit as st
import math
from scipy.special import comb





# Functions from your original script

def proba(dados_incognita: int, dados_almenos: int) -> float:
    rta = 0
    for dado in range(dados_almenos, dados_incognita + 1):
        if dado == 0:
            continue
        x = comb(dados_incognita, dado)
        y = (1 / 3) ** dado
        z = (1 - (1 / 3)) ** (dados_incognita - dado)
        resultado = x * y * z
        rta += resultado
    return rta

def jugada_optima(dados_incognitos: int, jugada: int) -> dict:
    # Dudar
    probabilidad_perder_si_dudo = proba(dados_incognitos, jugada)
    valor_esperado_dudar = (-1) * probabilidad_perder_si_dudo

    # Calzar
    x = comb(dados_incognitos, jugada)
    y = (1 / 3) ** jugada
    z = (2 / 3) ** (dados_incognitos - jugada)
    probabilidad_calzar = x * y * z
    valor_esperado_calzar = (probabilidad_calzar * 1) + ((1 - probabilidad_calzar) * -2)

    # Seguirla
    probabilidad_perder_si_sigo = proba(dados_incognitos, jugada + 1)
    valor_esperado_seguirla = ((1 - probabilidad_perder_si_sigo) * -1)

    valor_esperado_dudar = round(valor_esperado_dudar, 2)
    valor_esperado_calzar = round(valor_esperado_calzar, 2)
    valor_esperado_seguirla = round(valor_esperado_seguirla, 2)

    rta = {
        "DUDAR": valor_esperado_dudar,
        "SEGUIRLA": valor_esperado_seguirla,
        "CALZAR": valor_esperado_calzar
    }

    return rta

# Streamlit App

st.title("Jugada Óptima de Dudo")
st.write("Este programa calcula la respuesta óptima en el juego Dudo basado en probabilidades.")

# User Inputs
st.header("Ingrese los datos de la partida:")
dados_totales = st.number_input("Cantidad de dados totales en juego:", min_value=1, step=1)
dados_en_mano = st.number_input("Cantidad de dados que tienes en tu vaso:", min_value=0, step=1, max_value=int(dados_totales))
jugada_recibida = st.number_input("Jugada recibida en dados:", min_value=1, step=1)
dados_en_mano_totales = st.number_input("Cantidad de dados en tu vaso que coinciden con la jugada recibida:", min_value=0, step=1, max_value=int(dados_en_mano))

if st.button("Calcular"):
    # Ensure inputs are integers
    dados_totales = int(dados_totales)
    dados_en_mano = int(dados_en_mano)
    jugada_recibida = int(jugada_recibida)
    dados_en_mano_totales = int(dados_en_mano_totales)

    dados_incognitos = dados_totales - dados_en_mano
    jugada_recibida_incognita = jugada_recibida - dados_en_mano_totales

    rta = jugada_optima(dados_incognitos, jugada_recibida_incognita)
    rta2 = jugada_optima(dados_incognitos, jugada_recibida)

    all_actions = {
        "DUDAR": rta["DUDAR"],
        "SEGUIRLA": rta2["SEGUIRLA"],
        "CALZAR": rta["CALZAR"]
    }

    # Display Results
    st.subheader("Resultados:")
    st.write(f"**Valor esperado de Dudar**: {rta['DUDAR']}")
    st.write(f"**Valor esperado de Seguirla** (decir {jugada_recibida + 1} de algo): {rta2['SEGUIRLA']}")
    st.write(f"**Valor esperado de Calzar**: {rta['CALZAR']}")

    maximo = max(all_actions.values())
    estrategias_maximas = [key for key, value in all_actions.items() if value == maximo]
    estrategia = estrategias_maximas[0]

    st.success(f"Estrategia recomendada: **{estrategia}**")
