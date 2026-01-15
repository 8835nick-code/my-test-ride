import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# --- 1. 網頁基本設定 ---
st.set_page_config(page_title="機車試乘活動報名系統", page_icon="🏍️")

# --- 2. 初始化 Session State ---
if 'page' not in st.session_state:
    st.session_state['page'] = 1
if 'temp_data' not in st.session_state:
    st.session_state['temp_data'] = {}

# --- 3. 配置資訊 ---
# 這是你剛才產生的表單 ID 轉換而來的提交路徑
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSdczkNBFSVmUipEjm5zYwQLAKOzSJUz4ET7Wyqt4zNSRi-PMw/formResponse"

# 你的 Google 試算表網址 (用來讀取人數，請確保已設為「知道連結的人可以編輯」)
# 如果讀取還是報錯，建議這裡放「發布到網路」的 CSV 連結
SHEET_URL = "在此貼上你的Google試算表網址"

# --- 4. 頁面邏輯 ---

# 第一頁：基本資料
if st.session_state['page'] == 1:
    st.title("Step 1: 基本資料")
    name = st.text_input("1. 姓名", key="input_name")
    id_code = st.text_input("2. 識別代號", key="input_id")
    
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
    agreement_text = """
    【試乘活動事前切結書】
    一、本人自願參加本次機車試乘活動，並保證具備合法駕駛執照。
    二、試乘期間本人願遵守交通規則及工作人員之引導，若發生違規或事故，概由本人自行負責。
    三、如因駕駛不當造成車輛損壞，本人願負賠償責任。
    四、大型重機試乘者，當天須出示大型重型機車駕照供查驗，否則取消資格。
    """
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
    elif agree == "不同意":
        if st.button("結束填寫"):
            st.info("感謝參與，流程已結束。")

# 第三頁：機種選擇與提交
elif st.session_state['page'] == 3:
    st.title("Step 3: 機種與宣導")
    
    # 這裡暫時設定名額 (因為讀取試算表有時會因權限卡住，我們先確保能成功提交)
    options = ["CUXIE", "CGYNUS", "NMAX", "大型重機"]
    selected_model = st.radio("1. 欲試乘機種", options)
    promo = st.radio("2. 品牌宣導", ["參加", "不參加"])

    if st.button("確認提交報名"):
        # 這裡就是利用你提供的 entry ID 進行對應
        payload = {
            "entry.361499099": st.session_state['temp_data']["姓名"],
            "entry.1344609340": st.session_state['temp_data']["識別代號"],
            "entry.1297329962": st.session_state['temp_data']["立書人"],
            "entry.309920621": st.session_state['temp_data']["身份證字號"],
            "entry.1566749837": st.session_state['temp_data']["電話"],
            "entry.371178622": selected_model,
            "entry.1133738858": promo
        }
        
        try:
            res = requests.post(FORM_URL, data=payload)
            if res.status_code == 200:
                st.balloons()
                st.success("報名成功！資料已同步至雲端試算表。")
                st.session_state['page'] = 4
                st.rerun()
            else:
                st.error("提交失敗，請檢查網路連線。")
        except:
            st.error("傳輸出錯，請聯絡管理員。")

# 第四頁：完成
elif st.session_state['page'] == 4:
    st.title("報名成功")
    st.write("我們已收到您的報名資訊，期待當天見面！")
    if st.button("回首頁"):
        st.session_state['page'] = 1
        st.rerun()
