import streamlit as st
import pandas as pd
from datetime import datetime

# 設定網頁標題
st.set_page_config(page_title="機車試乘活動報名系統", layout="centered")

# 模擬資料庫 (實際使用時建議連結 Google Sheets 或資料庫)
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame(columns=['姓名', '識別代號', '立書人', '身份證字號', '電話', '試乘機種', '品牌宣導'])

if 'page' not in st.session_state:
    st.session_state.page = 1

# 設定各機種名額上限
CAPACITY = {"CUXIE": 50, "CGYNUS": 50, "NMAX": 50, "大型重機": 50}

# --- 頁面邏輯 ---

# 第一頁：基本資料
if st.session_state.page == 1:
    st.title("Step 1: 基本資料")
    name = st.text_input("1. 姓名")
    id_code = st.text_input("2. 識別代號")
    
    if st.button("下一頁"):
        if name and id_code:
            st.session_state.temp_data = {"姓名": name, "識別代號": id_code}
            st.session_state.page = 2
            st.rerun()
        else:
            st.error("請填寫所有欄位")

# 第二頁：切結書
elif st.session_state.page == 2:
    st.title("Step 2: 事前切結書")
    agree = st.radio("您是否同意事前切結書內容？", ["請選擇", "同意", "不同意"])
    
    if agree == "同意":
        signer = st.text_input("2. 立書人")
        personal_id = st.text_input("3. 身份證字號")
        phone = st.text_input("4. 電話")
        
        if st.button("下一頁"):
            if signer and personal_id and phone:
                st.session_state.temp_data.update({"立書人": signer, "身份證字號": personal_id, "電話": phone})
                st.session_state.page = 3
                st.rerun()
            else:
                st.error("請填寫所有欄位")
                
    elif agree == "不同意":
        if st.button("提交並結束"):
            st.write("感謝您的填寫。由於您不同意切結書，報名流程已結束。")
            if st.button("重新開始"):
                st.session_state.page = 1
                st.rerun()

# 第三頁：機種選擇與品牌宣導
elif st.session_state.page == 3:
    st.title("Step 3: 機種與宣導")
    
    # 計算剩餘名額
    counts = st.session_state.db['試乘機種'].value_counts()
    
    def get_label(model):
        remaining = CAPACITY[model] - counts.get(model, 0)
        return f"{model} (剩餘名額: {remaining})" if remaining > 0 else f"{model} (已額滿)"

    options = ["CUXIE", "CGYNUS", "NMAX", "大型重機"]
    # 檢查哪些選項已額滿
    available_options = [opt for opt in options if (CAPACITY[opt] - counts.get(opt, 0)) > 0]
    
    selected_model = st.radio("1. 欲試乘機種 (每項限50人)", options, 
                              index=None,
                              captions=["" if opt in available_options else "已額滿不可選" for opt in options])
    
    if selected_model == "大型重機":
        st.warning("⚠️ 須具備大型重型機車駕照，試乘當天將進行查驗。")

    promo = st.radio("2. 品牌宣導", ["參加", "不參加"])

    if st.button("完成報名"):
        if selected_model in available_options:
            st.session_state.temp_data.update({"試乘機種": selected_model, "品牌宣導": promo})
            # 存入資料庫
            new_entry = pd.DataFrame([st.session_state.temp_data])
            st.session_state.db = pd.concat([st.session_state.db, new_entry], ignore_index=True)
            st.success("報名成功！")
            st.balloons()
            if st.button("回首頁"):
                st.session_state.page = 1
                st.rerun()
        else:
            st.error("該機種已額滿，請選擇其他機種")

# --- 後台下載區 (隱藏區塊) ---
st.markdown("---")
with st.expander("🔐 管理員後台 (下載數據)"):
    pw = st.text_input("輸入密碼查看數據", type="password")
    if pw == "admin123": # 請自行更改密碼
        st.write("目前的報名名單：")
        st.dataframe(st.session_state.db)
        
        # 轉成 Excel 下載
        csv = st.session_state.db.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="點此下載 Excel (CSV) 數據",
            data=csv,
            file_name=f"報名清單_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
        )