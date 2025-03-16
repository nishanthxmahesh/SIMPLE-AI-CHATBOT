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
            username = input("\nEnter your Windows username: ").strip()
            filename = input("Enter file name with extension (e.g., data.xlsx, file.csv, document.pdf): ").strip()
            file_path = os.path.join(f"C:\\Users\\{username}", filename)

            if os.path.exists(file_path):
                self.current_file = file_path
                if filename.endswith(".csv"):
                    self.load_csv(file_path)
                elif filename.endswith((".xlsx", ".xls")):
                    self.load_excel(file_path)
                elif filename.endswith(".pdf"):
                    self.load_pdf(file_path)
                else:
                    print("\n❌ Unsupported file type! Use CSV, Excel, or PDF.")
                    continue
                return
            else:
                print("\n⚠️ File not found! Check the file name and try again.")

    def load_csv(self, file_path):
        try:
            df = pd.read_csv(file_path)
            self.data_sources[file_path] = df
            self.current_data = df.to_string()
            print(f"\n✅ CSV '{os.path.basename(file_path)}' loaded!\n", df.head())
        except Exception as e:
            print(f"\n❌ Error loading CSV: {e}")

    def load_excel(self, file_path):
        try:
            df = pd.read_excel(file_path)
            self.data_sources[file_path] = df
            self.current_data = df.to_string()
            print(f"\n✅ Excel '{os.path.basename(file_path)}' loaded!\n", df.head())
        except Exception as e:
            print(f"\n❌ Error loading Excel: {e}")

    def load_pdf(self, file_path):
        try:
            doc = fitz.open(file_path)
            text = "\n".join([page.get_text() for page in doc])
            self.data_sources[file_path] = text
            self.current_data = text
            print(f"\n✅ PDF '{os.path.basename(file_path)}' loaded!\n", text[:500])
        except Exception as e:
            print(f"\n❌ Error loading PDF: {e}")

    def summarize_data(self):
        if not self.current_file or self.current_file not in self.data_sources:
            return "⚠️ No file is loaded."

        response = ollama.chat(
            model="phi",
            messages=[
                {"role": "system", "content": "Summarize this data briefly (max 100 characters)."},
                {"role": "user", "content": self.current_data[:3000]}
            ]
        )
        return response['message']['content'][:100]

    def chat(self, user_input):
        if not self.current_data:
            return "⚠️ No file loaded."

        response = ollama.chat(
            model="phi",
            messages=[
                {"role": "system", "content": "Answer file-related questions only. Max 100 characters."},
                {"role": "user", "content": f"Data: {self.current_data[:3000]}\n\nQuestion: {user_input}"}
            ]
        )

        reply = response['message']['content'][:100]

        if "fraud" in reply.lower() or "scenario" in reply.lower() or "story" in reply.lower():
            return "Ask about the file only."

        return reply


chatbot = Chatbot()
chatbot.load_file()

while True:
    print("\nOptions:")
    print("1. Summarize Data")
    print("2. Ask a Question (File-related)")
    print("3. Change File")
    print("4. Exit")
    
    choice = input("Enter your choice: ")

    if choice == "1":
        print("\n🔍 Summarizing data...\n", chatbot.summarize_data())
    elif choice == "2":
        query = input("\nAsk your question (must be about the file): ")
        print("\n🤖 Chatbot:", chatbot.chat(query))
    elif choice == "3":
        chatbot.load_file()
    elif choice == "4":
        print("\n👋 Exiting...")
        break
    else:
        print("\n⚠️ Invalid choice. Select 1, 2, 3, or 4.")
