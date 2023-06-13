from playwright.sync_api import sync_playwright, TimeoutError

def run(playwright):
    try:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        page.goto('https://www.jobmaster.co.il/')
        page.wait_for_load_state()

        page.click('a.TransitionQuick.TopSargelWhiteItem.TopIconMe')
        page.wait_for_load_state()

        page.fill('#email', 'your_email@example.com')
        page.fill('#password', 'your_password')

        page.click('input[type="submit"][value="התחברות"]')
        page.wait_for_load_state()

        page.click('div.SargelSlider a.isSubscribe')
        page.wait_for_load_state()

        job_articles = page.query_selector_all('article.JobItem')
        successful_applications = 0
        if not job_articles:
            print("No jobs to apply!")
            browser.close()
            return

        for article in job_articles:
            try:
                job_item_right = article.query_selector('div.JobItemRight')
                if job_item_right and 'DevOps' in job_item_right.inner_text():
                    article.click(timeout=5000)  # Increase the timeout value to 5 seconds
                    page.wait_for_selector('div#enterJob')
                    applied_buttons = page.query_selector_all('div#enterJob div.jobHead__actionBtn__jobContact input.bttn[value="הגש מועמדות"]')
                    if applied_buttons:
                        continue
                    page.click('div#enterJob div.jobHead__actionBtn__jobContact input.bttn', timeout=5000)  # Increase the timeout value to 5 seconds
                    page.wait_for_selector('div#modal_window')
                    save_button = page.query_selector('div#modal_window form.CustomCheck div#buttons input.SaveButton')
                    if save_button:
                        save_button.click()
                        successful_applications += 1
                    page.wait_for_timeout(1000)
            except TimeoutError as e:
                print(f"Timeout error occurred during job application: {str(e)}")
            except Exception as e:
                print(f"Error occurred during job application: {str(e)}")

        card_headers = page.query_selector_all('a.CardHeader')
        for card_header in card_headers:
            card_header_text = card_header.inner_text()
            if 'DevOps' not in card_header_text:
                try:
                    card_header.click()
                    page.wait_for_selector('span.bottomItems.bottomItemsDelete')
                    delete_element = page.query_selector('span.bottomItems.bottomItemsDelete')
                    if delete_element:
                        delete_element.click()
                    page.wait_for_selector('i.fa-light.fa-trash')
                    trash_icon_elements = page.query_selector_all('i.fa-light.fa-trash')
                    for trash_icon in trash_icon_elements:
                        trash_icon.click()
                except TimeoutError as e:
                    print(f"Timeout error occurred during job deletion: {str(e)}")
                except Exception as e:
                    print(f"Error occurred during job deletion: {str(e)}")

        print(f"Successful applications: {successful_applications}")

        browser.close()
    except TimeoutError as e:
        print(f"Timeout error occurred: {str(e)}")
    except Exception as e:
        print(f"Error occurred: {str(e)}")

with sync_playwright() as playwright:
    run(playwright)
