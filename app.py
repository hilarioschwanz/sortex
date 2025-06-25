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

if not all(k in st.session_state for k in ("usuario", "usuario_email")):
    st.error("Erro ao recuperar sessão. Por favor, faça login novamente.")
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
<div style='background-color:#ffecb3;padding:20px;border-radius:10px;text-align:center'>
    <h2 style='color:#d40000'>🎁 Prêmio de Hoje</h2>
    <h1 style='font-size:50px;color:#000'>{valor}</h1>
    <p style='color:#333;font-size:18px;'>Assista ao anúncio e participe automaticamente!</p>
</div>
""", unsafe_allow_html=True)

st.markdown("## 🚀 Ganhe Rifacoins e Bilhetes")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🎬 Assistir Anúncio")
    st.markdown("Assista e ganhe **+1 Rifacoin**.")
    if st.button("▶️ Assistir agora"):
        st.markdown("[Clique aqui para assistir](https://www.profitableratecpm.com/xevfhnbgtr?key=3a03fde3a5386ae02c06b19a488d4e04)", unsafe_allow_html=True)
        usuario["rifacoins"] += 1
        salvar_json(ARQ_USUARIOS, usuarios)
    st.markdown("<hr style='border:1px dashed lightgray;'>", unsafe_allow_html=True)

with col2:
   link = f"{st.get_url()}?ref={email}"

st.markdown("### 📨 Indique Amigos")
st.markdown("Clique no campo abaixo para copiar automaticamente seu link de indicação!")

st.markdown(f"""
<input type="text" value="{link}" id="linkCopiavel" readonly onclick="this.select();document.execCommand('copy');" 
style="width:100%;padding:10px;border-radius:5px;border:1px solid lightgray;color:#333;font-weight:bold;text-align:center">

<p style="text-align:center;font-size:14px;color:green;">✅ Copiado ao clicar!</p>

<p style='text-align:center;margin-top:10px'>
<a href="https://wa.me/?text=Ei!%20Cadastre-se%20no%20SorteX%20e%20tente%20a%20sorte%20com%20esse%20link%3A%20{link}" 
target="_blank" style="text-decoration:none;color:white;background-color:#25D366;padding:10px 20px;border-radius:5px;display:inline-block">
📲 Compartilhar no WhatsApp
</a>
</p>
""", unsafe_allow_html=True)

with col3:
    st.markdown("### ⭐ Avalie o SorteX")
    st.markdown("Avalie e ganhe **+1 bilhete**!")
    if not usuario.get("avaliou", False):
        if st.button("🌟 Avaliar agora"):
            st.markdown("[Avaliar na Play Store](https://play.google.com)", unsafe_allow_html=True)
            if st.checkbox("✅ Já avaliei com 5 estrelas"):
                novo = random.randint(1000, 9999)
                usuario["bilhetes"].append(novo)
                usuario["avaliou"] = True
                salvar_json(ARQ_USUARIOS, usuarios)
                st.success(f"🎟️ Bilhete #{novo} adicionado!")
    else:
        st.info("✅ Obrigado por avaliar!")

st.markdown("## 🎟️ Bilhetes e Rifas")
col_a, col_b = st.columns(2)

with col_a:
    if st.button("🔁 Trocar 10 Rifacoins por 1 Bilhete"):
        if usuario["rifacoins"] >= 10:
            usuario["rifacoins"] -= 10
            novo = random.randint(1000, 9999)
            usuario["bilhetes"].append(novo)
            salvar_json(ARQ_USUARIOS, usuarios)
            st.success(f"Novo bilhete gerado: #{novo}")
        else:
            st.warning("Você precisa de 10 Rifacoins.")

with col_b:
    if st.button("📜 Ver bilhetes"):
        if usuario["bilhetes"]:
            st.code(", ".join(map(str, usuario["bilhetes"])))
        else:
            st.info("Você ainda não tem bilhetes.")

st.markdown("## 🧨 Pronto para testar a sorte?")
st.markdown(f"<h2 style='text-align:center;color:#d40000;'>🎯 SORTEIO DO DIA</h2>", unsafe_allow_html=True)
st.markdown(f"<h1 style='text-align:center;font-size:48px;color:#000'>{valor}</h1>", unsafe_allow_html=True)

if st.button("🎉 PARTICIPAR DO SORTEIO", use_container_width=True):
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
        st.warning("Você precisa de bilhetes.")

st.markdown("## 🏆 Últimos ganhadores")
if ganhadores:
    for g in reversed(ganhadores[-5:]):
        st.markdown(f"🎉 **{g['nome']}** — bilhete #{g['bilhete']} em {g['data']}")
else:
    st.info("Ainda não houve ganhadores registrados.")
