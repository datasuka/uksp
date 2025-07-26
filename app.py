
import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="Monitor Link Pendaftaran USKP", layout="centered")

st.title("🔍 Monitor Link Pendaftaran USKP Tingkat B")
st.markdown("Aplikasi ini auto-refresh setiap 5 menit dan mengirim webhook jika link aktif.")

# Konfigurasi webhook URL (isi jika ingin notifikasi ke Discord/Telegram/dll)
webhook_url = st.secrets.get("webhook_url", "")

default_uuids = [
    "103b54ac-e44e-4c59-a523-c5e8d28740f5",
    "ee064223-0297-456f-91da-52c8eb8d4618",
    "0b7424d5-e43c-451a-9e9c-52279a39bab6",
    "ac1d31dc-c659-4edb-b718-15c1e6cf606f",
    "9f0f6c17-d9d0-47f1-8c6a-a4d828e8503c",
    "5d28424b-7a6c-4439-a5fa-87f2a038bd76"
]

manual_input = st.text_area("➕ Masukkan UUID Tambahan (pisahkan dengan koma):", "")
manual_uuids = [u.strip() for u in manual_input.split(",") if len(u.strip()) == 36]
all_uuids = list(set(default_uuids + manual_uuids))

base_url_create = "https://bppk.kemenkeu.go.id/uskp/registrant/create/"
base_url_summary = "https://bppk.kemenkeu.go.id/uskp/registrant/"

st.markdown("⏳ Auto-refresh setiap 5 menit. Terakhir diperiksa:")
st.code(datetime.now().strftime('%d-%m-%Y %H:%M:%S'))

triggered_webhook = False
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

    if status_create == 200 or status_summary == 200:
        st.success(f"✅ [Aktif] UUID: `{uuid}`\n• [Formulir]({url_create}) → {status_create}\n• [Ringkasan]({url_summary}) → {status_summary}")
        if webhook_url and not triggered_webhook:
            payload = {
                "text": f"✅ USKP LINK AKTIF!\nUUID: {uuid}\nFormulir: {url_create}\nRingkasan: {url_summary}"
            }
            try:
                requests.post(webhook_url, json=payload, timeout=5)
                st.info("📨 Webhook triggered.")
                triggered_webhook = True
            except Exception as e:
                st.error(f"Gagal kirim webhook: {e}")
    else:
        st.warning(f"⏳ Belum aktif: `{uuid}`\n• {url_create} → {status_create}\n• {url_summary} → {status_summary}")

# Auto-refresh manual (5 menit)
st.markdown("<meta http-equiv='refresh' content='300'>", unsafe_allow_html=True)
