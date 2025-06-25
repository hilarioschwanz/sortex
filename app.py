import streamlit as st
import json
import os
import random
import time
from datetime import datetime

st.set_page_config(page_title="SorteX", layout="centered")

ARQ_USUARIOS = "usuarios.json"
ARQ_GANHADORES = "ganhadores.json"
ARQ_INDICACOES = "indicacoes.json"
ARQ_PREMIO = "premio.json"

def carregar_json(arq):
    return json.load(open(arq)) if os.path.exists(arq) else ({} if "usuarios" in arq or "indicacoes" in arq else [])

def salvar_json(arq, dados):
    with open(arq, "w") as f:
        json.dump(dados, f)

usuarios = carregar_json(ARQ_USUARIOS)
ganhadores = carregar_json(ARQ_GANHADORES)
indicacoes = carregar_json(ARQ_INDICACOES)
ref = st.query_params.get("ref", [None])[0]

if "logado" not in st.session_state:
    st.session_state.logado = False

if not st.session_state.logado:
    tipo = st.radio("👤 Acesso:", ["Já tenho conta", "Criar conta"])

    if tipo == "Já tenho conta":
        login_email = st.text_input("📧 E-mail")
        senha = st.text_input("🔑 Senha", type="password")
        if st.button("🔓 Entrar"):
            if login_email in usuarios and usuarios[login_email]["senha"] == senha:
                st.session_state.usuario = usuarios[login_email]
                st.session_state.usuario_email = login_email
                st.session_state.logado = True
                st.rerun()
            else:
                st.error("E-mail ou senha inválidos.")
        st.stop()
    else:
        st.markdown("### ✍️ Cadastro")
        nome = st.text_input("Nome")
        email = st.text_input("E-mail")
        telefone = st.text_input("Telefone")
        senha = st.text_input("Senha", type="password")
        captcha = st.text_input("Quanto é 3 + 4?")

        if st.button("✅ Finalizar Cadastro"):
            erros = []
            if not nome or not email or "@" not in email:
                erros.append("Dados inválidos.")
            if email in usuarios:
                erros.append("E-mail já cadastrado.")
            if captcha.strip() != "7":
                erros.append("Captcha incorreto.")
            if erros:
                for e in erros:
                    st.warning(e)
            else:
                usuarios[email] = {
                    "nome": nome,
                    "telefone": telefone,
                    "senha": senha,
                    "rifacoins": 0,
                    "bilhetes": [],
                    "avaliou": False
                }
                if ref and ref in usuarios and ref != email:
                    usuarios[ref]["bilhetes"].append(random.randint(1000, 9999))
                    indicacoes[email] = ref
                    salvar_json(ARQ_INDICACOES, indicacoes)

                salvar_json(ARQ_USUARIOS, usuarios)
                st.session_state.usuario = usuarios[email]
                st.session_state.usuario_email = email
                st.session_state.logado = True
                st.rerun()
        st.stop()
