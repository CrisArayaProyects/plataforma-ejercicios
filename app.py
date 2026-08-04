import streamlit as st
from streamlit_ace import st_ace
import os
import json
from corrector import corregir_ejercicio

st.set_page_config(page_title="Plataforma de Ejercicios", page_icon="💻")

st.title("💻 Plataforma de Ejercicios de Programación")

# --- Registro básico (sin verificación todavía) ---
st.subheader("Registro")
nombre = st.text_input("Nombre completo")
correo = st.text_input("Correo institucional")

if nombre and correo:
    st.success(f"Bienvenido/a, {nombre} 👋")

    # --- Mostrar el ejercicio de ejemplo ---
    st.subheader("Ejercicio 1: Lógica")

    ruta_ejercicio = "secciones/01_logica/ejercicio_01"

    with open(os.path.join(ruta_ejercicio, "enunciado.md"), "r", encoding="utf-8") as f:
        enunciado = f.read()

    st.markdown(enunciado)

    st.write("Escribe tu código aquí:")
    codigo_alumno = st_ace(
        language="python",
        theme="monokai",
        placeholder="# Escribe tu solución aquí",
        height=250,
        key="editor_ejercicio_01"
    )

    if st.button("Corregir"):
        if not codigo_alumno or codigo_alumno.strip() == "":
            st.warning("Escribe algo de código antes de corregir.")
        else:
            with open(os.path.join(ruta_ejercicio, "casos.json"), "r", encoding="utf-8") as f:
                casos = json.load(f)["casos"]

            with st.spinner("Ejecutando y comparando resultados..."):
                resultados, aciertos, total = corregir_ejercicio(codigo_alumno, casos)

            if aciertos == total:
                st.success(f"✅ ¡Correcto! Pasaste los {total} casos de prueba.")
            else:
                st.error(f"❌ Pasaste {aciertos} de {total} casos.")

            for r in resultados:
                if r["paso"]:
                    st.write(f"Caso {r['caso']}: ✅ {r['detalle']}")
                else:
                    st.write(f"Caso {r['caso']}: ❌ {r['detalle']}")
else:
    st.info("Completa tu nombre y correo para comenzar.")