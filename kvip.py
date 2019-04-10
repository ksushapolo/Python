from tkinter import Tk, PhotoImage, Label, Button, LEFT


isNotWork = True
health = 100
food = 100
mood = 100
knowledge = 0


root = Tk()
root.title("Kvip")
root.geometry("800x800")


def start(event):
    global isNotWork
    if isNotWork == False:
        pass
    else:
        startLabel.config(text="")
        updatedisplay()
        updatehealth()
        updatemood()
        updatefood()
        updateknowledge()
        isNotWork = False


root.bind('<Return>', start)

normal = PhotoImage(file="normal.png")
theend = PhotoImage(file="theend.png")
wanttoeat = PhotoImage(file="wanttoeat.png")
eat = PhotoImage(file="eat.png")
boring = PhotoImage(file="boring.png")
funny = PhotoImage(file="funny.png")
ill = PhotoImage(file="ill.png")
school = PhotoImage(file="school.png")
sleep = PhotoImage(file="sleep.png")
sport = PhotoImage(file="sport.png")


def updatedisplay():
    global food
    global health
    global mood
    global knowledge
    if real():
        if health <= 25:
            normalLabel.config(image=ill)
        elif food <= 50:
                normalLabel.config(image=wanttoeat)
        elif mood <= 75:
            normalLabel.config(image=boring)
        else:
            normalLabel.config(image=normal)
    else:
        normalLabel.config(image=theend)
        return
    foodLabel.config(text="Food:" + str(food))
    moodLabel.config(text="Mood:" + str(mood))
    healthLabel.config(text="Health:" + str(health))
    knowledgeLabel.config(text="Knowledge:" + str(knowledge))
    normalLabel.after(1000, updatedisplay)


def updatehealth():
    global health
    health -= 1
    if real():
        normalLabel.after(2000, updatehealth)
    else:
        return


def updatefood():
    global food
    food -= 1
    if real():
        normalLabel.after(1000, updatefood)
    else:
        return


def updatemood():
    global mood
    mood -= 1
    if real():
        normalLabel.after(500, updatemood)
    else:
        return


def updateknowledge():
    global knowledge
    knowledge += 1
    if real():
        normalLabel.after(5000, updateknowledge)
    else:
        return


def real():
    global health
    global food
    global mood
    if health == 0 or mood == 0 or food == 0:
        startLabel.config(text="You are the worst friend I've ever had. I'll go away!")
        normalLabel.config(image=theend)
        return False
    else:
        return True


def feed():
    global food
    if real():
        food += 25
        normalLabel.config(image=eat)
        normalLabel.after(1000000, updatedisplay)
    else:
        return


def sleeping():
    global health
    if real():
        health += 20
        normalLabel.config(image=sleep)
        normalLabel.after(1000000, updatedisplay)
    else:
        return


def treat():
    global health
    if real():
        health += 30
        normalLabel.config(image=sport)
        normalLabel.after(1000000, updatedisplay)
    else:
        return


def havefun():
    global mood
    if real():
        mood += 20
        normalLabel.config(image=funny)
        normalLabel.after(1000000, updatedisplay)
    else:
        return


def teach():
    global knowledge
    if real():
        knowledge += 1
        normalLabel.config(image=school)
        normalLabel.after(1000000, updatedisplay)


startLabel = Label(root, text="Press Enter to Start!")
btn_start = Button()
healthLabel = Label(root, text="Health:" + str(health))
foodLabel = Label(root, text="Food:" + str(food))
moodLabel = Label(root, text="Mood:" + str(mood))
knowledgeLabel = Label(root, text="Knowledge:" + str(knowledge))


normalLabel = Label(root, image=normal)


btn_eat = Button(root, text="Feed!", command=feed)
btn_sleep = Button(root, text="Sleep!", command=sleeping)
btn_havefun = Button(root, text="Have fun!", command=havefun)
btn_treat = Button(root, text="Treat!", command=treat)
btn_teach = Button(root, text="Teach!", command=teach)


startLabel.pack()
healthLabel.pack()
foodLabel.pack()
moodLabel.pack()
knowledgeLabel.pack()
normalLabel.pack()
btn_eat.pack(padx=55, pady=30, side=LEFT)
btn_havefun.pack(padx=55, pady=30, side=LEFT)
btn_sleep.pack(padx=55, pady=30, side=LEFT)
btn_teach.pack(padx=55, pady=30, side=LEFT)
btn_treat.pack(padx=55, pady=30, side=LEFT)


root.mainloop()
