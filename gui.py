from tkinter import *
import messagebox


class GUI:
    values = []

    def __init__(self):
        self.values = []
        self.window = Tk()

        self.window.config(padx=40, pady=20, bg="white")
        self.window.title("Amazon Deal Finder")

        self.canvas = Canvas(width=500, height=210, highlightthickness=0)
        self.amzn_img = PhotoImage(file="Deal Finder.png")
        self.canvas.create_image(250, 105, image=self.amzn_img)
        self.canvas.grid(column=0, row=0, columnspan=2)

        self.asin_label = Label(text="Enter the Product: ")
        self.asin_label.grid(column=0, row=1)

        self.asin_id = Entry()
        self.asin_id.grid(column=1, row=1)

        self.start_button = Button(text="Find Deal (SMS Notified/24hrs)", command=self.assign_values)
        self.start_button.grid(row=2, column=0, columnspan=2, pady=20)

        self.window.mainloop()

    def assign_values(self):
        self.values.append(self.asin_id.get())
        self.window.destroy()

    def failed(self):
        messagebox.showinfo(title="Error", message="Please try again!")

    def succeed(self):
        messagebox.showinfo(title="Success!", message=f"The product {self.values[0]}'s deals will be found"
                                                      f" and sent to you at 12:00 AM EST every day!")
