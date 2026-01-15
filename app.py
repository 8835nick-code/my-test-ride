import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. 網頁基本設定 ---
st.set_page_config(page_title="機車試乘活動報名系統", page_icon="🏍️")

# --- 2. 初始化 Session State ---
if 'page' not in st.session_state:
    st.session_state['page'] = 1
if 'temp_data' not in st.session_state:
    st.session_state['temp_data'] = {}

# --- 3. 頁面邏輯 ---

# 第一頁：基本資料
if st.session_state['page'] == 1:
    st.title("Step 1: 基本資料")
    name = st.text_input("1. 姓名")
    id_code = st.text_input("2. 識別代號")
    if st.button("下一頁"):
        if name and id_code:
            st.session_state['temp_data'] = {"姓名": name, "識別代號": id_code}
            st.session_state['page'] = 2
            st.rerun()
        else:
            st.error("請填寫所有欄位")

# 第二頁：切結書
elif st.session_state['page'] == 2:
    st.title("Step 2: 事前切結書")
    agreement_text = """【試乘活動事前切結書】\n一、本人自願參加本次機車試乘活動... (此處請保留您的完整條款)"""
    st.text_area("切結書內容：", value=agreement_text, height=200, disabled=True)
    agree = st.radio("您是否同意以上內容？", ["請選擇", "同意", "不同意"], index=0)
    if agree == "同意":
        s_name = st.text_input("2. 立書人 (全名)")
        s_id = st.text_input("3. 身份證字號")
        s_phone = st.text_input("4. 電話")
        if st.button("下一頁"):
            if s_name and s_id and s_phone:
                st.session_state['temp_data'].update({"立書人": s_name, "身份證字號": s_id, "電話": s_phone})
                st.session_state['page'] = 3
                st.rerun()
            else:
                st.error("請填寫完整資訊")

# 第三頁：機種選擇與提交
elif st.session_state['page'] == 3:
    st.title("Step 3: 機種與宣導")
    selected_model = st.radio("1. 欲試乘機種", ["CUXIE", "CGYNUS", "NMAX", "大型重機"])
    promo = st.radio("2. 品牌宣導", ["參加", "不參加"])

if st.button("確認提交報名"):
        # 建立參數 (確保 entry ID 與你之前提供的一致)
        params = (
            f"?entry.361499099={st.session_state['temp_data']['姓名']}"
            f"&entry.1344609340={st.session_state['temp_data']['識別代號']}"
            f"&entry.1297329962={st.session_state['temp_data']['立書人']}"
            f"&entry.309920621={st.session_state['temp_data']['身份證字號']}"
            f"&entry.1566749837={st.session_state['temp_data']['電話']}"
            f"&entry.371178622={selected_model}"
            f"&entry.1133738858={promo}"
            f"&submit=Submit"
        )
        
        # 組合完整網址
        base_url = "https://docs.google.com/forms/d/e/1FAIpQLSdczkNBFSVmUipEjm5zYwQLAKOzSJUz4ET7Wyqt4zNSRi-PMw/viewform?usp=pp_url&entry.361499099=1&entry.1344609340=2&entry.1297329962=3&entry.309920621=4&entry.1566749837=5&entry.371178622=6&entry.1133738858=7"
        target_url = base_url + params
        
        # 使用 HTML 進行提交
        st.components.v1.html(
            f'<img src="{target_url}" style="display:none;" onload="console.log(\'submitted\')">',
            height=0,
        )
        
        st.balloons()
        st.success("報名資訊已送出！")
        st.session_state['page'] = 4
        st.rerun()

# 第四頁：完成
elif st.session_state['page'] == 4:
    st.title("報名成功")
    st.write("感謝您的參與！")
    if st.button("回首頁"):
        st.session_state['page'] = 1
        st.rerun()

# --- 4. 管理員後台 ---
st.markdown("---")
with st.expander("🔐 管理員後台"):
    admin_pw = st.text_input("輸入管理密碼", type="password")
    if admin_pw == "admin123":
        st.success("密碼正確")
        # 解決下載問題：直接放一個超連結導向你的 Google 試算表
        st.write("### 報名資料管理")
        st.write("由於資料已同步至雲端，請直接點擊下方連結查看或下載 Excel：")
        
        # ⚠️ 請把下方的網址換成你的 Google 試算表網址
        sheet_url = "你的Google試算表網址" 
        st.markdown(f'[👉 點此開啟 Google 試算表資料庫]({sheet_url})')


