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

# 2. Inicializar los datos de los partidos
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
          "TE",
          "Leoni",
          "Clandestinos",
          "Parrilleros",
          "Crit Sonoa",
          "Malcriados",
          "Arrabaleros",
          "Costeños",
          "Pisacorres",
          "T&P",
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

# 3. Inicializar datos de Goleadores
if "df_goleadores" not in st.session_state:
  st.session_state.df_goleadores = pd.DataFrame({
      "Jugador": [
          "Carlos Pérez",
          "Juan Gómez",
          "Mario López",
          "Alejandro Ruiz",
          "José Torres",
      ],
      "Equipo": ["Crit Sonoa", "Leoni", "T&P", "Parrilleros", "Malcriados"],
      "Goles": [5, 4, 3, 3, 2],
  })

df = st.session_state.df_partidos
df_gols = st.session_state.df_goleadores

# --- PESTAÑAS DE NAVEGACIÓN ---
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Tabla General",
    "⚽ Resultados y Calendario",
    "👟 Tabla de Goleadores",
    "⚙️ Administrar Torneo",
])

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

# Pestaña 3: Tabla de Goleadores
with tab3:
  st.subheader("👟 Máximos Goleadores del Torneo")
  df_gols_sorted = df_gols.sort_values(by="Goles", ascending=False).reset_index(
      drop=True
  )
  df_gols_sorted.index = df_gols_sorted.index + 1
  st.dataframe(df_gols_sorted, use_container_width=True)

# Pestaña 4: Panel para actualizar resultados protegido por contraseña
with tab4:
  st.subheader("⚙️ Panel de Administración")
  st.markdown("Acceso exclusivo para el organizador del torneo.")

  # Configura aquí tu contraseña de administrador
  PASSWORD_ADMIN = "crit2026"

  # Campo de contraseña
  pwd_ingresada = st.text_input(
      "Introduce la contraseña de administrador:", type="password"
  )

  if pwd_ingresada == PASSWORD_ADMIN:
    st.success("¡Contraseña correcta! Ya puedes actualizar la información.")

    # Sub-pestañas dentro del panel de administración
    admin_opcion = st.radio(
        "¿Qué deseas actualizar?",
        ["Actualizar Resultados de Partidos", "Actualizar Goleadores"],
    )

    if admin_opcion == "Actualizar Resultados de Partidos":
      with st.form("form_resultado"):
        partido_idx = st.selectbox(
            "Selecciona el partido a actualizar:",
            df.index,
            format_func=lambda i: f"J{df.loc[i, 'Jornada']}: {df.loc[i, 'Local']} vs {df.loc[i, 'Visita']}",
        )
        nuevo_g_loc = st.number_input(
            "Goles Local",
            min_value=0,
            step=1,
            value=int(df.loc[partido_idx, "Goles Local"]),
        )
        nuevo_g_vis = st.number_input(
            "Goles Visita",
            min_value=0,
            step=1,
            value=int(df.loc[partido_idx, "Goles Visita"]),
        )
        marcar_jugado = st.checkbox(
            "¿Partido Jugado?", value=bool(df.loc[partido_idx, "Jugado"])
        )

        submitted = st.form_submit_button("Guardar Resultado del Partido")
        if submitted:
          df.loc[partido_idx, "Goles Local"] = nuevo_g_loc
          df.loc[partido_idx, "Goles Visita"] = nuevo_g_vis
          df.loc[partido_idx, "Jugado"] = marcar_jugado
          st.success("¡Resultado actualizado con éxito!")
          st.rerun()

    elif admin_opcion == "Actualizar Goleadores":
      with st.form("form_goleador"):
        jugador_sel = st.selectbox(
            "Selecciona o registra jugador:",
            df_gols["Jugador"].tolist() + ["+ Agregar Nuevo Jugador"],
        )

        if jugador_sel == "+ Agregar Nuevo Jugador":
          nuevo_jugador = st.text_input("Nombre del Nuevo Jugador")
          nuevo_equipo = st.selectbox("Equipo del Jugador", equipos_lista)
          nuevos_goles = st.number_input(
              "Goles Totales", min_value=0, step=1, value=1
          )
          add_g = st.form_submit_button("Registrar Nuevo Goleador")
          if add_g and nuevo_jugador:
            nueva_fila = pd.DataFrame({
                "Jugador": [nuevo_jugador],
                "Equipo": [nuevo_equipo],
                "Goles": [nuevos_goles],
            })
            st.session_state.df_goleadores = pd.concat(
                [df_gols, nueva_fila], ignore_index=True
            )
            st.success("¡Nuevo goleador registrado con éxito!")
            st.rerun()
        else:
          idx_g = df_gols[df_gols["Jugador"] == jugador_sel].index[0]
          goles_actuales = int(df_gols.loc[idx_g, "Goles"])
          actualizar_goles = st.number_input(
              "Actualizar Goles", min_value=0, step=1, value=goles_actuales
          )

          up_g = st.form_submit_button("Actualizar Goles del Jugador")
          if up_g:
            df_gols.loc[idx_g, "Goles"] = actualizar_goles
            st.success("¡Goles actualizados con éxito!")
            st.rerun()

  elif pwd_ingresada != "":
    st.error("Contraseña incorrecta. Intenta de nuevo.")
  else:
    st.info(
        "🔒 Por favor, ingresa la contraseña para desbloquear el panel de"
        " administración."
    )
