import tkinter as tk
import os
from tkinter import messagebox
from main import HandImageCapture
from user_module import HandGestureClassifier

class HandImageCaptureGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Sign Language Interpreter")
        
        self.parent_folder = "Signs"
        self.flag = True

        self.menu_frame = tk.Frame(self.master)
        self.menu_frame.pack(pady=10)
        
        self.user_button = tk.Button(self.menu_frame, text="User", command=self.start_user_module)
        self.user_button.grid(row=0, column=0, padx=10)
        
        self.admin_button = tk.Button(self.menu_frame, text="Admin", command=self.admin_login)
        self.admin_button.grid(row=0, column=1, padx=10)
        
        self.admin_buttons = []  # To store admin buttons for later access

    def start_user_module(self):
        # Start the user module
        gesture_classifier = HandGestureClassifier()
        gesture_classifier.process_frame()

    def admin_login(self):
        # Create a new Toplevel window for admin login
        self.admin_login_window = tk.Toplevel(self.master)
        self.admin_login_window.title("Admin Login")

        # Label and Entry widget for password input
        tk.Label(self.admin_login_window, text="Enter Password:").pack()
        self.password_entry = tk.Entry(self.admin_login_window, show="*")
        self.password_entry.pack()

        # Button to confirm password
        tk.Button(self.admin_login_window, text="Login", command=self.check_password).pack()

    def check_password(self):
        # Get the password from the entry widget
        password = self.password_entry.get()

        # Check if the password is correct
        if password == "1234":
            # Destroy the login window
            self.admin_login_window.destroy()
            # Enable admin buttons
            self.enable_admin_buttons()
        else:
            # Incorrect password, show error message
            messagebox.showerror("Error", "Incorrect Password")

    def enable_admin_buttons(self):
        # Show admin buttons
        self.train_existing_button = tk.Button(self.menu_frame, text="Train existing sign", command=self.train_existing_sign)
        self.train_existing_button.grid(row=0, column=0, padx=10)
        self.admin_buttons.append(self.train_existing_button)

        self.train_new_button = tk.Button(self.menu_frame, text="Train new sign", command=self.train_new_sign)
        self.train_new_button.grid(row=0, column=1, padx=10)
        self.admin_buttons.append(self.train_new_button)

        self.get_sample_count_button = tk.Button(self.menu_frame, text="Get sample count", command=self.get_sample_count)
        self.get_sample_count_button.grid(row=0, column=2, padx=10)
        self.admin_buttons.append(self.get_sample_count_button)

        self.print_samples_button = tk.Button(self.menu_frame, text="Print samples", command=self.print_samples)
        self.print_samples_button.grid(row=0, column=3, padx=10)
        self.admin_buttons.append(self.print_samples_button)

        self.user_button_admin = tk.Button(self.menu_frame, text="User", command=self.start_user_module)
        self.user_button_admin.grid(row=0, column=4, padx=10)
        self.admin_buttons.append(self.user_button_admin)

    
        

    def train_existing_sign(self):
        # Create a new Toplevel window for input
        self.existing_sign_window = tk.Toplevel(self.master)
        self.existing_sign_window.title("Train Existing Sign")

        # Label and Entry widget for sign name input
        tk.Label(self.existing_sign_window, text="Enter Sign Name:").pack()
        self.sign_name_entry = tk.Entry(self.existing_sign_window)
        self.sign_name_entry.pack()

        # Button to confirm sign name and start image collection
        tk.Button(self.existing_sign_window, text="Start Image Collection", command=self.start_image_collection).pack()

    def start_image_collection(self):
        # Get the sign name from the entry widget
        sign_name = self.sign_name_entry.get()

        # Close the Toplevel window
        self.existing_sign_window.destroy()

        # Initialize HandImageCapture object with the provided sign name
        hand_image_capture = HandImageCapture(sign_name)

        # Start image collection and save data in the corresponding folder
        hand_image_capture.capture_images()

    def train_new_sign(self):
        # Create a new Toplevel window for input
        self.new_sign_window = tk.Toplevel(self.master)
        self.new_sign_window.title("Enter Sign Name")

        # Label and Entry widget for sign name input
        tk.Label(self.new_sign_window, text="Enter Sign Name:").pack()
        self.sign_name_entry = tk.Entry(self.new_sign_window)
        self.sign_name_entry.pack()

        # Button to confirm sign name and create folder
        tk.Button(self.new_sign_window, text="Create Folder", command=self.create_sign_folder).pack()

    def create_sign_folder(self):
        # Get the sign name from the entry widget
        folder_name = self.sign_name_entry.get()

        # Create the folder path
        folder_path = os.path.join(self.parent_folder, folder_name)

        # Create the folder
        os.makedirs(folder_path, exist_ok=True)

        # Optionally, you might want to inform the user that the folder has been created
        print(f"Folder '{folder_name}' created.")

        # Call method to start image collection
        hand_image_capture = HandImageCapture(folder_name)
        hand_image_capture.capture_images()

        # Close the Toplevel window
        self.new_sign_window.destroy()

        self.flag = False

    def get_sample_count(self):
        # Create a new Toplevel window for input
        self.sample_count_window = tk.Toplevel(self.master)
        self.sample_count_window.title("Get Sample Count")

        # Label and Entry widget for sign name input
        tk.Label(self.sample_count_window, text="Which Sign? :").pack()
        self.sign_name_entry = tk.Entry(self.sample_count_window)
        self.sign_name_entry.pack()

        # Label to display sample count
        self.sample_count_label = tk.Label(self.sample_count_window, text="")
        self.sample_count_label.pack()

        # Button to confirm sign name and get sample count
        tk.Button(self.sample_count_window, text="Get Count", command=self.print_sign_sample_count).pack()

    def print_sign_sample_count(self):
        # Get the sign name from the entry widget
        sign_name = self.sign_name_entry.get()

        # Get the sample count for the specified sign
        num_samples = HandImageCapture.count_files(self.parent_folder, sign_name)
        
        # Display the sample count in the label
        self.sample_count_label.config(text=f"Number of samples for sign '{sign_name}': {num_samples}")

    def print_samples(self):
        # Create a new Toplevel window for input
        self.print_samples_window = tk.Toplevel(self.master)
        self.print_samples_window.title("Print Samples")

        # Label and Entry widget for sign name input
        tk.Label(self.print_samples_window, text="Enter Sign Name:").pack()
        self.sign_name_entry = tk.Entry(self.print_samples_window)
        self.sign_name_entry.pack()

        # Button to confirm sign name and print the samples
        tk.Button(self.print_samples_window, text="Print Samples", command=self.print_sign_samples).pack()

    def print_sign_samples(self):
        # Get the sign name from the entry widget
        sign_name = self.sign_name_entry.get()

        # Close the Toplevel window
        self.print_samples_window.destroy()

        # Print the samples in the specified sign folder
        print(f"Samples in folder '{sign_name}':")
        HandImageCapture.print_file_names(self.parent_folder, sign_name)


def main():
    root = tk.Tk()
    app = HandImageCaptureGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
