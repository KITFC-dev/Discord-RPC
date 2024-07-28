import customtkinter as ctk

class AnimatedCheckboxEntry(ctk.CTkFrame):
    def __init__(self, master, checkbox_text, entry1_text, entry2_text, **kwargs):
        super().__init__(master, **kwargs)
        # self.configure(fg_color="transparent")  # Make the frame background transparent

        # checkbox
        self.checkbox_var = ctk.StringVar(value="off")
        self.checkbox = ctk.CTkCheckBox(self, text=f"{checkbox_text}", variable=self.checkbox_var, 
                                        onvalue="on", offvalue="off", command=self.toggle_entries)
        self.checkbox.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        # labels and entries
        self.large_image_prompt_label = ctk.CTkLabel(self, text=f"{entry1_text}")
        self.large_image_prompt_entry = ctk.CTkEntry(self, width=150)
        self.alt_text_label = ctk.CTkLabel(self, text=f"{entry2_text}")
        self.alt_text_entry = ctk.CTkEntry(self, width=150)

        # animation variables
        self.entries_visible = False
        self.animating = False
        self.current_height = 0
        self.target_height = 0

    def toggle_entries(self):
        if not self.animating:
            self.entries_visible = not self.entries_visible
            self.target_height = 70 if self.entries_visible else 0
            self.animating = True
            self.animate()

    def animate(self):
        step_size = 5
        if self.entries_visible:
            self.current_height += step_size
            if self.current_height >= self.target_height:
                self.current_height = self.target_height
                self.animating = False
        else:
            self.current_height -= step_size
            if self.current_height <= self.target_height:
                self.current_height = self.target_height
                self.animating = False

        self.update_layout()

        if self.animating:
            self.after(10, self.animate)

    def update_layout(self):
        if self.current_height > 0:
            self.large_image_prompt_label.grid(row=1, column=0, padx=5, pady=(5, 0), sticky="w")
            self.large_image_prompt_entry.grid(row=1, column=1, padx=5, pady=(5, 0), sticky="ew")
            self.alt_text_label.grid(row=2, column=0, padx=5, pady=(5, 5), sticky="w")
            self.alt_text_entry.grid(row=2, column=1, padx=5, pady=(5, 5), sticky="ew")
        else:
            self.large_image_prompt_label.grid_forget()
            self.large_image_prompt_entry.grid_forget()
            self.alt_text_label.grid_forget()
            self.alt_text_entry.grid_forget()

        self.configure(height=30 + self.current_height)
        self.grid_propagate(False)
        self.columnconfigure(1, weight=1)

    def get_image_prompt(self):
        return self.large_image_prompt_entry.get()

    def get_alt_text(self):
        return self.alt_text_entry.get()

if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("400x300")

    animated_checkbox = AnimatedCheckboxEntry(root, checkbox_text="Show Details", 
                                              entry1_text="Image Prompt:", entry2_text="Alt Text:")
    animated_checkbox.place(relx=0.5, rely=0.35, anchor="center")

    root.mainloop()
