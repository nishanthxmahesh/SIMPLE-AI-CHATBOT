import pandas as pd
import fitz  # PyMuPDF
import os
import ollama

class Chatbot:
    def __init__(self):
        self.history = []
        self.data_sources = {}
        self.current_file = None
        self.current_data = None

    def load_file(self):
        while True:
            username = input("Windows username: ").strip()
            filename = input("File name (e.g., data.xlsx / file.csv / document.pdf): ").strip()
            file_path = os.path.join(f"C:\\Users\\{username}", filename)

            if not os.path.exists(file_path):
                print("❌ File not found. Try again.")
                continue

            self.current_file = file_path

            try:
                if filename.endswith(".csv"):
                    df = pd.read_csv(file_path)
                    self.data_sources[file_path] = df
                    self.current_data = df.to_markdown(index=False)
                    print(f"✔️ Loaded CSV: {os.path.basename(file_path)}")
                elif filename.endswith((".xlsx", ".xls")):
                    df = pd.read_excel(file_path)
                    self.data_sources[file_path] = df
                    self.current_data = df.to_markdown(index=False)
                    print(f"✔️ Loaded Excel: {os.path.basename(file_path)}")
                elif filename.endswith(".pdf"):
                    doc = fitz.open(file_path)
                    text = "\n".join([page.get_text() for page in doc])
                    self.data_sources[file_path] = text
                    self.current_data = text
                    print(f"✔️ Loaded PDF: {os.path.basename(file_path)}")
                else:
                    print("❌ Unsupported file type.")
                    continue
            except Exception as e:
                print(f"❌ Load error: {e}")
            return

    def summarize_data(self):
        if not self.current_file or self.current_file not in self.data_sources:
            return "⚠️ No file loaded."

        try:
            prompt = (
                "Below is some file content (Excel/CSV/PDF). "
                "Please summarize key insights or information in 75-100 characters only.\n\n"
                f"{self.current_data[:3000]}"
            )

            response = ollama.chat(
                model="llama3",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant who gives short, precise summaries of file content."},
                    {"role": "user", "content": prompt}
                ]
            )
            summary = response['message']['content'].strip()
            return summary if len(summary) <= 100 else summary[:100].rstrip() + "..."
        except Exception as e:
            return f"❌ Summary error: {e}"

    def chat(self, user_input):
        if not self.current_data:
            return "⚠️ No file loaded."

        try:
            prompt = (
                "Below is the loaded file content. Please answer ONLY questions related to this file in 100 characters max.\n\n"
                f"{self.current_data[:3000]}\n\nQuestion: {user_input}"
            )

            response = ollama.chat(
                model="llama3",
                messages=[
                    {"role": "system", "content": "Answer only file-related questions clearly in 100 characters."},
                    {"role": "user", "content": prompt}
                ]
            )
            reply = response['message']['content'].strip()
            if any(word in reply.lower() for word in ["fraud", "scenario", "story"]):
                return "Ask file-related questions only."
            return reply if len(reply) <= 100 else reply[:100].rstrip() + "..."
        except Exception as e:
            return f"❌ Chat error: {e}"

# ------------------- Main Program -------------------
chatbot = Chatbot()
chatbot.load_file()

while True:
    print("\n1. Summarize Data\n2. Ask a Question\n3. Change File\n4. Exit")
    choice = input("Choice: ").strip()

    if choice == "1":
        print("\nSummary:", chatbot.summarize_data())
    elif choice == "2":
        query = input("Ask your question: ").strip()
        print("Answer:", chatbot.chat(query))
    elif choice == "3":
        chatbot.load_file()
    elif choice == "4":
        break
    else:
        print("Invalid option.")
