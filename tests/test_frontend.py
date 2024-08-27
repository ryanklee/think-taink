import pytest
from playwright.sync_api import Page, expect
from flask import url_for

@pytest.mark.usefixtures("live_server")
class TestFrontend:
    def test_home_page(self, page: Page, live_server):
        page.goto(f"http://localhost:{live_server.client.application.config['PORT']}")
        expect(page).to_have_title("Multi-LLM Think Tank Simulation")
        expect(page.locator("body")).to_contain_text("Multi-LLM Think Tank Simulation")

    def test_ask_question_form(self, page: Page, live_server):
        page.goto(f"http://localhost:{live_server.client.application.config['PORT']}/ask")
        question_input = page.locator("input[name='question']")
        api_select = page.locator("select[name='api_type']")
        submit_button = page.locator("button#submit")

        expect(question_input).to_be_visible()
        expect(api_select).to_be_visible()
        expect(submit_button).to_be_visible()

    def test_question_submission(self, page: Page, live_server):
        page.goto(f"http://localhost:{live_server.client.application.config['PORT']}/ask")
        question_input = page.locator("input[name='question']")
        api_select = page.locator("select[name='api_type']")
        submit_button = page.locator("button#submit")

        question_input.fill("What is the capital of France?")
        api_select.select_option("openai")
        submit_button.click()

        response_element = page.locator("#response")
        expect(response_element).to_be_visible()
        expect(response_element).to_contain_text("Paris")

# Add more tests as needed
