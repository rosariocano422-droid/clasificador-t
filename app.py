import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

st.set_page_config(page_title="Clasificador de T", page_icon="🔤", layout="wide")

st.title("🔤 Clasificador Automático de la Letra T")
st.markdown("### ¿Puede una máquina decidir sola si una imagen es una T?")
st.markdown("---")

st.markdown("""
**¿Cómo funciona?**
- La máquina calcula un puntaje multiplicando cada píxel por su peso
- Compara el puntaje con el umbral (threshold)
- Si el puntaje supera el umbral → **ES una T**
- Si no lo supera → **NO es una T**
- Tu objetivo es encontrar la configuración perfecta que clasifique bien todas las imágenes
""")

st.markdown("---")

# ============================================================
# IMÁGENES
# ============================================================
imagenes_T = {
    "T normal": [[1,1,1],[0,1,0],[0,1,0]],
    "T centrada": [[1,1,1],[0,1,0],[0,1,0]],
    "T variante": [[1,1,1],[0,1,0],[0,1,0]],
}

imagenes_NO_T = {
    "Cruz (+)":      [[0,1,0],[1,1,1],[0,1,0]],
    "L invertida":   [[1,0,0],[1,0,0],[1,1,1]],
    "Diagonal":      [[1,0,0],[0,1,0],[0,0,1]],
    "Cuadrado":      [[1,1,1],[1,0,1],[1,1,1]],
    "Fila central":  [[0,0,0],[1,1,1],[0,0,0]],
    "T invertida":   [[0,1,0],[0,1,0],[1,1,1]],
}

# ============================================================
# SECCIÓN 1: PESOS Y THRESHOLD
# ============================================================
st.header("🎛️ Paso 1: Ajusta los pesos y el umbral")
st.markdown("Mueve los sliders para cambiar los pesos y el umbral de decisión.")

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("**Fila 1**")
    w00 = st.slider("Pos (1,1)", -5.0, 5.0, 2.0, 0.5, key="w00")
    w10 = st.slider("Pos (2,1)", -5.0, 5.0, -3.0, 0.5, key="w10")
    w20 = st.slider("Pos (3,1)", -5.0, 5.0, -3.0, 0.5, key="w20")
with col2:
    st.markdown("**Fila 2**")
    w01 = st.slider("Pos (1,2)", -5.0, 5.0, 2.0, 0.5, key="w01")
    w11 = st.slider("Pos (2,2)", -5.0, 5.0, 3.0, 0.5, key="w11")
    w21 = st.slider("Pos (3,2)", -5.0, 5.0, 3.0, 0.5, key="w21")
with col3:
    st.markdown("**Fila 3**")
    w02 = st.slider("Pos (1,3)", -5.0, 5.0, 2.0, 0.5, key="w02")
    w12 = st.slider("Pos (2,3)", -5.0, 5.0, -3.0, 0.5, key="w12")
    w22 = st.slider("Pos (3,3)", -5.0, 5.0, -3.0, 0.5, key="w22")

pesos = [
    [w00, w01, w02],
    [w10, w11, w12],
    [w20, w21, w22]
]

st.markdown("---")

# Threshold con slider Y caja numérica
col_sl, col_num = st.columns([3, 1])
with col_sl:
    threshold = st.slider(
        "🎯 Umbral de decisión (threshold)",
        min_value=-10.0, max_value=20.0,
        value=5.0, step=0.5
    )
with col_num:
    threshold_num = st.number_input(
        "Valor exacto",
        min_value=-10.0, max_value=20.0,
        value=threshold, step=0.5
    )
    if threshold_num != threshold:
        threshold = threshold_num

st.markdown(f"""
> **Regla de clasificación:**
> Si puntaje **>** {threshold} → ✅ **ES una T**
> Si puntaje **≤** {threshold} → ❌ **NO es una T**
""")

st.markdown("---")

# ============================================================
# FUNCIÓN DE PUNTUACIÓN Y CLASIFICACIÓN
# ============================================================
def calcular(imagen, pesos, threshold):
    puntaje = sum(imagen[i][j] * pesos[i][j] for i in range(3) for j in range(3))
    decision = "✅ ES una T" if puntaje > threshold else "❌ NO es una T"
    correcto_T = puntaje > threshold
    return puntaje, decision, correcto_T

# ============================================================
# FUNCIÓN PARA DIBUJAR CUADRÍCULA
# ============================================================
def dibujar(imagen, titulo, puntaje, decision, correcto):
    fig, ax = plt.subplots(figsize=(3, 3.2))
    ax.set_xlim(0, 3)
    ax.set_ylim(0, 3)
    ax.set_aspect('equal')
    ax.axis('off')

    for i in range(3):
        for j in range(3):
            color = '#2E75B6' if imagen[i][j] == 1 else '#F0F0F0'
            rect = patches.Rectangle((j, 2-i), 1, 1,
                                      linewidth=2, edgecolor='#CCCCCC',
                                      facecolor=color)
            ax.add_patch(rect)
            ax.text(j+0.5, 2-i+0.5, str(imagen[i][j]),
                    ha='center', va='center',
                    fontsize=14, fontweight='bold',
                    color='white' if imagen[i][j] == 1 else '#999999')

    color_titulo = '#1a7a1a' if correcto else '#cc0000'
    ax.set_title(
        f"{titulo}\nPuntaje: {puntaje:.1f}\n{decision}",
        fontsize=9, color=color_titulo, fontweight='bold'
    )
    plt.tight_layout()
    return fig

# ============================================================
# SECCIÓN 2: CLASIFICACIÓN AUTOMÁTICA
# ============================================================
st.header("🤖 Paso 2: Clasificación automática")

# Imágenes T
st.subheader("✅ Imágenes que SÍ son T")
cols = st.columns(3)
aciertos_T = 0
for idx, (nombre, imagen) in enumerate(imagenes_T.items()):
    puntaje, decision, correcto = calcular(imagen, pesos, threshold)
    if correcto:
        aciertos_T += 1
    with cols[idx]:
        fig = dibujar(imagen, nombre, puntaje, decision, correcto)
        st.pyplot(fig)
        plt.close()

st.markdown("---")

# Imágenes NO-T
st.subheader("❌ Imágenes que NO son T")
cols2 = st.columns(3)
aciertos_NO_T = 0
for idx, (nombre, imagen) in enumerate(imagenes_NO_T.items()):
    puntaje, decision, correcto_T = calcular(imagen, pesos, threshold)
    correcto_rechazo = not correcto_T
    if correcto_rechazo:
        aciertos_NO_T += 1
    with cols2[idx % 3]:
        fig = dibujar(imagen, nombre, puntaje, decision, correcto_rechazo)
        st.pyplot(fig)
        plt.close()

st.markdown("---")

# ============================================================
# SECCIÓN 3: EVALUACIÓN DE ERRORES
# ============================================================
st.header("📊 Paso 3: Evaluación de errores")

total = len(imagenes_T) + len(imagenes_NO_T)
total_correctos = aciertos_T + aciertos_NO_T

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("✅ T reconocidas", f"{aciertos_T} / {len(imagenes_T)}")
with col2:
    st.metric("❌ NO-T rechazadas", f"{aciertos_NO_T} / {len(imagenes_NO_T)}")
with col3:
    st.metric("🎯 Total correctos", f"{total_correctos} / {total}")
with col4:
    precision = (total_correctos / total) * 100
    st.metric("📈 Precisión", f"{precision:.0f}%")

st.progress(total_correctos / total)

# Análisis de errores
st.subheader("🔍 Análisis detallado")

falsos_positivos = []
falsos_negativos = []

for nombre, imagen in imagenes_NO_T.items():
    puntaje, _, correcto_T = calcular(imagen, pesos, threshold)
    if correcto_T:
        falsos_positivos.append((nombre, puntaje))

for nombre, imagen in imagenes_T.items():
    puntaje, _, correcto_T = calcular(imagen, pesos, threshold)
    if not correcto_T:
        falsos_negativos.append((nombre, puntaje))

col1, col2 = st.columns(2)

with col1:
    st.markdown("**⚠️ Falsos Positivos** (NO son T pero la máquina dijo que sí)")
    if falsos_positivos:
        for nombre, puntaje in falsos_positivos:
            st.error(f"❌ {nombre} → Puntaje: {puntaje:.1f} (umbral: {threshold})")
    else:
        st.success("✅ ¡Ninguno! La máquina rechazó correctamente todas las NO-T")

with col2:
    st.markdown("**⚠️ Falsos Negativos** (SÍ son T pero la máquina dijo que no)")
    if falsos_negativos:
        for nombre, puntaje in falsos_negativos:
            st.error(f"❌ {nombre} → Puntaje: {puntaje:.1f} (umbral: {threshold})")
    else:
        st.success("✅ ¡Ninguno! La máquina reconoció correctamente todas las T")

if total_correctos == total:
    st.success("🏆 ¡Configuración perfecta! La máquina clasifica correctamente todas las imágenes.")
    st.balloons()

st.markdown("---")

# ============================================================
# SECCIÓN 4: CÁLCULO DETALLADO
# ============================================================
st.header("🔢 Paso 4: Ve el cálculo detallado")

todas = {**imagenes_T, **imagenes_NO_T}
seleccion = st.selectbox("Selecciona una imagen:", list(todas.keys()))

imagen_sel = todas[seleccion]
puntaje_sel = sum(imagen_sel[i][j] * pesos[i][j] for i in range(3) for j in range(3))
decision_sel = "✅ ES una T" if puntaje_sel > threshold else "❌ NO es una T"

col1, col2 = st.columns(2)
with col1:
    st.subheader("📐 Matriz de la imagen")
    for fila in imagen_sel:
        st.text("  ".join(str(p) for p in fila))
    st.subheader("⚖️ Pesos actuales")
    for fila in pesos:
        st.text("  ".join(f"{p:+.1f}" for p in fila))

with col2:
    st.subheader("🧮 Decisión automática")
    pasos = []
    for i in range(3):
        for j in range(3):
            pasos.append(f"({imagen_sel[i][j]}×{pesos[i][j]:+.1f})")
    st.markdown(f"**Fórmula:** `y = {' + '.join(pasos)}`")
    st.markdown(f"**Puntaje:** `{puntaje_sel:.2f}`")
    st.markdown(f"**Umbral:** `{threshold}`")
    st.markdown(f"**Comparación:** `{puntaje_sel:.2f} {'>' if puntaje_sel > threshold else '≤'} {threshold}`")

    if puntaje_sel > threshold:
        st.success(f"✅ Puntaje {puntaje_sel:.2f} > {threshold} → **ES una T**")
    else:
        st.error(f"❌ Puntaje {puntaje_sel:.2f} ≤ {threshold} → **NO es una T**")

st.markdown("---")

# ============================================================
# SECCIÓN 5: FRONTERA DE DECISIÓN
# ============================================================
st.header("📈 Frontera de decisión en tiempo real")

fig2, ax2 = plt.subplots(figsize=(7, 6))
ax2.set_facecolor('#f8f9fa')
fig2.patch.set_facecolor('#ffffff')

puntajes_T = [sum(img[i][j]*pesos[i][j] for i in range(3) for j in range(3))
              for img in imagenes_T.values()]
puntajes_NO_T = [sum(img[i][j]*pesos[i][j] for i in range(3) for j in range(3))
                 for img in imagenes_NO_T.values()]

nombres_T = list(imagenes_T.keys())
nombres_NO_T = list(imagenes_NO_T.keys())

x_T = list(range(len(puntajes_T)))
x_NO_T = list(range(len(puntajes_NO_T)))

ax2.bar([x - 0.2 for x in x_T], puntajes_T, 0.4,
        label='Imágenes T', color='#2196F3', alpha=0.8)
ax2.bar([x + 0.2 for x in x_NO_T], puntajes_NO_T, 0.4,
        label='Imágenes NO-T', color='#f44336', alpha=0.8)

ax2.axhline(y=threshold, color='#ff9800', linewidth=2.5,
            linestyle='--', label=f'Umbral = {threshold}')

ax2.fill_between([-0.5, max(len(puntajes_T), len(puntajes_NO_T)) - 0.5],
                 threshold, max(max(puntajes_T), max(puntajes_NO_T)) + 2,
                 alpha=0.1, color='green', label='Zona T')
ax2.fill_between([-0.5, max(len(puntajes_T), len(puntajes_NO_T)) - 0.5],
                 min(min(puntajes_T), min(puntajes_NO_T)) - 2, threshold,
                 alpha=0.1, color='red', label='Zona NO-T')

ax2.set_xticks(range(max(len(puntajes_T), len(puntajes_NO_T))))
ax2.set_xticklabels(nombres_T[:max(len(puntajes_T), len(puntajes_NO_T))],
                    rotation=15, ha='right', fontsize=9)
ax2.set_ylabel('Puntaje', fontsize=11)
ax2.set_title('Puntajes vs Umbral de Decisión', fontsize=13, fontweight='bold')
ax2.legend(fontsize=9)
ax2.grid(True, alpha=0.3)

plt.tight_layout()
st.pyplot(fig2)
plt.close()

st.markdown("---")
st.markdown("🎓 **Aplicación desarrollada para la asignatura: Autómatas, Gramáticas y Lenguaje - IU Digital de Antioquia**")
