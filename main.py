from bs4 import BeautifulSoup
import requests
import os
import json
from dotenv import load_dotenv
from openai import AzureOpenAI
from query_similarity import search_from_query
from scraper import scrape_form_inputs
from text2speech import generate_conversational_response
from stt import record_audio, transcribe_audio

load_dotenv()

ENDPOINT_URL = os.environ.get("ENDPOINT_URL")
API_KEY = os.environ.get("API_KEY")
API_VERSION = "2023-09-01-preview"
DEPLOYMENT_NAME = "gpt-4o"

def prompt_form_intro(field_lookup):
    prompt = (
        "we are about to help the user fill in a form using speech-to-text. "
        "here is a dictionary of field names to human-readable labels:\n"
        f"{json.dumps(field_lookup, indent=2)}\n\n"
        "generate a short, friendly message that lists the fields and tells the user we're going to start filling them one by one."
    )

    response = client.chat.completions.create(
        model=DEPLOYMENT_NAME,
        messages=[
            {"role": "system", "content": "you are a helpful assistant guiding users through filling out a form."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

# stub: fill in the form via speech
# helper: submit the form and return status + feedback
def submit_form(url, data):
    res = requests.post(url, data=data)
    soup = BeautifulSoup(res.text, "html.parser")

    # check for success message in body
    success = soup.find(string=lambda s: s and "success" in s.lower())
    if success:
        return True, success.strip()

    # else: parse the form again and see which fields are still empty
    remaining = []
    for tag in soup.find_all(["input", "textarea", "select"]):
        name = tag.get("name")
        value = tag.get("value", "")
        if name and not value:  # empty field means user input didn't stick
            remaining.append(name)

    return False, remaining

# updated fill_form_via_speech with submission flow
def fill_form_via_speech(form_id):
    form_id = form_id[:-5]
    url = f"http://127.0.0.1:5000/{form_id}"
    print(f"[speech form filling] loading form at: {url}")
    #
    inputs = scrape_form_inputs(url)
    if not inputs:
        print("no form inputs found on page.")
        return
    #
    responses = {}
    field_lookup = {field["name"]: field["label"] for field in inputs}
    intro = prompt_form_intro(field_lookup)
    print(intro)

    record_audio()
    print(transcribe_audio())
    



    #
    # while True:
    #     print("\n🗣️ starting input...\n")
    #
    #     for name in field_lookup:
    #         if name not in responses:
    #             label = field_lookup[name]
    #             print(f"🗣️ please provide input for: {label}")
    #             value = simulate_speech_input(label)
    #             responses[name] = value
    #
    #     # submit attempt
    #     print("\n⏳ submitting form...")
    #     success, result = submit_form(url, responses)
    #
    #     if success:
    #         print(f"\n✅ success: {result}")
    #         break
    #     else:
    #         print("\n⚠️ form validation error — please re-enter the following:")
    #         for name in result:
    #             if name in field_lookup:
    #                 print(f"- {field_lookup[name]}")
    #                 responses.pop(name, None)

def simulate_speech_input(prompt):
    return input(f"(you say): ")

# stub: manual fill
def fill_form_manually(form_id):
    form_id=form_id[:-5]
    print(f"Here is the link to fill in the form manually: http://127.0.0.1:5000/{form_id}")
    # simulate form field inputs manually
    pass

# define available functions
functions = [
    {
        "name": "search_form_index",
        "description": "search the government form index based on user input",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "the user input that describes the form they are looking for",
                },
            },
            "required": ["query"],
        },
    }
]

# init client
client = AzureOpenAI(
    azure_endpoint=ENDPOINT_URL,
    api_key=API_KEY,
    api_version=API_VERSION,
)

# start interaction
messages = [
    {
        "role": "system",
        "content": (
            "you are helping a user find and fill out a government form. "
            "always start by asking what the form is about. "
            "after finding matching forms, ask if they want to fill it manually or with speech-to-text."
        ),
    },
    # {"role": "user", "content": "i need help with renewing my passport"},
]

def parse_form_result(result_str):
    lines = result_str.split("\n")
    id_ = link = desc = ""
    for line in lines:
        if "id:" in line:
            id_ = line.split("id:")[1].strip().strip(",")
        elif "link:" in line:
            raw_link = line.split("link:")[1].strip().strip(",")
            try:
                parsed = eval(raw_link)
                link = parsed[1] if isinstance(parsed, list) else parsed
            except Exception:
                link = raw_link
        elif "description:" in line:
            desc = line.split("description:")[1].strip()
    return {"id": id_, "link": link, "description": desc}

# first model call
while True:
    completion = client.chat.completions.create(
        model=DEPLOYMENT_NAME,
        messages=messages,
        functions=functions,
    )

    choice = completion.choices[0]

    if choice.finish_reason == "function_call":
        func_call = choice.message.function_call
        func_name = func_call.name
        args = json.loads(func_call.arguments)

        if func_name == "search_form_index":
            raw_results = search_from_query(**args)
            parsed_results = [parse_form_result(r) for r in raw_results]

            print("\nfound matching forms:\n")
            for i, r in enumerate(parsed_results):
                print(f"{i+1}. id: {r['id']}")
                print(f"   link: {r['link']}")
                print(f"   desc: {r['description']}\n")

            selected_index = int(input("pick a form number: ")) - 1
            selected_form = parsed_results[selected_index]
            print(f"\nyou selected: {selected_form['id']}")

            method = input("type 'm' to fill manually or 's' for speech-to-text: ").strip().lower()
            if method == "s":
                fill_form_via_speech(selected_form["link"])
            else:
                fill_form_manually(selected_form["link"])
            break
        else:
            print("unknown function requested:", func_name)
            break

    else:
        reply = choice.message.content
        print(reply)
        user_input = input("> ")
        messages.append({"role": "assistant", "content": reply})
        messages.append({"role": "user", "content": user_input})
