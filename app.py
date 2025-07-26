
import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="Monitor Link Pendaftaran USKP", layout="centered")

st.title("🔍 Monitor Link Pendaftaran USKP Tingkat B")
st.markdown("Aplikasi ini memantau status link-link pendaftaran yang diduga untuk **USKP Tingkat B**.")

default_uuids = [
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

manual_input = st.text_area("➕ Masukkan UUID Tambahan (pisahkan dengan koma):", "")
manual_uuids = [u.strip() for u in manual_input.split(",") if len(u.strip()) == 36]

all_uuids = list(set(default_uuids + manual_uuids))

base_url_create = "https://bppk.kemenkeu.go.id/uskp/registrant/create/"
base_url_summary = "https://bppk.kemenkeu.go.id/uskp/registrant/"

st.info("Klik tombol di bawah untuk memulai pengecekan link (create & summary).")

if st.button("🔄 Cek Status Link Sekarang"):
    results = []
    for uuid in all_uuids:
        url_create = base_url_create + uuid + "/"
        url_summary = base_url_summary + uuid + "/summary/"
        try:
            status_create = requests.head(url_create, allow_redirects=True, timeout=5).status_code
        except:
            status_create = "ERR"
        try:
            status_summary = requests.head(url_summary, allow_redirects=True, timeout=5).status_code
        except:
            status_summary = "ERR"
        results.append((uuid, url_create, status_create, url_summary, status_summary))

    st.markdown(f"### ⏱️ Diperiksa pada: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}")
    for uuid, url_create, status_c, url_summary, status_s in results:
        if status_c == 200 or status_s == 200:
            st.success(f"✅ [Aktif] UUID: `{uuid}`  
• [Formulir]({url_create}) → {status_c}  
• [Ringkasan]({url_summary}) → {status_s}")
        else:
            st.warning(f"⏳ Belum aktif: `{uuid}`  
• {url_create} → {status_c}  
• {url_summary} → {status_s}")
