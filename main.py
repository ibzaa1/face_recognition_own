# IMPORT FOR UI
import tkinter as tk
# IMPORT FOR FILE MANIPULATION
from tkinter import filedialog

# IMPORT FOR DETECTING FACES (MAIN FUNCTION)
import face_recognition

# PROGRAMME CLASS - ONLY 1 NEEDED (MAIN PROGRAMME)
class App:
    def __init__(self, root):
        # DEFINING GEOMETRY OF PROGRAMME AND TITLE
        self.root = root
        self.root.title("ImageCompare.com")
        self.root.geometry("800x400")  # Set a fixed size for the window

        # NO IMAGE PATH WHEN PROGRAMME INITIALISED
        self.image1_path = None
        self.image2_path = None

        # BUTTONS STYLES FOR IMPROVED UI
        browse_button = {'font': ('Arial', 14), 'fg': 'black', 'padx': 10, 'pady': 5}
        delete_button = {'font': ('Arial', 14), 'fg': 'red', 'padx': 10, 'pady': 5}
        compare_button = {'font': ('Arial', 14), 'fg': 'blue', 'padx': 10, 'pady': 5}
        reset_button = {'font': ('Arial', 14), 'fg': 'red', 'padx': 10, 'pady': 5}

        # IMAGE 1 FRAME COMPONENT
        self.image1_frame = tk.Frame(root, pady=10)
        self.image1_frame.pack(side=tk.LEFT, anchor=tk.N, padx=20)

        self.image1_label = tk.Label(self.image1_frame, text="First Image:", font=('Arial', 14))
        self.image1_label.pack()

        self.browse_button1 = tk.Button(self.image1_frame, text="Browse Image", command=self.browse_image1,
                                        **browse_button)
        self.browse_button1.pack()

        self.delete_button1 = tk.Button(self.image1_frame, text="Delete Image", command=self.delete_image1,
                                        **delete_button)
        self.delete_button1.pack()

        self.image1_status = tk.Label(self.image1_frame, text="")
        self.image1_status.pack()

        # IMAGE 2 FRAME COMPONENT
        self.image2_frame = tk.Frame(root, pady=10)
        self.image2_frame.pack(side=tk.RIGHT, anchor=tk.N, padx=20)

        self.image2_label = tk.Label(self.image2_frame, text="Second Image:", font=('Arial', 14))
        self.image2_label.pack()

        self.browse_button2 = tk.Button(self.image2_frame, text="Browse Image", command=self.browse_image2, **browse_button)
        self.browse_button2.pack()

        self.delete_button2 = tk.Button(self.image2_frame, text="Delete Image", command=self.delete_image2, **delete_button)
        self.delete_button2.pack()

        self.image2_status = tk.Label(self.image2_frame, text="")
        self.image2_status.pack()

        # RESULT FRAME COMPONENT
        self.result_frame = tk.Frame(root, pady=20)
        self.result_frame.pack(side=tk.BOTTOM)

        self.compare_button = tk.Button(self.result_frame, text="Compare", command=self.compare_faces, **compare_button)
        self.compare_button.pack(side=tk.LEFT)

        self.reset_button = tk.Button(self.result_frame, text="RESET", command=self.reset, **reset_button)
        self.reset_button.pack(side=tk.RIGHT)

        self.result_label = tk.Label(root, text="", font=('Arial', 14   ), pady=10)
        self.result_label.pack()

    # BROWSE FOR IMAGE 1 FUNCTION
    def browse_image1(self):
        image_path = filedialog.askopenfilename()
        if image_path:
            self.image1_path = image_path
            self.image1_status.config(text="Image 1 selected")

    # BROWSE FOR IMAGE 2 FUNCTION
    def browse_image2(self):
        image_path = filedialog.askopenfilename()
        if image_path:
            self.image2_path = image_path
            self.image2_status.config(text="Image 2 selected")

    # DELETE IMAGE 1 FUNCTION
    def delete_image1(self):
        self.image1_path = None
        self.image1_label.config(image="")
        self.image1_status.config(text="")

    # DELETE IMAGE 2 FUNCTION
    def delete_image2(self):
        self.image2_path = None
        self.image2_label.config(image="")
        self.image2_status.config(text="")

    # RESET ALL VARIABLES FUNCTION
    def reset(self):
        self.image1_path = None
        self.image2_path = None
        self.image1_label.config(image="")
        self.image2_label.config(image="")
        self.image1_status.config(text="")
        self.image2_status.config(text="")
        self.result_label.config(text="")

    # ENCODING CREATES UNIQUE NUMERICAL VALUES FOR FACES SELECTED BY THE USER, WHICH THEN THE "FACE_RECOGNITION" LIBRARY COMPARES
    # THESE VALUES TO FIND SIMILARITIES - THIS IS ALL DONE BY THE COMPUTER THROUGH NETWORKS AND IMAGE TOLERANCE LEVELS.
    def load_and_encode_image(self, image_path):
        image = face_recognition.load_image_file(image_path) # LOAD IMAGE TO PROGRAMME TO ENCODE IMAGE
        face_encodings = face_recognition.face_encodings(image) # FACE_RECOGNITION LIBRARY
        if len(face_encodings) > 0: # IF THERE ARE FACE ENCODINGS WITHIN PICTURES SELECTED, RETURN THE UNIQUE FACE ENCODING VALUE
            return face_encodings[0]
        else:
            return None # IF THERE ARE NO FACE ECONDING VALUES, RETURN NONE - THIS WILL BE USED TO CREATE THE PRINT ERRORS, FAILS, AND SUCCESSES BELOW

    # MAIN FUNCTION
    def compare_faces(self):
        if self.image1_path and self.image2_path: # IF THE USER HAS SELECTED 2 PATHS THEN:
            encoding1 = self.load_and_encode_image(self.image1_path) # IMAGE1_PATH = SELECTED PATH BY BROWSING IMAGE
            encoding2 = self.load_and_encode_image(self.image2_path) # IMAGE2_PATH = SELECTED PATH BY BROWSING IMAGE

            if encoding1 is not None and encoding2 is not None: # IF BOTH PATHS ARE VALID IMAGE PATHS AND CONTAINS 2 FACES THEN:
                results = face_recognition.compare_faces([encoding1], encoding2, tolerance=0.6)
                if results[0]:
                    self.result_label.config(text="SUCCESS: SIMILAR FACES FOUND IN BOTH IMAGES", fg='#4CAF50') # PRINT SIMILARITIES FOUND
                else:
                    self.result_label.config(text="FAIL: SIMILAR FACES WAS NOT FOUND IN BOTH IMAGES", fg='red') # OTHERWISE NO SIMILARITIES FOUND
            else:
                self.result_label.config(text="ERROR: FACE WAS NOT FOUND IN AN IMAGE", fg='red') # ONE OR BOTH IMAGES DIDNT HAVE A FACE
        else:
            self.result_label.config(text="ERROR: SELECT 2 IMAGES", fg='red') # ONE OF BOTH IMAGES WAS NOT SELECTED


# INITIALISE PROGRAMME
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
