
An AI-powered API built with **FastAPI** and **LangChain** that allows users to:
- ✅ Summarize YouTube video transcripts
- 🧠 Chat with the content (with memory)
- 📋 Generate quizzes from YouTube videos

---

## 🚀 Features

- 🔍 Extracts transcripts from YouTube videos
- 📝 Summarizes long videos into concise text
- 💬 Chat with the content using session-based memory (via `session_id`)
- 🎯 Generates multiple-choice quizzes
- ⚡ FastAPI backend with clear endpoints
- 🧠 LangChain + ChatNVIDIA integration

---

## 📦 Requirements

- Python 3.9+
- CHATNVIDIA API key

---

## 🔧 Installation

```bash
git clone https://github.com/yourusername/youtube-assistant-api.git
cd youtube-assistant-api
pip install -r requirements.txt
```

Make sure to set your OpenAI key:

```bash
# .env
NVIDIA_API_KEY=your-key-here
```

## 🏃‍♂️ Run the API

```bash
uvicorn main:app --reload
```

Access the interactive docs at:
```
http://127.0.0.1:8000/docs
```

---

## 📂 API Endpoints

### `GET /`
Returns a welcome message.

### `GET /health`
Returns API health status and version.

### `POST /summarizer`
Summarizes the transcript of a YouTube video.

**Request:**
```json
{
  "url": "https://www.youtube.com/watch?v=abc123"
}
```

### `POST /quiz`
Generates a quiz from the video transcript.

**Request:**
```json
{
  "url": "https://www.youtube.com/watch?v=abc123",
  "no_of_questions": 5
}
```

### `POST /chat`
Chat with the content of a YouTube video using session-based memory.

**Request:**
```json
{
  "session_id": "unique-session-id",
  "url": "https://www.youtube.com/watch?v=abc123",
  "query": "What is the video about?"
}
```

### `POST /chat/reset`
Reset chat memory for a session.

**Request:**
```
/chat/reset?session_id=your-session-id
```

---

## 🧠 Memory Handling

- Each chat session uses `session_id` to retain memory
- Memory is capped at a configurable limit (`MAX_HISTORY`)
- Use `/chat/reset` to clear memory on frontend refresh



## 🛠️ Future Improvements

- Vector search for long transcripts
- Redis-based memory persistence
- WebSocket/streaming responses
- Frontend dashboard (React/Vue)

---

## 🧑‍💻 Author

- 👤 Shiwang Upadhyay
- 📧 shiwangupadhyay05@gmail.com

---
