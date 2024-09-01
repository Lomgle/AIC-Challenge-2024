from side_functions import locate_element, progress_feedback
import time


def find_images_info(driver, progress, number_of_picture, timeout):
    received_images = {}
    try:
        for i in range(number_of_picture):
            while True:
                file_path = ""
                image_name = ""
                ptsTime_frameIdx = ""

                image_name = locate_element(
                    driver,
                    timeout,
                    "presence_of_element_located",
                    'div[data-cy="sidebar-entry-video"]',
                ).text

                file_path = locate_element(
                    driver,
                    timeout,
                    "presence_of_element_located",
                    'div[data-cy="sidebar-entry-filepath"]',
                ).text

                ptsTime_frameIdx = locate_element(
                    driver,
                    timeout,
                    "presence_of_element_located",
                    'div[data-cy="sidebar-entry-pts_time, frame_index"]',
                ).text

                if file_path and image_name and ptsTime_frameIdx:
                    break
            print(
                i + 1,
                file_path,
                "->",
                f"{image_name}, {ptsTime_frameIdx}",
                end="\n",
            )

            received_images[file_path] = (image_name, ptsTime_frameIdx)

            progress_feedback(
                progress, f"Đang tải ảnh ({i + 1}/{number_of_picture}). . ."
            )

            next_button = locate_element(
                driver,
                2,
                "element_to_be_clickable",
                'svg[data-cy="nav-right-button"]',
            )
            next_button.click()
            time.sleep(0.25)
    except:
        print("Done!")
        pass

    return received_images
