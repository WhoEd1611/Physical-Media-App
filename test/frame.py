# # ## Holds the classes used to create the frames for the visual display
# # import customtkinter as ctk
# # import tkinter as tk
# # from dataClasses import Media, Franchise

# # def get_screen_size():
# #     root = ctk.CTk()  # Use CTk from customtkinter
# #     screen_width = root.winfo_screenwidth()
# #     screen_height = root.winfo_screenheight()
# #     root.destroy()  # Destroy the CTk instance since it's not needed anymore
# #     return screen_width, screen_height

# # ### These frames are static
# # class startFrame(ctk.CTkFrame):
# #     def __init__(self, master):
# #         super().__init__(master)

# # class randomFrame(ctk.CTkFrame):
# #     def __init__(self, master):
# #         pass

# # def pickRandomMedia():
# #     pass

# # class newMediaFrame(ctk.CTkFrame):
# #     def __init__(self, master):
# #         pass

# # ### These frames need to be dynamically made
# # class mediaFrame(ctk.CTkFrame):
# #     """
# #     At current, it can correctly read the attributes. It needs to be correctly 'decorated'.
# #     """
# #     def __init__(self, master):
# #         super().__init__(master)
# #         randomButton = ctk.CTkLabel(master, text = "Random Button")
# #         randomButton.grid(row = 0, column = 0, pady=10, padx=10)

# # class franchiseFrame(ctk.CTkFrame):
# #     def __init__(self, master, franchise: Franchise):
# #         pass

# # class app(ctk.CTk):
# #     def __init__(self):
# #         super().__init__()

# # if __name__ == "__main__":
# #     ### Create default appearance scheme
# #     width, height = get_screen_size()
# #     text = f"{width}x{height}"
# #     ctk.set_appearance_mode("System")
# #     ctk.set_default_color_theme("green")

# #     app = mediaFrame()
# #     app.geometry(text)
# #     app.mainloop()

# import customtkinter


# class App(customtkinter.CTk):
#     def __init__(self):
#         super().__init__()

#         self.geometry("500x300")
#         self.title("RadioButtonFrame test")

#         self.radio_button_frame_1 = RadioButtonFrame(self, header_name="RadioButtonFrame 1")
#         self.radio_button_frame_1.grid(row=0, column=0, padx=20, pady=20)

#         self.frame_1_button = customtkinter.CTkButton(self, text="Print value of frame 1", command=self.print_value_frame_1)
#         self.frame_1_button.grid(row=1, column=0, padx=20, pady=10)

#     def print_value_frame_1(self):
#         print(f"Frame 1 value: {self.radio_button_frame_1.get_value()}")

# class RadioButtonFrame(customtkinter.CTkFrame):
#     def __init__(self, *args, header_name="RadioButtonFrame", **kwargs):
#         super().__init__(*args, **kwargs)
        
#         self.header_name = header_name

#         self.header = customtkinter.CTkLabel(self, text=self.header_name)
#         self.header.grid(row=0, column=0, padx=10, pady=10)

#         self.radio_button_var = customtkinter.StringVar(value="")

#         self.radio_button_1 = customtkinter.CTkRadioButton(self, text="Option 1", value="Option 1", variable=self.radio_button_var)
#         self.radio_button_1.grid(row=1, column=0, padx=10, pady=10)
#         self.radio_button_2 = customtkinter.CTkRadioButton(self, text="Option 2", value="Option 2", variable=self.radio_button_var)
#         self.radio_button_2.grid(row=2, column=0, padx=10, pady=10)
#         self.radio_button_3 = customtkinter.CTkRadioButton(self, text="Option 3", value="Option 3", variable=self.radio_button_var)
#         self.radio_button_3.grid(row=3, column=0, padx=10, pady=(10, 20))

#     def get_value(self):
#         """ returns selected value as a string, returns an empty string if nothing selected """
#         return self.radio_button_var.get()

#     def set_value(self, selection):
#         """ selects the corresponding radio button, selects nothing if no corresponding radio button """
#         self.radio_button_var.set(selection)

# if __name__ == "__main__":
#     app = App()
#     app.mainloop()

import customtkinter as ctk
import tkinter as tk

root = tk.Tk()
frame = ctk.CTkScrollableFrame(root)
frame.pack()

# Test destruction
frame.destroy()

root.mainloop()

tk.Entry(validate='key')