import streamlit as st
from PIL import Image, ImageDraw
import io

# Configuração da Página
st.set_page_config(page_title="Dandan Studio Web", layout="wide")

# Estilo para o Banner Laranja
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        color: white;
        background-color: #e67e22;
        padding: 10px;
        border-radius: 10px;
        font-family: 'Arial Black';
    }
    </style>
    <h1 class='main-title'>DANDAN STUDIO WEB</h1>
    """, unsafe_allow_html=True)

# --- BARRA LATERAL (FERRAMENTAS) ---
st.sidebar.header("🛠️ Ferramentas")

# 1. Upload da Imagem
arquivo = st.sidebar.file_uploader("📂 Abrir Folha de Sprites", type=["png", "jpg", "jpeg"])

# 2. Escolha da Ferramenta
ferramenta = st.sidebar.radio("Ferramenta:", ["🖌️ Pincel", "🖍️ Lápis", "🧼 Borracha", "🔲 Cortar"])

# 3. Grossura (Manivela)
grossura = st.sidebar.slider("Grossura do Traço", 1, 40, 1)

# 4. Paleta de Cores
st.sidebar.subheader("🎨 Cores")
cor_escolhida = st.sidebar.color_picker("Escolha a cor", "#000000")

# --- ÁREA PRINCIPAL ---
if arquivo:
    # Carregar imagem na memória
    img = Image.open(arquivo).convert("RGBA")
    
    # Criar uma camada de desenho caso não seja apenas corte
    if ferramenta != "🔲 Cortar":
        st.info("Para desenhar na Web: Use as coordenadas ou botões de edição abaixo.")
        
    # Lógica de Corte (Coordenadas)
    if ferramenta == "🔲 Cortar":
        st.subheader("Selecione a área para recortar")
        col1, col2, col3, col4 = st.columns(4)
        with col1: x1 = st.number_input("X Inicial", 0, img.width, 0)
        with col2: y1 = st.number_input("Y Inicial", 0, img.height, 0)
        with col3: x2 = st.number_input("X Final", 0, img.width, 100)
        with col4: y2 = st.number_input("Y Final", 0, img.height, 100)
        
        if x2 > x1 and y2 > y1:
            recorte = img.crop((x1, y1, x2, y2))
            st.image(recorte, caption="Prévia do Sprite")
            
            # Botão de Salvar Recorte
            buf = io.BytesIO()
            recorte.save(buf, format="PNG")
            st.download_button(
                label="💾 SALVAR RECORTE",
                data=buf.getvalue(),
                file_name="sprite_dandan.png",
                mime="image/png"
            )
    
    # Exibir a Imagem Principal
    st.subheader("Visualização da Folha")
    st.image(img, use_column_width=True)

    # Botão para salvar a imagem inteira (Igual ao que você pediu)
    st.sidebar.markdown("---")
    buf_full = io.BytesIO()
    img.save(buf_full, format="PNG")
    st.sidebar.download_button(
        label="💾 SALVAR TUDO (PAINT)",
        data=buf_full.getvalue(),
        file_name="desenho_completo.png",
        mime="image/png"
    )

else:
    st.warning("Por favor, faça o upload de uma imagem (PNG ou JPG) para começar.")
    
    # Botão para criar tela em branco (MODO PAINT)
    if st.button("🎨 CRIAR TELA BRANCA (MODO PAINT)"):
        img_branca = Image.new("RGBA", (800, 600), (255, 255, 255, 255))
        st.session_state['imagem'] = img_branca
        st.success("Tela branca criada! Agora faça o download para usar como base.")
