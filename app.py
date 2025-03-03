import streamlit as st
import pandas as pd

# Function to perform unit conversion
def convert_units(value, from_unit, to_unit, category):
    conversion_factors = {
        "Length": {
            "Meters": {"Kilometers": 0.001, "Centimeters": 100, "Feet": 3.28084},
            "Kilometers": {"Meters": 1000, "Miles": 0.621371},
            "Miles": {"Kilometers": 1.60934, "Meters": 1609.34},
            "Feet": {"Meters": 0.3048, "Centimeters": 30.48},
            "Centimeters": {"Meters": 0.01, "Feet": 0.0328084}
        },
        "Weight": {
            "Kilograms": {"Grams": 1000, "Pounds": 2.20462},
            "Grams": {"Kilograms": 0.001},
            "Pounds": {"Kilograms": 0.453592, "Ounces": 16},
            "Ounces": {"Pounds": 0.0625}
        },
        "Temperature": {
            "Celsius": {"Fahrenheit": lambda c: (c * 9/5) + 32, "Kelvin": lambda c: c + 273.15},
            "Fahrenheit": {"Celsius": lambda f: (f - 32) * 5/9, "Kelvin": lambda f: (f - 32) * 5/9 + 273.15},
            "Kelvin": {"Celsius": lambda k: k - 273.15, "Fahrenheit": lambda k: (k - 273.15) * 9/5 + 32}
        }
    }

    if from_unit == to_unit:
        return value

    if category in conversion_factors and from_unit in conversion_factors[category]:
        factor = conversion_factors[category][from_unit].get(to_unit)
        if callable(factor):  # For temperature conversions
            return factor(value)
        elif factor:
            return value * factor

    return None

# Streamlit UI
st.title("🌟 Advanced Unit Converter")
st.sidebar.header("Conversion Settings")

# Select conversion category
category = st.sidebar.selectbox("Select Category", ["Length", "Weight", "Temperature"])

# Select units based on category
units_dict = {
    "Length": ["Meters", "Kilometers", "Miles", "Feet", "Centimeters"],
    "Weight": ["Kilograms", "Grams", "Pounds", "Ounces"],
    "Temperature": ["Celsius", "Fahrenheit", "Kelvin"]
}
units = units_dict[category]

from_unit = st.sidebar.selectbox("From", units)
to_unit = st.sidebar.selectbox("To", units)

# Input value
value = st.sidebar.number_input("Enter Value", min_value=0.0, format="%.2f")

# Convert button
if st.sidebar.button("Convert"):
    result = convert_units(value, from_unit, to_unit, category)
    if result is not None:
        st.success(f"{value} {from_unit} = {result:.4f} {to_unit}")
    else:
        st.error("Conversion not possible!")

# Light/Dark Mode Toggle
st.sidebar.markdown("---")
st.sidebar.markdown("*UI Theme*")
theme = st.sidebar.radio("Select Theme", ["Light", "Dark"])

if theme == "Dark":
    st.markdown("<style>body { background-color: #333; color: white; }</style>", unsafe_allow_html=True)

# Download results option (CSV format)
if st.sidebar.button("Download CSV"):
    df = pd.DataFrame([[value, from_unit, result, to_unit]], columns=["Value", "From", "Converted Value", "To"])
    csv = df.to_csv(index=False)
    st.sidebar.download_button(label="Download CSV", data=csv, file_name="conversion_results.csv", mime="text/csv")