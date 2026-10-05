from datetime import datetime
import os
import pandas as pd
import streamlit as st

# Configuración inicial de la página web
st.set_page_config(
    page_title="Torneo de Fútbol - Teletón Sonora", page_icon="⚽", layout="wide"
)

FILE_EQUIPOS = "equipos.csv"
FILE_PARTIDOS = "partidos.csv"
FILE_GOLEADORES = "goleadores.csv"


def guardar_local(path_archivo, df_o_contenido):
  """Guarda un archivo CSV localmente."""
  try:
    if isinstance(df_o_contenido, pd.DataFrame):
      df_o_contenido.to_csv(path_archivo, index=False)
    else:
      with open(path_archivo, "w", encoding="utf-8") as f:
        f.write(df_o_contenido)
    return True
  except Exception as e:
    st.error(f"Error al guardar localmente ({path_archivo}): {e}")
    return False


def cargar_o_crear_local(path_archivo, df_default):
  """Carga el archivo CSV local si existe; si no, usa el default y lo guarda."""
  if os.path.exists(path_archivo):
    try:
      return pd.read_csv(path_archivo)
    except Exception:
      pass
  # Si no existe o hay error, creamos el archivo por defecto
  guardar_local(path_archivo, df_default)
  return df_default


# Funciones para cargar datos iniciales locales
def cargar_datos():
  # 1. Equipos por defecto
  df_eq_default = pd.DataFrame({
      "Equipo": [
          "REAL SOCIEDAD",
          "LOS DEFENSORES",
          "LA CARIDAD FC",
          "ORGULLOSAMENTE TERCOS",
          "CUERVOS FC - AXOMA",
          "CLUB GRIEGOS ISJ",
          "Piratitas del Sahuaro FC",
          "TELETONES",
          "MASTER FC JUAREZ",
          "ELECTRICA FLORES BRAVOS HERMOSILLO",
          "CENTRO DE FORMACION DEL CLUB AMERICA HERMOSILLO",
          "ACADEMIA TOROS",
          "ARBITROS ZONA NORTE",
          "HOSPITAL MILITAR-SEDENA",
          "AXOMA",
          "LOS FELIX",
      ]
  })
  df_eq = cargar_o_crear_local(FILE_EQUIPOS, df_eq_default)
  equipos_lista = df_eq["Equipo"].tolist()

  # 2. Partidos por defecto
  df_part_default = pd.DataFrame({
      "Jornada": [1, 1, 1, 1, 1, 1, 1, 1],
      "Local": [
          "REAL SOCIEDAD",
          "LOS DEFENSORES",
          "LA CARIDAD FC",
          "ORGULLOSAMENTE TERCOS",
          "CUERVOS FC - AXOMA",
          "CLUB GRIEGOS ISJ",
          "Piratitas del Sahuaro FC",
          "TELETONES",
      ],
      "Goles Local": [0, 0, 0, 0, 0, 0, 0, 0],
      "Goles Visita": [0, 0, 0, 0, 0, 0, 0, 0],
      "Visita": [
          "LOS FELIX",
          "AXOMA",
          "HOSPITAL MILITAR-SEDENA",
          "ARBITROS ZONA NORTE",
          "ACADEMIA TOROS",
          "CENTRO DE FORMACION DEL CLUB AMERICA HERMOSILLO",
          "ELECTRICA FLORES BRAVOS HERMOSILLO",
          "MASTER FC JUAREZ",
      ],
      "Jugado": [False, False, False, False, False, False, False, False],
  })
  df_part = cargar_o_crear_local(FILE_PARTIDOS, df_part_default)

  # 3. Goleadores por defecto
  df_gol_default = pd.DataFrame(columns=["Jugador", "Equipo", "Goles"])
  df_gol = cargar_o_crear_local(FILE_GOLEADORES, df_gol_default)

  return equipos_lista, df_part, df_gol


# Inicializar estado con los archivos locales
if "datos_cargados" not in st.session_state:
  (
      st.session_state.equipos_lista,
      st.session_state.df_partidos,
      st.session_state.df_goleadores,
  ) = cargar_datos()
  if "fotos_partidos" not in st.session_state:
    st.session_state.fotos_partidos = {}
  st.session_state.datos_cargados = True

equipos_lista = st.session_state.equipos_lista
df = st.session_state.df_partidos
df_gols = st.session_state.df_goleadores

# --- ESTILOS CSS PERSONALIZADOS ---
st.markdown(
    """
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stApp { background: linear-gradient(135deg, #3A0CA3 0%, #4A154B 50%, #240046 100%); color: #FFFFFF; }
        h1, h2, h3, h4, h5, h6, p, span, label, .stMarkdown { color: #FFFFFF !important; }
        h1 { font-weight: 900; text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.6); }
        div.stTabs [data-baseweb="tab-list"] { gap: 10px; background-color: rgba(255, 255, 255, 0.05); padding: 10px; border-radius: 12px; }
        div.stTabs [data-baseweb="tab"] { background: linear-gradient(145deg, #5C1D5D, #4A154B); border-radius: 8px; color: #FFFFFF !important; font-weight: 700; border-top: 4px solid #FFD100; }
        div.stTabs [aria-selected="true"] { background: linear-gradient(145deg, #FFD100, #ffc107) !important; color: #3A0CA3 !important; border-top: 4px solid #FFFFFF !important; font-weight: 900 !important; }
        div.stTabs [aria-selected="true"] * { color: #3A0CA3 !important; }
        .dataframe { background-color: rgba(255, 255, 255, 0.95) !important; color: #1a1a1a !important; border-radius: 12px !important; }
        div.stExpander, div.stForm { background: rgba(255, 255, 255, 0.08); border-radius: 12px; border: 1px solid rgba(255, 209, 0, 0.3); }
        div.stButton > button:first-child { background: linear-gradient(135deg, #FFD100 0%, #f4b400 100%); color: #3A0CA3; font-weight: 900; border-radius: 10px; }
    </style>
""",
    unsafe_allow_html=True,
)

# --- ENCABEZADO CON LOGO ---
col_logo, col_titulo = st.columns([1, 5])
with col_logo:
  try:
    st.image("logo_crit.png", width=120)
  except:
    st.markdown("🏟️", unsafe_allow_html=True)
with col_titulo:
  st.title("🏆 Torneo de Fútbol - CRIT SONORA")
  st.markdown("⚽ *Seguimiento en tiempo real (Modo Local).*")

st.markdown("---")

# --- PESTAÑAS DE NAVEGACIÓN ---
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Tabla General",
    "⚽ Resultados y Calendario",
    "👟 Tabla de Goleadores",
    "⚙️ Administrar Torneo",
])

# Pestaña 1: Tabla de Posiciones
with tab1:
  st.subheader("🌟 Clasificación General del Torneo")
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
    g_loc, g_vis = int(row["Goles Local"]), int(row["Goles Visita"])

    if loc in stats:
      stats[loc]["JJ"] += 1
      stats[loc]["GF"] += g_loc
      stats[loc]["GC"] += g_vis
    if vis in stats:
      stats[vis]["JJ"] += 1
      stats[vis]["GF"] += g_vis
      stats[vis]["GC"] += g_loc

    if loc in stats and vis in stats:
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

  st.dataframe(df_tabla, use_container_width=True, height=600)

# Pestaña 2: Calendario y Resultados
with tab2:
  st.subheader("📅 Calendario y Resultados por Jornada")
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

# Pestaña 3: Tabla de Goleadores
with tab3:
  st.subheader("👟 Tabla de Máximos Goleadores")
  if df_gols.empty:
    st.info("ℹ️ Aún no hay goleadores registrados.")
  else:
    df_gols_sorted = df_gols.sort_values(by="Goles", ascending=False).reset_index(
        drop=True
    )
    df_gols_sorted.index = df_gols_sorted.index + 1
    st.dataframe(df_gols_sorted, use_container_width=True)

# Pestaña 4: Administrar Torneo
with tab4:
  st.subheader("⚙️ Panel de Administración")
  PASSWORD_ADMIN = "crit2026"
  pwd_ingresada = st.text_input(
      "Introduce la contraseña de administrador:", type="password"
  )

  if pwd_ingresada == PASSWORD_ADMIN:
    st.success("🎉 ¡Contraseña correcta!")
    admin_opcion = st.radio(
        "¿Qué deseas realizar?",
        [
            "🏟️ Administrar Equipos (Agregar / Modificar / Eliminar)",
            "Actualizar Resultados",
            "Actualizar o Agregar Goleadores",
            "🗑️ Eliminar Goleadores",
        ],
    )

    if admin_opcion == "🏟️ Administrar Equipos (Agregar / Modificar / Eliminar)":
      op_equipo = st.selectbox(
          "Selecciona una acción:",
          ["Agregar Nuevo Equipo", "Modificar / Renombrar Equipo", "Eliminar Equipo"],
      )

      if op_equipo == "Agregar Nuevo Equipo":
        with st.form("form_add_equipo"):
          nuevo_eq = st.text_input("Nombre del nuevo equipo:")
          btn_add_eq = st.form_submit_button("Agregar Equipo")
          if btn_add_eq:
            if nuevo_eq and nuevo_eq not in equipos_lista:
              equipos_lista.append(nuevo_eq)
              df_eq_new = pd.DataFrame({"Equipo": equipos_lista})
              guardar_local(FILE_EQUIPOS, df_eq_new)
              st.success(f"✅ ¡Equipo '{nuevo_eq}' agregado localmente!")
              st.rerun()
            else:
              st.warning("⚠️ El nombre está vacío o ya existe.")

      elif op_equipo == "Modificar / Renombrar Equipo":
        with st.form("form_edit_equipo"):
          eq_a_mod = st.selectbox("Selecciona el equipo a modificar:", equipos_lista)
          nuevo_nombre_eq = st.text_input(
              "Nuevo nombre para el equipo:", value=eq_a_mod
          )
          btn_edit_eq = st.form_submit_button("Guardar Cambios")
          if btn_edit_eq:
            if nuevo_nombre_eq and nuevo_nombre_eq not in equipos_lista:
              idx_e = equipos_lista.index(eq_a_mod)
              equipos_lista[idx_e] = nuevo_nombre_eq
              guardar_local(
                  FILE_EQUIPOS, pd.DataFrame({"Equipo": equipos_lista})
              )

              df["Local"] = df["Local"].replace(eq_a_mod, nuevo_nombre_eq)
              df["Visita"] = df["Visita"].replace(eq_a_mod, nuevo_nombre_eq)
              guardar_local(FILE_PARTIDOS, df)

              if not df_gols.empty:
                df_gols["Equipo"] = df_gols["Equipo"].replace(
                    eq_a_mod, nuevo_nombre_eq
                )
                guardar_local(FILE_GOLEADORES, df_gols)

              st.success("✅ ¡Actualizado localmente con éxito!")
              st.rerun()

    elif admin_opcion == "Actualizar Resultados":
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
          guardar_local(FILE_PARTIDOS, df)
          st.success("✅ ¡Resultado guardado localmente!")
          st.rerun()

    elif admin_opcion == "Actualizar o Agregar Goleadores":
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
            guardar_local(FILE_GOLEADORES, st.session_state.df_goleadores)
            st.success("✅ ¡Goleador registrado localmente!")
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
            guardar_local(FILE_GOLEADORES, df_gols)
            st.success("✅ ¡Goles actualizados localmente!")
            st.rerun()

    elif admin_opcion == "🗑️ Eliminar Goleadores":
      with st.form("form_eliminar_goleador"):
        if df_gols.empty:
          st.info("No hay goleadores registrados.")
          st.form_submit_button("Sin registros")
        else:
          jugador_a_eliminar = st.selectbox(
              "Selecciona el jugador a eliminar:", df_gols["Jugador"].tolist()
          )
          btn_del_g = st.form_submit_button("Eliminar Goleador")
          if btn_del_g:
            st.session_state.df_goleadores = df_gols[
                df_gols["Jugador"] != jugador_a_eliminar
            ].reset_index(drop=True)
            guardar_local(FILE_GOLEADORES, st.session_state.df_goleadores)
            st.success("✅ ¡Goleador eliminado!")
            st.rerun()

  elif pwd_ingresada != "":
    st.error("❌ Contraseña incorrecta.")
