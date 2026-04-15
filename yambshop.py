
import streamlit as st
import streamlit.components.v1 as components
import base64
import uuid
import pandas as pd
import os
import requests

st.set_page_config(page_title="YAMBSHOP | 3D Studio", page_icon="shirt", layout="wide")

if "orders" not in st.session_state: st.session_state.orders = []

# Logo Base64
LOGO_URL = 'https://cdn-icons-png.flaticon.com/512/3534/3534312.png'
try:
    logo_b64 = base64.b64encode(requests.get(LOGO_URL).content).decode()
except: logo_b64 = ""

with st.sidebar:
    if logo_b64:
        st.markdown(f'<img src="data:image/png;base64,{logo_b64}" width="100">', unsafe_allow_html=True)
    st.markdown("<h2 style=\'color:#ff3131; font-weight:900; margin:0;\'>YAMBSHOP.</h2>", unsafe_allow_html=True)
    theme_mode = st.radio("Visual Theme", ["Dark Mode", "Light Mode"], horizontal=True)
    pwd = st.text_input("Admin Access", type="password")
    is_admin = pwd == "admin123"

bg_color = "#0a0a0a" if theme_mode == "Dark Mode" else "#fcfcfc"
text_color = "#ffffff" if theme_mode == "Dark Mode" else "#1a1a1a"
card_bg = "#151515" if theme_mode == "Dark Mode" else "#ffffff"
card_border = "#333333" if theme_mode == "Dark Mode" else "#f0f0f0"
logo_filter = "invert(1)" if theme_mode == "Dark Mode" else "none"

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;900&display=swap');
    .stApp {{{{ background-color: {bg_color}; color: {text_color}; font-family: 'Inter', sans-serif; }}}}
    
    /* Header Responsivo */
    .header-box {{{{ 
        display: flex; align-items: center; border-left: 8px solid #ff3131; 
        padding: 20px; margin-bottom: 30px; background: {card_bg}; 
        border-radius: 0 0 20px 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }}}}
    
    .brand-logo-img {{{{ height: 80px; width: auto; filter: {logo_filter}; }}}}
    
    /* PC / Desktop */
    @media (min-width: 1024px) {{{{ 
        .brand-logo-img {{{{ height: 100px; }}}}
        .header-box h1 {{{{ font-size: 3rem !important; }}}}
    }}}}
    
    /* Tablet */
    @media (max-width: 1024px) and (min-width: 768px) {{{{ 
        .brand-logo-img {{{{ height: 80px; }}}}
        .header-box h1 {{{{ font-size: 2.2rem !important; }}}}
    }}}}
    
    /* Mobile */
    @media (max-width: 767px) {{{{ 
        .header-box {{{{ flex-direction: column; text-align: center; border-left: none; border-top: 8px solid #ff3131; padding: 15px; }}}}
        .brand-logo-img {{{{ height: 60px; margin-bottom: 10px; }}}}
        .header-box h1 {{{{ font-size: 1.8rem !important; }}}}
        .header-box div {{{{ margin-left: 0 !important; }}}}
    }}}}

    .stButton>button {{{{ background-color: #ff3131 !important; color: white !important; font-weight: 800; border-radius: 12px; border: none; padding: 15px 30px; }}}}
    .item-card {{{{ background: {card_bg}; border: 1px solid {card_border}; padding: 25px; border-radius: 20px; margin-bottom: 20px; }}}}
    h1, h2, h3 {{{{ color: {text_color} !important; font-weight: 900; }}}}
</style>
""", unsafe_allow_html=True)

if is_admin:
    st.header("ORDERS DASHBOARD")
    st.dataframe(pd.DataFrame(st.session_state.orders), use_container_width=True)
else:
    st.markdown(f"""
    <div class='header-box'>
        <img src='data:image/png;base64,{logo_b64}' class='brand-logo-img'>
        <div style='margin-left: 30px;'>
            <h1 style='margin:0; font-weight:900;'>YAMBSHOP.</h1>
            <p style='color:#ff3131 !important; font-weight:900; margin:0; letter-spacing:5px; font-size: 0.8rem;'>PREMIUM 3D DESIGN STUDIO</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_v, col_c = st.columns([1.6, 1], gap="large")

    with col_v:
        st.markdown("<div class='item-card'>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        tipo = c1.selectbox("ITEM", ["Camiseta", "Gorra"])
        colores_map = {"Black Out": "#111111", "Gym Red": "#FF3131", "Pure White": "#FFFFFF"}
        color_hex = colores_map[c2.selectbox("BASE COLOR", list(colores_map.keys()))]
        disenos = {"Classic Logo": "https://cdn-icons-png.flaticon.com/512/3534/3534312.png", "Skull Art": "https://cdn-icons-png.flaticon.com/512/4334/4334053.png"}
        logo_sel = c3.selectbox("ESTAMPADO", list(disenos.keys()))

        try:
            logo_data_raw = requests.get(disenos[logo_sel]).content
            logo_b64_3d = base64.b64encode(logo_data_raw).decode()
        except: logo_b64_3d = ""

        glb_name = "tshirt.glb" if tipo == "Camiseta" else "gorra.glb"
        d_pos_val = "new THREE.Vector3(0, 0.2, 0.5)" if tipo == "Camiseta" else "new THREE.Vector3(0, 0.45, 0.85)"
        raw_git_url = "https://raw.githubusercontent.com/MemozMultimedia/yambshop/main/"

        three_js = f"""
        <html><body style='margin:0; background:transparent;'>
        <script src='https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js'></script>
        <script src='https://cdn.jsdelivr.net/gh/mrdoob/three.js@r128/examples/js/loaders/GLTFLoader.js'></script>
        <script src='https://cdn.jsdelivr.net/gh/mrdoob/three.js@r128/examples/js/geometries/DecalGeometry.js'></script>
        <script>
            const scene = new THREE.Scene();
            const camera = new THREE.PerspectiveCamera(40, window.innerWidth/500, 0.1, 1000);
            const renderer = new THREE.WebGLRenderer({{{{ antialias: true, alpha: true }}}});
            renderer.setSize(window.innerWidth, 500);
            document.body.appendChild(renderer.domElement);
            scene.add(new THREE.AmbientLight(0xffffff, 1.2));
            const light = new THREE.DirectionalLight(0xffffff, 1); light.position.set(5,10,7.5); scene.add(light);
            const group = new THREE.Group(); scene.add(group);

            new THREE.GLTFLoader().load('{raw_git_url}{glb_name}', (gltf) => {{{{ 
                const m = gltf.scene;
                m.traverse(n => {{{{ 
                    if(n.isMesh) {{{{ 
                        n.material.color.set('{color_hex}'); 
                        const tex = new THREE.TextureLoader().load(\'data:image/png;base64,{logo_b64_3d}\');
                        const mat = new THREE.MeshStandardMaterial({{{{ map: tex, transparent: true, polygonOffset: true, polygonOffsetFactor: -4 }}}});
                        const decal = new THREE.Mesh(new THREE.DecalGeometry(n, {d_pos_val}, new THREE.Euler(0,0,0), new THREE.Vector3(1,1,1)), mat);
                        group.add(decal);
                    }}}} 
                }}}});
                group.add(m);
            }}}});
            camera.position.z = 5.5;
            function animate() {{{{ requestAnimationFrame(animate); group.rotation.y += 0.007; renderer.render(scene, camera); }}}} animate();
        </script></body></html>"""
        components.html(three_js, height=500)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_c:
        st.markdown("<div class='item-card'>", unsafe_allow_html=True)
        st.subheader("RESUMEN")
        nombre = st.text_input("Nombre")
        talla = st.select_slider("TALLA", options=["S", "M", "L", "XL"])
        qty = st.number_input("Cantidad", 1, 100)
        total = qty * (1500 if tipo == "Camiseta" else 1200)
        st.markdown(f"<h1 style='color:#ff3131; font-weight:900;'>RD$ {total:,.0f}</h1>", unsafe_allow_html=True)

        if st.button("PLACE ORDER", use_container_width=True):
            if nombre:
                ref = str(uuid.uuid4())[:6].upper()
                st.session_state.orders.append({{"Ref": ref, "Name": nombre, "Item": tipo, "Size": talla, "Total": total}})
                st.success(f"ORDEN: {ref}")
                st.balloons()
            else: st.error("Ingresa tu nombre para continuar")
        st.markdown("</div>", unsafe_allow_html=True)
