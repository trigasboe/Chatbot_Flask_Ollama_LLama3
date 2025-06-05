from flask import Flask, render_template, request
import requests

app = Flask(__name__)
OLLAMA_URL = "http://localhost:11434/api/generate"

chat_history = []

@app.route("/", methods=["GET", "POST"])
def index():
    status = ""
    if request.method == "POST":
        question = request.form.get("question", "").strip()
        if question:
            try:
                response = requests.post(
                    OLLAMA_URL,
                    json={
                        "model": "llama3",
                        "prompt": f"Jelaskan dalam bahasa Indonesia: {question}",
                        "stream": False
                    }
                )
                data = response.json()
                answer = data.get("response", "Tidak ada jawaban.")
                chat_history.append((question, answer))
                status = "✅ Jawaban siap."
            except Exception as e:
                chat_history.append((question, f"(Kesalahan: {e})"))
                status = "❌ Gagal menjawab."
        else:
            status = "❗ Pertanyaan tidak boleh kosong."

    return render_template("index.html", history=chat_history, status=status)

# if __name__ == "__main__":
#     app.run(debug=True)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)