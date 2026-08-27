import tkinter as tk
from tkinter import scrolledtext
import wikipedia

# Set Wikipedia language
wikipedia.set_lang("en")

# Rule-based + general info response
def get_response(user_input):
    user_input = user_input.lower().strip()

    # Rule-based responses
    if "hi" in user_input or "hello" in user_input:
        return "Hello! How can I help you?"
    elif "how are you" in user_input:
        return "I'm just code, but thanks for asking!"
    elif "your name" in user_input:
        return "I'm InfoBot, a simple rule-based chatbot."
    elif "bye" in user_input or "exit" in user_input:
        return "Goodbye! Have a great day!"
    elif "help" in user_input:
        return "You can ask me anything like 'What is Python?' or 'Tell me about India'."
    elif "what can you do" in user_input:
        return "I can answer simple questions and fetch general info from Wikipedia."

    # Wikipedia fallback for general knowledge
    try:
        result = wikipedia.summary(user_input, sentences=2)
        return result
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Please be more specific. Did you mean: {', '.join(e.options[:3])}?"
    except wikipedia.exceptions.PageError:
        return "I couldn't find any info about that. Try rephrasing."
    except:
        return "Sorry, I couldn't understand. Please try something else."

# Function to send user message and get response
def send_message():
    user_msg = entry.get()
    if not user_msg.strip():
        return

    chat_window.insert(tk.END, f"You: {user_msg}\n")
    response = get_response(user_msg)
    chat_window.insert(tk.END, f"Bot: {response}\n\n")
    entry.delete(0, tk.END)

# GUI Setup
root = tk.Tk()
root.title("Rule-Based Universal Chatbot")
root.geometry("500x600")
root.resizable(False, False)

chat_window = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Arial", 12))
chat_window.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

entry = tk.Entry(root, font=("Arial", 12))
entry.pack(padx=10, pady=10, fill=tk.X)
entry.bind("<Return>", lambda event: send_message())

send_button = tk.Button(root, text="Send", command=send_message, font=("Arial", 12), bg="lightblue")
send_button.pack(pady=10)

root.mainloop()
