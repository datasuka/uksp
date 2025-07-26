
import streamlit as st
import requests

st.set_page_config(page_title="Monitor Link Pendaftaran USKP", layout="centered")

st.title("🔍 Monitor Link Pendaftaran USKP Tingkat B")
st.markdown("Aplikasi ini memantau status link-link pendaftaran yang diduga untuk **USKP Tingkat B**.")

uuid_list = [
    "103b54ac-e44e-4c59-a523-c5e8d28740f5",
    "ee064223-0297-456f-91da-52c8eb8d4618",
    "0b7424d5-e43c-451a-9e9c-52279a39bab6",
    "ac1d31dc-c659-4edb-b718-15c1e6cf606f",
    "9f0f6c17-d9d0-47f1-8c6a-a4d828e8503c",
    "5d28424b-7a6c-4439-a5fa-87f2a038bd76",
    "cb902160-82f0-4bda-aad6-61d00755d2cc",
    "ceed730f-d65f-4baf-a071-64d56b429750",
    "33354f7d-fa3b-4d17-ba07-b7340660ff16",
    "71c35a2b-99d3-451d-8ec1-9e6e49802d4a"
]

base_url = "https://bppk.kemenkeu.go.id/uskp/registrant/create/"

st.info("Klik tombol di bawah untuk memulai pengecekan link.")

if st.button("🔄 Cek Status Link"):
    results = []
    for uuid in uuid_list:
        url = base_url + uuid + "/"
        try:
            r = requests.head(url, allow_redirects=True, timeout=5)
            status = r.status_code
        except Exception as e:
            status = str(e)
        results.append((uuid, url, status))

    st.markdown("### Hasil Pengecekan:")
    for uuid, url, status in results:
        if status == 200:
            st.success(f"✅ [Link Aktif]({url}) - UUID: {uuid}")
        else:
            st.warning(f"❌ Link belum aktif - UUID: {uuid} (Status: {status})")
