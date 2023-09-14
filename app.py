
import sqlite3
from tkinter import ttk
from tkinter import *
class Card_class:
    db = 'database/Cards.db'
    def __init__(self, root):
        
        self.windows = root
        self.windows.title('Magic the gathering')
        self.windows.resizable(1,1)
        self.windows.wm_iconbitmap('sources/icon.ico')
        self.windows.resizable(1,1)
        frame = LabelFrame(self.windows, text = "Add new card")
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)
        #Label name
        self.label_name = Label(frame, text="Name: ")
        self.label_name.grid(row=1, column=0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row=1, column=1)
        #label expansion
        self.label_expansion = Label(frame, text="Expansion: ")
        self.label_expansion.grid(row=2, column=0)
        self.expansion = Entry(frame)
        self.expansion.grid(row=2, column=1)
        #label rarity
        self.label_rarity = Label(frame, text="Rarity: ")
        self.label_rarity.grid(row=3, column=0)
        self.rarity = Entry(frame)
        self.rarity.grid(row=3, column=1)
        #label language
        self.label_language = Label(frame, text="Language: ")
        self.label_language.grid(row=4, column=0)
        self.language = Entry(frame)
        self.language.grid (row=4, column=1)
        #label quantity
        self.label_quantity = Label(frame, text="Quantity: ")
        self.label_quantity.grid(row=5, column=0)
        self.quantity = Entry(frame)
        self.quantity.grid (row=5, column=1)
        #button save
        self.button_add = ttk.Button(frame, text = "Save card", command = self.add_card)
        self.button_add.grid(row=6, columnspan = 2, sticky = W + E)
        #card table
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 11))
        style.configure("mystyle.Treeview.Heading", font=("Calibri", 13, "bold"))
        style.layout("mystyle.Treeview", [("mystyle.Treeview.treearea", {'sticky':'nswe'})])
        #table form
        self.table = ttk.Treeview(height = 20, columns = ('Expansion', 'Rarity', 'Language', 'Quantity'), style="mystyle.Treeview")
        self.table.grid(row = 7, column = 0, columnspan = 2)
        self.table.heading('#0', text='Name', anchor = CENTER)
        self.table.heading('Expansion', text='Expansion', anchor = CENTER)
        self.table.heading('Rarity', text='Rarity', anchor = CENTER)
        self.table.heading('Language', text='Language', anchor = CENTER)
        self.table.column('Quantity', width=100)
        self.table.heading('Quantity', text='Quantity', anchor = CENTER)
        self.get_cards()
        #button delete
        button_delete = ttk.Button(text = 'DELETE', command = self.del_card)
        button_delete.grid(row = 8, column = 0, sticky = W + E)
        #informative message
        self.message = Label(text = '', fg = 'red')
        self.message.grid(row = 7, column = 0, columnspan = 2, sticky = W + E)
        #key enter
        self.windows.bind('<Return>', self.on_enter_press)
    
    
    def db_consulta(self, consulta, parametros = ()):
        with sqlite3.connect(self.db) as con:
            cursor = con.cursor()
            resultado = cursor.execute(consulta, parametros)
            con.commit()
        return resultado
    
    
    def get_cards(self):
        registros_tabla = self.table.get_children()
        for fila in registros_tabla:
            self.table.delete(fila)
        query = 'SELECT * FROM Cards ORDER BY name DESC'
        registros = self.db_consulta(query)
        
        for fila in registros:
            print(fila)
            self.table.insert('', 0, text = fila[0], values = (fila[1], fila[2], fila[3], fila[4]))

    
    
    
    def add_card(self):
        name_card = self.name.get().capitalize()
        if (Validator.is_non_empty(self.name) and Validator.is_non_empty(self.expansion) and Validator.is_non_empty(self.rarity) and Validator.is_non_empty(self.language) and Validator.is_non_empty(self.quantity)):
            query = 'SELECT * FROM Cards WHERE name = ?'
            existing_card = self.db_consulta(query, (name_card,)).fetchone()

            if existing_card:
                query = 'UPDATE Cards SET quantity = quantity + 1 WHERE name = ?'
                self.db_consulta(query, (self.name.get(),))
                self.message['text'] = 'Quantity of card {} increased by 1'.format(self.name.get())
            else:
                query_insert = 'INSERT INTO Cards VALUES(?,?,?,?,?)'
                parameters = (self.name.get(), self.expansion.get(), self.rarity.get(), self.language.get(), self.quantity.get())
                self.db_consulta(query_insert, parameters)
                self.message['text'] = 'Cards {} added'.format(self.name.get())
             
            self.name.delete(0, END)
            self.expansion.delete(0, END)
            self.rarity.delete(0, END)
            self.language.delete(0, END)
            self.quantity.delete(0, END)
        else:
            print('Missing data')
            self.message['text'] = 'Missing data'
        
        self.get_cards()
    
    def del_card(self):
        self.message['text'] = ''
        try:
            self.table.item(self.table.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'Select a card'
            return
        self.message['text'] = ''
        name = self.table.item(self.table.selection())['text']
        query = 'DELETE FROM Cards WHERE name = ?'
        self.db_consulta(query, (name,))
        self.message['text'] = 'Card {} deleted'.format(name)
        self.get_cards()
        
    
    def on_enter_press(self, event):
        self.add_card()


class Validator:
    @staticmethod
    def is_non_empty(entry_widget):
        """Validate if the provided widget has non-empty content"""
        return len(entry_widget.get()) != 0



if __name__ == '__main__':
    root = Tk()
    root.configure(bg="#000000")
    app = Card_class(root)
    root.mainloop()
