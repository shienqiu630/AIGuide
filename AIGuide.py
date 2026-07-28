import streamlit as st
from google import genai
import os
import time
from PIL import Image

# ==================== 1. 頁面基本設定 ====================
st.set_page_config(
    page_title="AI 玩樂指南 - 智慧旅遊推薦系統", 
    page_icon="✈️", 
    layout="wide"
)

# 載入 API Key
api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

# ==================== 2. 側邊欄：全域功能切換 ====================
st.sidebar.title("🧭 AI 玩樂指南控制台")
app_mode = st.sidebar.selectbox("📂 選擇系統核心功能", [
    "🗺️ AI 智慧旅遊行程規劃引擎", 
    "📸 AI 智慧以圖搜景與周遭探索"
])

st.sidebar.markdown("---")

# ==================== 模式 A：原本的智慧行程規劃引擎 ====================
if app_mode == "🗺️ AI 智慧旅遊行程規劃引擎":
    
    st.sidebar.header("🎯 AI 智慧推薦系統設定")
    destination = st.sidebar.text_input("🌍 目的地", placeholder="請輸入想去的國家或城市，例如：京都、巴黎")
    days = st.sidebar.slider("📅 旅遊天數", min_value=1, max_value=30, value=3)
    people = st.sidebar.number_input("👥 旅伴人數", min_value=1, max_value=20, value=2)
    budget = st.sidebar.number_input("💰 總預算 (TWD)", min_value=1000, max_value=1000000, value=30000, step=1000)
    transport = st.sidebar.selectbox("🚗 主要交通方式", ["大眾運輸", "自駕", "步行/單車"])

    st.sidebar.markdown("---")
    st.sidebar.subheader("🧠 系統進階偏好")

    travel_type = st.sidebar.selectbox(
        "👥 旅遊類型", 
        ["朋友", "情侶", "家庭", "親子", "背包客", "銀髮族"]
    )

    preferences = st.sidebar.multiselect(
        "🏷️ 旅遊偏好（可複選）", 
        ["美食", "拍照", "夜景", "自然", "歷史文化", "博物館", "購物", "動漫", "親子"],
        default=["美食", "拍照", "購物"]
    )

    rain_backup = st.sidebar.radio("☔ 是否需要雨天備案", ["Yes", "No"], index=0)

    generate_btn = st.sidebar.button("🚀 啟動 AI 智慧推薦與排程引擎", type="primary")

    # 主畫面標題與狀態
    st.title("🗺️ 「AI 玩樂指南」：動態 AI 智慧旅遊推薦系統")
    st.markdown("##### 💡 結合多維度權重分析、動態候選景點評分、Double Check機制的進階 AI 旅遊決策中樞")
    st.markdown("---")

    if generate_btn:
        if not destination.strip():
            st.warning("⚠️ 請先在左側輸入您的旅遊目的地！")
        elif not api_key:
            st.error("⚠️ 尚未設定 API Key！請至 Streamlit Cloud 後台 Settings -> Secrets 中設定 GEMINI_API_KEY。")
        else:
            status_box = st.status("🧠 AI 智慧推薦中樞啟動中...", expanded=True)
            
            with status_box:
                st.write(f"🌐 正在解析目的地：【{destination}】之地理與旅遊特徵（規劃天數：{days}天）...")
                time.sleep(0.4)
                st.write(f"⚖️ 正在根據「{travel_type}」與偏好動態計算權重模型...")
                time.sleep(0.4)
                st.write("🔍 正在執行候選景點搜尋、多輪過濾篩選與 Day1~DayN 擴展運算...")
                time.sleep(0.4)
                st.write("🛡️ 正在執行 AI Double Check 最終檢核、動線最佳化與可信度評級...")
                
                try:
                    client = genai.Client(api_key=api_key)
                    
                    prompt = f"""
                    你是一個專業的 AI 智慧旅遊推薦系統與高階行程規劃師。請針對以下使用者輸入的獨特條件，進行即時的動態分析與思考運算。
                    【絕對警告】：請勿使用任何預先寫死或固定的罐頭景點與模板！所有內容都必須100%根據本次輸入現場動態生成。

                    [使用者輸入參數]
                    - 目的地：{destination}
                    - 旅遊天數：{days} 天 (必須嚴格依照輸入天數完整生成 Day 1 到 Day {days} 的行程，不可寫死或縮減為 7 天)
                    - 旅伴人數：{people} 人
                    - 總預算：{budget} 新台幣
                    - 交通方式：{transport}
                    - 旅遊類型：{travel_type}
                    - 旅遊偏好：{', '.join(preferences) if preferences else '無特別指定'}
                    - 需要雨天備案：{rain_backup}

                    【整體一致性強制要求】：
                    AI 在輸出完整行程前，需再次確認：
                    ① 每日住宿與隔日動線是否一致。
                    ② 今日景點是否真的在同一區域。
                    ③ 是否符合使用者偏好（美食、拍照、購物等）。
                    ④ 是否符合交通方式。
                    ⑤ 是否符合旅遊類型。
                    ⑥ 是否符合預算。
                    ⑦ 是否符合旅遊天數（Day 1 ~ Day {days}）。
                    若不符合，請自動重新安排。

                    請以繁體中文回答，並嚴格按照以下 10 個章節標題順序輸出：

                    ### ① AI需求分析
                    - 分析旅遊限制與特色：
                    - 適合玩法：

                    ### ② AI權重分析
                    - 說明系統如何針對本次條件動態調整以下指標的權重（推薦度、交通、CP值、拍照、美食、雨天適合度）：

                    ### ③ AI候選景點評分
                    - 請現場動態列出被保留的候選景點，並針對每個景點提供包含以下格式的詳細評分與簡短理由：
                      景點名稱：[景點]
                      - 交通：[分數]
                        原因：[理由簡述]
                      - 拍照：[分數]
                        原因：[理由簡述]
                      - CP值：[分數]
                        原因：[理由簡述]
                      - 綜合分數：[分數]

                    ### ④ AI淘汰原因
                    - 說明有哪些候選景點被淘汰及其具體原因。

                    ### ⑤ AI動線最佳化
                    - 解釋為何這樣安排以減少交通時間、避免折返與控制預算。

                    ### ⑥ 每日詳細行程
                    (請完整依照 Day 1 至 Day {days} 逐日詳細列出：每日住宿區域、上午、午餐、下午、晚餐、晚上、交通、預估花費。絕對不可中途截斷或只寫到 Day 7)

                    ### ⑦ 雨天備案
                    (針對戶外行程提供對應的室內雨天替代方案與說明)

                    ### ⑧ AI 行程可信度
                    AI 行程可信度：
                    [請依照分數給予對應星級：★★★★★ (98-100%) / ★★★★☆ (90-97%) / ★★★☆☆ (80-89%) / ★★☆☆☆ (70-79%) / ★☆☆☆☆ (60-69%)]

                    可信度分析：
                    優點：
                    • [優點1]
                    • [優點2]

                    可能風險：
                    • [風險1]

                    降低可信度原因：
                    • [原因]

                    ### ⑨ AI決策摘要
                    - 分析景點數量：
                    - 最後採用景點數量：
                    - 一句總結：

                    ### ⑩ AI Double Check
                    AI 必須在完成行程後，再重新檢查一次整份行程（涵蓋重複性、折返、交通銜接、預算、時間壓力、公休日、預約需求、夜間安全與天候風險）。

                    Double Check 結果：
                    交通：
                    [✅ 通過 / ⚠ 建議調整...]

                    預算：
                    [✅ 通過 / ⚠ 建議調整...]

                    景點：
                    [✅ 通過 / ⚠ 建議調整...]

                    時間：
                    [✅ 通過 / ⚠ 建議調整...]

                    住宿：
                    [✅ 通過 / ⚠ 建議調整...]

                    安全：
                    [✅ 通過 / ⚠ 建議調整...]

                    AI 修正建議：
                    (若發現問題已於排程中自動修正的說明記錄)
                    """
                    
                    response = client.models.generate_content(
                        model='gemini-3.5-flash',
                        contents=prompt,
                    )
                    
                    st.session_state["ai_response"] = response.text
                    st.session_state["generated"] = True
                    status_box.update(label="✅ AI 智慧推薦、Double Check 與決策中樞運算完成！", state="complete", expanded=False)
                    
                except Exception as e:
                    status_box.update(label="❌ 運算發生錯誤", state="error", expanded=True)
                    st.error(f"❌ 呼叫 AI 時發生錯誤：{e}")

    #呈現介面 (Tabs + 切割顯示與獨立編號)
    if st.session_state.get("generated", False):
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(label="🤖 AI 模型核心", value="Gemini-3.5-Flash")
        with col2:
            st.metric(label="📅 規劃天數", value=f"{days} 天")
        with col3:
            st.metric(label="💰 預算上限", value=f"${budget:,} TWD")
        with col4:
            st.metric(label="👥 同行人數", value=f"{people} 人")
            
        st.markdown("---")
        
        tab_itinerary, tab_analysis, tab_decision = st.tabs(["📋 AI 行程總覽", "📊 AI 分析與權重", "⚙️ AI 決策與透明度日誌"])
        
        full_text = st.session_state["ai_response"]
        
        def extract_section(text, start_marker, end_marker):
            try:
                start = text.index(start_marker)
                if end_marker:
                    end = text.index(end_marker)
                    return text[start:end]
                return text[start:]
            except:
                return ""

        with tab_itinerary:
            st.subheader(f"✨ 「{destination}」動態生成專屬智慧行程（共 {days} 天）")
            itinerary_part = extract_section(full_text, "### ⑥ 每日詳細行程", "### ⑦ 雨天備案")
            backup_part = extract_section(full_text, "### ⑦ 雨天備案", "### ⑧ AI 行程可信度")
            
            itinerary_part = itinerary_part.replace("### ⑥ 每日詳細行程", "### ① 每日詳細行程")
            backup_part = backup_part.replace("### ⑦ 雨天備案", "### ② 雨天備案")
            
            st.markdown(itinerary_part)
            st.markdown(backup_part)

        with tab_analysis:
            st.subheader("📊 篩選流程、多維度權重與評分依據模型")
            
            sec_req = extract_section(full_text, "### ① AI需求分析", "### ② AI權重分析")
            sec_weight = extract_section(full_text, "### ② AI權重分析", "### ③ AI候選景點評分")
            sec_score = extract_section(full_text, "### ③ AI候選景點評分", "### ④ AI淘汰原因")
            
            with st.expander("🔍 點擊展開：① AI 需求分析", expanded=True):
                st.markdown(sec_req)
                
            with st.expander("📈 點擊展開：② AI 權重分析", expanded=False):
                st.markdown(sec_weight)
                
            with st.expander("⭐ 點擊展開：③ AI 景點評分（含詳細依據）", expanded=False):
                st.markdown(sec_score)

        with tab_decision:
            st.subheader("⚙️ 決策中樞：淘汰原因、動線、可信度與 Double Check 日誌")
            
            sec_eliminate = extract_section(full_text, "### ④ AI淘汰原因", "### ⑤ AI動線最佳化").replace("### ④ AI淘汰原因", "### ① AI淘汰原因")
            sec_optimize = extract_section(full_text, "### ⑤ AI動線最佳化", "### ⑥ 每日詳細行程").replace("### ⑤ AI動線最佳化", "### ② AI動線最佳化")
            sec_credibility = extract_section(full_text, "### ⑧ AI 行程可信度", "### ⑨ AI決策摘要").replace("### ⑧ AI 行程可信度", "### ③ AI 行程可信度")
            sec_summary = extract_section(full_text, "### ⑨ AI決策摘要", "### ⑩ AI Double Check").replace("### ⑨ AI決策摘要", "### ④ AI決策摘要")
            sec_doublecheck = extract_section(full_text, "### ⑩ AI Double Check", None).replace("### ⑩ AI Double Check", "### ⑤ AI Double Check 最終驗證")
            
            with st.expander("🗑️ 點擊展開：① AI 淘汰原因", expanded=True):
                st.markdown(sec_eliminate)
                
            with st.expander("🛣️ 點擊展開：② AI 動線最佳化", expanded=False):
                st.markdown(sec_optimize)
                
            with st.expander("🎯 點擊展開：③ AI 行程可信度（星級評等）", expanded=False):
                st.markdown(sec_credibility)
                
            with st.expander("📌 點擊展開：④ AI 決策摘要", expanded=False):
                st.markdown(sec_summary)

            with st.expander("🛡️ 點擊展開：⑤ AI Double Check 最終驗證日誌", expanded=False):
                st.markdown(sec_doublecheck)

    else:
        st.info("👈 請在左側輸入您想去的目的地與進階偏好（支援 1~30 天彈性天數），並點擊 **`🚀 啟動 AI 智慧推薦與排程引擎`**，讓系統即時為您現場運算具備 Double Check機制的推薦報告！")

# ==================== 模式 B：新增的 AI 以圖搜景與周遭推薦 ====================
elif app_mode == "📸 AI 智慧以圖搜景與周遭探索":
    
    st.title("📸 AI 智慧以圖搜景與周遭全方位推薦")
    st.markdown("##### 💡 拍一張旅遊照片或上傳地標影像，AI 將自動辨識定位，並為您深度推薦周遭的景點、美食、購物、咖啡廳、夜景與隱藏私房秘境！")
    st.markdown("---")
    
    uploaded_file = st.file_uploader("📤 請上傳一張旅遊景點或地標照片...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        
        # 左右排版：左邊秀圖片，右邊按按鈕
        col_img, col_btn = st.columns([1, 1])
        with col_img:
            st.image(image, caption="已上傳的使用者照片", use_column_width=True)
            
        with col_btn:
            st.markdown("### 🔍 準備就緒")
            st.markdown("系統已透過多模態視覺模型載入您的影像。點擊下方按鈕，AI 將立刻進行空間定位與深度周遭探勘！")
            search_vision_btn = st.button("🚀 開始 AI 影像辨識與周遭探索", type="primary")
            
        if search_vision_btn:
            if not api_key:
                st.error("⚠️ 尚未設定 API Key！請至 Streamlit Cloud 後台 Settings -> Secrets 中設定 GEMINI_API_KEY。")
            else:
                with st.spinner("🤖 AI 正在解析圖片視覺特徵、比對全球地標並挖掘周遭吃喝玩樂好去處..."):
                    try:
                        client = genai.Client(api_key=api_key)
                        
                        vision_prompt = """
                        你是一個專業的 AI 智慧旅遊導遊與地理定位專家。請分析使用者上傳的這張照片：
                        1. 辨識照片中的具體位置、地標或城市區域。
                        2. 若無法 100% 確定精確地址，請根據照片特徵推估其所在的核心商圈或區域，並以此區域為中心，推薦周遭的必訪地點。

                        請以繁體中文回答，並嚴格按照以下類別與格式詳細推薦：

                        ### 📍 AI 視覺定位結果
                        - 辨識地點名稱：
                        - 影像辨識信心水準：[XX]%
                        - 位置特徵說明：

                        ### 🏛️ 周遭景點推薦
                        (列出 3~4 個附近必去景點，包含名稱與特色)

                        ### 🍜 周遭美食推薦
                        (列出 3~4 家附近在地知名美食或小吃)

                        ### 🛍️ 周遭購物推薦
                        (列出 2~3 個逛街、買伴手禮或商場的好去處)

                        ### ☕ 周遭咖啡廳推薦
                        (列出 2~3 家特色咖啡廳或歇腳處)

                        ### 🌃 周遭夜景推薦
                        (列出 1~2 個欣賞夜景的絕佳視角或高處)

                        ### 🤫 周遭隱藏私房景點 (Local Secret)
                        (列出 1~2 個觀光客較少、在地人才知道的私房秘境)
                        """
                        
                        response = client.models.generate_content(
                            model='gemini-3.5-flash',
                            contents=[image, vision_prompt]
                        )
                        
                        st.markdown("---")
                        st.success("✨ AI 視覺辨識與周遭探索報告生成完畢！")
                        st.markdown(response.text)
                        
                    except Exception as e:
                        st.error(f"❌ 影像辨識與呼叫 AI 時發生錯誤：{e}")
    else:
        st.info("👈 請上方上傳您的旅遊照片，讓 AI 帶您體驗「以圖搜景」的全新智慧導覽互動！")
