import streamlit as st
from supabase import create_client

DOMINIO_PERMITIDO = "@alumnos.ucn.cl"


@st.cache_resource
def obtener_cliente():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)


def correo_valido(correo):
    return correo.strip().lower().endswith(DOMINIO_PERMITIDO)


def enviar_codigo(correo):
    cliente = obtener_cliente()
    cliente.auth.sign_in_with_otp({"email": correo})


def verificar_codigo(correo, codigo):
    cliente = obtener_cliente()
    resultado = cliente.auth.verify_otp({
        "email": correo,
        "token": codigo,
        "type": "email"
    })
    return resultado