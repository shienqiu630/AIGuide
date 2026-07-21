import streamlit as st
from google import genai
import os

st.set_page_config(
    page_title="AI 玩樂指南 - 智慧行程生成系統", 
    page_icon="✈️", 
    layout="wide"
)

st.title("🗺️ 「AI 玩樂指南」：動態 AI 智慧行程生成系統")
st.markdown("---")

# 從 Streamlit Secrets 或環境變數自動讀取 API Key
api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

# ==================== 側邊欄：使用者輸入區 ====================
st.sidebar.header("🎯 請輸入您的旅遊需求")

destination = st.sidebar.text_input("目的地", "東京")
days = st.sidebar.slider("旅遊天數", min_value=1, max_value=7, value=3)
people = st.sidebar.number_input("旅伴人數", min_value=1, max_value=20, value=2)
budget = st.sidebar.number_input("總預算 (TWD)", min_value=1000, max_value=200000, value=30000, step=1000)
transport = st.sidebar.selectbox("交通方式", ["大眾運輸", "自駕", "步行/單車"])

generate_btn = st.sidebar.button("🚀 呼叫 Gemini AI 生成行程", type="primary")

# ==================== 主畫面邏輯 ====================
if generate_btn:
    if not api_key:
        st.error("⚠️ 尚未設定 API Key！請至 Streamlit Cloud 後台 Settings -> Secrets 中設定 GEMINI_API_KEY。")
    else:
        with st.spinner(f"🤖 Gemini AI 正在為您規劃 {destination} 的 {days} 天專屬行程中..."):
            try:
                client = genai.Client(api_key=api_key)
                
                prompt = f"""
                你是一個專業的 AI 旅遊規劃師。請根據以下需求，為使用者規劃一份詳細的旅遊行程：
                - 目的地：{destination}
                - 旅遊天數：{days} 天
                - 旅伴人數：{people} 人
                - 總預算：{budget} 新台幣
                - 主要交通方式：{transport}
                
                請使用繁體中文回答，並依照天數 (Day 1, Day 2...) 詳細列出每日的上、午、下午、晚上行程、推薦美食與預估花費。語氣要生動專業。
                """
                
                response = client.models.generate_content(
                    model='gemini-3.5-flash',
                    contents=prompt,
                )
                
                st.success(f"✨ 成功生成「{destination}」專屬行程！")
                st.markdown("### 📝 AI 深度客製化行程結果")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"❌ 呼叫 AI 時發生錯誤：{e}")
else:
    st.info("👈 請在左側輸入旅遊條件，點擊按鈕即可讓 AI 即時幫你寫行程！")import streamlit as st
from google import genai
import os

# ==================== 1. 頁面基本設定 ====================
st.set_page_config(
    page_title="AI 玩樂指南 - 智慧旅遊推薦系統", 
    page_icon="✈️", 
    layout="wide"
)

# 載入 API Key
api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

# ==================== 2. 側邊欄：進階推薦系統輸入區 ====================
st.sidebar.header("🎯 AI 智慧推薦系統設定")

destination = st.sidebar.text_input("🌍 目的地", placeholder="請輸入想去的國家或城市，例如：巴黎")
days = st.sidebar.slider("📅 旅遊天數", min_value=1, max_value=7, value=3)
people = st.sidebar.number_input("👥 旅伴人數", min_value=1, max_value=20, value=2)
budget = st.sidebar.number_input("💰 總預算 (TWD)", min_value=1000, max_value=200000, value=30000, step=1000)
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

# ==================== 3. 主畫面標題與狀態 ====================
st.title("🗺️ 「AI 玩樂指南」：動態 AI 智慧旅遊推薦系統")
st.markdown("##### 💡 結合多維度權重分析、候選景點評分與動線最佳化的新一代 AI 旅遊決策中樞")
st.markdown("---")

# ==================== 4. 核心 AI 邏輯與區塊 ====================
if generate_btn:
    if not api_key:
        st.error("⚠️ 尚未設定 API Key！請至 Streamlit Cloud 後台 Settings -> Secrets 中設定 GEMINI_API_KEY。")
    else:
        with st.spinner(f"🤖 AI 推薦引擎正在運算 {destination} 的最佳旅遊決策模型（分析需求、權重、景點評分與動線）..."):
            try:
                client = genai.Client(api_key=api_key)
                
                # 組裝嚴謹的結構化 Prompt
                prompt = f"""
                你是一個專業的 AI 智慧旅遊推薦系統與高階行程規劃師。請根據以下使用者參數，進行深度思考與系統化分析，並嚴格按照指定的 8 個步驟格式輸出報告：

                [使用者輸入參數]
                - 目的地：{destination}
                - 旅遊天數：{days} 天
                - 旅伴人數：{people} 人
                - 總預算：{budget} 新台幣
                - 交通方式：{transport}
                - 旅遊類型：{travel_type}
                - 旅遊偏好：{', '.join(preferences) if preferences else '無特別指定'}
                - 需要雨天備案：{rain_backup}

                請以繁體中文回答，並使用以下標題與結構輸出：

                ### ① AI需求分析
                - 分析旅遊限制：
                - 旅遊特色：
                - 適合玩法：

                ### ② AI權重分析
                - 依照上述需求，說明系統如何動態調整以下指標的權重（給予原因）：
                  - 推薦度
                  - 交通
                  - CP值
                  - 拍照
                  - 美食
                  - 雨天適合度

                ### ③ AI景點評分
                - 請先列出 6~10 個候選景點，並必須使用 Markdown 表格呈現，欄位包含：| 景點 | 推薦度 | 交通 | CP值 | 拍照 | 美食 | 綜合分數 |，並依照綜合分數排序。

                ### ④ AI淘汰原因
                - 列出有哪些候選景點沒有被安排？
                - 列出淘汰原因（例如：距離太遠、交通太久、性質重複、時間不足等）。

                ### ⑤ AI動線最佳化
                - 解釋為何這樣安排：
                - 如何減少交通時間：
                - 如何避免折返：
                - 如何控制預算：

                ### ⑥ 每日詳細行程
                (請依照 Day 1, Day 2... 逐日詳細列出：上午、午餐、下午、晚餐、晚上、交通、預估花費)

                ### ⑦ 雨天備案
                (針對戶外行程提供對應的室內雨天替代方案與說明)

                ### ⑧ AI決策摘要
                - 分析景點數量：
                - 最後採用景點數量：
                - AI推薦可信度（%）：
                - 一句總結：
                """
                
                response = client.models.generate_content(
                    model='gemini-3.5-flash',
                    contents=prompt,
                )
                
                # 將結果暫存於 session_state 中，避免切換分頁時遺失
                st.session_state["ai_response"] = response.text
                st.session_state["generated"] = True
                
            except Exception as e:
                st.error(f"❌ 呼叫 AI 時發生錯誤：{e}")

# ==================== 5. 呈現介面 (Tabs + Metrics + Expanders) ====================
if st.session_state.get("generated", False):
    
    # 頂部儀表板數據指標 (st.metric)
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
    
    # 三大核心分頁 (st.tabs)
    tab_itinerary, tab_analysis, tab_decision = st.tabs(["📋 AI 行程總覽", "📊 AI 分析與權重", "⚙️ AI 決策與淘汰機制"])
    
    full_text = st.session_state["ai_response"]
    
    # 簡單切割字串用來分發到不同分頁展示
    with tab_itinerary:
        st.subheader(f"✨ 「{destination}」專屬智慧行程")
        # 顯示⑥每日詳細行程與⑦雨天備案相關內容
        st.markdown(full_text)

    with tab_analysis:
        st.subheader("📊 多維度權重分析與候選評分模型")
        with st.expander("🔍 點擊展開：① AI 需求分析與 ② 權重計算過程", expanded=True):
            st.info("系統透過使用者的旅遊類型與偏好，自動計算各項評分權重：")
            st.markdown(full_text)

    with tab_decision:
        st.subheader("⚙️ 決策中樞：景點評分表、淘汰原因與動線最佳化")
        with st.expander("📈 點擊展開：③ 候選景點評分表與 ④ 淘汰機制說明", expanded=True):
            st.markdown(full_text)

else:
    st.info("👈 請在左側設定好旅遊需求與進階偏好，並點擊 **「🚀 啟動 AI 智慧推薦與排程引擎」**，讓系統為您產出完整的智慧旅遊決策報告！")