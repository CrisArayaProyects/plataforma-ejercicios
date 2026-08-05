import streamlit as st
from streamlit_ace import st_ace
import os
import json
from corrector import corregir_ejercicio
from db import correo_valido, enviar_codigo, verificar_codigo

st.set_page_config(page_title="Plataforma de Ejercicios", page_icon="💻", layout="wide")

# --- Inicializar estado de sesión ---
if "vista" not in st.session_state:
    st.session_state.vista = "verificacion"
if "correo_pendiente" not in st.session_state:
    st.session_state.correo_pendiente = ""
if "nombre" not in st.session_state:
    st.session_state.nombre = ""
if "correo_verificado" not in st.session_state:
    st.session_state.correo_verificado = ""


# ============================================================
# VISTA: VERIFICACIÓN
# ============================================================
def vista_verificacion():
    st.title("💻 Plataforma de Ejercicios de Programación")
    st.subheader("Ingresa con tu correo institucional")

    # Paso 1: pedir correo, si aún no se envió código
    if not st.session_state.correo_pendiente:
        nombre = st.text_input("Nombre completo")
        correo = st.text_input("Correo institucional (@alumnos.ucn.cl)")

        if st.button("Enviar código"):
            if not nombre.strip():
                st.warning("Ingresa tu nombre.")
            elif not correo_valido(correo):
                st.error("Debes usar un correo que termine en @alumnos.ucn.cl")
            else:
                try:
                    enviar_codigo(correo)
                    st.session_state.correo_pendiente = correo.strip().lower()
                    st.session_state.nombre = nombre.strip()
                    st.success("Código enviado. Revisa tu correo.")
                    st.rerun()
                except Exception as e:
                    st.error(f"No se pudo enviar el código: {e}")

    # Paso 2: pedir el código, ya que se envió
    else:
        st.info(f"Código enviado a {st.session_state.correo_pendiente}")
        codigo = st.text_input("Código de 6 dígitos")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Verificar código"):
                try:
                    verificar_codigo(st.session_state.correo_pendiente, codigo)
                    st.session_state.correo_verificado = st.session_state.correo_pendiente
                    st.session_state.vista = "ejercicios"
                    st.rerun()
                except Exception as e:
                    st.error(f"Código incorrecto o expirado: {e}")
        with col2:
            if st.button("Usar otro correo"):
                st.session_state.correo_pendiente = ""
                st.rerun()


# ============================================================
# VISTA: EJERCICIOS
# ============================================================
def vista_ejercicios():
    with st.sidebar:
        st.write(f"👤 {st.session_state.nombre}")
        st.caption(st.session_state.correo_verificado)
        st.divider()
        st.page_link if False else None  # (placeholder, sin uso)
        if st.button("Cerrar sesión"):
            st.session_state.correo_verificado = ""
            st.session_state.correo_pendiente = ""
            st.session_state.vista = "verificacion"
            st.rerun()

    st.title("💻 Ejercicios")
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
                icono = "✅" if r["paso"] else "❌"
                st.write(f"Caso {r['caso']}: {icono} {r['detalle']}")


# ============================================================
# RUTEO PRINCIPAL
# ============================================================
if st.session_state.vista == "verificacion":
    vista_verificacion()
else:
    vista_ejercicios()