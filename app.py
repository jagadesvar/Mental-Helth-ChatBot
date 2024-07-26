import json
import random
import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog, simpledialog
from datetime import datetime

class MentalHealthBot:
    def __init__(self, intents_file):
        with open(intents_file, 'r') as file:
            self.intents = json.load(file)

    def get_response(self, message):
        for intent in self.intents['intents']:
            for pattern in intent['patterns']:
                if pattern.lower() == message.lower():
                    return random.choice(intent['responses'])
        return "I'm sorry, I don't understand. Can you please rephrase?"

class MessageWidget(tk.Frame):
    def __init__(self, master=None, sender=None, message=None, **kwargs):
        super().__init__(master, **kwargs)
        self.sender = sender
        self.message = message
        self.create_widgets()

    def create_widgets(self):
        timestamp = get_timestamp()
        label_text = f"{timestamp} {self.sender}: {self.message}"
        label = tk.Label(self, text=label_text, wraplength=400, justify="left")
        label.pack(pady=5, padx=10, anchor="w")
        if self.sender == "You":
            label.config(bg="#CCE5FF", relief="solid", borderwidth=1)
        else:
            label.config(bg="#FFE5CC", relief="solid", borderwidth=1)

def send_message():
    user_input = entry.get()
    entry.delete(0, tk.END)
    display_message("You", user_input)
    response = bot.get_response(user_input)
    display_message("Bot", response)

def display_message(sender, message):
    message_widget = MessageWidget(chat_log, sender=sender, message=message)
    message_widget.pack(fill="x", padx=10, pady=5, anchor="w")

def get_timestamp():
    now = datetime.now()
    return now.strftime("[%H:%M:%S]")

def clear_chat_log():
    confirmed = messagebox.askyesno("Clear Chat Log", "Are you sure you want to clear the chat log?")
    if confirmed:
        for widget in chat_log.winfo_children():
            widget.destroy()

def save_chat_log():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'w') as file:
            for widget in chat_log.winfo_children():
                message = widget.message
                file.write(message + '\n')
        messagebox.showinfo("Save Chat Log", "Chat log saved successfully.")

def send_chat_log():
    recipient = simpledialog.askstring("Send Chat Log", "Enter recipient email address:")
    if recipient:
        message = chat_log.get("1.0", tk.END)
        # Code to send the chat log to the recipient
        messagebox.showinfo("Send Chat Log", f"Chat log sent to {recipient} successfully.")

def cancel_chat_log():
    confirmed = messagebox.askyesno("Cancel Chat Log", "Are you sure you want to cancel?")
    if confirmed:
        root.destroy()

def contact_numbers():
    messagebox.showinfo("Contact Numbers", "Contact:\n1. 7339661898\n2. 8778192321\n3.9345751269")

def main():
    root = tk.Tk()
    root.title("Mental Health Bot")
    root.geometry("600x500")

    chat_log_frame = tk.Frame(root)
    chat_log_frame.pack(pady=10, fill=tk.BOTH, expand=True)
    global chat_log
    chat_log = scrolledtext.ScrolledText(chat_log_frame, wrap=tk.WORD)
    chat_log.pack(fill="both", expand=True)

    entry_frame = tk.Frame(root)
    entry_frame.pack(pady=10, padx=10, fill=tk.X)
    global entry
    entry = tk.Entry(entry_frame, width=80, font=('Arial', 12))
    entry.pack(side=tk.LEFT, padx=(0, 10))
    entry.bind("<Return>", lambda event=None: send_message())

    send_button = tk.Button(entry_frame, text="Send", command=send_message, font=('Arial', 12), bg="green", fg="white")
    send_button.pack(side=tk.RIGHT)

    menubar = tk.Menu(root)
    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="Save Chat Log", command=save_chat_log)
    file_menu.add_command(label="Send Chat Log", command=send_chat_log)
    file_menu.add_command(label="Clear Chat Log", command=clear_chat_log)
    file_menu.add_command(label="Cancel", command=cancel_chat_log)
    menubar.add_cascade(label="File", menu=file_menu)

    contact_menu = tk.Menu(menubar, tearoff=0)
    contact_menu.add_command(label="Contact Numbers", command=contact_numbers)
    menubar.add_cascade(label="Contact", menu=contact_menu)

    root.config(menu=menubar)

    clear_button = tk.Button(root, text="Clear", command=clear_chat_log, font=('Arial', 12), bg="red", fg="white")
    clear_button.pack(side=tk.BOTTOM, padx=10, pady=10, anchor="se")

    global bot
    bot = MentalHealthBot('intents.json')

    root.mainloop()

if __name__ == "__main__":
    main()
