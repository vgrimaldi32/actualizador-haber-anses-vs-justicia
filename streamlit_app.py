
import streamlit as st
import pandas as pd
from datetime import datetime

df_anses = pd.read_csv("coef_anses.csv", sep=";")
df_justicia = pd.read_csv("coef_justicia.csv", sep=";")

df_anses["coef_anses"] = df_anses["coef_anses"].astype(str).str.replace(",", ".").astype(float)
df_justicia["coef_justicia"] = df_justicia["coef_justicia"].astype(str).str.replace(",", ".").astype(float)

df = pd.merge(df_anses, df_justicia, on="fecha")
df["fecha"] = pd.to_datetime(df["fecha"], format="%Y-%m")

st.title("Actualizador de Haber – Comparación ANSeS vs Justicia")

haber_input = st.text_input("Ingrese el haber base", "53036,00")
try:
    haber_inicial = float(haber_input.replace(",", "."))
except ValueError:
    st.error("⚠ Ingresá el haber en formato numérico válido (ej: 53036.00 o 53036,00)")
    st.stop()

fecha_base = st.text_input("Fecha del haber base (YYYY-MM)", "2020-01")

try:
    fecha_base_dt = datetime.strptime(fecha_base, "%Y-%m")

    marzo_dt = datetime.strptime("2020-03", "%Y-%m")
    if fecha_base_dt < marzo_dt:
        coef_marzo_2020 = 1.023 + (1500 / haber_inicial)
        nueva_fila = pd.DataFrame([{
            "fecha": marzo_dt,
            "coef_anses": coef_marzo_2020,
            "coef_justicia": coef_marzo_2020
        }])
        df = pd.concat([df, nueva_fila], ignore_index=True)
        df = df.sort_values("fecha")

    df["fecha"] = pd.to_datetime(df["fecha"])
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
        st.write("**Diferencia:** ${{:,.2f}} ({{:.2f}}%%)".format(diferencia, diferencia_pct))
    else:
        st.warning("No hay coeficientes posteriores a la fecha ingresada.")
except ValueError:
    st.error("⚠ Ingresá la fecha en formato YYYY-MM (ejemplo: 2020-04)")
