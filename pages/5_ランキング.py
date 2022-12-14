import streamlit as st
import json
import pandas as pd
from google.cloud import firestore

cert = {
    "type": st.secrets["type"],
    "project_id": st.secrets["project_id"],
    "private_key_id": st.secrets["private_key_id"],
    "private_key": st.secrets["private_key"],
    "client_email": st.secrets["client_email"],
    "client_id": st.secrets["client_id"],
    "auth_uri": st.secrets["auth_uri"],
    "token_uri": st.secrets["token_uri"],
    "auth_provider_x509_cert_url": st.secrets["auth_provider_x509_cert_url"],
    "client_x509_cert_url": st.secrets["client_x509_cert_url"]
}

db = firestore.Client.from_service_account_info(cert)

st.set_page_config(page_title="ランキング", page_icon="static/description/favicon.png")



st.sidebar.header("ランキングを確認する")
with open("static/theme/name_to_path.json", encoding="utf-8") as f:
    name_to_path = json.load(f)
option = st.sidebar.selectbox('▼ ランキングを確認したいお題を選んでください', name_to_path.keys())

st.header(f"👑ものまねランキング👑 {option}編")
doc_ref_ranking = db.collection("ranking").document(f"{option}")
docs = doc_ref_ranking.get()
score_dict = docs.to_dict()

if score_dict == None:
        #デフォルトのランキングセット
        doc_ref_ranking.set({
            '1位': ["太郎", 5],
            '2位': ["次郎", 4],
            '3位': ["三郎", 3],
            '4位': ["四郎", 2],
            '5位': ["五郎", 1]
        })

doc_ref_ranking = db.collection("ranking").document(f"{option}")
docs = doc_ref_ranking.get()
score_dict = docs.to_dict()

df = pd.DataFrame.from_dict(score_dict, orient="index")
df.columns = ["プレイヤー名", "得点"]

df_sorted = df.sort_values(by="得点",ascending=False)
st.balloons()
st.table(df_sorted)

st.markdown("---")

