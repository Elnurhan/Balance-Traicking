import os
import json
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from tkinter import *


SAVE_PATH = 'saves.json'

class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.title('MoneyTrack')
        self.geometry('800x400')
        self.resizable(width=False, height=False)

        self.balance = 0
        self.history = []

        # Ищем сохранения.
        if os.path.exists(SAVE_PATH):
            with open(SAVE_PATH, 'r') as f:
                data = json.loads(f.read())
                print(data['Balance'])
                print(data['History'])
                self.balance = data['Balance']
                self.history = data['History']
                print(type(self.balance))

        self.header_label = Label(text='Отслеживание баланса', font=('Arial Bold', 35))
        self.header_label.place(relx=.13, rely=.0)

        self.input_label = Label(text='Введите сумму:')
        self.input_label.place(relx=.05, rely=.15)

        self.input_entry = Entry(textvariable=self.balance)
        self.input_entry.place(relx=.2, rely=.15)

        self.input_button = Button(text='Внести')
        self.input_button.place(relx=.05, rely=.21)
        self.input_button.bind('<Button-1>', self.balance_add)

        self.chart_button = Button(text='Построить график')
        self.chart_button.place(relx=.15, rely=.21)
        self.chart_button.bind('<Button-1>', self.create_chart)

        self.current_balance_label = Label(text=f'Ваш баланс: {self.balance}', fg='green', font=('Arial Bold', 20))
        self.current_balance_label.place(relx=.05, rely=.9)

        self.history_label = Label(text='История: ', font=('Arial Bold', 15))
        self.history_label.place(relx=.05, rely=.3)

        self.history_listbox = Listbox(width=10, height=8)
        self.history_listbox.place(relx=.05, rely=.38)
        # Если есть сохраненная история, то заполняем ею ListBox
        if len(self.history):
            self.history.reverse()
            for i in self.history:
                self.history_listbox.insert(0, i)


    def balance_add(self, event):
        '''
        Функция для добавления денег в текущий баланс.
        '''
        money = int(self.input_entry.get())
        current_balance = int(self.current_balance_label['text'][12:])
        new_balance = str(current_balance + money)
        self.current_balance_label['text'] = f'Ваш баланс: {new_balance}'
        # Обновим историю
        self.history_listbox.insert(0, money)

    def create_chart(self, event):
        '''
        Функция для создания графика, исходя из операций пользователя
        '''
        data = []
        for i in range(0, self.history_listbox.size()):
            data.append(self.history_listbox.get(i))
        f = Figure(figsize=(5, 3.3), dpi=100)
        a = f.add_subplot(111)
        data.reverse()
        a.plot(data)

        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()

        canvas.get_tk_widget().place(relx=.43, rely=.15)
        
    def on_exit(self):
        '''
        Функция выполняемая при выходе из приложения.
        Она сохраняет данные в JSON-формате, на компьютере,
        Чтобы в дальнейшем загружать этот файл при открытии
        '''
        print('let\'s do something')
        with open("saves.json", 'w') as f:
            # В истории будет хранится не более 20 операций
            history = [self.history_listbox.get(i) for i in range(0, self.history_listbox.size())]
            if len(history) > 20:
                tmp = {'Balance': self.current_balance_label['text'][12:], 'History': history[:20]}
            else:
                tmp = {'Balance': self.current_balance_label['text'][12:], 'History': history}
            tmp_json = json.dumps(tmp)
            print(tmp_json)
            f.write(tmp_json)
        self.destroy()


if __name__ == '__main__':
    root = Root()
    root.protocol("WM_DELETE_WINDOW", root.on_exit)
    root.mainloop()