
---

# ✈️ FlightAI Chatbot

A conversational AI assistant built using Ollama and Gradio to help users get ticket prices for different destinations. The assistant is trained to respond courteously and accurately, using tool-calling to fetch relevant data such as ticket prices.

---

## 🚀 Features

- Conversational AI chatbot using the Ollama API  
- Tool-calling capability for retrieving ticket prices  
- Secure Gradio interface with authentication  
- Customizable ticket pricing logic  
- Environment variable support using `.env` file  

---

## 🧠 Powered By

- [Ollama](https://ollama.com) for LLM chat  
- [Gradio](https://www.gradio.app) for UI  
- [Python-dotenv](https://pypi.org/project/python-dotenv/) for environment variables

---

## 📁 Project Structure

```
├── .env                 # Environment variables
├── app.py               # Main chatbot logic
├── README.md            # Project documentation
```

---

## ⚙️ Environment Variables

Create a `.env` file in your project root with the following variables:

```env
mod=your_model_name_here
id=your_gradio_login_username
pas=your_gradio_login_password
```

---

## 🧩 Functionality

The chatbot supports a function `get_ticket_price` which retrieves the price of a return ticket to a given city. This function is automatically called by the model when ticket pricing information is requested.

### Available Destinations

| City        | Price     |
|-------------|-----------|
| Dhaka       | 10000tk   |
| Thakurgaon  | 5000tk    |
| Sylet       | 7000tk    |
| Morocco     | 40000tk   |

---

## 💬 Example Interaction

**User**: How much is a ticket to Morocco?  
**Assistant**: The return ticket to Morocco is 40000tk.

---
Project WorkFLow

![FLight ai](https://github.com/user-attachments/assets/86a9a6be-e7fe-47d5-987d-808ab350fa32)


## 🔐 Running the Project

1. Install the required packages:

```bash
pip install -r requirements.txt
```

> Sample `requirements.txt`:
```
python-dotenv
gradio
ollama
```

2. Set up your `.env` file with your model and credentials.

3. Run the application:

```bash
python app.py
```

4. Access the chatbot via the link printed in the terminal. Authentication will be required.

---

## 📦 Deployment

You can deploy this chatbot to platforms like **Render**, **Hugging Face Spaces**, or your own server using Python and `gunicorn`.

---

## 📝 License

This project is open-source and available under the [MIT License](LICENSE).

---

## 👩‍💻 Author

Developed with ❤️ by [Your Name]. Feel free to contribute or raise issues!

---

