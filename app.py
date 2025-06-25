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
                st.success(f"Bem-vindo, {usuarios[login_email]['nome']}!")
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
                st.success("Cadastro completo!")
                st.rerun()
        st.stop()

usuario = st.session_state.usuario
email = st.session_state.usuario_email
nivel = len(usuario["bilhetes"]) // 5 + 1

st.title(f"🎲 SorteX — Olá, {usuario['nome']}!")
st.markdown(f"🏅 Nível: {nivel} &nbsp;&nbsp;&nbsp; 💰 Rifacoins: {usuario['rifacoins']} &nbsp;&nbsp;&nbsp; 🎟️ Bilhetes: {len(usuario['bilhetes'])}")

if st.button("🚪 Sair"):
    st.session_state.clear()
    st.rerun()

try:
    valor = carregar_json(ARQ_PREMIO)["premio_do_dia"]
except:
    valor = "R$ 0,00"

st.markdown(f"""
<div style='background-color:#ffe600;padding:20px;border-radius:10px;text-align:center'>
    <h2 style='color:#000000;margin-bottom:10px;'>🎁 Prêmio de Hoje</h2>
    <h1 style='color:#d40000;font-size:60px;margin:10px 0;'>{valor}</h1>
    <p style='color:#555;font-size:13px;margin-top:-8px;'>o prêmio total será atualizado em breve</p>
    <p style='color:#333333;font-size:18px;'>Assista ao anúncio e participe automaticamente!</p>
</div>
""", unsafe_allow_html=True)

st.markdown("## 🚀 Ganhe Rifacoins e Bilhetes")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🎬 Assistir Anúncio")
    st.markdown("Assista a um vídeo curto e ganhe **+1 Rifacoin** automaticamente.")
    if st.button("▶️ Assistir agora"):
        st.markdown("[Clique aqui para assistir](https://www.profitableratecpm.com/xevfhnbgtr?key=3a03fde3a5386ae02c06b19a488d4e04)", unsafe_allow_html=True)
        usuario["rifacoins"] += 1
        salvar_json(ARQ_USUARIOS, usuarios)

with col2:
    st.markdown("### 📨 Indique Amigos")
    st.markdown("Compartilhe o link abaixo. Quando um amigo se cadastrar, você ganha **+1 bilhete**!")
    link = f"https://effective-space-trout-jj9ggqpvwwrqhqp69-8501.app.github.dev/?ref={email}"
    st.text_input("Seu link de indicação", value=link, disabled=True, label_visibility="collapsed")

with col3:
    st.markdown("### ⭐ Avalie o SorteX")
    st.markdown("Avalie nosso app na Play Store e receba **+1 bilhete** como agradecimento.")
    if not usuario.get("avaliou", False):
        if st.button("🌟 Avaliar agora"):
            st.markdown("[Avaliar na Play Store](https://play.google.com)", unsafe_allow_html=True)
            if st.checkbox("✅ Já avaliei com 5 estrelas"):
                novo = random.randint(1000, 9999)
                usuario["bilhetes"].append(novo)
                usuario["avaliou"] = True
                salvar_json(ARQ_USUARIOS, usuarios)
                st.success(f"🎟️ Bilhete #{novo} adicionado com sucesso!")
    else:
        st.info("✅ Obrigado por avaliar!")

if st.button("🔁 Trocar 10 Rifacoins por 1 Bilhete"):
    if usuario["rifacoins"] >= 10:
        usuario["rifacoins"] -= 10
        novo = random.randint(1000, 9999)
        usuario["bilhetes"].append(novo)
        salvar_json(ARQ_USUARIOS, usuarios)
        st.success(f"Novo bilhete gerado: #{novo}")
    else:
        st.warning("Você precisa de 10 Rifacoins.")

if st.button("📜 Ver bilhetes"):
    if usuario["bilhetes"]:
        st.code(", ".join(map(str, usuario["bilhetes"])))
    else:
        st.info("Você ainda não tem bilhetes.")

if st.button("🎯 Sortear"):
    if usuario["bilhetes"]:
        with st.spinner("Sorteando..."):
            time.sleep(2)
        vencedor = random.choice(usuario["bilhetes"])
        st.success(f"🎉 Bilhete sorteado: #{vencedor}")
        usuario["rifacoins"] = 0
        usuario["bilhetes"] = []
        salvar_json(ARQ_USUARIOS, usuarios)

        ganhadores.append({
            "nome": usuario["nome"],
            "bilhete": vencedor,
            "data": datetime.now().strftime("%d/%m/%Y")
        })
        salvar_json(ARQ_GANHADORES, ganhadores)
        st.balloons()
    else:
        st.warning("Você precisa de bilhetes para sortear.")

st.markdown("## 🏆 Últimos ganhadores")
if ganhadores:
    for g in reversed(ganhadores[-5:]):
        st.markdown(f"🎉 **{g['nome']}** — bilhete #{g['bilhete']} em {g['data']}")
else:
    st.info("Ainda não houve ganhadores registrados.")
