import pandas as pd
import streamlit as st

# Configuración inicial de la página web
st.set_page_config(
    page_title="Torneo de Fútbol - Teletón Sonora", page_icon="⚽", layout="wide"
)

# --- ESTILOS CSS PERSONALIZADOS (Tema Teletón 3D Morado Intenso y Amarillo Brillante) ---
st.markdown("""
    <style>
        /* Fondo general de la aplicación con degradado morado 3D profundo */
        .stApp {
            background: linear-gradient(135deg, #3A0CA3 0%, #4A154B 50%, #240046 100%);
            color: #FFFFFF;
        }
        
        /* Textos generales en blanco brillante para excelente visibilidad */
        h1, h2, h3, h4, h5, h6, p, span, label, .stMarkdown {
            color: #FFFFFF !important;
        }

        /* Encabezado Principal 3D */
        h1 {
            font-weight: 900;
            text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.6), 0px 0px 15px rgba(255, 209, 0, 0.4);
            letter-spacing: 1px;
        }

        /* Pestañas de navegación con efecto 3D flotante */
        div.stTabs [data-baseweb="tab-list"] {
            gap: 10px;
            background-color: rgba(255, 255, 255, 0.05);
            padding: 10px;
            border-radius: 12px;
            box-shadow: inset 0 4px 6px rgba(0,0,0,0.3);
        }
        
        div.stTabs [data-baseweb="tab"] {
            background: linear-gradient(145deg, #5C1D5D, #4A154B);
            border-radius: 8px;
            color: #FFFFFF !important;
            font-weight: 700;
            box-shadow: 0px 6px 10px rgba(0, 0, 0, 0.4), 0px 1px 3px rgba(255,255,255,0.1) inset;
            border-top: 4px solid #FFD100;
            transition: all 0.3s ease-in-out;
        }

        div.stTabs [data-baseweb="tab"]:hover {
            transform: translateY(-2px);
            box-shadow: 0px 8px 14px rgba(0, 0, 0, 0.5);
        }

        div.stTabs [aria-selected="true"] {
            background: linear-gradient(145deg, #FFD100, #ffc107) !important;
            color: #3A0CA3 !important;
            box-shadow: 0px 8px 16px rgba(255, 209, 0, 0.5), inset 0px 2px 4px rgba(255,255,255,0.6) !important;
            border-top: 4px solid #FFFFFF !important;
            font-weight: 900 !important;
        }
        div.stTabs [aria-selected="true"] * {
            color: #3A0CA3 !important;
        }

        /* Tablas y DataFrames con diseño flotante y contraste nítido */
        .dataframe {
            background-color: rgba(255, 255, 255, 0.95) !important;
            color: #1a1a1a !important;
            border-radius: 12px !important;
            box-shadow: 0 10px 25px rgba(0,0,0,0.5) !important;
        }
        
        /* Contenedores de elementos y cajas estilo 3D */
        div.stExpander, div.stForm {
            background: rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            border: 1px solid rgba(255, 209, 0, 0.3);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
        }

        /* Botones principales Teletón (Amarillo 3D impactante) */
        div.stButton > button:first-child {
            background: linear-gradient(135deg, #FFD100 0%, #f4b400 100%);
            color: #3A0CA3;
            font-weight: 900;
            border-radius: 10px;
            border: 2px solid #ffffff;
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.4), inset 0 2px 4px rgba(255, 255, 255, 0.8);
            transition: all 0.2s ease;
        }
        
        div.stButton > button:first-child:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 20px rgba(255, 209, 0, 0.6), inset 0 2px 4px rgba(255, 255, 255, 0.9);
            background: linear-gradient(135deg, #ffe033 0%, #FFD100 100%);
            color: #240046;
        }

        /* Campos de texto, selectores y entradas flotantes con visibilidad clara */
        .stSelectbox div[data-baseweb="select"], .stTextInput input, .stNumberInput input {
            background-color: rgba(255, 255, 255, 0.9) !important;
            color: #1a1a1a !important;
            border-radius: 8px !important;
            font-weight: 600;
        }
        
        /* Mensajes informativos y de éxito */
        .stAlert {
            background: rgba(255, 255, 255, 0.1) !important;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 209, 0, 0.5);
            color: #FFFFFF !important;
            box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        }
    </style>
""", unsafe_allow_html=True)

# --- ENCABEZADO CON LOGO ---
col_logo, col_titulo = st.columns([1, 5])

with col_logo:
    try:
        st.image("logo_crit.png", width=120)
    except:
        st.markdown("🏟️", unsafe_allow_html=True)

with col_titulo:
    st.title("🏆 Torneo de Fútbol - CRIT SONORA")
    st.markdown(
        "⚽ *Seguimiento en tiempo real de resultados, tabla general y"
        " estadísticas con causa Teletón.*"
    )

st.markdown("---")

# 1. Inicializar la lista de equipos en el session_state
if "equipos_lista" not in st.session_state:
    st.session_state.equipos_lista = [
        "Crit Sonora",
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
            "Crit Sonora",
            "TE",
            "Leoni",
            "Clandestinos",
            "Parrilleros",
            "Crit Sonora",
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

equipos_lista = st.session_state.equipos_lista
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
        g_loc, g_vis = row["Goles Local"], row["Goles Visita"]

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

    st.dataframe(df_tabla, use_container_width=True)

# Pestaña 2: Calendario, Resultados e Imágenes por Jornada
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

    st.markdown("---")
    st.subheader("📸 Fotografías de los Partidos")

    hay_fotos_jornada = False
    for idx, row in df_jornada.iterrows():
        if idx in st.session_state.fotos_partidos:
            hay_fotos_jornada = True
            archivo_subido = st.session_state.fotos_partidos[idx]

            with st.expander(
                f"📷 Ver foto del partido: {row['Local']} vs {row['Visita']}"
            ):
                st.image(archivo_subido, use_container_width=True)

    if not hay_fotos_jornada:
        st.info("ℹ️ No hay fotos registradas para los partidos de esta jornada.")

# Pestaña 3: Tabla de Goleadores
with tab3:
    st.subheader("👟 Tabla de Máximos Goleadores")
    if df_gols.empty:
        st.info(
            "ℹ️ Aún no hay goleadores registrados. Se irán agregando desde el panel"
            " de administración."
        )
    else:
        df_gols_sorted = df_gols.sort_values(by="Goles", ascending=False).reset_index(
            drop=True
        )
        df_gols_sorted.index = df_gols_sorted.index + 1
        st.dataframe(df_gols_sorted, use_container_width=True)

# Pestaña 4: Panel para Administrar (Equipos, Resultados, Goleadores y Reset)
with tab4:
    st.subheader("⚙️ Panel de Administración")
    st.markdown("🔒 *Acceso exclusivo para el organizador del torneo.*")

    PASSWORD_ADMIN = "crit2026"
    pwd_ingresada = st.text_input(
        "Introduce la contraseña de administrador:", type="password"
    )

    if pwd_ingresada == PASSWORD_ADMIN:
        st.success("🎉 ¡Contraseña correcta! Ya puedes administrar el torneo.")

        admin_opcion = st.radio(
            "¿Qué deseas realizar?",
            [
                "🏟️ Administrar Equipos (Agregar / Modificar / Eliminar)",
                "Actualizar Resultados y Fotos",
                "Actualizar o Agregar Goleadores",
                "🗑️ Eliminar Goleadores",
                "⚠️ Reiniciar Torneo (Reset)",
            ],
        )

        if admin_opcion == "🏟️ Administrar Equipos (Agregar / Modificar / Eliminar)":
            st.markdown("### Gestión de Equipos del Torneo")
            st.write("📋 **Equipos actuales registrados:**", ", ".join(equipos_lista))

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
                            st.session_state.equipos_lista.append(nuevo_eq)
                            st.success(f"✅ ¡Equipo '{nuevo_eq}' agregado con éxito!")
                            st.rerun()
                        else:
                            st.warning(
                                "⚠️ El nombre está vacío o ya existe en la lista de equipos."
                            )

            elif op_equipo == "Modificar / Renombrar Equipo":
                with st.form("form_edit_equipo"):
                    eq_a_mod = st.selectbox(
                        "Selecciona el equipo a modificar:", equipos_lista
                    )
                    nuevo_nombre_eq = st.text_input(
                        "Nuevo nombre para el equipo:", value=eq_a_mod
                    )
                    btn_edit_eq = st.form_submit_button("Guardar Cambios")
                    if btn_edit_eq:
                        if nuevo_nombre_eq and nuevo_nombre_eq not in equipos_lista:
                            idx_e = equipos_lista.index(eq_a_mod)
                            st.session_state.equipos_lista[idx_e] = nuevo_nombre_eq

                            df["Local"] = df["Local"].replace(eq_a_mod, nuevo_nombre_eq)
                            df["Visita"] = df["Visita"].replace(eq_a_mod, nuevo_nombre_eq)

                            if not df_gols.empty:
                                df_gols["Equipo"] = df_gols["Equipo"].replace(
                                    eq_a_mod, nuevo_nombre_eq
                                )

                            st.success(
                                f"✅ ¡Equipo actualizado de '{eq_a_mod}' a '{nuevo_nombre_eq}'"
                                " con éxito!"
                            )
                            st.rerun()
                        else:
                            st.warning("⚠️ El nuevo nombre está vacío o ya se encuentra registrado.")

            elif op_equipo == "Eliminar Equipo":
                with st.form("form_del_equipo"):
                    eq_a_del = st.selectbox(
                        "Selecciona el equipo que deseas eliminar:", equipos_lista
                    )
                    btn_del_eq = st.form_submit_button("Eliminar Equipo")
                    if btn_del_eq:
                        if len(equipos_lista) > 2:
                            st.session_state.equipos_lista.remove(eq_a_del)
                            st.success(
                                f"✅ ¡El equipo '{eq_a_del}' ha sido eliminado del torneo!"
                            )
                            st.rerun()
                        else:
                            st.error("❌ El torneo debe tener al menos 2 equipos registrados.")

        elif admin_opcion == "Actualizar Resultados y Fotos":
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
                    st.success("✅ ¡Resultado actualizado con éxito!")
                    st.rerun()

            st.markdown("---")
            st.markdown("### 📷 Subir o cambiar foto del partido")
            partido_foto_idx = st.selectbox(
                "Selecciona el partido para la foto:",
                df.index,
                key="select_foto",
                format_func=lambda i: f"J{df.loc[i, 'Jornada']}: {df.loc[i, 'Local']} vs {df.loc[i, 'Visita']}",
            )
            foto_subida = st.file_uploader(
                "Sube la imagen del partido (PNG, JPG)", type=["png", "jpg", "jpeg"]
            )

            if st.button("Guardar Foto"):
                if foto_subida is not None:
                    st.session_state.fotos_partidos[partido_foto_idx] = foto_subida
                    st.success("✅ ¡Foto guardada correctamente!")
                    st.rerun()
                else:
                    st.warning("⚠️ Por favor selecciona una imagen primero.")

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
                        st.success("✅ ¡Nuevo goleador registrado con éxito!")
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
                        st.success("✅ ¡Goles actualizados con éxito!")
                        st.rerun()

        elif admin_opcion == "🗑️ Eliminar Goleadores":
            st.markdown("### Eliminar registros de goleadores")
            if df_gols.empty:
                st.info("ℹ No hay goleadores registrados actualmente para eliminar.")
            else:
                with st.form("form_eliminar_goleador"):
                    jugadores_a_borrar = st.multiselect(
                        "Selecciona el o los jugadores que deseas eliminar:",
                        df_gols["Jugador"].tolist(),
                    )
                    eliminar_btn = st.form_submit_button(
                        "Eliminar Jugadores Seleccionados"
                    )

                    if eliminar_btn and jugadores_a_borrar:
                        st.session_state.df_goleadores = df_gols[
                            ~df_gols["Jugador"].isin(jugadores_a_borrar)
                        ].reset_index(drop=True)
                        st.success("✅ ¡Los goleadores seleccionados han sido eliminados!")
                        st.rerun()

                st.markdown("---")
                if st.button("🗑️ Vaciar Tabla de Goleadores por Completo"):
                    st.session_state.df_goleadores = pd.DataFrame(
                        columns=["Jugador", "Equipo", "Goles"]
                    )
                    st.success("✅ ¡Se ha vaciado la tabla de goleadores por completo!")
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
                    del st.session_state.equipos_lista
                    del st.session_state.df_partidos
                    del st.session_state.fotos_partidos
                    del st.session_state.df_goleadores
                    st.success(
                        "🔄 ¡El torneo se ha reiniciado por completo exitosamente!"
                    )
                    st.rerun()
                else:
                    st.error(
                        "❌ Debes marcar la casilla de confirmación para poder reiniciar los"
                        " datos."
                    )

    elif pwd_ingresada != "":
        st.error("❌ Contraseña incorrecta. Intenta de nuevo.")
    else:
        st.info(
            "🔒 Por favor, ingresa la contraseña para desbloquear el panel de"
            " administración."
        )
