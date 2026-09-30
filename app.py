import pandas as pd
import streamlit as st

# Configuración inicial de la página web
st.set_page_config(
    page_title="Torneo de Fútbol - Dashboard", page_icon="⚽", layout="wide"
)

# --- ENCABEZADO CON LOGO ---
col_logo, col_titulo = st.columns([1, 5])

with col_logo:
  try:
    st.image("logo_crit.png", width=120)
  except:
    st.write("🏟️")

with col_titulo:
  st.title("🏆 Torneo de Fútbol - CRIT SONORA")
  st.markdown(
      "Seguimiento en tiempo real de resultados, tabla general y"
      " estadísticas."
  )

st.markdown("---")

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

# 2. Inicializar los datos de los partidos (En ceros y sin jugar desde el inicio)
if "df_partidos" not in st.session_state:
  st.session_state.df_partidos = pd.DataFrame({
      "Jornada": [1, 1, 1, 1, 1, 2, 2, 2, 2, 2],
      "Local": [
          "Crit Sonoa",
          "TE",
          "Leoni",
          "Clandestinos",
          "Parrilleros",
          "Crit Sonoa",
          "TE",
          "Leoni",
          "Clandestinos",
          "Parrilleros",
      ],
      "Goles Local": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      "Goles Visita": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      "Visita": [
          "TE",
          "Leoni",
          "Clandestinos",
          "Parrilleros",
          "T&P",
          "Malcriados",
          "Arrabaleros",
          "Costeños",
          "Pisacorres",
          "T&P",
      ],
      "Jugado": [
          False,
          False,
          False,
          False,
          False,
          False,
          False,
          False,
          False,
          False,
      ],
  })

# Diccionario independiente para guardar las fotos por índice de partido
if "fotos_partidos" not in st.session_state:
  st.session_state.fotos_partidos = {}

# 3. Inicializar tabla de Goleadores vacía desde el inicio
if "df_goleadores" not in st.session_state:
  st.session_state.df_goleadores = pd.DataFrame(
      columns=["Jugador", "Equipo", "Goles"]
  )

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

# Pestaña 2: Calendario, Resultados y Enlaces/Rutas de Fotos por Jornada
with tab2:
  st.subheader("Calendario y Resultados por Jornada")
  jornada_sel = st.selectbox(
      "Selecciona la Jornada:", sorted(df["Jornada"].unique())
  )
  df_jornada = df[df["Jornada"] == jornada_sel]

  st.dataframe(
      df_jornada[[
          "Jornada",
          "Local",
          "Goles Local",
          "Goles Visita",
          "Visita",
          "Jugado",
      ]],
      use_container_width=True,
  )

  st.markdown("---")
  st.subheader("📁 Archivos y Rutas de Fotos de los Partidos")

  # Mostrar la ruta o nombre del archivo de la foto registrada en formato de lista/enlace
  hay_fotos_jornada = False
  for idx, row in df_jornada.iterrows():
    if idx in st.session_state.fotos_partidos:
      hay_fotos_jornada = True
      archivo_subido = st.session_state.fotos_partidos[idx]
      nombre_archivo = (
          archivo_subido.name
          if hasattr(archivo_subido, "name")
          else "imagen_partido.png"
      )

      st.markdown(
          f"🔹 **Partido:** {row['Local']} ({row['Goles Local']}) vs"
          f" {row['Visita']} ({row['Goles Visita']})"
      )
      st.code(
          f"Ruta/Archivo registrado: media/partidos/{nombre_archivo}",
          language="text",
      )

      # Si aún deseas ver la miniatura al hacer clic o de forma desplegable:
      with st.expander(
          f"Ver imagen vinculada: {row['Local']} vs {row['Visita']}"
      ):
        st.image(archivo_subido, use_container_width=True)

  if not hay_fotos_jornada:
    st.info("No hay rutas o archivos de fotos registrados para esta jornada.")

# Pestaña 3: Tabla de Goleadores
with tab3:
  st.subheader("👟 Máximos Goleadores del Torneo")
  if df_gols.empty:
    st.info(
        "Aún no hay goleadores registrados. Se irán agregando desde el panel de"
        " administración."
    )
  else:
    df_gols_sorted = df_gols.sort_values(by="Goles", ascending=False).reset_index(
        drop=True
    )
    df_gols_sorted.index = df_gols_sorted.index + 1
    st.dataframe(df_gols_sorted, use_container_width=True)

# Pestaña 4: Panel para actualizar resultados y resetear datos protegido por contraseña
with tab4:
  st.subheader("⚙ Panel de Administración")
  st.markdown("Acceso exclusivo para el organizador del torneo.")

  PASSWORD_ADMIN = "crit2026"
  pwd_ingresada = st.text_input(
      "Introduce la contraseña de administrador:", type="password"
  )

  if pwd_ingresada == PASSWORD_ADMIN:
    st.success("¡Contraseña correcta! Ya puedes administrar el torneo.")

    admin_opcion = st.radio(
        "¿Qué deseas realizar?",
        [
            "Actualizar Resultados y Fotos",
            "Actualizar Goleadores",
            "⚠️ Reiniciar Torneo (Reset)",
        ],
    )

    if admin_opcion == "Actualizar Resultados y Fotos":
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

        submitted = st.form_submit_button("Guardar Resultado")
        if submitted:
          df.loc[partido_idx, "Goles Local"] = nuevo_g_loc
          df.loc[partido_idx, "Goles Visita"] = nuevo_g_vis
          df.loc[partido_idx, "Jugado"] = marcar_jugado
          st.success("¡Resultado actualizado con éxito!")
          st.rerun()

      st.markdown("---")
      st.subheader("📷 Subir o cambiar archivo/ruta de foto del partido")
      partido_foto_idx = st.selectbox(
          "Selecciona el partido para la foto:",
          df.index,
          key="select_foto",
          format_func=lambda i: f"J{df.loc[i, 'Jornada']}: {df.loc[i, 'Local']} vs {df.loc[i, 'Visita']}",
      )
      foto_subida = st.file_uploader(
          "Sube la imagen del partido (PNG, JPG)", type=["png", "jpg", "jpeg"]
      )

      if st.button("Guardar Referencia de Foto"):
        if foto_subida is not None:
          st.session_state.fotos_partidos[partido_foto_idx] = foto_subida
          st.success("¡Referencia de foto guardada correctamente!")
          st.rerun()
        else:
          st.warning("Por favor selecciona una imagen primero.")

    elif admin_opcion == "Actualizar Goleadores":
      with st.form("form_goleador"):
        lista_opciones = ["+ Agregar Nuevo Jugador"]
        if not df_gols.empty:
          lista_opciones = df_gols["Jugador"].tolist() + [
              "+ Agregar Nuevo Jugador"
          ]

        jugador_sel = st.selectbox("Selecciona o registra jugador:", lista_opciones)

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

    elif admin_opcion == "⚠️ Reiniciar Torneo (Reset)":
      st.warning(
          "⚠️ **¡CUIDADO!** Esta acción borrará todos los marcadores, goles,"
          " estadísticas y fotos registradas, regresando todo a cero."
      )

      confirmar_reset = st.checkbox(
          "Confirmo que deseo reiniciar todos los datos del torneo"
      )

      if st.button("Ejecutar Reinicio Completo", type="primary"):
        if confirmar_reset:
          # Borrar las variables de sesión para reiniciar los valores por defecto
          del st.session_state.df_partidos
          del st.session_state.fotos_partidos
          del st.session_state.df_goleadores
          st.success(
              "¡El torneo se ha reiniciado por completo exitosamente!"
          )
          st.rerun()
        else:
          st.error(
              "Debes marcar la casilla de confirmación para poder reiniciar los"
              " datos."
          )

  elif pwd_ingresada != "":
    st.error("Contraseña incorrecta. Intenta de nuevo.")
  else:
    st.info(
        "🔒 Por favor, ingresa la contraseña para desbloquear el panel de"
        " administración."
    )
