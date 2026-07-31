import streamlit as st
import os
import json

st.set_page_config(page_title="Plataforma de Ejercicios", page_icon="💻")

st.title("💻 Plataforma de Ejercicios de Programación")

# --- Registro básico (sin verificación todavía) ---
st.subheader("Registro")
nombre = st.text_input("Nombre completo: ")
correo = st.text_input("Correo institucional (@ucn.cl): ")

if nombre and correo:
    st.success(f"Bienvenido/a, {nombre} 👋")

    # --- Mostrar el ejercicio de ejemplo ---
    st.subheader("Ejercicio 1: Lógica")

    ruta_ejercicio = "secciones/01_logica/ejercicio_01"

    with open(os.path.join(ruta_ejercicio, "enunciado.md"), "r", encoding="utf-8") as f:
        enunciado = f.read()

    st.markdown(enunciado)

    respuesta = st.text_area("Escribe tu código Python aquí")

    if st.button("Ver casos de prueba"):
        with open(os.path.join(ruta_ejercicio, "casos.json"), "r", encoding="utf-8") as f:
            casos = json.load(f)
        st.json(casos)
else:
    st.info("Completa tu nombre y correo para comenzar.")