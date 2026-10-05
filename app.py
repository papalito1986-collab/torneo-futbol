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
            # Forzar la lectura de columnas clave como texto para soportar jornadas y fases personalizadas
            df = pd.read_csv(
                path_archivo, dtype={"Jornada": str, "Local": str, "Visita": str}
            )
            return df.reset_index(drop=True)
        except Exception:
            pass
    guardar_local(path_archivo, df_default)
    return df_default.reset_index(drop=True)


# Funciones para cargar datos iniciales locales
def cargar_datos():
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

    df_part_default = pd.DataFrame({
        "Jornada": [
            "6 de Octubre",
            "6 de Octubre",
            "6 de Octubre",
            "6 de Octubre",
            "7 de Octubre",
            "7 de Octubre",
            "7 de Octubre",
            "7 de Octubre",
        ],
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
    st.session_state.datos_cargados = True

equipos_lista = st.session_state.equipos_lista
df = st.session_state.df_partidos.reset_index(drop=True)
df_gols = st.session_state.df_goleadores.reset_index(drop=True)

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
        div.stButton > button:first-child { background: linear-gradient(135deg, #FFD100 0%, #f4b400 100%) !important; color: #3A0CA3 !important; font-weight: 900 !important; border-radius: 10px !important; border: none !important; }
        div.stButton > button:first-child:hover { background: linear-gradient(135deg, #ffdc33 0%, #ffc107 100%) !important; color: #240046 !important; }
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
    st.markdown("⚽ *Seguimiento en tiempo real.*")

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
        loc, vis = str(row["Local"]), str(row["Visita"])
        try:
            g_loc, g_vis = int(row["Goles Local"]), int(row["Goles Visita"])
        except:
            continue

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
    st.subheader("📅 Calendario y Resultados por Jornada / Fase")
    if df.empty:
        st.info("ℹ️ No hay encuentros programados.")
    else:
        jornadas_disponibles = df["Jornada"].dropna().unique().tolist()
        jornada_sel = st.selectbox(
            "Selecciona la Jornada o Fase:", jornadas_disponibles
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
                "⚽ Administrar Partidos (Agregar / Editar / Eliminar)",
                "Actualizar Resultados de Partidos",
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
                            st.session_state.equipos_lista = equipos_lista
                            df_eq_new = pd.DataFrame({"Equipo": equipos_lista})
                            guardar_local(FILE_EQUIPOS, df_eq_new)
                            st.success(
                                f"✅ ¡Equipo '{nuevo_eq}' agregado con éxito!"
                            )
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
                            st.session_state.equipos_lista = equipos_lista
                            guardar_local(
                                FILE_EQUIPOS, pd.DataFrame({"Equipo": equipos_lista})
                            )

                            df["Local"] = df["Local"].replace(eq_a_mod, nuevo_nombre_eq)
                            df["Visita"] = df["Visita"].replace(eq_a_mod, nuevo_nombre_eq)
                            df_clean = df.reset_index(drop=True)
                            st.session_state.df_partidos = df_clean
                            guardar_local(FILE_PARTIDOS, df_clean)

                            if not df_gols.empty:
                                df_gols["Equipo"] = df_gols["Equipo"].replace(
                                    eq_a_mod, nuevo_nombre_eq
                                )
                                df_gols_clean = df_gols.reset_index(drop=True)
                                st.session_state.df_goleadores = df_gols_clean
                                guardar_local(FILE_GOLEADORES, df_gols_clean)

                            st.success(
                                f"✅ ¡Equipo '{eq_a_mod}' renombrado a '{nuevo_nombre_eq}'!"
                            )
                            st.rerun()
                        else:
                            st.warning("⚠️ El nuevo nombre está vacío o ya existe.")

            elif op_equipo == "Eliminar Equipo":
                with st.form("form_delete_equipo"):
                    eq_a_del = st.selectbox("Selecciona el equipo a eliminar:", equipos_lista)
                    btn_del_eq = st.form_submit_button("Eliminar Equipo")
                    if btn_del_eq:
                        if eq_a_del in equipos_lista:
                            equipos_lista.remove(eq_a_del)
                            st.session_state.equipos_lista = equipos_lista
                            guardar_local(
                                FILE_EQUIPOS, pd.DataFrame({"Equipo": equipos_lista})
                            )

                            df_filtrado = df[
                                (df["Local"] != eq_a_del) & (df["Visita"] != eq_a_del)
                            ].reset_index(drop=True)
                            st.session_state.df_partidos = df_filtrado
                            guardar_local(FILE_PARTIDOS, df_filtrado)

                            st.success(
                                f"✅ ¡Equipo '{eq_a_del}' eliminado del torneo!"
                            )
                            st.rerun()

        elif admin_opcion == "⚽ Administrar Partidos (Agregar / Editar / Eliminar)":
            sub_partido_op = st.selectbox(
                "Selecciona la acción para partidos:",
                ["Agregar Nuevo Partido", "Editar Partido Existente", "Eliminar Partido"],
            )

            if sub_partido_op == "Agregar Nuevo Partido":
                with st.form("form_add_partido"):
                    st.markdown("### Programa un nuevo encuentro")
                    nueva_jornada = st.text_input(
                        "Jornada o Fase (ej. '6 de Octubre', 'Cuartos de Final', 'Semifinal', 'Final')"
                    )
                    col_l, col_v = st.columns(2)
                    with col_l:
                         equipo_local = st.selectbox("Equipo Local", equipos_lista, key="add_loc")
                    with col_v:
                         equipo_visita = st.selectbox("Equipo Visita", equipos_lista, key="add_vis")
                    
                    btn_crear_partido = st.form_submit_button("Guardar Nuevo Partido")
                    if btn_crear_partido:
                        if nueva_jornada and equipo_local != equipo_visita:
                            nueva_fila = pd.DataFrame({
                                "Jornada": [nueva_jornada],
                                "Local": [equipo_local],
                                "Goles Local": [0],
                                "Goles Visita": [0],
                                "Visita": [equipo_visita],
                                "Jugado": [False]
                            })
                            df_updated = pd.concat([df, nueva_fila], ignore_index=True)
                            st.session_state.df_partidos = df_updated
                            guardar_local(FILE_PARTIDOS, df_updated)
                            st.success("✅ ¡Partido agregado con éxito!")
                            st.rerun()
                        else:
                            st.warning("⚠️ Asegúrate de escribir la jornada/fase y que el local y visita sean distintos.")

            elif sub_partido_op == "Editar Partido Existente":
                if df.empty:
                    st.info("No hay partidos registrados para editar.")
                else:
                    with st.form("form_edit_partido"):
                        df_edit = df.reset_index(drop=True)
                        partidos_ids = [
                            f"[{row['Jornada']}] {row['Local']} vs {row['Visita']} (Idx: {idx})"
                            for idx, row in df_edit.iterrows()
                        ]
                        partido_elegido = st.selectbox("Selecciona el partido a editar:", partidos_ids)
                        idx_sel = int(partido_elegido.split("(Idx: ")[1].replace(")", ""))

                        row_actual = df_edit.loc[idx_sel]
                        nueva_j = st.text_input("Jornada o Fase", value=str(row_actual["Jornada"]))
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            nuevo_l = st.selectbox("Local", equipos_lista, index=equipos_lista.index(row_actual["Local"]) if row_actual["Local"] in equipos_lista else 0, key="edit_l")
                            g_l = st.number_input("Goles Local", min_value=0, step=1, value=int(row_actual["Goles Local"]))
                        with col2:
                            nuevo_v = st.selectbox("Visita", equipos_lista, index=equipos_lista.index(row_actual["Visita"]) if row_actual["Visita"] in equipos_lista else 0, key="edit_v")
                            g_v = st.number_input("Goles Visita", min_value=0, step=1, value=int(row_actual["Goles Visita"]))
                        
                        jugado_val = st.checkbox("¿Jugado?", value=bool(row_actual["Jugado"]))

                        btn_guardar_edit = st.form_submit_button("Actualizar Partido")
                        if btn_guardar_edit:
                            df_edit.loc[idx_sel, "Jornada"] = nueva_j
                            df_edit.loc[idx_sel, "Local"] = nuevo_l
                            df_edit.loc[idx_sel, "Visita"] = nuevo_v
                            df_edit.loc[idx_sel, "Goles Local"] = g_l
                            df_edit.loc[idx_sel, "Goles Visita"] = g_v
                            df_edit.loc[idx_sel, "Jugado"] = jugado_val

                            st.session_state.df_partidos = df_edit
                            guardar_local(FILE_PARTIDOS, df_edit)
                            st.success("✅ ¡Partido actualizado correctamente!")
                            st.rerun()

            elif sub_partido_op == "Eliminar Partido":
                if df.empty:
                    st.info("No hay partidos para eliminar.")
                else:
                    with st.form("form_del_partido"):
                        df_del = df.reset_index(drop=True)
                        partidos_ids_del = [
                            f"[{row['Jornada']}] {row['Local']} vs {row['Visita']} (Idx: {idx})"
                            for idx, row in df_del.iterrows()
                        ]
                        partido_a_borrar = st.selectbox("Selecciona el partido a eliminar:", partidos_ids_del)
                        idx_del = int(partido_a_borrar.split("(Idx: ")[1].replace(")", ""))

                        btn_confirmar_del = st.form_submit_button("Eliminar Partido Seleccionado")
                        if btn_confirmar_del:
                            df_final_del = df_del.drop(idx_del).reset_index(drop=True)
                            st.session_state.df_partidos = df_final_del
                            guardar_local(FILE_PARTIDOS, df_final_del)
                            st.success("🗑️ ¡Partido eliminado con éxito!")
                            st.rerun()

        elif admin_opcion == "Actualizar Resultados de Partidos":
            with st.form("form_resultado"):
                df_reset = df.reset_index(drop=True)
                if df_reset.empty:
                    st.info("No hay partidos registrados.")
                    st.form_submit_button("Sin partidos")
                else:
                    lista_partidos_ids = []
                    for idx, row in df_reset.iterrows():
                        p_id = f"[{str(row['Jornada'])}]: {str(row['Local'])} vs {str(row['Visita'])}"
                        lista_partidos_ids.append(p_id)
                    
                    df_reset["Partido_ID"] = lista_partidos_ids

                    partido_sel = st.selectbox(
                        "Selecciona el partido a actualizar:",
                        df_reset["Partido_ID"].tolist(),
                    )

                    fila_partido = df_reset[df_reset["Partido_ID"] == partido_sel].iloc[0]
                    partido_idx = fila_partido.name

                    nuevo_g_loc = st.number_input(
                        "Goles Local",
                        min_value=0,
                        step=1,
                        value=int(fila_partido["Goles Local"]),
                    )
                    nuevo_g_vis = st.number_input(
                        "Goles Visita",
                        min_value=0,
                        step=1,
                        value=int(fila_partido["Goles Visita"]),
                    )
                    marcar_jugado = st.checkbox(
                        "¿Partido Jugado?", value=bool(fila_partido["Jugado"])
                    )

                    submitted = st.form_submit_button("Guardar Resultado")
                    if submitted:
                        df_reset = df_reset.drop(columns=["Partido_ID"])
                        df_reset.loc[partido_idx, "Goles Local"] = nuevo_g_loc
                        df_reset.loc[partido_idx, "Goles Visita"] = nuevo_g_vis
                        df_reset.loc[partido_idx, "Jugado"] = marcar_jugado

                        df_clean = df_reset.reset_index(drop=True)
                        st.session_state.df_partidos = df_clean
                        guardar_local(FILE_PARTIDOS, df_clean)
                        st.success("✅ ¡Resultado guardado con éxito!")
                        st.rerun()

        elif admin_opcion == "Actualizar o Agregar Goleadores":
            with st.form("form_goleador"):
                lista_opciones = ["+ Agregar Nuevo Jugador"]
                df_gols_reset = df_gols.reset_index(drop=True)
                if not df_gols_reset.empty:
                    lista_opciones = df_gols_reset["Jugador"].tolist() + [
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
                        df_gols_updated = pd.concat(
                            [df_gols_reset, nueva_fila], ignore_index=True
                        ).reset_index(drop=True)
                        st.session_state.df_goleadores = df_gols_updated
                        guardar_local(FILE_GOLEADORES, df_gols_updated)
                        st.success(
                            f"✅ ¡Goleador '{nuevo_jugador}' registrado con éxito!"
                        )
                        st.rerun()
                else:
                    idx_g = df_gols_reset[
                        df_gols_reset["Jugador"] == jugador_sel
                    ].index[0]
                    goles_actuales = int(df_gols_reset.loc[idx_g, "Goles"])
                    actualizar_goles = st.number_input(
                        "Actualizar Goles", min_value=0, step=1, value=goles_actuales
                    )
                    up_g = st.form_submit_button("Actualizar Goles del Jugador")
                    if up_g:
                        df_gols_reset.loc[idx_g, "Goles"] = actualizar_goles
                        df_gols_clean = df_gols_reset.reset_index(drop=True)
                        st.session_state.df_goleadores = df_gols_clean
                        guardar_local(FILE_GOLEADORES, df_gols_clean)
                        st.success("✅ ¡Goles actualizados con éxito!")
                        st.rerun()

        elif admin_opcion == "🗑️ Eliminar Goleadores":
            with st.form("form_eliminar_goleador"):
                df_gols_reset = df_gols.reset_index(drop=True)
                if df_gols_reset.empty:
                    st.info("No hay goleadores registrados.")
                    st.form_submit_button("Sin registros")
                else:
                    jugador_a_eliminar = st.selectbox(
                        "Selecciona el jugador a eliminar:",
                        df_gols_reset["Jugador"].tolist(),
                    )
                    btn_del_g = st.form_submit_button("Eliminar Goleador")
                    if btn_del_g:
                        df_gols_clean = df_gols_reset[
                            df_gols_reset["Jugador"] != jugador_a_eliminar
                        ].reset_index(drop=True)
                        st.session_state.df_goleadores = df_gols_clean
                        guardar_local(FILE_GOLEADORES, df_gols_clean)
                        st.success("✅ ¡Goleador eliminado con éxito!")
                        st.rerun()

    elif pwd_ingresada != "":
        st.error("❌ Contraseña incorrecta.")
