
import streamlit as st
import pandas as pd
from datetime import datetime

# Aumentos de movilidad preprocesados
data = []

df = pd.DataFrame(data)
df['fecha'] = pd.to_datetime(df['fecha'], format="%Y-%m")

st.title("Actualizador de Haber – Comparación ANSeS vs Justicia")

haber_inicial = st.number_input("Ingrese el haber base", value=53036.00, format="%.2f")
fecha_base = st.text_input("Fecha del haber base (YYYY-MM)", "2020-04")

try:
    fecha_base_dt = datetime.strptime(fecha_base, "%Y-%m")
    df_tramo = df[df["fecha"] > fecha_base_dt].copy()

    if not df_tramo.empty:
        factor_anses = df_tramo["coef_anses"].prod()
        factor_justicia = df_tramo["coef_justicia"].prod()

        haber_anses = haber_inicial * factor_anses
        haber_justicia = haber_inicial * factor_justicia
        diferencia = haber_justicia - haber_anses
        diferencia_pct = (diferencia / haber_anses * 100) if haber_anses != 0 else 0

        st.subheader("Resultados:")
        st.write("**Haber actualizado según ANSeS:** ${{:,.2f}}".format(haber_anses))
        st.write("**Haber actualizado según Justicia:** ${{:,.2f}}".format(haber_justicia))
        st.write("**Diferencia:** ${{:,.2f}} ({{:.2f}}%)".format(diferencia, diferencia_pct))
    else:
        st.warning("No hay coeficientes posteriores a la fecha ingresada.")
except ValueError:
    st.error("⚠ Ingresá la fecha en formato YYYY-MM (ejemplo: 2020-04)")
