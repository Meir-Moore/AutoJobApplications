from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto('https://www.jobmaster.co.il/')
    page.wait_for_load_state()

    page.click('a.TransitionQuick.TopSargelWhiteItem.TopIconMe')
    page.wait_for_load_state()

    page.fill('#email', 'email')
    page.fill('#password', 'password')

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

    card_headers = page.query_selector_all('a.CardHeader')
    for card_header in card_headers:
        if 'DevOps' not in card_header.inner_text():
            card_header.click()
            page.wait_for_selector('span.bottomItems.bottomItemsDelete')
            delete_element = page.query_selector('span.bottomItems.bottomItemsDelete')
            if delete_element:
                delete_element.click()
            page.wait_for_selector('i.fa-light.fa-trash')
            trash_icon_elements = page.query_selector_all('i.fa-light.fa-trash')
            for trash_icon in trash_icon_elements:
                trash_icon.click()

    print(f"Successful applications: {successful_applications}")

    browser.close()

with sync_playwright() as playwright:
    run(playwright)
