# 🕌 FatwaBot (فتوى)

FatwaBot is an Islamic chatbot that provides answers to fatwa-related questions. Built using Django and powered by AI and semantic search, the bot can understand and respond to religious questions using a dataset of trusted fatwas.

---

## ✨ Version 2 Highlights

- ✅ **Semantic Search**: Matches user questions with the most relevant fatwa from the dataset.
- ✅ **Dataset Integration**: Answers come directly from preloaded authentic fatwas.
- ✅ **Random Question Feature**: Users can click a button to get a random question from the dataset for exploration or testing.
- ✅ **Improved Accuracy**: Better matching and understanding of Arabic questions.

---

## 📦 Tech Stack

- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, jQuery
- **AI**: Sentence Transformers (for semantic similarity)
- **Data Source**: Custom fatwa dataset (in CSV format)

---

## 🚀 Try It Locally

### 1. Clone the Project

```bash
git clone git@github.com:MAlharbi-dev/FatwaBot.git
cd FatwaBot
```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv env
source env/bin/activate  # On Windows use: env\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

> Make sure you have `transformers`, `torch`, and `sentence-transformers` installed for the AI part.

### 4. Run Migrations

```bash
python manage.py migrate
```

### 5. Run the Server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/chatbot/` to start chatting with the bot.

---

## 🧠 Dataset Format

The fatwa dataset should be a `.csv` file located at:

```
chatbot/static/chatbot/data/fatwas.csv
```

**Required Columns:**
- `titles`: The fatwa question.
- `answer`: The corresponding answer.

---

## 🎯 How It Works

1. The user types a question in Arabic.
2. The system calculates the semantic similarity between the user’s question and all dataset questions using an Arabic language model.
3. The most similar question is retrieved, and its answer is shown.
4. Users can also try a **random question** from the dataset by clicking a button.

---

## 📄 License

This project is for educational and nonprofit use. Always consult scholars for sensitive religious matters.

---

## 🤝 Contributing

Pull requests and suggestions are welcome. For major changes, please open an issue first.

---

## 🧪 Want to Test Fast?

If you just want to explore the bot:
- Clone the project.
- Run the server.
- Click the **"Random Question"** button to see an example from the dataset instantly!

---

**Built with ❤️ and respect for knowledge.**
