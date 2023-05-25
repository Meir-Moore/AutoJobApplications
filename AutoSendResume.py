from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    # Open new page
    page = context.new_page()

    # Go to main page
    page.goto('https://www.jobmaster.co.il/')

    # Click on the login page link
    page.click('a.TransitionQuick.TopSargelWhiteItem.TopIconMe')

    # Wait for the page to load after logging in
    page.wait_for_load_state()

    # Fill in the email and password fields with your credentials
    page.fill('#email', 'email')
    page.fill('#password', 'password')

    # Click the login button
    page.click('input[type="submit"][value="התחברות"]')

    # Wait for the page to load after logging in
    page.wait_for_load_state()

    # Click on the 'isSubscribe' link inside 'SargelSlider'
    page.click('div.SargelSlider a.isSubscribe')

    # Wait for the page to load after clicking on the link
    page.wait_for_load_state()

    # Click on each job article and apply if "DevOps" keywords exist
    job_articles = page.query_selector_all('article.JobItem')
    successful_applications = 0
    if not job_articles:
        print("No jobs to apply!")
        browser.close()  # Close the browser
        return  # Terminate the program

    for article in job_articles:
        job_item_right = article.query_selector('div.JobItemRight')
        if job_item_right and 'DevOps' in job_item_right.inner_text():
            article.click()
            page.wait_for_selector('div#enterJob')
            applied_buttons = page.query_selector_all('div#enterJob div.jobHead__actionBtn__jobContact input.bttn[value="הגש שוב"]')
            if applied_buttons:
                continue  # Skip the already applied job
            page.click('div#enterJob div.jobHead__actionBtn__jobContact input.bttn')
            page.wait_for_selector('div#modal_window')
            page.wait_for_selector('div#modal_window div#buttons input.SaveButton')
            save_button = page.query_selector('div#modal_window div#buttons input.SaveButton')
            if save_button:
                save_button.click()
                successful_applications += 1
            page.wait_for_timeout(1000)  # Wait for 1 second

    # Click on each card header that does not contain "DevOps" and click on the delete elements
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

    # Print the number of successful applications
    print(f"Successful applications: {successful_applications}")

    # Close the browser
    browser.close()
    print("Browser closed.")

with sync_playwright() as playwright:
    run(playwright)
