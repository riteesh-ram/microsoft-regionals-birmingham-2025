import requests
from bs4 import BeautifulSoup


# helper: fetch + parse form inputs from html
def scrape_form_inputs(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    inputs = []

    # grab input fields
    for tag in soup.find_all(["input", "textarea", "select"]):
        name = tag.get("name")
        input_type = tag.get("type", "text")
        if name:
            inputs.append({
                "name": name,
                "type": input_type,
                "label": get_label_for_input(soup, tag),
            })

    return inputs

# helper: try to find associated label for an input
def get_label_for_input(soup, input_tag):
    label = None

    # check if there's a <label for="">
    input_id = input_tag.get("id")
    if input_id:
        label_tag = soup.find("label", attrs={"for": input_id})
        if label_tag:
            label = label_tag.text.strip()

    # fallback: use name or placeholder
    if not label:
        label = input_tag.get("placeholder") or input_tag.get("name")

    return label

# stub to simulate speech-to-text
def simulate_speech_input(prompt):
    return input(f"(you say): ")

