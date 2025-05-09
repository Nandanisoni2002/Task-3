from flask import Flask, request, render_template
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = ""
    if request.method == 'POST':
        url = request.form['url']
        try:
            result += f"[+] Scanning: {url}\n\n"

            # Headers
            response = requests.get(url)
            result += "[+] HTTP Headers:\n"
            for h in response.headers:
                result += f"{h}: {response.headers[h]}\n"

            # XSS Test
            xss_payload = "<script>alert('xss')</script>"
            xss_test = requests.get(url + f"?q={xss_payload}")
            if xss_payload in xss_test.text:
                result += "\n[!] XSS Vulnerability Detected!\n"
            else:
                result += "\n[-] No XSS Found.\n"

            # SQLi Test
            sqli_payload = "' OR '1'='1"
            sqli_test = requests.get(url + f"?id={sqli_payload}")
            if "sql" in sqli_test.text.lower() or "syntax" in sqli_test.text.lower():
                result += "[!] SQL Injection Detected!\n"
            else:
                result += "[-] No SQLi Found.\n"

            result += "\n[✔] Scan Completed."
        except Exception as e:
            result = f"[X] Error: {str(e)}"

    return render_template("index.html", result=result)

if __name__ == '__main__':
    app.run(debug=True)
