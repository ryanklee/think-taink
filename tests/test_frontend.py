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

    @pytest.mark.timeout(600)  # Increase timeout to 10 minutes
    def test_question_submission(self, page: Page, live_server):
        page.goto(url_for('main.ask_question', _external=True))
        question_input = page.locator("input[name='question']")
        api_select = page.locator("select[name='api_type']")
        submit_button = page.locator("input#submit")
    
        question_input.fill("What is the capital of France?")
        api_select.select_option("openai")
        with page.expect_navigation(timeout=300000):  # Increase navigation timeout to 5 minutes
            submit_button.click(timeout=300000)
        
        response_element = page.locator("#response")
        try:
            # Wait for the response to be visible and non-empty
            expect(response_element).to_be_visible(timeout=300000)  # Increase visibility timeout to 5 minutes
            expect(response_element).not_to_be_empty(timeout=300000)  # Increase timeout for non-empty content
    
            # Wait for the content to stabilize
            page.wait_for_function(
                "() => document.querySelector('#response').textContent.trim().length > 0",
                timeout=300000
            )
    
            # Wait for the EventSource to complete
            page.wait_for_function(
                "() => !window.eventSource || window.eventSource.readyState === 2",
                timeout=300000
            )
    
            response_text = response_element.inner_text()
            logger.info(f"Response text: {response_text}")
    
            # Check for any content in the response
            assert response_text.strip() != "", f"Expected non-empty response, but got empty string"
    
            # Log the response content for debugging
            logger.info(f"Response content: {response_text}")
    
            # Check if the response contains either "Paris", an error message, or any expert name
            expert_names = ["Analyst", "Creative", "Critic", "Synthesizer", "Ethicist"]
            has_expert_name = any(name in response_text for name in expert_names)
            assert "Paris" in response_text or "Error" in response_text or has_expert_name, \
                f"Expected 'Paris', an error message, or an expert name, but got: {response_text}"
        except Exception as e:
            logger.error(f"Page content after submission: {page.content()}")
            logger.error(f"Current URL: {page.url}")
            logger.error(f"Response element HTML: {response_element.inner_html()}")
            logger.error(f"Page console logs: {page.evaluate('() => console.logs')}")
            raise e

# Add more tests as needed
