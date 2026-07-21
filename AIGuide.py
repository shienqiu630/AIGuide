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
                    model='gemini-1.5-flash',
                    contents=prompt,
                )
                
                st.success(f"✨ 成功生成「{destination}」專屬行程！")
                st.markdown("### 📝 AI 深度客製化行程結果")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"❌ 呼叫 AI 時發生錯誤：{e}")
else:
    st.info("👈 請在左側輸入旅遊條件，點擊按鈕即可讓 AI 即時幫你寫行程！")