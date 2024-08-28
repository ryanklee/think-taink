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
    def test_home_page(self, page: Page, live_server_url):
        page.goto(f"{live_server_url}/")
        expect(page).to_have_title("Multi-LLM Think Tank Simulation")
        expect(page.locator("body")).to_contain_text("Multi-LLM Think Tank Simulation")

    def test_ask_question_form(self, page: Page, live_server_url):
        page.goto(f"{live_server_url}/ask")
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

    def test_question_submission(self, page: Page, live_server_url):
        page.goto(f"{live_server_url}/ask")
        question_input = page.locator("input[name='question']")
        api_select = page.locator("select[name='api_type']")
        submit_button = page.locator("input#submit")

        question_input.fill("Test question")
        api_select.select_option("openai")
        submit_button.click()

        response_element = page.locator("#response")
        try:
            # Wait for the page to load
            page.wait_for_load_state("networkidle")
            logger.info("Page loaded")
            
            # Log the initial page state
            logger.info(f"Initial page content: {page.content()}")
            
            # Wait for the EventSource to be established with an increased timeout
            page.wait_for_function(
                "() => window.eventSource && window.eventSource.readyState === 1",
                timeout=60000
            )
            logger.info("EventSource established")

            # Wait for the response element to be visible
            expect(response_element).to_be_visible(timeout=60000)
            logger.info("Response element is visible")

            # Wait for some content to appear in the response element
            page.wait_for_function(
                "() => document.querySelector('#response').textContent.trim().length > 0",
                timeout=60000
            )
            logger.info("Content appeared in the response element")

            # Get the final response text
            response_text = response_element.inner_text()
            logger.info(f"Response text: {response_text}")

            # Check for non-empty response
            assert response_text.strip() != "", "Expected non-empty response, but got empty string"

            # Check if the response contains expected content
            expected_content = ["Test", "question", "response"]
            assert any(content in response_text for content in expected_content), \
                f"Expected content not found in response: {response_text}"

        except Exception as e:
            logger.error(f"Test failed: {str(e)}")
            logger.error(f"Page content: {page.content()}")
            logger.error(f"Current URL: {page.url}")
            logger.error(f"Response element HTML: {response_element.inner_html()}")
            logger.error(f"Page console logs: {page.evaluate('() => console.logs')}")
            raise e

# Add more tests as needed
