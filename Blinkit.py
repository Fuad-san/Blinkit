import customtkinter as ctk
import cv2
from PIL import Image, ImageTk
from tkinter import messagebox
from Blinkit_GameEngine import GameLogic
import numpy as np
import time

class ModernDontBlinkGame:
    def __init__(self, root):
        print("Initializing game...")
        self.root = root
        self.root.title("Don't Blink Challenge")
        self.root.geometry("1024x768")
        
        # Initialize game logic
        self.game_logic = GameLogic()
        self.high_score = 0  # Track the high score
        
        # Configure custom theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Setup UI components
        self.setup_ui()
        print("UI setup complete.")

        # Add restart and quit buttons
        self.restart_button = ctk.CTkButton(self.root, text="Restart", command=self.restart_game)
        self.quit_button = ctk.CTkButton(self.root, text="Quit", command=self.quit_game)

        # Initially hide restart and quit buttons
        self.restart_button.pack_forget()  
        self.quit_button.pack_forget()
        
        self.start_time = None
        
    def setup_ui(self):
    # Create Title
        self.title_label = ctk.CTkLabel(self.root, text="Don't blink, Blink and you lose!", font=('Helvetica', 18, 'bold'))
        self.title_label.pack(pady=5)

        # Score Labels
        self.score_label = ctk.CTkLabel(self.root, text="Score: 0", font=('Helvetica', 16))
        self.score_label.pack(pady=10)

        self.high_score_label = ctk.CTkLabel(self.root, text="High Score: 0", font=('Helvetica', 16))
        self.high_score_label.pack(pady=5)

        # Elapsed Time Label
        self.elapsed_time_label = ctk.CTkLabel(self.root, text="Time: 0s", font=('Helvetica', 16))
        self.elapsed_time_label.pack(pady=5)


        # Video Frame
        self.video_label = ctk.CTkLabel(self.root, text='Let the game start now', font=('Helvetica',50))
        self.video_label.pack(expand=True, fill="both")

        # Buttons
        self.start_button = ctk.CTkButton(self.root, text="Start Game", command=self.start_game)
        self.start_button.pack(pady=10)

        self.quit_button = ctk.CTkButton(self.root, text="Quit", command=self.quit_game)
        self.quit_button.pack(pady=10)

        
    def start_game(self):
        print("Starting game...")

        self.title_label.pack_forget()
        self.score_label.pack_forget()
        self.high_score_label.pack_forget()
        self.start_button.pack_forget()
        self.quit_button.pack_forget()

        # Optionally, you can add a new label to show game instructions
        self.instruction_label = ctk.CTkLabel(self.root, text="Don't Blink! Good luck!", font=('Helvetica', 24))
        self.instruction_label.pack(pady=20)

        # Clear the video label text
        self.video_label.configure(text="")

        self.start_time = time.time()

        # Reset and start the game logic
        self.game_logic.reset_game()
        self.update_frame()

    def end_game(self):
        # Display game over message
        total_time = int(time.time() - self.start_time)  # Calculate elapsed time
        messagebox.showinfo("Game Over", f"You blinked! Your score was: {self.game_logic.score}. You lasted {total_time} seconds.")
        
        # Release the camera if it's open
        if hasattr(self, 'cap') and self.cap.isOpened():
            self.cap.release()

        self.instruction_label.pack_forget()

        # Show the restart and quit buttons
        self.restart_button.pack(pady=10)

    def restart_game(self):
        print("Restart button clicked")  # Debug print
        # Hide the restart and quit buttons
        self.restart_button.pack_forget()
        self.quit_button.pack_forget()

        # Reset the game logic
        self.game_logic.reset_game()

        # Reset score display
        self.score_label.configure(text="Score: 0")  # Reset score display
        self.elapsed_time_label.configure(text="Time: 0s") 

        # Hide restart and quit buttons
        self.restart_button.pack_forget()
        self.quit_button.pack_forget()

        # Start the game again
        self.start_game()  # Call start_game to initialize everything again

    def update_frame(self):
        if not hasattr(self, 'cap') or not self.cap.isOpened():
            self.cap = cv2.VideoCapture(0)  # Initialize camera
            if not self.cap.isOpened():
                messagebox.showerror("Error", "Unable to access camera.")
                return

        # Capture frame-by-frame
        ret, frame = self.cap.read()
        if not ret:
            return

        # Convert frame to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.game_logic.detector(gray)

        # Process each detected face
        for face in faces:
            landmarks = self.game_logic.predictor(gray, face)
            
            # Extract eye points
            left_eye_points = [(landmarks.part(n).x, landmarks.part(n).y) for n in range(36, 42)]
            right_eye_points = [(landmarks.part(n).x, landmarks.part(n).y) for n in range(42, 48)]
            
            # Calculate EAR for both eyes
            left_ear = self.game_logic.get_ear(left_eye_points)
            right_ear = self.game_logic.get_ear(right_eye_points)
            self.game_logic.ear = (left_ear + right_ear) / 2.0
            
            # Draw contours around eyes
            cv2.drawContours(frame, [cv2.convexHull(np.array(left_eye_points))], -1, (0, 255, 0), 1)
            cv2.drawContours(frame, [cv2.convexHull(np.array(right_eye_points))], -1, (0, 255, 0), 1)
            
            # Update score based on EAR threshold
            if not self.game_logic.update_score():
                self.end_game()  # Trigger game over if blinking is detected
                return
            
            # Update score display
            self.score_label.configure(text=f"Score: {self.game_logic.score}")
        
        if self.start_time is not None:
            elapsed_time = int(time.time() - self.start_time)
            self.elapsed_time_label.configure(text=f"Time: {elapsed_time}s")
        
        # Display EAR on the screen
        ear_text = f"EAR: {self.game_logic.ear:.2f}"
        cv2.putText(frame, ear_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Convert frame to a format Tkinter can display
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        
        # Resize image to fit window dimensions, maintaining aspect ratio
        display_size = (800, 600)
        img.thumbnail(display_size, Image.Resampling.LANCZOS)
        
        # Convert to ImageTk format and display in the label
        imgtk = ImageTk.PhotoImage(image=img)
        self.video_label.imgtk = imgtk
        self.video_label.configure(image=imgtk)
        
        # Schedule the next frame update
        self.root.after(10, self.update_frame)


    def quit_game(self):
        # Release the camera if it's open
        if hasattr(self, 'cap') and self.cap.isOpened():
            self.cap.release()
        
        # Confirm quit action with the user
        if messagebox.askokcancel("Quit", "Are you sure you want to quit?"):
            self.root.quit()

# Start Tkinter application
if __name__ == "__main__":
    root = ctk.CTk()
    app = ModernDontBlinkGame(root)
    print("Entering mainloop.")
    root.mainloop()
