# main.py
import streamlit as st
import sys
sys.stdout.reconfigure(encoding="utf-8")
from api import get_ai_response
from prompts import SYSTEM_PROMPT

st.set_page_config(page_title="小航·郑州航院校园信息助手")
st.markdown("# 小航·郑州航院校园信息助手")

user_type = st.selectbox("你是？", ["新生", "在校生", "毕业生"])

st.markdown("### 试试这些问题：")
col1, col2, col3, col4 = st.columns(4)
with col1:
    b1 = st.button("报到那天先去哪？")
with col2:
    b2 = st.button("学费什么时候交？")
with col3:
    b3 = st.button("宿舍是4人间还是6人间？")
with col4:
    b4 = st.button("有人冒充辅导员要钱怎么办？")

input_text = st.text_input("有啥想问的？")
query = ""
if b1:
    query = "报到那天先去哪？"
if b2:
    query = "学费什么时候交？"
if b3:
    query = "宿舍是4人间还是6人间？"
if b4:
    query = "有人冒充辅导员要钱怎么办？"
if input_text:
    query = input_text

if query:
    st.divider()
    st.write(f"用户：{query}")
    try:
        reply = get_ai_response(query, SYSTEM_PROMPT)
        st.write(f"小航助手：{reply}")
    except Exception as e:
        st.error(f"请求失败：{str(e)}")

st.divider()
st.markdown("## 📞 电话黄页")
st.caption("AI答不上来时，可以直接查这里")
data = [
    ["校园110（保卫处24h)", "0371‑61916110"],
    ["学校总值班室", "0371‑61911000"],
    ["后勤管理处", "0371‑61912800"],
    ["后勤服务热线/物业报修", "0371‑61913110"]
]
st.table(data)

if __name__ == "__main__":
    pass