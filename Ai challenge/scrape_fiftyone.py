from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import inspect_images
from side_functions import locate_element, progress_feedback


def run_fiftyone(video_desc, progress, number_of_picture, timeout, dataset_name):
    options = webdriver.EdgeOptions()
    options.add_argument("headless")

    driver = webdriver.Edge()
    driver.get("http://localhost:5151/datasets/" + dataset_name)

    # Nhan nut tim kiem
    reveal_button = locate_element(
        driver,
        60,
        "element_to_be_clickable",
        'div[data-cy="action-sort-by-similarity"]',
    )
    reveal_button.click()

    progress_feedback(progress, "Đang đưa dữ liệu vào ô tìm kiếm. . .")

    # Paste du lieu vao o tim kiem
    search_box = locate_element(
        driver,
        timeout,
        "visibility_of_element_located",
        'input[placeholder="Type anything!"][data-cy="input-Type anything!"]',
    )
    search_box.send_keys(video_desc)

    # bam vao phan cai dat cua tim kiem
    config_button = locate_element(
        driver,
        timeout,
        "element_to_be_clickable",
        'button[arial-label="Advanced settings"]',
    )
    config_button.click()

    # input so luong anh can tim
    quantity_input = locate_element(
        driver,
        timeout,
        "visibility_of_element_located",
        'input[placeholder="k"][data-cy="input-k"]',
    )
    quantity_input.clear()
    quantity_input.send_keys(number_of_picture)

    search_box.send_keys(Keys.RETURN)

    # Cai nay de lam j v?!?!
    WebDriverWait(driver, timeout).until(
        EC.staleness_of(
            driver.find_element(
                By.CSS_SELECTOR,
                'div[data-cy="looker"][title="Click to expand"]',
            )
        )
    )
    # Bam vao hinh dau tien cua ket qua tim kiem
    image_click = locate_element(
        driver,
        timeout,
        "element_to_be_clickable",
        'div[data-cy="looker"][title="Click to expand"]',
    )
    image_click.click()

    received_images = inspect_images.find_images_info(
        driver, progress, number_of_picture, timeout
    )

    return received_images
