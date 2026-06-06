import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

st.set_page_config(page_title="Clasificador de T", page_icon="🔤", layout="wide")

st.title("🔤 Clasificador Automático de la Letra T")
st.markdown("### Actividad 3 — Autómatas, Gramáticas y Lenguaje")
st.markdown("---")

st.markdown("""
**¿Qué hace esta aplicación?**

En la actividad anterior construimos una máquina que calculaba un puntaje para cada imagen.
Ahora esa máquina da un paso más: **decide sola** si la imagen es una T o no, comparando el puntaje con un umbral.

**¿Cómo funciona?**
- Cada imagen es una cuadrícula de 3x3 píxeles (1 = activo, 0 = apagado)
- La máquina multiplica cada píxel por su peso y suma todo → obtiene un **puntaje**
- Compara ese puntaje con el **umbral** de decisión
- Si el puntaje supera el umbral → dice automáticamente **✅ ES una T**
- Si no lo supera → dice automáticamente **❌ NO es una T**
""")

st.markdown("---")

imagenes_T = {
    "T normal":   [[1,1,1],[0,1,0],[0,1,0]],
    "T centrada": [[1,1,1],[0,1,0],[0,1,0]],
    "T variante": [[1,1,1],[0,1,0],[0,1,0]],
}

imagenes_NO_T = {
    "Cruz (+)":     [[0,1,0],[1,1,1],[0,1,0]],
    "L invertida":  [[1,0,0],[1,0,0],[1,1,1]],
    "Diagonal":     [[1,0,0],[0,1,0],[0,0,1]],
    "Cuadrado":     [[1,1,1],[1,0,1],[1,1,1]],
    "Fila central": [[0,0,0],[1,1,1],[0,0,0]],
    "T invertida":  [[0,1,0],[0,1,0],[1,1,1]],
}

st.header("🎛️ Paso 1: Ajusta los pesos de cada posición")
st.markdown("Igual que en la actividad anterior, cada slider controla el peso de un píxel en la cuadrícula 3x3.")

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("**Fila 1 (barra superior de la T)**")
    w00 = st.slider("Pos (1,1)", -5.0, 5.0, 2.0, 0.5, key="w00")
    w10 = st.slider("Pos (2,1)", -5.0, 5.0, -3.0, 0.5, key="w10")
    w20 = st.slider("Pos (3,1)", -5.0, 5.0, -3.0, 0.5, key="w20")
with col2:
    st.markdown("**Fila 2 (columna central)**")
    w01 = st.slider("Pos (1,2)", -5.0, 5.0, 2.0, 0.5, key="w01")
    w11 = st.slider("Pos (2,2)", -5.0, 5.0, 3.0, 0.5, key="w11")
    w21 = st.slider("Pos (3,2)", -5.0, 5.0, 3.0, 0.5, key="w21")
with col3:
    st.markdown("**Fila 3 (barra superior de la T)**")
    w02 = st.slider("Pos (1,3)", -5.0, 5.0, 2.0, 0.5, key="w02")
    w12 = st.slider("Pos (2,3)", -5.0, 5.0, -3.0, 0.5, key="w12")
    w22 = st.slider("Pos (3,3)", -5.0, 5.0, -3.0, 0.5, key="w22")

pesos = [
    [w00, w01, w02],
    [w10, w11, w12],
    [w20, w21, w22]
]

st.markdown("---")

st.header("🎯 Paso 2: Define el umbral de decisión")
st.markdown("""
El umbral es el **límite** que usa la máquina para decidir.
- Si el puntaje de la imagen es **mayor** al umbral → la máquina dice **ES una T**
- Si el puntaje es **menor o igual** al umbral → la máquina dice **NO es una T**
""")

col_sl, col_num = st.columns([3, 1])
with col_sl:
    threshold = st.slider(
        "Umbral de decisión",
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

st.info(f"📌 Regla actual: Si puntaje > **{threshold}** → ✅ ES una T | Si puntaje ≤ **{threshold}** → ❌ NO es una T")

st.markdown("---")

def calcular(imagen, pesos, threshold):
    puntaje = sum(imagen[i][j] * pesos[i][j] for i in range(3) for j in range(3))
    decision = "✅ ES una T" if puntaje > threshold else "❌ NO es una T"
    correcto_T = puntaje > threshold
    return puntaje, decision, correcto_T

def dibujar(imagen, titulo, puntaje, decision, correcto):
    fig, ax = plt.subplots(figsize=(2, 2.3))
    ax.set_xlim(0, 3)
    ax.set_ylim(0, 3)
    ax.set_aspect('equal')
    ax.axis('off')
    for i in range(3):
        for j in range(3):
            color = '#2E75B6' if imagen[i][j] == 1 else '#F0F0F0'
            rect = patches.Rectangle((j, 2-i), 1, 1,
                                      linewidth=1.5,
                                      edgecolor='#CCCCCC',
                                      facecolor=color)
            ax.add_patch(rect)
            ax.text(j+0.5, 2-i+0.5, str(imagen[i][j]),
                    ha='center', va='center',
                    fontsize=11, fontweight='bold',
                    color='white' if imagen[i][j] == 1 else '#999999')
    color_titulo = '#1a7a1a' if correcto else '#cc0000'
    ax.set_title(
        f"{titulo}\nPuntaje: {puntaje:.1f} | {decision}",
        fontsize=7.5, color=color_titulo, fontweight='bold'
    )
    plt.tight_layout()
    return fig

st.header("🤖 Paso 3: Clasificación automática")
st.markdown("""
Aquí es donde la máquina **decide sola**. No necesita que tú le digas si es una T o no.
Ella calcula el puntaje de cada imagen y lo compara con el umbral automáticamente.
""")

st.subheader("✅ Imágenes que SÍ son T")
st.markdown("La máquina debe reconocer estas como T (puntaje mayor al umbral).")
cols = st.columns(6)
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

st.subheader("❌ Imágenes que NO son T")
st.markdown("La máquina debe rechazar estas como NO-T (puntaje menor o igual al umbral).")
cols2 = st.columns(6)
aciertos_NO_T = 0
for idx, (nombre, imagen) in enumerate(imagenes_NO_T.items()):
    puntaje, decision, correcto_T = calcular(imagen, pesos, threshold)
    correcto_rechazo = not correcto_T
    if correcto_rechazo:
        aciertos_NO_T += 1
    with cols2[idx]:
        fig = dibujar(imagen, nombre, puntaje, decision, correcto_rechazo)
        st.pyplot(fig)
        plt.close()

st.markdown("---")

st.header("📊 Paso 4: Evaluación de errores")
st.markdown("""
Aquí puedes ver qué tan bien está funcionando tu configuración.
El objetivo es llegar a **9/9** con **100% de precisión**.
""")

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

st.subheader("🔍 ¿Qué errores cometió la máquina?")
st.markdown("""
- **Falso Positivo:** La máquina dijo ES una T, pero NO lo era
- **Falso Negativo:** La máquina dijo NO es una T, pero SÍ lo era
""")

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
    st.markdown("**⚠️ Falsos Positivos**")
    if falsos_positivos:
        for nombre, puntaje in falsos_positivos:
            st.error(f"❌ {nombre} → Puntaje: {puntaje:.1f} (umbral: {threshold})")
    else:
        st.success("✅ ¡Ninguno! La máquina rechazó correctamente todas las NO-T")

with col2:
    st.markdown("**⚠️ Falsos Negativos**")
    if falsos_negativos:
        for nombre, puntaje in falsos_negativos:
            st.error(f"❌ {nombre} → Puntaje: {puntaje:.1f} (umbral: {threshold})")
    else:
        st.success("✅ ¡Ninguno! La máquina reconoció correctamente todas las T")

if total_correctos == total:
    st.success("🏆 ¡Configuración perfecta! La máquina clasifica correctamente todas las imágenes.")
    st.balloons()

st.markdown("---")

st.header("🔢 Paso 5: Ve el cálculo detallado paso a paso")
st.markdown("Selecciona cualquier imagen y verás exactamente cómo la máquina tomó su decisión.")

todas = {**imagenes_T, **imagenes_NO_T}
seleccion = st.selectbox("Selecciona una imagen:", list(todas.keys()))

imagen_sel = todas[seleccion]
puntaje_sel = sum(imagen_sel[i][j] * pesos[i][j] for i in range(3) for j in range(3))

col1, col2 = st.columns(2)
with col1:
    st.subheader("📐 Imagen seleccionada")
    for fila in imagen_sel:
        st.text("  ".join(str(p) for p in fila))
    st.subheader("⚖️ Pesos actuales")
    for fila in pesos:
        st.text("  ".join(f"{p:+.1f}" for p in fila))

with col2:
    st.subheader("🧮 ¿Cómo decidió la máquina?")
    pasos = []
    for i in range(3):
        for j in range(3):
            pasos.append(f"({imagen_sel[i][j]}×{pesos[i][j]:+.1f})")
    st.markdown(f"**1. Fórmula:** `y = {' + '.join(pasos)}`")
    st.markdown(f"**2. Puntaje calculado:** `{puntaje_sel:.2f}`")
    st.markdown(f"**3. Umbral definido:** `{threshold}`")
    st.markdown(f"**4. Comparación:** `{puntaje_sel:.2f} {'>' if puntaje_sel > threshold else '≤'} {threshold}`")
    st.markdown("**5. Decisión automática:**")
    if puntaje_sel > threshold:
        st.success(f"✅ Como {puntaje_sel:.2f} > {threshold} → La máquina dice: **ES una T**")
    else:
        st.error(f"❌ Como {puntaje_sel:.2f} ≤ {threshold} → La máquina dice: **NO es una T**")

st.markdown("---")

st.header("📈 Gráfica: Puntajes vs Umbral de Decisión")
st.markdown("""
Esta gráfica muestra el puntaje de cada imagen.
La línea naranja es el umbral. Las barras **por encima** de la línea son clasificadas como T,
las que están **por debajo** son clasificadas como NO-T.
""")

nombres_T = list(imagenes_T.keys())
nombres_NO_T = list(imagenes_NO_T.keys())

puntajes_T = [
    sum(img[i][j] * pesos[i][j] for i in range(3) for j in range(3))
    for img in imagenes_T.values()
]
puntajes_NO_T = [
    sum(img[i][j] * pesos[i][j] for i in range(3) for j in range(3))
    for img in imagenes_NO_T.values()
]

fig2, ax2 = plt.subplots(figsize=(11, 5))
ax2.set_facecolor('#f8f9fa')
fig2.patch.set_facecolor('#ffffff')

x_T = list(range(len(puntajes_T)))
x_NO_T = [x + len(puntajes_T) + 1 for x in range(len(puntajes_NO_T))]

barras_T = ax2.bar(x_T, puntajes_T, 0.6,
                   label='Imágenes T', color='#2196F3', alpha=0.85)
barras_NO_T = ax2.bar(x_NO_T, puntajes_NO_T, 0.6,
                      label='Imágenes NO-T', color='#f44336', alpha=0.85)

ax2.axhline(y=threshold, color='#ff9800', linewidth=2.5,
            linestyle='--', label=f'Umbral = {threshold}', zorder=5)

todos_x = x_T + x_NO_T
todos_nombres = nombres_T + nombres_NO_T
ax2.set_xticks(todos_x)
ax2.set_xticklabels(todos_nombres, rotation=20, ha='right', fontsize=9)
ax2.set_ylabel('Puntaje', fontsize=11)
ax2.set_title('Puntajes de cada imagen vs Umbral de Decisión',
              fontsize=13, fontweight='bold')
ax2.legend(fontsize=9)
ax2.grid(True, alpha=0.3, axis='y')

for bar, puntaje in zip(barras_T, puntajes_T):
    ax2.text(bar.get_x() + bar.get_width()/2,
             bar.get_height() + 0.2,
             f'{puntaje:.1f}',
             ha='center', va='bottom', fontsize=9, fontweight='bold')

for bar, puntaje in zip(barras_NO_T, puntajes_NO_T):
    ypos = bar.get_height() + 0.2 if puntaje >= 0 else bar.get_height() - 0.8
    ax2.text(bar.get_x() + bar.get_width()/2,
             ypos,
             f'{puntaje:.1f}',
             ha='center', va='bottom', fontsize=9, fontweight='bold')

plt.tight_layout()
st.pyplot(fig2)
plt.close()

st.markdown("---")
st.markdown("🎓 **Aplicación desarrollada para la asignatura: Autómatas, Gramáticas y Lenguaje - IU Digital de Antioquia**")
