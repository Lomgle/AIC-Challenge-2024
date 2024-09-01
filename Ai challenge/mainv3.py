import streamlit as st
import scrape_fiftyone as sfo
import fiftyone as fo
import time
from side_functions import (
    display_images,
    progress_feedback,
    load_css,
)

# Chỉnh web///////////////////////////////////////////////////////////////////////////////////
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
load_css("style.css")

# Header + subheader/////////////////////////////////////////////////////////////////////////
st.header("colgate MaxFresh", anchor=False)
st.subheader("- presents -", anchor=False)
st.divider()

# Yes////////////////////////////////////////////////////////////////////////////////////////
progress = st.empty()
dataset_list = []
if "received_images" not in st.session_state:
    st.session_state.received_images = None
if "dataset_list" not in st.session_state:
    st.session_state.dataset_list = []


# Sidebar///////////////////////////////////////////////////////////////////////////////////////
st.sidebar.markdown('<h1 class="font">⚙Cài Đặt</h1>', unsafe_allow_html=True)

with st.sidebar.expander("Số lượng ảnh tìm kiếm"):
    num_pic = st.slider(
        label="skibidi", label_visibility="hidden", min_value=1, max_value=150, value=15
    )

with st.sidebar.expander("Thời gian Timeout"):
    timeout = st.slider(
        label="skibidi",
        label_visibility="hidden",
        min_value=10,
        max_value=240,
        value=30,
    )

with st.sidebar.expander("Dataset"):
    dts1, dts2 = st.columns([5.5, 1])
    display_dataset_info = st.empty()
    with dts1:
        dataset_name_input = st.text_input(
            "Nhập tên dataset qua Fiftyone",
            placeholder="Chỉ hỗ trợ Fiftyone",
        )
    with dts2:
        confirm = st.button("→", use_container_width=True)
        if confirm:
            try:
                if dataset_name_input in st.session_state.dataset_list:
                    raise ValueError
                with display_dataset_info:
                    start = time.time()
                    dataset = fo.load_dataset(dataset_name_input)
                    st.write(f"Đã hoàn tất trong {(time.time() - start):5.3f}s!")
                    st.session_state.dataset_list.append(dataset_name_input)
            except fo.DatasetNotFoundError:
                with display_dataset_info:
                    st.error(
                        f"Không thể tải dataset: không tìm thấy dataset '{dataset_name_input}!'"
                    )
            except ValueError:
                with display_dataset_info:
                    st.error(f"Trùng dataset: '{dataset_name_input}' đã được tải!")

    dataset_choice = st.selectbox(
        "Dataset được sử dụng: ",
        options=st.session_state.dataset_list,
        placeholder="Hãy chọn dataset",
    )

with st.sidebar:
    reset = st.button(
        "RESET (chx sài đc)",
        help="Reset cài đặt (bao gồm cả dataset được tải) và đưa về mặc định",
        use_container_width=True,
    )

# Nội dung chính //////////////////////////////////////////////////////////////////////////////
col1, col2 = st.columns([6, 1])

with col1:
    video_desc_input = st.text_input(
        label="skibidi",
        placeholder="Mô tả video cần tìm bằng tiếng Anh",
        label_visibility="hidden",
    )

with col2:
    search_button = st.button(
        "Tìm!", key="search", help="Bấm vào đây để tìm", use_container_width=True
    )

    if search_button and video_desc_input:
        progress_feedback(progress, "Đang khởi chạy web. . .")
        num_pic = num_pic or 15
        st.session_state.received_images = sfo.run_fiftyone(
            video_desc=video_desc_input,
            progress=progress,
            number_of_picture=num_pic,
            timeout=timeout,
            dataset_name=dataset_choice,  # 2024.08.31.11.07.00    "2024.08.20.00.49.43"
        )
        progress_feedback(progress, "Hoàn tất! . . .")

try:
    display_images(received_images=st.session_state.received_images, num_columns=3)
except Exception:
    pass
progress.empty()
