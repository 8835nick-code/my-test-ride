import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# 網頁設定
st.set_page_config(page_title="機車試乘活動報名系統", page_icon="🏍️", layout="centered")

# --- 1. 初始化 Session State (確保不會報錯) ---
if 'page' not in st.session_state:
    st.session_state.page = 1
if 'temp_data' not in st.session_state:
    st.session_state.temp_data = {}

# --- 2. 連接 Google 試算表 ---
# ⚠️ 請在下方雙引號內貼入你的試算表網址
SHEET_URL = "https://docs.google.com/spreadsheets/d/1nnVGBTNKTEdo_h2Vt2Jo1avIlB70oE8DAaFveXCBCiM/edit?usp=sharing"

conn = st.connection("gsheets", type=GSheetsConnection)

# 讀取現有資料
try:
    existing_data = conn.read(spreadsheet=SHEET_URL, ttl="0")
    if existing_data is None or existing_data.empty:
        existing_data = pd.DataFrame(columns=['姓名', '識別代號', '立書人', '身份證字號', '電話', '試乘機種', '品牌宣導'])
except:
    existing_data = pd.DataFrame(columns=['姓名', '識別代號', '立書人', '身份證字號', '電話', '試乘機種', '品牌宣導'])

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
    
    # 這裡放入你的切結書具體內容
    agreement_text = """
    【試乘活動事前切結書】
    
    本人於民國115年1月30日，參加由台灣山葉機車工業股份有限公司所舉辦之『忘年會試乘活動』(以下簡稱”本活動”)，活動期間，本人完全了解並同意遵守主辦單位所規定之一切安全規則以及下列事項。
1.	本人自願參加本活動，並了解本活動若無嚴苛管控將具有一定程度危險性，本人應完全遵照台灣山葉機車工業股份有限公司(以下稱”主辦單位”)所有相關規範(包括但不限於車輛使用方式、騎乘時應穿戴之安全防護具等)，知悉並遵守主辦單位之規範及安全規範，不得有規範外之行為。
2.	本人已自行評估不論是在心智或是身體狀態皆適合參與本活動，現階段並無飲用任何含酒精飲品、嗜睡類型藥物等無法安全駕駛車輛之情事。
3.	仔細聆聽騎乘前訓練簡介及注意事項之宣達，並遵守工作人員所提出之指示及建議。
4.	參與本活動時，全程嚴守主辦單位工作人員之指揮及調度，避免造成影響騎乘之狀況發生。
5.	本活動期間，本人應完全遵守所有規定並配戴穿著標準人身部品及護具(全罩或3/4安全帽、機車專用手套、防摔衣褲或護膝護肘、一般休閒鞋/球鞋、長袖及長褲)，參與本活動之車輛為台灣山葉機車所有之車輛，本人須考量自身狀態及車輛性能，於本活動進行中如有發生車輛或身體上之損傷均由本人自行負責。
6.	在參加本活動期間，倘若本人未遵守主辦單位工作人員之指示或場內所有規定導致發生任何意外事故，致本人或他人之身體或財產上受到損害，本人同意負所有相關之民、刑事責任。若因此造成主辦單位之損失或損害時，亦應一併賠償。
7.	重要物品應自行保管，有任何遺失、失竊等狀況，主辦單位將不承擔其保管及賠償責任。
8.	在本活動舉辦期間，本人所參與之各項活動，主辦單位得從事攝影、拍照等相關行為，本人亦同意主辦單位擁有本人參與本活動之肖像及車輛照片使用權利，並得用於宣傳或其他商業行為。
9.	若本人有任何違反上述規定、不遵守安全規則或不服從主辦單位指示之情事發生時，山葉有權拒絕提供或立即終止其試駕體驗活動。
10.	本人於簽署前，已充分閱讀過並明確了解此切結書之內容，並已年滿18歲，為民法所規定之完全行為能力人並具資格簽署此份切結書。

本人在此同意上述所有聲明並願意遵守相關活動規則及遵循山葉指示，確認已逐條閱讀本切結書上述各條款，並了解其所表達之涵義，且保證遵守本切結書之內容。

此致 台灣山葉機車工業股份有限公司

    
    
    """
    
    # 顯示切結書內容（用 text_area 或 markdown）
    st.text_area("請閱讀以下條款：", value=agreement_text, height=200, disabled=True)
    
    st.markdown("---")
    
    agree = st.radio("您是否同意以上切結書內容？", ["請選擇", "同意", "不同意"], index=0)
    
    if agree == "同意":
        st.success("您已選擇同意，請填寫下方立書人資訊")
        signer = st.text_input("2. 立書人 (請簽署全名)")
        personal_id = st.text_input("3. 身份證字號")
        phone = st.text_input("4. 電話")
        
        if st.button("下一頁"):
            if signer and personal_id and phone:
                st.session_state.temp_data.update({"立書人": signer, "身份證字號": personal_id, "電話": phone})
                st.session_state.page = 3
                st.rerun()
            else:
                st.error("請完整填寫立書人資訊")
                
    elif agree == "不同意":
        st.warning("若不同意切結書，將無法完成報名。")
        if st.button("提交並結束"):
            st.write("感謝您的填寫。由於您不同意切結書，報名流程已結束。")
            # 這裡可以選擇不存入資料庫，直接結束


# 第三頁：機種選擇 (名額控管)
elif st.session_state['page'] == 3:
    st.title("Step 3: 機種與宣導")
    
    # --- 關鍵修正：使用 existing_data 而不是 st.session_state.db ---
    # 這裡計算目前 Google 試算表中各機種的已報名人數
    if not existing_data.empty and '試乘機種' in existing_data.columns:
        counts = existing_data['試乘機種'].value_counts()
    else:
        counts = pd.Series() # 如果還沒有人報名，就建立空的計數器
    
    CAPACITY = {"CUXIE": 50, "CGYNUS": 50, "NMAX": 50, "大型重機": 50}
    options = ["CUXIE", "CGYNUS", "NMAX", "大型重機"]
    
    # 建立選項標籤，顯示剩餘名額
    def get_label(opt):
        already_taken = counts.get(opt, 0)
        rem = CAPACITY[opt] - already_taken
        if rem <= 0:
            return f"{opt} (已額滿)"
        return f"{opt} (剩餘名額: {rem})"

    selected_model = st.radio("1. 欲試乘機種", options, format_func=get_label)
    
    if selected_model == "大型重機":
        st.warning("⚠️ 須具備大型重型機車駕照，當天查驗")

    promo = st.radio("2. 品牌宣導", ["參加", "不參加"])

    if st.button("確認提交報名"):
        # 再次檢查該機種是否還有名額
        current_taken = counts.get(selected_model, 0)
        if current_taken < CAPACITY[selected_model]:
            # 更新暫存資料
            st.session_state['temp_data'].update({
                "試乘機種": selected_model, 
                "品牌宣導": promo
            })
            
            # --- 寫入 Google Sheets ---
            new_row = pd.DataFrame([st.session_state['temp_data']])
            # 確保欄位順序正確
            final_df = pd.concat([existing_data, new_row], ignore_index=True)
            conn.update(spreadsheet=SHEET_URL, data=final_df)
            
            st.success("報名成功！資料已同步至雲端。")
            st.session_state['page'] = 4
            st.rerun()
        else:
            st.error("抱歉，該機種剛剛已額滿，請選擇其他機種。")

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



