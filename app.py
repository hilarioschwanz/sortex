import streamlit as st
import json
import os
import random
import time

st.set_page_config(page_title="SorteX", layout="centered")
ARQUIVO_USUARIOS = "usuarios.json"

# Carrega usuários salvos
if os.path.exists(ARQUIVO_USUARIOS):
    with open(ARQUIVO_USUARIOS, "r") as f:
        usuarios = json.load(f)
else:
    usuarios = {}

def salvar_dados():
    with open(ARQUIVO_USUARIOS, "w") as f:
        json.dump(usuarios, f)

# Sessão
if "logado" not in st.session_state:
    st.session_state.logado = False

if not st.session_state.logado:
    tipo = st.radio("👤 Acesso:", ["Já tenho conta", "Criar nova conta"])

    if tipo == "Já tenho conta":
        login_email = st.text_input("📧 E-mail")
        senha = st.text_input("🔑 Senha", type="password")

        if st.button("🔓 Entrar"):
            if login_email in usuarios:
                if usuarios[login_email]["senha"] == senha:
                    st.session_state.usuario = usuarios[login_email]
                    st.session_state.usuario_email = login_email
                    st.session_state.logado = True
                    st.success(f"Bem-vindo de volta, {usuarios[login_email]['nome']}!")
                    st.rerun()
                else:
                    st.error("Senha incorreta.")
            else:
                st.error("E-mail não cadastrado.")
        st.stop()

    else:
        st.markdown("### ✍️ Cadastro")
        nome = st.text_input("👤 Nome completo:")
        email = st.text_input("📧 E-mail para login:")
        telefone = st.text_input("📱 Telefone:")
        senha = st.text_input("🔑 Crie uma senha", type="password")

        if "captcha1" not in st.session_state:
            st.session_state.captcha1 = random.randint(1, 9)
        if "captcha2" not in st.session_state:
            st.session_state.captcha2 = random.randint(1, 9)

        captcha = st.text_input(f"🤖 Quanto é {st.session_state.captcha1} + {st.session_state.captcha2}?")

        if st.button("✅ Finalizar Cadastro"):
            erros = []
            if not nome.strip():
                erros.append("Nome obrigatório.")
            if "@" not in email or "." not in email:
                erros.append("E-mail inválido.")
            if email in usuarios:
                erros.append("E-mail já cadastrado. Faça login.")
            if not telefone.strip().isdigit() or len(telefone.strip()) < 8:
                erros.append("Telefone inválido.")
            if not senha.strip():
                erros.append("Senha obrigatória.")
            if not captcha.strip().isdigit() or int(captcha) != (
                st.session_state.captcha1 + st.session_state.captcha2):
                erros.append("Captcha incorreto.")

            if erros:
                st.warning("⚠️ Corrija os erros:")
                for e in erros:
                    st.markdown(f"- {e}")
            else:
                usuarios[email] = {
                    "nome": nome,
                    "telefone": telefone,
                    "senha": senha,
                    "rifacoins": 0,
                    "bilhetes": []
                }
                salvar_dados()
                st.session_state.usuario = usuarios[email]
                st.session_state.usuario_email = email
                st.session_state.logado = True
                del st.session_state.captcha1
                del st.session_state.captcha2
                st.success("✅ Cadastro realizado com sucesso!")
                st.rerun()
        st.stop()

# Usuário logado
usuario = st.session_state.usuario
email = st.session_state.usuario_email

st.title(f"🎲 SorteX — Olá, {usuario['nome']}!")
st.markdown(f"💰 Rifacoins: {usuario['rifacoins']} &nbsp;&nbsp;&nbsp;&nbsp; 🎟️ Bilhetes: {len(usuario['bilhetes'])}")
st.markdown("___")

if st.button("🚪 Sair"):
    st.session_state.clear()
    st.rerun()

# Destaque do prêmio do dia
try:
    with open("premio.json", "r") as f:
        valor = json.load(f)["premio_do_dia"]
except:
    valor = "R$ 5,00"

st.markdown(f"""
<div style='background-color:#ffe600;padding:20px;border-radius:10px;text-align:center'>
    <h2 style='color:#000000;margin-bottom:10px;'>🎁 Prêmio Total</h2>
    <h1 style='color:#d40000;font-size:60px;margin:10px 0;'>{valor}</h1>
    <p style='color:#555;font-size:13px;margin-top:-8px;'>o prêmio total será atualizado em breve</p>
    <p style='color:#333333;font-size:18px;'>Assista ao anúncio e participe automaticamente!</p>
</div>
""", unsafe_allow_html=True)

# Ações
st.markdown("## 🎥 Anúncio Patrocinado")
if st.button("▶️ Assistir agora"):
    st.markdown("[👉 Clique aqui para assistir ao anúncio](https://www.profitableratecpm.com/xevfhnbgtr?key=3a03fde3a5386ae02c06b19a488d4e04)", unsafe_allow_html=True)
    usuario["rifacoins"] += 1
    usuarios[email] = usuario
    salvar_dados()

if st.button("🔁 Trocar 10 Rifacoins por 1 Bilhete"):
    if usuario["rifacoins"] >= 10:
        usuario["rifacoins"] -= 10
        bilhete = random.randint(1000, 9999)
        usuario["bilhetes"].append(bilhete)
        usuarios[email] = usuario
        salvar_dados()
        st.success(f"🎟️ Novo bilhete: #{bilhete}")
    else:
        st.warning("Você precisa de 10 Rifacoins.")

if st.button("📜 Ver bilhetes"):
    if usuario["bilhetes"]:
        st.info("Seus bilhetes:")
        st.code(", ".join(map(str, usuario["bilhetes"])))
    else:
        st.info("Você ainda não tem bilhetes.")

st.markdown("___")

if st.button("🎯 Sortear"):
    if usuario["bilhetes"]:
        with st.spinner("Girando..."):
            time.sleep(2)
        vencedor = random.choice(usuario["bilhetes"])
        st.success(f"🎉 Bilhete sorteado: #{vencedor}! Parabéns!")
        usuario["rifacoins"] = 0
        usuario["bilhetes"] = []
        usuarios[email] = usuario
        salvar_dados()
        st.balloons()
    else:
        st.warning("Você precisa de pelo menos 1 bilhete.")
