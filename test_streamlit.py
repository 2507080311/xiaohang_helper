import streamlit as st

st.title("Streamlit 交互体验")

name = st.text_input("你的名字：")
grade = st.selectbox("你的年级：", ["大一", "大二", "大三", "大四"])

if st.button("打招呼"):
    if name:
        st.success(f"你好，{name}！你是{grade}学生。")
    else:
        st.warning("请输入名字")