import pandas as pd
import streamlit as st

# Configuración inicial de la página web
st.set_page_config(
    page_title="Torneo de Fútbol - Dashboard", page_icon="⚽", layout="wide"
)

st.title("🏆 Dashboard Oficial del Torneo de Fútbol de CRIT SONORA")
st.markdown("Seguimiento en tiempo real de resultados, tabla general y estadísticas.")

# 1. Definición de los 10 equipos del torneo
equipos_lista = [
    "Crit Sonoa",
    "TE",
    "Leoni",
    "Clandestinos",
    "Parrilleros",
    "T&P",
    "Malcriados",
    "Arrabaleros",
    "Costeños",
    "Pisacorres",
]

# 2. Inicializar los datos de los partidos (Jornadas de ejemplo)
if "df_partidos" not in st.session_state:
  st.session_state.df_partidos = pd.DataFrame({
      "Jornada": [1, 1, 1, 1, 1, 2, 2, 2, 2, 2],
      "Local": [
          "Crit Sonoa",
    "TE",
    "Leoni",
    "Clandestinos",
    "Parrilleros",
    "T&P",
    "Malcriados",
    "Arrabaleros",
    "Costeños",
    "Pisacorres",
      ],
      "Goles Local": [2, 1, 3, 0, 2, 1, 2, 1, 0, 2],
      "Goles Visita": [1, 1, 1, 2, 2, 1, 2, 3, 0, 2],
      "Visita": [
          "Crit Sonoa",
    "TE",
    "Leoni",
    "Clandestinos",
    "Parrilleros",
    "T&P",
    "Malcriados",
    "Arrabaleros",
    "Costeños",
    "Pisacorres",
      ],
      "Jugado": [
          True,
          True,
          True,
          True,
          True,
          True,
          True,
          True,
          True,
          True,
      ],
  })

df = st.session_state.df_partidos

# --- PESTAÑAS DE NAVEGACIÓN ---
tab1, tab2, tab3 = st.tabs(
    ["📊 Tabla General", "⚽ Resultados y Calendario", "⚙️ Administrar Torneo"]
)

# Pestaña 1: Tabla de Posiciones calculada automáticamente
with tab1:
  st.subheader("Clasificación General")

  stats = {
      eq: {
          "JJ": 0,
          "G": 0,
          "E": 0,
          "P": 0,
          "GF": 0,
          "GC": 0,
          "DG": 0,
          "Pts": 0,
      }
      for eq in equipos_lista
  }

  for _, row in df[df["Jugado"] == True].iterrows():
    loc, vis = row["Local"], row["Visita"]
    g_loc, g_vis = row["Goles Local"], row["Goles Visita"]

    stats[loc]["JJ"] += 1
    stats[vis]["JJ"] += 1
    stats[loc]["GF"] += g_loc
    stats[loc]["GC"] += g_vis
    stats[vis]["GF"] += g_vis
    stats[vis]["GC"] += g_loc

    if g_loc > g_vis:
      stats[loc]["G"] += 1
      stats[loc]["Pts"] += 3
      stats[vis]["P"] += 1
    elif g_loc < g_vis:
      stats[vis]["G"] += 1
      stats[vis]["Pts"] += 3
      stats[loc]["P"] += 1
    else:
      stats[loc]["E"] += 1
      stats[loc]["Pts"] += 1
      stats[vis]["E"] += 1
      stats[vis]["Pts"] += 1

  for eq in stats:
    stats[eq]["DG"] = stats[eq]["GF"] - stats[eq]["GC"]

  df_tabla = pd.DataFrame.from_dict(stats, orient="index").reset_index()
  df_tabla.rename(columns={"index": "Equipo"}, inplace=True)
  df_tabla = df_tabla.sort_values(
      by=["Pts", "DG", "GF"], ascending=[False, False, False]
  ).reset_index(drop=True)
  df_tabla.index = df_tabla.index + 1

  st.dataframe(df_tabla, use_container_width=True)

# Pestaña 2: Calendario y Resultados por Jornada
with tab2:
  st.subheader("Calendario y Resultados por Jornada")
  jornada_sel = st.selectbox(
      "Selecciona la Jornada:", sorted(df["Jornada"].unique())
  )
  df_jornada = df[df["Jornada"] == jornada_sel]
  st.dataframe(df_jornada, use_container_width=True)

# Pestaña 3: Panel para actualizar resultados manualmente
with tab3:
  st.subheader("Actualizar Resultado de Partido")
  with st.form("form_resultado"):
    partido_idx = st.selectbox(
        "Selecciona el partido a actualizar:",
        df.index,
        format_func=lambda i: f"J{df.loc[i, 'Jornada']}: {df.loc[i, 'Local']} vs {df.loc[i, 'Visita']}",
    )
    nuevo_g_loc = st.number_input(
        "Goles Local", min_value=0, step=1, value=int(df.loc[partido_idx, "Goles Local"])
    )
    nuevo_g_vis = st.number_input(
        "Goles Visita", min_value=0, step=1, value=int(df.loc[partido_idx, "Goles Visita"])
    )
    marcar_jugado = st.checkbox("¿Partido Jugado?", value=bool(df.loc[partido_idx, "Jugado"]))

    submitted = st.form_submit_button("Guardar Resultado")
    if submitted:
      df.loc[partido_idx, "Goles Local"] = nuevo_g_loc
      df.loc[partido_idx, "Goles Visita"] = nuevo_g_vis
      df.loc[partido_idx, "Jugado"] = marcar_jugado
      st.success("¡Resultado actualizado con éxito!")
      st.rerun()