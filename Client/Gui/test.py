from tkinter import *


class mainwindow(Tk):
    def __init__(self, title):
        self.seconds = 0
        self.minutes = 0
        self.hours = 0
        self.text = "%02d:%02d:%02d" % (self.hours, self.minutes, self.seconds)
        self.carry_on = True

        self.master = Tk()
        self.master.title(title)

        # set up a main frame
        self.window = Frame(self.master, bd=0, relief=SUNKEN)
        self.window.grid(column=0, row=0)

        self.ScoreL = Label(self.window, text=self.text)
        self.ScoreL.grid(row=0, column=0, sticky='NSWE', padx=5, pady=5)

        self.master.mainloop()

    def update(self):
        self.seconds += 1
        if self.seconds == 60:
            self.seconds = 0
            self.minutes += 1
        if self.minutes == 60:
            self.minutes = 0
            self.hours += 1
        self.text = "%02d:%02d:%02d" % (self.hours, self.minutes, self.seconds)
        self.ScoreL.configure(text=self.text)
        if self.carry_on == True:
            # schedule next update 1 second later
            self.master.after(1000, self.update)

    def start(self):
        self.seconds = 0
        self.minutes = 0
        self.hours = 0
        self.carry_on = True
        self.master.after(1000, self.update)

    def stop(self):
        self.carry_on = False


if __name__ == '__main__':
    mainwin = mainwindow("Timer")
