import streamlit as st
import requests
import time
from pathlib import Path
from prompts import load_school_info, get_system_prompt, PRESET_QUESTIONS
from api import get_ai_answer

# 页面基础配置
st.set_page_config(page_title="小航 · 郑州航院校园信息助手")
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
# 全局统计提问次数
if "ask_count" not in st.session_state:
    st.session_state.ask_count = 0
# 临时存储本次问答，仅当前页面渲染使用
if "temp_chat" not in st.session_state:
    st.session_state.temp_chat = None
if "input_question" not in st.session_state:
    st.session_state["input_question"] = ""
st.title("小航 · 郑州航院校园信息助手")

# 1. 身份选择下拉框
role = st.selectbox("你是？", ["新生", "在校生", "教师"])

# 2. 预设推荐问题按钮（12个按身份切换）
st.markdown("### 试试这些问题：")
# 创建3个分类标签页
tab1, tab2, tab3 = st.tabs(["新生指南", "办事流程", "应急防骗"])

# 标签1：新生指南
with tab1:
    new_questions = ["报到那天先去哪?", "学费什么时候交?", "宿舍几间?", "军训准备啥?"]
    cols = st.columns(2)
    for i, q in enumerate(new_questions):
        with cols[i % 2]:
            if st.button(q, key=f"new_{i}"):
                st.session_state["input_question"] = q
                st.rerun()

# 标签2：办事流程
with tab2:
    process_questions = ["怎么开具在读证明", "校园卡丢失如何补办", "转专业申请条件是什么", "怎么申请助学金"]
    cols = st.columns(2)
    for i, q in enumerate(process_questions):
        with cols[i % 2]:
            if st.button(q, key=f"proc_{i}"):
                st.session_state["input_question"] = q
                st.rerun()

# 标签3：应急防骗
with tab3:
    safe_questions = ["遇到电信诈骗怎么办", "兼职刷单可信吗", "陌生人索要验证码要不要给", "校园贷的危害是什么"]
    cols = st.columns(2)
    for i, q in enumerate(safe_questions):
        with cols[i % 2]:
            if st.button(q, key=f"safe_{i}"):
                st.session_state["input_question"] = q
                st.rerun()

# 3. 文本输入框
user_input = st.text_input("有啥想问的？", value=st.session_state["input_question"])
query = user_input.strip()

# 4. AI问答核心逻辑
if query:
    st.divider()
    start_time = time.time()
    # 加载状态动画
    with st.spinner("AI正读取知识库并生成回答，请稍候..."):
        # 检测data知识库是否缺失
        md_file_list = list(Path("data").glob("*.md"))
        if not md_file_list:
            st.warning("数据文件缺失，请补齐data目录下的4个md文件")
        else:
            try:
                school_data = load_school_info()
                sys_prompt = get_system_prompt(role, school_data)
                response = get_ai_answer(sys_prompt, query)
                if response.status_code == 401:
                    st.error("API Key 失效，请联系老师重新获取密钥")
                elif response.status_code != 200:
                    st.error(f"API接口异常，状态码：{response.status_code}")
                else:
                    res_json = response.json()
                    try:
                        reply = res_json["choices"][0]["message"]["content"]
                        # 统计耗时、提问次数
                        use_time = round(time.time() - start_time, 2)
                        st.session_state.ask_count += 1
                        # 展示问答信息
                        st.write(f"用户：{query}")
                        st.write(f"小航：{reply}")
                        st.info(f"本次问答耗时：{use_time}秒 | 累计提问次数：{st.session_state.ask_count}")
                        st.session_state.temp_chat = {"user": query, "robot": reply}
                        st.session_state.chat_history.append(st.session_state.temp_chat)
                    except (KeyError, IndexError):
                        st.error("AI返回数据格式异常，请重新提问")
            except requests.exceptions.Timeout:
                st.error("AI响应超时，请稍后再试")
            except requests.exceptions.ConnectionError:
                st.error("网络连接失败，请检查网络")
            except Exception as err:
                st.error(f"程序运行出错：{str(err)}")
elif user_input is not None and query == "":
    st.info("请输入你的问题再提问")

# 清空历史对话按钮（同步清零提问计数）
if st.button("清空历史对话", type="secondary"):
    st.session_state.chat_history = []
    st.session_state.temp_chat = None
    st.session_state.ask_count = 0
    st.rerun()

# 5. 历史问答：只展示刷新前的旧记录，不包含刚发送的当前问题
st.subheader("历史问答")
for item in st.session_state.chat_history:
    if item == st.session_state.temp_chat:
        continue
    st.write(f"用户：{item['user']}")
    st.write(f"小航：{item['robot']}")
    st.divider()

# 6. 静态电话黄页
st.divider()
st.header("📞 电话黄页")
st.caption("AI答不上来时，可以直接查这里")
yellow_page_markdown = """
| 部门 | 联系电话 |
|------|------|
| 校园110(保卫处24h) | 0371-61916110  |
| 学校总值班室 | 0371-61911000  |
| 后勤管理处 | 0371-61912800  |
| 后勤服务热线/物业报修 | 0371-61913110 |
| 校医院急诊(24h) | 0371-61912730  |
| 招生办公室 | 0371-61916161  |
| 信息管理中心(网信中心) | 0371-61912718  |
"""
st.markdown(yellow_page_markdown)