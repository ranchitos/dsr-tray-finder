import streamlit as st
from tray_lookup import load_tray_data, get_tray

data = load_tray_data('tray_data.csv')

st.title("Tray Finder")

hall = st.text_input("Enter hall (e.g. Cedar)")
room = st.text_input("Enter room (e.g. E410, 205, A110-1)")

if st.button("Find Tray"):
    tray = get_tray(hall, room, data)
    if tray:
        st.success(f"Room {room} in {hall} belongs to Tray {tray}")
    else:
        st.error("No matching tray found")