import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

def receive_messages():
    while True:
        try:
            # Receive message from the server
            message = client.recv(1024).decode('utf-8')
            if message:
                display_message(message)
            else:
                break
        except:
            display_message("Disconnected from server.")
            break

def send_message():
    message = message_input.get()
    if message:
        client.send(message.encode('utf-8'))
        message_input.delete(0, tk.END)  # Clear the input box after sending

def display_message(message):
    chat_window.config(state=tk.NORMAL)  # Allow editing the chat window
    chat_window.insert(tk.END, message + "\n")  # Insert the message at the end
    chat_window.config(state=tk.DISABLED)  # Disable editing after insertion
    chat_window.see(tk.END)  # Scroll to the bottom to see the latest message

def on_closing():
    client.close()  # Close the connection when the window is closed
    root.destroy()

# Create socket and connect to the server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('192.168.56.1', 5555))  # Server IP address and port

# Create the GUI window
root = tk.Tk()
root.title("Python Whatsapp")

chat_frame = tk.Frame(root)
chat_frame.pack(padx=10, pady=10)

# ScrolledText widget for the chat window, set to read-only
chat_window = scrolledtext.ScrolledText(chat_frame, wrap=tk.WORD, width=50, height=20, state=tk.DISABLED)
chat_window.pack()

# Input box for the message
message_input = tk.Entry(root, width=40)
message_input.pack(side=tk.LEFT, padx=10, pady=10)

# Send button
send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack(side=tk.RIGHT, padx=10, pady=10)

# Handle window closing
root.protocol("WM_DELETE_WINDOW", on_closing)

# Start a thread to receive messages from the server
threading.Thread(target=receive_messages, daemon=True).start()

# Start the Tkinter main loop
root.mainloop()
