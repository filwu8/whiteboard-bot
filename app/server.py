from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import requests
import re

url = "http://192.168.88.2:50008/v1/chat/completions"
api_key = "qwen3-30b-a3b"

SYSTEM_PROMPT = """
Create a Mermaid diagram using the provided text description of a scenario. Your task is to translate the text into a Mermaid Live Editor format, focusing solely on the conversion without including any extraneous content. The output should be a clear and organized visual representation of the relationships or processes described in the text.
Here is an example of the expected output:

graph TB
    PersonA[Person A] -- Relationship1 --> PersonB[Person B]
    PersonC[Person C] -- Relationship2 --> PersonB
    PersonD[Person D] -- Relationship3 --> PersonB
    PersonE[Person E] -- Relationship4 --> PersonC
    PersonF[Person F] -- Relationship5 --> PersonA
    PersonG[Person G] -- Relationship6 --> PersonF

/no_think

"""

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

def create_diagram(prompt):
    payload = {
        "model": "qwen3-30b-a3b",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        "extra_body": {"chat_template_kwargs": {"enable_thinking": False}},
        "temperature": 0.2
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        raise Exception(f"API request failed: {e}")

def strip_markdown_code(text):
    match = re.search(r"```(?:\w+)?\n([\s\S]+?)\n```", text)
    return match.group(1) if match else text


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "OPTIONS, GET, POST")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(b"Hello from GET method!")

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')

        try:
            post_data_json = json.loads(post_data)
            prompt = post_data_json.get("prompt")
            if not prompt:
                raise ValueError("Missing 'prompt' field in request")

            response = create_diagram(prompt)
            response_text = strip_markdown_code(response.json()["choices"][0]["message"]["content"])

            result = {
                "generatedResponse": response_text
            }

        except Exception as e:
            result = {
                "error": str(e)
            }

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(result, indent=2).encode('utf-8'))


def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Server started on port {port}...')
    httpd.serve_forever()


if __name__ == '__main__':
    run()