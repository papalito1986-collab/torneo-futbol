import os
import sqlite3
import pandas as pd
import streamlit as st

# Configuración inicial de la página web
st.set_page_config(
    page_title="Torneo de Fútbol - Teletón Sonora", page_icon="⚽", layout="wide"
)

# Nombre de la base de datos persistente
DB_NAME = "torneo_crit.db"


def obtener_conexion():
    """Crea y retorna una conexión a la base de datos."""
    conn = sqlite3.connect(DB_NAME)
    return conn


def inicializar_base_datos():
    """Crea las tablas y asegura que los equipos estén listos en la base de datos."""
    conn = obtener_conexion()
    cursor = conn.cursor()

    # Tabla de Equipos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS equipos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT UNIQUE NOT NULL
        )
    """)

    # Tabla de Partidos con ID único explícito
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS partidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            jornada TEXT NOT NULL,
            local TEXT NOT NULL,
            goles_local INTEGER DEFAULT 0,
            goles_visita INTEGER DEFAULT 0,
            visita TEXT NOT NULL,
            jugado BOOLEAN DEFAULT 0
        )
    """)

    # Tabla de Goleadores
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS goleadores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            jugador TEXT NOT NULL,
            equipo TEXT NOT NULL,
            goles INTEGER DEFAULT 0
        )
    """)
    conn.commit()

    # Insertar equipos iniciales si la tabla está vacía (convertidos a mayúsculas)
    cursor.execute("SELECT COUNT(*) FROM equipos")
    if cursor.fetchone()[0] == 0:
        equipos_default = [
            ("REAL SOCIEDAD",),
            ("LOS DEFENSORES",),
            ("LA CARIDAD FC",),
            ("ORGULLOSAMENTE TERCOS",),
            ("CUERVOS FC - AXOMA",),
            ("CLUB GRIEGOS ISJ",),
            ("PIRATITAS DEL SAHUARO FC",),
            ("TELETONES",),
            ("MASTER FC JUAREZ",),
            ("ELECTRICA FLORES BRAVOS HERMOSILLO",),
            ("CENTRO DE FORMACION DEL CLUB AMERICA HERMOSILLO",),
            ("ACADEMIA TOROS",),
            ("ARBITROS ZONA NORTE",),
            ("HOSPITAL MILITAR-SEDENA",),
            ("AXOMA",),
            ("LOS FELIX",),
        ]
        cursor.executemany("INSERT INTO equipos (nombre) VALUES (?)", equipos_default)
        conn.commit()
    else:
        # Asegurar que los existentes estén en mayúsculas por si acaso
        cursor.execute("SELECT id, nombre FROM equipos")
        for eq_id, nombre in cursor.fetchall():
            nombre_upper = nombre.upper()
            if nombre != nombre_upper:
                cursor.execute("UPDATE equipos SET nombre = ? WHERE id = ?", (nombre_upper, eq_id))
        conn.commit()

    conn.close()


# Inicializar base de datos al arrancar
inicializar_base_datos()


# Funciones para cargar datos desde la base de datos
def cargar_datos_db():
    conn = obtener_conexion()
    
    # Cargar equipos
    df_eq = pd.read_sql("SELECT nombre AS Equipo FROM equipos", conn)
    equipos_lista = df_eq["Equipo"].tolist()

    # Cargar partidos incluyendo el ID único de la base de datos
    df_part = pd.read_sql(
        "SELECT id, jornada AS Jornada, local AS Local, goles_local AS 'Goles Local', goles_visita AS 'Goles Visita', visita AS Visita, jugado AS Jugado FROM partidos",
        conn,
    )
    if not df_part.empty:
        df_part["Jugado"] = df_part["Jugado"].astype(bool)

    # Cargar goleadores
    df_gol = pd.read_sql(
        "SELECT id, jugador AS Jugador, equipo AS Equipo, goles AS Goles FROM goleadores",
        conn,
    )
    
    conn.close()
    return equipos_lista, df_part, df_gol


# Inicializar estado de sesión
if "datos_cargados" not in st.session_state:
    st.session_state.datos_cargados = True

equipos_lista, df, df_gols = cargar_datos_db()

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

# Pestaña 1: Tabla de Posiciones y selección de fases
with tab1:
    st.subheader("🌟 Clasificación y Tablas por Fase")
    
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

    if df.empty:
        st.info("ℹ️ No hay partidos registrados todavía. Ve al Panel de Administración para programar encuentros o nuevas fases.")
    else:
        jornadas_disponibles = df["Jornada"].dropna().unique().tolist()
        opciones_tabla = ["📊 Tabla General (Toda la Temporada / Acumulada)"] + [f"Fase/Jornada: {j}" for j in jornadas_disponibles]
        
        tabla_seleccionada = st.selectbox("Selecciona qué tabla deseas visualizar:", opciones_tabla)
        
        if tabla_seleccionada.startswith("📊"):
            df_a_procesar = df
            st.markdown("### 📋 Tabla General Acumulada")
        else:
            jornada_elegida = tabla_seleccionada.replace("Fase/Jornada: ", "")
            df_a_procesar = df[df["Jornada"] == jornada_elegida]
            st.markdown(f"### 📋 Tabla / Resultados de: {jornada_elegida}")

        for _, row in df_a_procesar[df_a_procesar["Jugado"] == True].iterrows():
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
        st.info("ℹ️ No hay encuentros programados. Usa la pestaña 'Administrar Torneo' para agregar nuevos partidos o fases (Cuartos de Final, Semifinal, Final).")
    else:
        jornadas_disponibles = df["Jornada"].dropna().unique().tolist()
        jornada_sel = st.selectbox(
            "Selecciona la Jornada o Fase:", jornadas_disponibles, key="cal_jornada"
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
        st.dataframe(df_gols_sorted[["Jugador", "Equipo", "Goles"]], use_container_width=True)

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

        conn = obtener_conexion()
        cursor = conn.cursor()

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
                        nuevo_eq_upper = nuevo_eq.strip().upper()
                        if nuevo_eq_upper and nuevo_eq_upper not in equipos_lista:
                            try:
                                cursor.execute("INSERT INTO equipos (nombre) VALUES (?)", (nuevo_eq_upper,))
                                conn.commit()
                                st.success(f"✅ ¡Equipo '{nuevo_eq_upper}' agregado con éxito!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error: {e}")
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
                        nuevo_nombre_upper = nuevo_nombre_eq.strip().upper()
                        if nuevo_nombre_upper and (nuevo_nombre_upper == eq_a_mod or nuevo_nombre_upper not in equipos_lista):
                            cursor.execute("UPDATE equipos SET nombre = ? WHERE nombre = ?", (nuevo_nombre_upper, eq_a_mod))
                            cursor.execute("UPDATE partidos SET local = ? WHERE local = ?", (nuevo_nombre_upper, eq_a_mod))
                            cursor.execute("UPDATE partidos SET visita = ? WHERE visita = ?", (nuevo_nombre_upper, eq_a_mod))
                            cursor.execute("UPDATE goleadores SET equipo = ? WHERE equipo = ?", (nuevo_nombre_upper, eq_a_mod))
                            conn.commit()
                            st.success(f"✅ ¡Equipo '{eq_a_mod}' renombrado a '{nuevo_nombre_upper}' con éxito!")
                            st.rerun()
                        else:
                            st.warning("⚠️ El nuevo nombre está vacío o ya existe.")

            elif op_equipo == "Eliminar Equipo":
                with st.form("form_delete_equipo"):
                    eq_a_del = st.selectbox("Selecciona el equipo a eliminar:", equipos_lista)
                    btn_del_eq = st.form_submit_button("Eliminar Equipo")
                    if btn_del_eq:
                        cursor.execute("DELETE FROM equipos WHERE nombre = ?", (eq_a_del,))
                        cursor.execute("DELETE FROM partidos WHERE local = ? OR visita = ?", (eq_a_del, eq_a_del))
                        conn.commit()
                        st.success(f"✅ ¡Equipo '{eq_a_del}' eliminado del torneo!")
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
                        "Jornada o Fase (ej. 'Cuartos de Final', 'Semifinal', 'Final')"
                    )
                    col_l, col_v = st.columns(2)
                    with col_l:
                         equipo_local = st.selectbox("Equipo Local", equipos_lista, key="add_loc")
                    with col_v:
                         equipo_visita = st.selectbox("Equipo Visita", equipos_lista, key="add_vis")
                    
                    btn_crear_partido = st.form_submit_button("Guardar Nuevo Partido")
                    if btn_crear_partido:
                        if nueva_jornada and equipo_local != equipo_visita:
                            cursor.execute(
                                "INSERT INTO partidos (jornada, local, goles_local, goles_visita, visita, jugado) VALUES (?, ?, 0, 0, ?, 0)",
                                (nueva_jornada, equipo_local, equipo_visita)
                            )
                            conn.commit()
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
                            f"ID: {row['id']} - [{row['Jornada']}] {row['Local']} vs {row['Visita']}"
                            for idx, row in df_edit.iterrows()
                        ]
                        partido_elegido = st.selectbox("Selecciona el partido a editar:", partidos_ids)
                        partido_id_sel = int(partido_elegido.split("ID: ")[1].split(" - ")[0])

                        row_actual = df_edit[df_edit["id"] == partido_id_sel].iloc[0]
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
                            cursor.execute(
                                "UPDATE partidos SET jornada = ?, local = ?, goles_local = ?, goles_visita = ?, visita = ?, jugado = ? WHERE id = ?",
                                (nueva_j, nuevo_l, g_l, g_v, nuevo_v, int(jugado_val), partido_id_sel)
                            )
                            conn.commit()
                            st.success("✅ ¡Partido actualizado y guardado correctamente!")
                            st.rerun()

            elif sub_partido_op == "Eliminar Partido":
                if df.empty:
                    st.info("No hay partidos para eliminar.")
                else:
                    with st.form("form_del_partido"):
                        df_del = df.reset_index(drop=True)
                        partidos_ids_del = [
                            f"ID: {row['id']} - [{row['Jornada']}] {row['Local']} vs {row['Visita']}"
                            for idx, row in df_del.iterrows()
                        ]
                        partido_a_borrar = st.selectbox("Selecciona el partido a eliminar:", partidos_ids_del)
                        partido_id_del = int(partido_a_borrar.split("ID: ")[1].split(" - ")[0])

                        btn_confirmar_del = st.form_submit_button("Eliminar Partido Seleccionado")
                        if btn_confirmar_del:
                            cursor.execute("DELETE FROM partidos WHERE id = ?", (partido_id_del,))
                            conn.commit()
                            st.success("🗑️ ¡Partido eliminado con éxito!")
                            st.rerun()

        elif admin_opcion == "Actualizar Resultados de Partidos":
            df_reset = df.reset_index(drop=True)
            if df_reset.empty:
                st.info("ℹ️ No hay partidos registrados todavía para actualizar. Agrega partidos primero.")
            else:
                st.markdown("### ⚽ Actualizar Resultado y Marcador")
                lista_partidos_ids = []
                for idx, row in df_reset.iterrows():
                    p_id = f"ID: {row['id']} - [{str(row['Jornada'])}]: {str(row['Local'])} vs {str(row['Visita'])}"
                    lista_partidos_ids.append(p_id)
                
                partido_sel = st.selectbox("Selecciona el partido a actualizar:", lista_partidos_ids)
                partido_id_sel = int(partido_sel.split("ID: ")[1].split(" - ")[0])

                fila_partido = df_reset[df_reset["id"] == partido_id_sel].iloc[0]

                col_g1, col_g2 = st.columns(2)
                with col_g1:
                    nuevo_g_loc = st.number_input(f"Goles ({fila_partido['Local']})", min_value=0, step=1, value=int(fila_partido["Goles Local"]), key="g_loc_input")
                with col_g2:
                    nuevo_g_vis = st.number_input(f"Goles ({fila_partido['Visita']})", min_value=0, step=1, value=int(fila_partido["Goles Visita"]), key="g_vis_input")
                
                marcar_jugado = st.checkbox("¿Marcar como Partido Jugado?", value=bool(fila_partido["Jugado"]), key="jugado_input")

                if st.button("💾 Guardar Resultado en la Base de Datos"):
                    cursor.execute(
                        "UPDATE partidos SET goles_local = ?, goles_visita = ?, jugado = ? WHERE id = ?",
                        (int(nuevo_g_loc), int(nuevo_g_vis), int(marcar_jugado), int(partido_id_sel))
                    )
                    conn.commit()
                    st.success(f"✅ ¡Resultado guardado con éxito para el partido ID {partido_id_sel}!")
                    st.rerun()

        elif admin_opcion == "Actualizar o Agregar Goleadores":
            st.markdown("### 👟 Actualizar o Agregar Goleador")
            df_gols_reset = df_gols.reset_index(drop=True)
            
            # Crear opciones identificadas por ID único para evitar mezclar registros
            opciones_goleadores = ["+ Agregar Nuevo Jugador"]
            mapa_goleadores = {}
            if not df_gols_reset.empty:
                for _, row in df_gols_reset.iterrows():
                    etiqueta = f"ID: {row['id']} - {row['Jugador']} ({row['Equipo']})"
                    opciones_goleadores.append(etiqueta)
                    mapa_goleadores[etiqueta] = row

            goleador_sel = st.selectbox("Selecciona o registra jugador:", opciones_goleadores)

            if goleador_sel == "+ Agregar Nuevo Jugador":
                with st.form("form_add_goleador_nuevo"):
                    nuevo_jugador = st.text_input("Nombre del Nuevo Jugador")
                    nuevo_equipo = st.selectbox("Equipo del Jugador", equipos_lista)
                    nuevos_goles = st.number_input("Goles Totales", min_value=0, step=1, value=1)
                    add_g = st.form_submit_button("Registrar Nuevo Goleador")
                    if add_g:
                        if nuevo_jugador.strip() != "":
                            cursor.execute(
                                "INSERT INTO goleadores (jugador, equipo, goles) VALUES (?, ?, ?)",
                                (nuevo_jugador.strip().upper(), nuevo_equipo, nuevos_goles)
                            )
                            conn.commit()
                            st.success(f"✅ ¡Goleador '{nuevo_jugador.strip().upper()}' registrado con éxito!")
                            st.rerun()
                        else:
                            st.warning("⚠️ Por favor escribe el nombre del jugador.")
            else:
                datos_jugador = mapa_goleadores[goleador_sel]
                id_jugador = int(datos_jugador["id"])
                goles_actuales = int(datos_jugador["Goles"])
                nombre_jugador = datos_jugador["Jugador"]

                with st.form(f"form_up_goles_{id_jugador}"):
                    st.markdown(f"**Jugador seleccionado:** {nombre_jugador} ({datos_jugador['Equipo']})")
                    actualizar_goles = st.number_input("Actualizar Goles Totales", min_value=0, step=1, value=goles_actuales)
                    btn_up_goles = st.form_submit_button("💾 Actualizar Goles del Jugador")
                    
                    if btn_up_goles:
                        cursor.execute(
                            "UPDATE goleadores SET goles = ? WHERE id = ?",
                            (int(actualizar_goles), id_jugador)
                        )
                        conn.commit()
                        st.success(f"✅ ¡Goles actualizados con éxito para {nombre_jugador}!")
                        st.rerun()

        elif admin_opcion == "🗑️ Eliminar Goleadores":
            df_gols_reset = df_gols.reset_index(drop=True)
            if df_gols_reset.empty:
                st.info("ℹ️ No hay goleadores registrados para eliminar.")
            else:
                with st.form("form_del_goleador"):
                    opciones_del = [f"ID: {row['id']} - {row['Jugador']} ({row['Equipo']})" for _, row in df_gols_reset.iterrows()]
                    goleador_a_eliminar = st.selectbox("Selecciona el jugador a eliminar:", opciones_del)
                    
                    btn_del_g = st.form_submit_button("🗑️ Eliminar Goleador Seleccionado")
                    if btn_del_g:
                        id_del = int(goleador_a_eliminar.split("ID: ")[1].split(" - ")[0])
                        cursor.execute("DELETE FROM goleadores WHERE id = ?", (id_del,))
                        conn.commit()
                        st.success("✅ ¡Goleador eliminado con éxito!")
                        st.rerun()

        conn.close()

    elif pwd_ingresada != "":
        st.error("❌ Contraseña incorrecta.")