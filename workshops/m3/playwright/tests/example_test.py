import re
from playwright.sync_api import Page, expect

def test_has_title(page: Page):
    page.goto("https://playwright.dev/")

    # Expect a title "to contain" a substring.
    expect(page).to_have_title(re.compile("Playwright"))

def test_get_started_link(page: Page):
    page.goto("https://playwright.dev/")

    # Click the get started link.
    page.get_by_role("link", name="Get started").click()

    # Expects page to have a heading with the name of Installation.
    expect(page.get_by_role("heading", name="Installation")).to_be_visible()

def test_example(page: Page) -> None:
    page.goto("https://demo.playwright.dev/todomvc/")

    page.get_by_placeholder("What needs to be done?").click()

    page.get_by_placeholder("What needs to be done?").fill("Take the trash out")
    page.get_by_placeholder("What needs to be done?").press("Enter")

    page.get_by_placeholder("What needs to be done?").fill("Do the dishes")
    page.get_by_placeholder("What needs to be done?").press("Enter")

    expect(page.get_by_text("Take the trash out")).to_be_visible()
    expect(page.get_by_text("Do the dishes")).to_be_visible()

    page.locator("li").filter(has_text="Take the trash out").get_by_label("Toggle Todo").check()

    page.get_by_role("button", name="Delete").click()

    expect(page.get_by_test_id("todo-title")).to_be_visible()
