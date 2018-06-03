import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os, json, sys, random, time
from sys import platform

window = tk.Tk()
window.geometry('500x800+500+500')
window.title('QuizCreator')
window.resizable(False, False)
window.configure(background = 'olive drab')

try:
    from num2words import num2words
except ImportError:
    if messagebox.askyesno('ImportFix', 'There are missing dependencies needed for the program to work (module "num2words"). Would you like the program to install them?') == True:    
        import subprocess
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--user', 'num2words==0.5.6'])
        from num2words import num2words
    else:
        sys.exit()

windowTitle = ''
widgetPositions = [20, 20]
YforAdd = 20
itera = 0
iter2 = 1
Questions = [] # stores a list of button objects
Questions_Two = [] # used to dynamically create variables, which will correspond to another button
Question_List = {}
data = {}
load_data = ''
correct_ans_int = 0
questionName = ''
correctans = 0
incorrectans = 0

# I.E. "One" in Questions_Two is a variable and corresponds to "One" in Questions

path = path = os.path.dirname(os.path.abspath(__file__))

# Creates and Manages Widget Questions
class Widget():

    def __init__(self, name, Q):
        self.name = name
        self.questions = Q
        self.questions.append(name)

    def initialize(self, index, imported):
        if imported == False:
            pass
        elif imported == True:
            self.indexNum = index
            self.questions[self.indexNum] = tk.Button(window, text = '', command = lambda: self.reRoute(self.indexNum))
            self.questions[self.indexNum].place(x = widgetPositions[0], y = widgetPositions[1])
            self.questions[self.indexNum].config(width = 54)
            self.fix_imports()
            return

        self.indexNum = index
        self.questions[self.indexNum] = tk.Button(window, text = '', command = lambda: self.reRoute(self.indexNum))
        self.questions[self.indexNum].place(x = widgetPositions[0], y = widgetPositions[1])
        self.questions[self.indexNum].config(width = 54)

        def destroy(event, var):
            global Question_List, questionName
            questionName = var.get()
            Question_List[self.indexNum + 1] = var.get()
            self.questions[self.indexNum].config(text = var.get().title())
            var.destroy()
            print(Question_List)

        temp = tk.Entry(window)
        temp.place(x = widgetPositions[0] + 50, y = widgetPositions[1] + 4)
        temp.bind('<Return>', lambda event, var = temp: destroy(event, temp))
        
    def reRoute(self, index):
        self.editWidget(index)

    def editWidget(self, index):  

        def on_closing():
            temporary = 'Question_' + str(self.indexNum + 1)
            data[temporary] = []
            data[temporary].append({
                'Title' : questionName,
                'Answer_One' : Q1.get(),
                'Answer_Two' : Q2.get(),
                'Answer_Three' : Q3.get(),
                'Answer_Four' : Q4.get(),
                'Correct' : str(correct_ans_int),
            })    
            with open(path + '/' + windowTitle + '.json', 'w') as outfile:
                json.dump(data, outfile, indent = 2)
            edit.destroy()

        def modify(number, button):
            global correct_ans_int
            if button['background'] == 'green':
                button.config(background = AddWidget.cget('bg'))
            else:
                button.config(background = 'green', activebackground = 'green')
                correct_ans_int = number

        def on_open():
            newname = 'Question_' + str(self.indexNum + 1)
            if os.stat(path + '/' + windowTitle + '.json').st_size > 0:
                with open(path + '/' + windowTitle + '.json', 'r') as handle:
                    load_data = json.load(handle)
                    if newname in load_data:
                        for parse in load_data[newname]:
                            V1.set(parse['Answer_One'])
                            V2.set(parse['Answer_Two'])
                            V3.set(parse['Answer_Three'])
                            V4.set(parse['Answer_Four'])
                            modify(parse['Correct'], button_data[int(parse['Correct'])])
                    else:
                        pass
            else:
                pass

        edit = tk.Toplevel()
        edit.geometry('400x300')
        edit.title('Edit Question # ' + str(self.indexNum + 1))
        edit.resizable(False, False)
        edit.configure(background = 'chocolate')
        edit.protocol("WM_DELETE_WINDOW", on_closing)
        try:
            question_title = tk.Label(edit, text = Question_List[self.indexNum + 1].title(), relief = 'sunken', width = 50)
        except KeyError:
            edit.destroy()
            return
        instructions = tk.Label(edit, background = 'dark slate gray', text = 'Once all answers have been added, select \na correct answer with the check marks beside them.\n[Only one answer can be selected]', relief = 'groove', width = 50)
        V1 = tk.StringVar()
        V2 = tk.StringVar()
        V3 = tk.StringVar()
        V4 = tk.StringVar()
        Q1 = tk.Entry(edit, width = 10, textvariable = V1)
        Q2 = tk.Entry(edit, width = 10, textvariable = V2)
        Q3 = tk.Entry(edit, width = 10, textvariable = V3)
        Q4 = tk.Entry(edit, width = 10, textvariable = V4)
        A1 = tk.Button(edit, text = u'\u2713', width = 1, command = lambda: modify(1, A1))
        A2 = tk.Button(edit, text = u'\u2713', width = 1, command = lambda: modify(2, A2))
        A3 = tk.Button(edit, text = u'\u2713', width = 1, command = lambda: modify(3, A3))
        A4 = tk.Button(edit, text = u'\u2713', width = 1, command = lambda: modify(4, A4))

        question_title.place(relx=0.5, anchor = 'n')
        instructions.place(x = 0, y = 40)
        Q1.place(x = 110, y = 100)
        Q2.place(x = 210, y = 100)
        Q3.place(x = 110, y = 130)
        Q4.place(x = 210, y = 130)
        A1.place(x = 70, y = 97)
        A2.place(x = 300, y = 97)
        A3.place(x = 70, y = 127)
        A4.place(x = 300, y = 127)

        button_data = {
            1 : A1,
            2 : A2,
            3 : A3,
            4 : A4
        }

        on_open()

    def fix_imports(self):
        with open(path + '/' + windowTitle + '.json', 'r') as fix:
            importData = json.load(fix)
            newname = 'Question_' + str(self.indexNum + 1)
            for parse in importData[newname]:
                Question_List[self.indexNum + 1] = parse['Title']
                print(Question_List)
                self.questions[self.indexNum].config(text = parse['Title'].title())

# Initialize Class 
def W_init(name, did_import):
    global widgetPositions, itera
    name.initialize(itera, did_import)
    widgetPositions[1] += 30
    itera += 1
# Create Question Widgets
def create_widget():
    global Questions_Two, AddWidget, YforAdd, iter2
    dynamicName = num2words(iter2).title()
    Questions_Two.append(dynamicName)
    Questions_Two[itera] = Widget(dynamicName, Questions)
    W_init(Questions_Two[itera], False)
    YforAdd += 30
    iter2 += 1
    AddWidget.place_configure(y = YforAdd)
#When Done...
def finish_edits():
    questionplay = []
    ready = tk.Toplevel() 
    newx = 0

    ready.title('Play Quiz - ' + windowTitle)
    ready.geometry('500x500')
    ready.resizable(False, False)
    ready.attributes("-topmost", True)
    ready.configure(background = 'gray20')

    with open(path + '/' + windowTitle + '.json', 'r') as toPlay:
        playData = json.load(toPlay)
        for x in range(len(playData) - 1):
            questionplay.append('Question_' + str(x + 1))
        random.shuffle(questionplay)

        def checkifCorrect(ansNum):
            global correctans, incorrectans
            if ansNum == int(playData[questionplay[newx]][0]['Correct']):
                correctans += 1
                questionplay.pop(0)
                if len(questionplay) == 0:
                    Ans1.destroy()
                    Ans2.destroy()
                    Ans3.destroy()
                    Ans4.destroy()
                    centeredQ.config(text = 'You got {0}\n\n{1} Correct, {2} Incorrect'.format(str((correctans / (correctans + incorrectans)) * 100) + '%', correctans, incorrectans))
                    centeredQ.config(width = 20, height = 4)
                    time.sleep(0.1)
                else:
                    newQ()
            else:
                incorrectans += 1
                questionplay.pop(0)
                if len(questionplay) == 0:
                    Ans1.destroy()
                    Ans2.destroy()
                    Ans3.destroy()
                    Ans4.destroy()
                    centeredQ.config(text = 'You got {0}\n\n{1} Correct, {2} Incorrect'.format(str((correctans / (correctans + incorrectans)) * 100) + '%', correctans, incorrectans))
                    centeredQ.config(width = 20, height = 4)
                    time.sleep(0.1)
                else:
                    newQ()

        centeredQ = tk.Label(ready, text = playData[questionplay[newx]][0]['Title'], relief = 'raised', background = 'dark slate gray', fg = 'ivory')
        centeredQ.place(relx = 0.5, y = 80, anchor = 'center')
        centeredQ.config(height = 2)

        def newQ():
            centeredQ.config(text = playData[questionplay[newx]][0]['Title'])
            Ans1.config(text = playData[questionplay[newx]][0]['Answer_One'])
            Ans2.config(text = playData[questionplay[newx]][0]['Answer_Two'])
            Ans3.config(text = playData[questionplay[newx]][0]['Answer_Three'])
            Ans4.config(text = playData[questionplay[newx]][0]['Answer_Four'])

        Ans1 = tk.Button(ready, text = playData[questionplay[newx]][0]['Answer_One'], command = lambda: checkifCorrect(1))
        Ans2 = tk.Button(ready, text = playData[questionplay[newx]][0]['Answer_Two'], command = lambda: checkifCorrect(2))
        Ans3 = tk.Button(ready, text = playData[questionplay[newx]][0]['Answer_Three'], command = lambda: checkifCorrect(3))
        Ans4 = tk.Button(ready, text = playData[questionplay[newx]][0]['Answer_Four'], command = lambda: checkifCorrect(4))

        Ans1.config(width = 28, height = 7)
        Ans2.config(width = 28, height = 7)
        Ans3.config(width = 28, height = 7)
        Ans4.config(width = 28, height = 7)

        Ans1.place(x = 0, y = 200)
        Ans2.place(x = 250, y = 200)
        Ans3.place(x = 0, y = 310)
        Ans4.place(x = 250, y = 310)            

#Import Files
def import_file():
    global windowTitle, new
    global Questions_Two, AddWidget, YforAdd, iter2
    name = filedialog.askopenfilename(initialdir = path, title = 'Select File', filetypes = (("text files","*.json"),("all files","*.*")))
    with open(name, 'r+') as newfile:
        newdata = json.load(newfile)
        windowTitle = newdata['NameOfFile'][0]
        for a in range(len(newdata) - 1):
            dynamicName = num2words(iter2).title()
            Questions_Two.append(dynamicName)
            Questions_Two[itera] = Widget(dynamicName, Questions)
            W_init(Questions_Two[itera], True)
            YforAdd += 30
            iter2 += 1
            AddWidget.place_configure(y = YforAdd)
    window.title('QuizCreator - ' + windowTitle)
    new.destroy()

#Create New File
def newfilecreation(item, item_2, root):
    item.destroy()
    item_2.destroy()

    def finish(entry):
        global windowTitle, window, data
        windowTitle = entry.get().title()
        window.title('QuizCreator - ' + windowTitle)
        try:
            os.mknod(path + '/' + windowTitle + '.json')
        except AttributeError:
            f = open(path + '/' + windowTitle + '.json', 'w+')
            f.close()
        with open(path + '/' + windowTitle + '.json', 'w') as name:
            data['NameOfFile'] = [windowTitle]
            json.dump(data, name)
        labelEntry.destroy()
        done.destroy()
        root.destroy()

    nameofFile = tk.Entry(root)
    nameofFile.place(relx = 0.5, rely = 0.5, anchor = 'center')
    labelEntry = tk.Label(root, text = 'Name of Quiz', relief = 'raised')
    labelEntry.place(x = 200, y = 60)
    done = tk.Button(root, text = 'Done', command = lambda: finish(nameofFile))
    done.place(x = 212, y = 170)

#Buttons on Main
AddWidget = tk.Button(window, text = u"\u2795", highlightbackground = 'sienna', command = create_widget)
Present = tk.Button(window, text = 'Save&Play', command = finish_edits)

AddWidget.place(x = 232, y = YforAdd)
Present.place(x = 222, y = 770.)

#Import or Continue? First Window
new = tk.Toplevel()
new.title('Select Option')
new.geometry('480x200+510+300')
new.resizable(False, False)
new.configure(background = 'sienna4')
new.attributes("-topmost", True)

Import = tk.Button(new, text = 'Import File', command = import_file)
Newfile = tk.Button(new, text = 'New File',  command = lambda: newfilecreation(Newfile, Import, new))
Help = tk.Text(new, height = 3, borderwidth = 0, relief = 'raised', background = 'dark slate gray', cursor = 'hand2')
Help.tag_configure('center', justify = 'center')
Help.insert(1.0, 'For help, go to\nhttps://github.com/Rohan-Bansal/quiz-creator/wiki/Using-The-Creator')
Help.tag_add("center", "1.0", "end")
Help.configure(state="disabled")

Help.place(relx = 0.5, anchor = 'n')
Import.place(x = 140, y = 100)
Newfile.place(x = 240, y = 100)

window.mainloop()
