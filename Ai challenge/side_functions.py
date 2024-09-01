from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import streamlit as st


def locate_element(
    driver, timeout, search_attr, filter_data
):  # tim element trong web fiftyone
    converted_search_attr = getattr(EC, search_attr)
    found_element = WebDriverWait(driver, timeout=timeout).until(
        converted_search_attr((By.CSS_SELECTOR, filter_data))
    )
    return found_element


def display_images(received_images, num_columns=2):  # hien thi hinh anh
    columns = st.columns(num_columns)

    for index, image_path in enumerate(received_images):
        with columns[index % num_columns]:
            image_name_ptfi = received_images[
                image_path
            ]  # ptfi co nghia la ptsTime & frameIndex
            st.image(
                image_path,
                use_column_width=True,
                caption=f"{image_name_ptfi[0]} \n {image_name_ptfi[1]}",
            )


def progress_feedback(progress_variable, progress_text):  # thong bao tien trinh
    progress_variable.empty()
    with progress_variable.container():
        st.write(progress_text)


def load_css(file_name):  # doc file css
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
