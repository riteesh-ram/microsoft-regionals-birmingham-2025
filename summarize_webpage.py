import os
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from openai import AzureOpenAI
import pickle

# Load environment variables
load_dotenv()

# Azure OpenAI setup
ENDPOINT_URL = os.environ.get("ms_hackathon_endpoint")
API_KEY = os.environ.get("ms_hackathon_api")
API_VERSION = "2024-02-01"
MODEL_NAME = "gpt-4"

client = AzureOpenAI(
    azure_endpoint=ENDPOINT_URL,
    api_key=API_KEY,
    api_version=API_VERSION,
)

def clean_html(html_content):
    """Clean HTML by removing unnecessary scripts/styles."""
    soup = BeautifulSoup(html_content, "html.parser")

    # Remove script and style elements
    for tag in soup(["script", "style"]):
        tag.decompose()

    return soup.get_text(separator=" ", strip=True)

def get_form_description_from_page(full_page_text):
    """Ask Azure OpenAI to summarize what the form(s) on the page are about."""
    
    response_word_limit = 20

    system_message = f"""You are an AI assistant. Summarize the html page sent to you which contains a form related
    to Birmingham City Council. You response should be short and should describe what the form is about so that
    a potential user of this form can understand what it's about using this description. Keep the response to less than {response_word_limit} words."""

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": full_page_text},
    ]

    completion = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
    )

    return completion.choices[0].message.content.strip()

def process_forms_in_folder(folder_path):
    """Read HTML files from a folder, summarize form descriptions via LLM.
    Returns a list of tuples: (id, link, description)
    """
    form_descriptions = []

    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(".html"):
                full_path = os.path.join(root, file)
                parent_folder = os.path.basename(os.path.dirname(full_path))

                with open(full_path, "r", encoding="utf-8") as f:
                    html_content = f.read()

                cleaned_text = clean_html(html_content)
                description = get_form_description_from_page(cleaned_text)

                form_descriptions.append((parent_folder, full_path, description))

    return form_descriptions


def webpage_summary(forms_folder_path=None, fresh=False):
    """
    Summarize the webpage content and return in the following form:
    (id, link, description), where:
    • id is the name of the parent folder of the HTML file.
    • link is the full path to the HTML file.
    • description is the LLM-generated summary of the form/page.
    """
    if forms_folder_path is None:
        forms_folder_path = os.path.join(os.getcwd(), "forms")

    # Define path for the cached results
    cache_path = os.path.join(forms_folder_path, "summary_results.pkl")

    # Check if cached file exists and fresh is False
    if not fresh and os.path.exists(cache_path):
        with open(cache_path, "rb") as f:
            results = pickle.load(f)
    else:
        results = process_forms_in_folder(forms_folder_path)
        with open(cache_path, "wb") as f:
            pickle.dump(results, f)

    return results