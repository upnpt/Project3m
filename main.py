import customtkinter as ctk
from tkinter import filedialog, messagebox
import re


class RegexApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Regex Text Processing System")
        self.root.geometry("1200x700")

        # Title
        title = ctk.CTkLabel(
            root,
            text="Regex Text Processing System",
            font=("Arial", 24, "bold")
        )
        title.pack(pady=10)

        # Top Frame
        top_frame = ctk.CTkFrame(root)
        top_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(
            top_frame,
            text="Load File",
            command=self.load_file
        ).pack(side="left", padx=5, pady=5)

        ctk.CTkButton(
            top_frame,
            text="Clear",
            command=self.clear_all
        ).pack(side="left", padx=5, pady=5)

        # Main Frame
        main_frame = ctk.CTkFrame(root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Input
        left_frame = ctk.CTkFrame(main_frame)
        left_frame.pack(side="left", fill="both", expand=True, padx=5)

        ctk.CTkLabel(
            left_frame,
            text="Input Text"
        ).pack(pady=5)

        self.txt_input = ctk.CTkTextbox(left_frame)
        self.txt_input.pack(fill="both", expand=True, padx=5, pady=5)

        # Output
        right_frame = ctk.CTkFrame(main_frame)
        right_frame.pack(side="right", fill="both", expand=True, padx=5)

        ctk.CTkLabel(
            right_frame,
            text="Result"
        ).pack(pady=5)

        self.txt_output = ctk.CTkTextbox(right_frame)
        self.txt_output.pack(fill="both", expand=True, padx=5, pady=5)

        # Control Frame
        control_frame = ctk.CTkFrame(root)
        control_frame.pack(fill="x", padx=10, pady=5)

        self.option_menu = ctk.CTkOptionMenu(
            control_frame,
            values=[
                "Find Emails",
                "Find Phones",
                "Find URLs",
                "Find Numbers",
                "Find Capital Words",
                "Count Words",
                "Custom Search",
                "Replace Text",
                "Remove Extra Spaces",
                "Split Sentences"
            ]
        )
        self.option_menu.pack(side="left", padx=10, pady=10)

        self.param_entry = ctk.CTkEntry(
            control_frame,
            width=300,
            placeholder_text="Parameter / Pattern"
        )
        self.param_entry.pack(side="left", padx=10)

        ctk.CTkButton(
            control_frame,
            text="Process",
            command=self.process_text
        ).pack(side="left", padx=10)

        self.status_label = ctk.CTkLabel(
            root,
            text="Ready"
        )
        self.status_label.pack(pady=5)

    def load_file(self):
        try:
            file_path = filedialog.askopenfilename(
                filetypes=[
                    ("Text Files", "*.txt"),
                    ("All Files", "*.*")
                ]
            )

            if file_path:
                with open(file_path, "r", encoding="utf-8") as file:
                    data = file.read()

                self.txt_input.delete("1.0", "end")
                self.txt_input.insert("1.0", data)

                self.status_label.configure(
                    text=f"Loaded : {file_path}"
                )

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def process_text(self):
        try:

            text = self.txt_input.get("1.0", "end").strip()

            if not text:
                raise ValueError("กรุณาใส่ข้อความก่อน")

            option = self.option_menu.get()
            param = self.param_entry.get()

            result = ""

            # 1 Find Emails
            if option == "Find Emails":
                result = "\n".join(
                    re.findall(
                        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
                        text
                    )
                )

            # 2 Find Phones
            elif option == "Find Phones":
                result = "\n".join(
                    re.findall(
                        r"\d{3}-\d{3}-\d{4}",
                        text
                    )
                )

            # 3 Find URLs
            elif option == "Find URLs":
                result = "\n".join(
                    re.findall(
                        r"https?://\S+",
                        text
                    )
                )

            # 4 Find Numbers
            elif option == "Find Numbers":
                result = "\n".join(
                    re.findall(
                        r"\d+",
                        text
                    )
                )

            # 5 Find Capital Words
            elif option == "Find Capital Words":
                result = "\n".join(
                    re.findall(
                        r"\b[A-Z][A-Za-z]+\b",
                        text
                    )
                )

            # 6 Count Words
            elif option == "Count Words":
                words = re.findall(
                    r"\S+",
                    text
                )
                result = f"Total Words : {len(words)}"

            # 7 Custom Search
            elif option == "Custom Search":

                if not param:
                    raise ValueError(
                        "กรุณาใส่ Regex Pattern"
                    )

                matches = [
                    m.group()
                    for m in re.finditer(param, text)
                ]

                result = "\n".join(matches)

            # 8 Replace Text
            elif option == "Replace Text":

                if "," not in param:
                    raise ValueError(
                        "รูปแบบ old,new"
                    )

                old_text, new_text = param.split(",", 1)

                result = re.sub(
                    old_text,
                    new_text,
                    text
                )

            # 9 Remove Extra Spaces
            elif option == "Remove Extra Spaces":

                result = re.sub(
                    r"\s+",
                    " ",
                    text
                )

            # 10 Split Sentences
            elif option == "Split Sentences":

                sentences = [
                    s.strip()
                    for s in re.split(
                        r"[.!?]+",
                        text
                    )
                    if s.strip()
                ]

                result = "\n".join(sentences)

            self.txt_output.delete("1.0", "end")
            self.txt_output.insert("1.0", result)

            self.status_label.configure(
                text="Process Complete ✅"
            )

        except re.error as e:
            messagebox.showerror(
                "Regex Error",
                str(e)
            )

        except Exception as e:
            messagebox.showerror(
                "Error",
                str(e)
            )

    def clear_all(self):
        self.txt_input.delete("1.0", "end")
        self.txt_output.delete("1.0", "end")
        self.param_entry.delete(0, "end")
        self.status_label.configure(text="Ready")


if __name__ == "__main__":
    ctk.set_appearance_mode("Light")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    app = RegexApp(root)
    root.mainloop()