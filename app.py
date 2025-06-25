# ... [o início do código permanece igual até o bloco de "st.title()"]

st.title(f"🎲 SorteX — Olá, {usuario['nome']}!")
st.markdown(f"🏅 Nível: {nivel} &nbsp;&nbsp;&nbsp; 💰 Rifacoins: {usuario['rifacoins']} &nbsp;&nbsp;&nbsp; 🎟️ Bilhetes: {len(usuario['bilhetes'])}")

if st.button("🚪 Sair"):
    st.session_state.clear()
    st.rerun()

# Bloco do prêmio em destaque
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
    st.markdown("Assista a um vídeo curto e ganhe **+1 Rifacoin** automaticamente.")
    if st.button("▶️ Assistir agora"):
        st.markdown("[Clique aqui para assistir](https://www.profitableratecpm.com/xevfhnbgtr?key=3a03fde3a5386ae02c06b19a488d4e04)", unsafe_allow_html=True)
        usuario["rifacoins"] += 1
        salvar_json(ARQ_USUARIOS, usuarios)
    st.markdown("<hr style='border:1px dashed lightgray;'>", unsafe_allow_html=True)

with col2:
    st.markdown("### 📨 Indique Amigos")
    st.markdown("Compartilhe o link e ganhe **+1 bilhete**!")
    link = f"https://effective-space-trout-jj9ggqpvwwrqhqp69-8501.app.github.dev/?ref={email}"
    st.text_input("Seu link de indicação", value=link, disabled=True, label_visibility="collapsed")
    st.markdown("<hr style='border:1px dashed lightgray;'>", unsafe_allow_html=True)

with col3:
    st.markdown("### ⭐ Avalie o SorteX")
    st.markdown("Avalie nosso app na Play Store e receba **+1 bilhete**")
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

# Trocar Rifacoins e Ver Bilhetes lado a lado
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

# Botão de sorteio com destaque
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
        st.warning("Você precisa de bilhetes para sortear.")

# Últimos ganhadores
st.markdown("## 🏆 Últimos ganhadores")
if ganhadores:
    for g in reversed(ganhadores[-5:]):
        st.markdown(f"🎉 **{g['nome']}** — bilhete #{g['bilhete']} em {g['data']}")
else:
    st.info("Ainda não houve ganhadores registrados.")
