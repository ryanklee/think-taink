import pytest
from flask import url_for
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def driver():
    driver = webdriver.Firefox()  # or webdriver.Chrome()
    yield driver
    driver.quit()

def test_home_page(client):
    response = client.get(url_for('main.index'))
    assert response.status_code == 200
    assert b"Multi-LLM Think Tank Simulation" in response.data

def test_ask_question_form(driver, live_server):
    driver.get(url_for('main.ask_question', _external=True))
    question_input = driver.find_element(By.NAME, "question")
    api_select = driver.find_element(By.NAME, "api_type")
    submit_button = driver.find_element(By.ID, "submit")
    
    assert question_input.is_displayed()
    assert api_select.is_displayed()
    assert submit_button.is_displayed()

def test_question_submission(driver, live_server):
    driver.get(url_for('main.ask_question', _external=True))
    question_input = driver.find_element(By.NAME, "question")
    api_select = driver.find_element(By.NAME, "api_type")
    submit_button = driver.find_element(By.ID, "submit")
    
    question_input.send_keys("What is the capital of France?")
    api_select.send_keys("openai")
    submit_button.click()
    
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "response"))
    )
    
    response_element = driver.find_element(By.ID, "response")
    assert "Paris" in response_element.text

# Add more tests as needed
