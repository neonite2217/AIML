import tkinter as tk
from tkinter import Entry, scrolledtext, messagebox
from transformers import AutoTokenizer, AutoModelForCausalLM
import threading

# Load the model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("microsoft/phi-1_5")
model = AutoModelForCausalLM.from_pretrained("microsoft/phi-1_5", trust_remote_code=True)

# Function to generate a response from the model
def generate_response(message):
    inputs = tokenizer(message, return_tensors='pt', truncation=True)
    outputs = model.generate(**inputs, max_length=150, pad_token_id=tokenizer.eos_token_id)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

# Function to handle when the user sends a message
def on_send(event=None):
    message = user_input.get()
    if message:
        chat_window.configure(state=tk.NORMAL)
        chat_window.insert(tk.END, f"You: {message}\n")
        chat_window.configure(state=tk.DISABLED)
        user_input.delete(0, tk.END)
        
        # Run response generation in a separate thread
        threading.Thread(target=generate_and_display_response, args=(message,)).start()

def generate_and_display_response(message):
    try:
        # Indicate loading
        chat_window.configure(state=tk.NORMAL)
        chat_window.insert(tk.END, "Bot is thinking & typing...\n")
        chat_window.configure(state=tk.DISABLED)

        response = generate_response(message)
        
        # Remove loading text and display the response
        chat_window.configure(state=tk.NORMAL)
        chat_window.insert(tk.END, f"Bot: {response}\n")
        chat_window.configure(state=tk.DISABLED)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Function to save conversation to a file
def save_conversation():
    with open("conversation.txt", "w") as file:
        file.write(chat_window.get("1.0", tk.END))
    messagebox.showinfo("Saved", "Conversation saved to conversation.txt")

# Create the main window
window = tk.Tk()
window.title("Local Bot")

# Create the chat window
chat_window = scrolledtext.ScrolledText(window, width=80, height=20, state=tk.DISABLED)
chat_window.pack()

# Create the user input field
user_input = Entry(window, width=80)
user_input.pack()
user_input.focus_set()

# Create the save button
save_button = tk.Button(window, text="Save Conversation", command=save_conversation)
save_button.pack()

# Bind the Enter key to the on_send function
user_input.bind("<Return>", on_send)

# Start the Tkinter event loop
window.mainloop()
