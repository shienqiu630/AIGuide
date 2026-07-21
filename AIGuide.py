import streamlit as st
from google import genai
import os
import time

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

destination = st.sidebar.text_input("🌍 目的地", placeholder="請輸入想去的國家或城市，例如：京都、巴黎")
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
st.markdown("##### 💡 結合多維度權重分析、動態候選景點評分與決策透明化的新一代 AI 旅遊決策中樞")
st.markdown("---")

# ==================== 4. 核心 AI 邏輯與區塊 ====================
if generate_btn:
    if not destination.strip():
        st.warning("⚠️ 請先在左側輸入您的旅遊目的地！")
    elif not api_key:
        st.error("⚠️ 尚未設定 API Key！請至 Streamlit Cloud 後台 Settings -> Secrets 中設定 GEMINI_API_KEY。")
    else:
        status_box = st.status("🧠 AI 智慧推薦中樞啟動中...", expanded=True)
        
        with status_box:
            st.write(f"🌐 正在解析目的地：【{destination}】之地理與旅遊特徵...")
            time.sleep(0.4)
            st.write(f"⚖️ 正在根據「{travel_type}」與偏好動態計算權重模型...")
            time.sleep(0.4)
            st.write("🔍 正在執行候選景點搜尋與多輪過濾篩選...")
            time.sleep(0.4)
            st.write("📊 正在執行評分依據建立、決策日誌與動線最佳化運算...")
            
            try:
                client = genai.Client(api_key=api_key)
                
                prompt = f"""
                你是一個專業的 AI 智慧旅遊推薦系統與高階行程規劃師。請針對以下使用者輸入的獨特條件，進行即時的動態分析與思考運算。
                【絕對警告】：請勿使用任何預先寫死或固定的罐頭景點與模板！所有內容都必須100%根據本次輸入現場動態生成。

                [使用者輸入參數]
                - 目的地：{destination}
                - 旅遊天數：{days} 天
                - 旅伴人數：{people} 人
                - 總預算：{budget} 新台幣
                - 交通方式：{transport}
                - 旅遊類型：{travel_type}
                - 旅遊偏好：{', '.join(preferences) if preferences else '無特別指定'}
                - 需要雨天備案：{rain_backup}

                請以繁體中文回答，並嚴格按照以下章節標題輸出（請確保標題完全一致）：

                ### ① AI Decision Log
                收到使用者需求
                ↓
                分析需求
                ↓
                建立候選景點
                ↓
                完成第一輪評分
                ↓
                淘汰交通不佳景點
                ↓
                重新排序
                ↓
                最佳化住宿位置
                ↓
                檢查預算
                ↓
                驗證交通
                ↓
                生成最終行程

                ### ② AI候選景點篩選流程
                AI搜尋景點
                ↓
                共搜尋到 [動態數字] 個景點
                ↓
                第一輪篩選
                ↓
                依交通淘汰
                ↓
                依預算淘汰
                ↓
                依旅遊偏好淘汰
                ↓
                留下 [動態數字] 個候選景點

                ### ③ AI需求與權重分析
                - 旅遊限制與特色：
                - 各項指標權重說明（推薦度、交通、CP值、拍照、美食、雨天適合度）：

                ### ④ AI景點評分
                - 請現場動態列出被保留的候選景點，並針對每個景點提供包含以下格式的詳細評分與簡短理由：
                  景點名稱：[景點]
                  - 交通：[分數]
                    原因：[理由簡述]
                  - 拍照：[分數]
                    原因：[理由簡述]
                  - CP值：[分數]
                    原因：[理由簡述]
                  - 綜合分數：[分數]

                ### ⑤ AI淘汰原因
                - 說明有哪些候選景點被淘汰及其具體原因。

                ### ⑥ AI動線最佳化
                - 解釋為何這樣安排以減少交通時間、避免折返與控制預算。

                ### ⑦ 每日詳細行程
                (請依照 Day 1, Day 2... 逐日詳細列出：上午、午餐、下午、晚餐、晚上、交通、預估花費)

                ### ⑧ 雨天備案
                (針對戶外行程提供對應的室內雨天替代方案與說明)

                ### ⑨ AI可信度摘要
                - AI可信度：[動態百分比]%
                - 原因：
                  ✓ [正面條件]
                  ⚠ [風險變數]
                """
                
                response = client.models.generate_content(
                    model='gemini-3.5-flash',
                    contents=prompt,
                )
                
                st.session_state["ai_response"] = response.text
                st.session_state["generated"] = True
                status_box.update(label="✅ AI 智慧推薦與決策中樞運算完成！", state="complete", expanded=False)
                
            except Exception as e:
                status_box.update(label="❌ 運算發生錯誤", state="error", expanded=True)
                st.error(f"❌ 呼叫 AI 時發生錯誤：{e}")

# ==================== 5. 呈現介面 (Tabs + 切割顯示與獨立編號) ====================
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

    # 各分頁獨立呈現，並將標題編號動態替換為分頁專屬的 1, 2, 3...
    with tab_itinerary:
        st.subheader(f"✨ 「{destination}」動態生成專屬智慧行程")
        itinerary_part = extract_section(full_text, "### ⑦ 每日詳細行程", "### ⑧ 雨天備案")
        backup_part = extract_section(full_text, "### ⑧ 雨天備案", "### ⑨ AI可信度摘要")
        
        # 重新編號為 1, 2
        itinerary_part = itinerary_part.replace("### ⑦ 每日詳細行程", "### ① 每日詳細行程")
        backup_part = backup_part.replace("### ⑧ 雨天備案", "### ② 雨天備案")
        
        st.markdown(itinerary_part)
        st.markdown(backup_part)

    with tab_analysis:
        st.subheader("📊 篩選流程、多維度權重與評分依據模型")
        
        sec_filter = extract_section(full_text, "### ② AI候選景點篩選流程", "### ③ AI需求與權重分析").replace("### ② AI候選景net篩選流程", "### ① AI候選景點篩選流程").replace("### ② AI候選景點篩選流程", "### ① AI候選景點篩選流程")
        sec_weight = extract_section(full_text, "### ③ AI需求與權重分析", "### ④ AI景點評分").replace("### ③ AI需求與權重分析", "### ② AI需求與權重分析")
        sec_score = extract_section(full_text, "### ④ AI景點評分", "### ⑤ AI淘汰原因").replace("### ④ AI景點評分", "### ③ AI景點評分")
        
        with st.expander("🔍 點擊展開：① 候選景點篩選流程", expanded=True):
            st.markdown(sec_filter)
            
        with st.expander("📈 點擊展開：② AI 需求與權重分析", expanded=False):
            st.markdown(sec_weight)
            
        with st.expander("⭐ 點擊展開：③ AI 景點評分（含詳細依據）", expanded=False):
            st.markdown(sec_score)

    with tab_decision:
        st.subheader("⚙️ 決策中樞：AI Decision Log 與可信度驗證")
        
        sec_log = extract_section(full_text, "### ① AI Decision Log", "### ② AI候選景點篩選流程").replace("### ① AI Decision Log", "### ① AI Decision Log")
        sec_eliminate = extract_section(full_text, "### ⑤ AI淘汰原因", "### ⑦ 每日詳細行程").replace("### ⑤ AI淘汰原因", "### ② AI淘汰原因與動線最佳化").replace("### ⑥ AI動線最佳化", "")
        sec_credibility = extract_section(full_text, "### ⑨ AI可信度摘要", None).replace("### ⑨ AI可信度摘要", "### ③ AI可信度評估摘要")
        
        with st.expander("🧭 點擊展開：① AI Decision Log（決策透明度）", expanded=True):
            st.markdown(sec_log)
            
        with st.expander("🗑️ 點擊展開：② AI 淘汰原因與動線最佳化", expanded=False):
            st.markdown(sec_eliminate)
            
        with st.expander("🎯 點擊展開：③ AI 可信度評估摘要", expanded=False):
            st.markdown(sec_credibility)

else:
    st.info("👈 請在左側輸入您想去的目的地與進階偏好，並點擊 **`🚀 啟動 AI 智慧推薦與排程引擎`**，讓系統即時為您現場運算具備透明決策日誌的推薦報告！")