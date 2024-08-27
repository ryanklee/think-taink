import pytest
from playwright.sync_api import Page, expect
from flask import url_for
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

import pytest
from playwright.sync_api import Page, expect
from flask import url_for

@pytest.mark.usefixtures("live_server")
class TestFrontend:
    def test_home_page(self, page: Page, live_server):
        page.goto(url_for('main.index', _external=True))
        expect(page).to_have_title("Multi-LLM Think Tank Simulation")
        expect(page.locator("body")).to_contain_text("Multi-LLM Think Tank Simulation")

    def test_ask_question_form(self, page: Page, live_server):
        page.goto(url_for('main.ask_question', _external=True))
        page.wait_for_load_state('networkidle')
        question_input = page.locator("input[name='question']")
        api_select = page.locator("select[name='api_type']")
        submit_button = page.locator("input[type='submit']")

        if not submit_button.is_visible():
            logger.error(f"Page content: {page.content()}")
            logger.error(f"All input elements: {page.eval_on_selector_all('input', 'elements => elements.map(e => e.outerHTML)')}")
        expect(question_input).to_be_visible(timeout=10000)
        expect(api_select).to_be_visible(timeout=10000)
        expect(submit_button).to_be_visible(timeout=10000)

    @pytest.mark.timeout(180)  # Increase timeout to 3 minutes
    def test_question_submission(self, page: Page, live_server):
        page.goto(url_for('main.ask_question', _external=True))
        question_input = page.locator("input[name='question']")
        api_select = page.locator("select[name='api_type']")
        submit_button = page.locator("input#submit")

        question_input.fill("What is the capital of France?")
        api_select.select_option("openai")
        with page.expect_navigation(timeout=90000):  # Increase navigation timeout
            submit_button.click(timeout=90000)
        page.wait_for_timeout(5000)  # Increase wait time after navigation

        response_element = page.locator("#response")
        try:
            expect(response_element).to_be_visible(timeout=60000)  # Increase visibility timeout
            expect(response_element).not_to_be_empty(timeout=60000)  # Add check for non-empty content
            
            # Check for error message
            error_message = page.locator("text=Error:")
            if error_message.is_visible():
                error_text = error_message.inner_text()
                logger.error(f"Error message found: {error_text}")
                raise AssertionError(f"Error occurred: {error_text}")
            
            expect(response_element).to_contain_text("Paris", timeout=30000)
        except Exception as e:
            logger.error(f"Page content after submission: {page.content()}")
            logger.error(f"Current URL: {page.url}")
            logger.error(f"Response element HTML: {response_element.inner_html()}")
            logger.error(f"Page console logs: {page.evaluate('() => console.logs')}")
            raise e

# Add more tests as needed
