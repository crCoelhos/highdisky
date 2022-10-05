import tkinter as tk
from tkinter import ttk
from tkinter import *
# from tkcalendar import Calendar
from tkinter import messagebox
from turtle import color
import sqlite3
from sqlite3 import Error, connect

import db_directives as db


# TO DO
# crud funcionarios
# crud generos musicais
# crud disco com valor

class Screen():
    def __init__(self, master, selected_mont=None):
        self.window = master
        self.window.title('HighDisk')
        self.window.geometry('750x850')
        self.window.minsize(1750, 850)
        # self.window.attributes('-fullscreen', True)
        self.window.state('zoomed')

        # frames
        self.frm_logo_view = tk.Frame(self.window)
        self.frm_logo_view.place(rely=0, relx=0.02, relwidth=0.758, relheight=0.164)

        self.frm_insert_on_tvw = tk.Frame(self.window)
        self.frm_insert_on_tvw.place(rely=0.28, relx=0.01, relwidth=0.23, relheight=0.35)

        self.frm_list_view = tk.Frame(self.window)
        self.frm_list_view.place(rely=0.28, relx=0.32, relwidth=0.5, relheight=0.55)

        self.frm_stock_view = tk.Frame(self.window)
        self.frm_stock_view.place(rely=0.01, relx=0.80, relwidth=0.4, relheight=0.85)

        # subframes
        self.frm_insert_genre = tk.Frame(self.frm_insert_on_tvw)
        self.frm_insert_genre.place(rely=0, relx=0)

        self.frm_insert_disk = tk.Frame(self.frm_insert_on_tvw)
        self.frm_insert_disk.place(rely=0.5, relx=0)

        self.frm_search = tk.Frame(self.frm_list_view)
        self.frm_search.place(relx=0, rely=0, relheight=0.15, relwidth=1)

        def product_in():
            pass

        

        def genre_insertion():
            genre_name = self.ent_insert_new_genre.get()
            if genre_name == '':
                messagebox.showwarning('Aviso', 'Necessario um nome e um genero principal!')
            else:
                sql_directive = f"INSERT INTO genre VALUES(NULL, '{genre_name}');"
                db.insert(sql_directive)
                # update_view()
                messagebox.showinfo('Aviso', 'Gênero registrado com sucesso!')
                self.ent_insert_disk_author.delete(0, 'end')
                self.cbb_genres.delete(0, 'end')

        def author_insertion():
            author_name = self.ent_insert_new_author.get()
            # if author_name == '':
            #     messagebox.showwarning('Aviso', 'Necessario um nome e um artista principal!')
            # else:
            sql_directive = f"INSERT INTO author VALUES(NULL, '{author_name}');"
            db.insert(sql_directive)               
            # messagebox.showinfo('Aviso', 'Artista cadastrado com sucesso!')

            # self.new_author_toplv.destroy()
            self.new_author_toplv.deiconify()
            


        def genre_registration():
            new_genre_toplv = tk.Toplevel()
            new_genre_toplv.geometry("250x250")
            new_genre_toplv.title("Cadastrar gênero")

            self.lbl_insert_new_genre = tk.Label(new_genre_toplv, text="Nome: ")
            self.lbl_insert_new_genre.grid(column=0, row=0)
            self.ent_insert_new_genre = tk.Entry(new_genre_toplv, width=25)
            self.ent_insert_new_genre.grid(column=1, row=0)

            self.btn_create_genre = tk.Button(new_genre_toplv, text='Inserir', command=genre_insertion)
            self.btn_create_genre.grid(column=1, row=4, columnspan=2)
        
        def author_registration():
            new_author_toplv = tk.Toplevel()
            new_author_toplv.geometry("250x250")
            new_author_toplv.title("Cadastrar artista")

            self.lbl_insert_new_author = tk.Label(new_author_toplv, text="Nome: ")
            self.lbl_insert_new_author.grid(column=0, row=0)
            self.ent_insert_new_author = tk.Entry(new_author_toplv, width=25)
            self.ent_insert_new_author.grid(column=1, row=0)

            self.btn_create_author = tk.Button(new_author_toplv, text='Inserir', command=author_insertion)
            self.btn_create_author.grid(column=1, row=4, columnspan=2)


        def product_registration():
            disk_name = self.ent_insert_disk_name.get()

            author_id_query = f"SELECT id FROM author WHERE author_name LIKE '{self.cbb_authors.get()}';"
            author_id = db.search(author_id_query)
            right_author_id = ''.join(map(str, (author_id[0])))

            genre_id_query = f"SELECT id FROM genre WHERE genre_name = '{self.cbb_genres.get()}';"
            genre_id = db.search(genre_id_query)
            right_genre_id = ''.join(map(str, (genre_id[0])))
            print(right_author_id, right_genre_id)



            year = ''.join(map(str,{self.ent_insert_disk_release_date.get()}))

            if author_id == '' and genre_id == '':
                messagebox.showwarning('Aviso', 'Necessario um nome e um genero principal!')
            else:
                sql_directive = f"INSERT INTO disk VALUES(NULL,'{disk_name}', '{right_author_id}', '{right_genre_id}', '{year}');"
                db.insert(sql_directive)
                update_view()
                
                messagebox.showinfo('Aviso', 'Disco inserido com sucesso!')
                # self.ent_insert_disk_author.delete(0, 'end')
                self.cbb_genres.delete(0, 'end')

        def product_create_product():
            product_toplv = tk.Toplevel()
            product_toplv.geometry("450x450")
            product_toplv.title("Criar Produto")
            selected_genre = tk.StringVar()
            selected_author = tk.StringVar()

            self.lbl_insert_disk_name = tk.Label(product_toplv, text="Nome: ")
            self.lbl_insert_disk_name.grid(column=0, row=0)
            self.ent_insert_disk_name = tk.Entry(product_toplv, width=25)
            self.ent_insert_disk_name.grid(column=1, row=0)

            self.lbl_insert_disk_author = tk.Label(product_toplv, text="Autor: ")
            self.lbl_insert_disk_author.grid(column=0, row=1)
            author_list = db.search('SELECT DISTINCT author_name FROM author')
            self.cbb_authors = ttk.Combobox(product_toplv, width=25, textvariable=selected_author, state="readonly" ,values = [data_author for data_author, in author_list])
            self.cbb_authors.grid(column=1, row=1)

            self.lbl_genre = tk.Label(product_toplv, text="Genero: ")
            self.lbl_genre.grid(column=0, row=2)
            genre_list = db.search('SELECT DISTINCT genre_name FROM genre')
            self.cbb_genres = ttk.Combobox(product_toplv, width=25, textvariable=selected_genre, state="readonly", values = [data_genre for data_genre, in genre_list])
            self.cbb_genres.grid(column=1, row=2)

            self.lbl_insert_disk_release_date = tk.Label(product_toplv, text="Ano: ")
            self.lbl_insert_disk_release_date.grid(column=0, row=3)
            self.ent_insert_disk_release_date = tk.Entry(product_toplv, width=4)
            self.ent_insert_disk_release_date.grid(column=1, row=3)

            # directive = f'INSERT INTO product {}'
            self.btn_create_product = tk.Button(product_toplv, text='Inserir', command=product_registration)
            self.btn_create_product.grid(column=1, row=4, columnspan=2)



        def product_edit_product():
            product_toplv = tk.Toplevel()
            product_toplv.geometry("450x450")
            product_toplv.title("Criar Produto")

        def product_add_product():
            product_toplv = tk.Toplevel()
            product_toplv.geometry("400x250")
            product_toplv.title("Inserir Produto")

            n = tk.StringVar()
            # isso aqui tem que virar a lista de discos pra adicionar quantidade em uma relação
            self.cbb_genres = ttk.Combobox(product_toplv, width=25, textvariable=n)
            self.cbb_genres['values'] = ('Rock', 'Rap', 'Indie', 'Pagode', 'Samba', 'MPB', 'Neo MPB', 'teste')
            self.cbb_genres.grid(column=0, row=0)

            self.lbl_quantity = tk.Label(product_toplv, text="Quantidade: ")
            self.lbl_quantity.grid(column=1, row=0)
            self.ent_quantity = tk.Entry(product_toplv, width=5)
            self.ent_quantity.grid(column=2, row=0)

            self.btn_insert_genre = tk.Button(product_toplv, text='Inserir')
            self.btn_insert_genre.grid(column=1, row=1, columnspan=1)

        #menu

        self.menu_bar = Menu(self.window)
        self.window.config(menu=self.menu_bar)

        self.config_menu = Menu(self.menu_bar, tearoff=0)
        self.config_menu.add_command(label="Sair", command=self.window.quit)
        self.menu_bar.add_cascade(label="Configurações", menu=self.config_menu)

        self.product_menu = Menu(self.menu_bar, tearoff=0)
        self.product_menu.add_command(label="Criar produto", command=product_create_product)
        self.product_menu.add_command(label="Editar produto", command=product_edit_product)
        self.product_menu.add_command(label="Adicionar produto", command=product_add_product)
        self.menu_bar.add_cascade(label="Produtos", menu=self.product_menu)

        self.genre_menu = Menu(self.menu_bar, tearoff=0)
        self.genre_menu.add_command(label="Adicionar genero", command=genre_registration)
        self.genre_menu.add_command(label="Editar genero")
        self.menu_bar.add_cascade(label="Generos", menu=self.genre_menu)

        self.author_menu = Menu(self.menu_bar, tearoff=0)
        self.author_menu.add_command(label="Adicionar autor", command=author_registration)
        self.author_menu.add_command(label="Editar autor")
        self.menu_bar.add_cascade(label="Autor", menu=self.author_menu)

        self.user_menu = Menu(self.menu_bar, tearoff=0)
        self.user_menu.add_command(label="Criar usuario")
        self.user_menu.add_command(label="Editar usuario")
        self.user_menu.add_command(label="Remover usuario")
        self.user_menu.add_command(label="Logout")
        self.menu_bar.add_cascade(label="Usuarios", menu=self.user_menu)

        self.preferences_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Preferencias", menu=self.preferences_menu)





        #content

        # logo_view content
        self.lbl_logo = tk.Label(self.frm_logo_view, text="PLACEHOLDER", background="orange")
        self.lbl_logo.place(rely=0.1, relx=0.05, relheight=0.9, relwidth=0.125)
        self.lbl_bus_name = tk.Label(self.frm_logo_view, text="HighDisk", background="red")
        self.lbl_bus_name.place(rely=0.1, relx=0.41, relheight=0.9, relwidth=0.55)


        # frm_insert_on_tvw content
        # self.lbl_insert_genre = tk.Label(self.frm_insert_genre, text='Insira um genero', background='yellow')
        # self.lbl_insert_genre.grid(column=0, row=0)
        # self.ent_insert_genre = tk.Entry(self.frm_insert_genre, width=25)
        # self.ent_insert_genre.grid(column=1, row=0)

        # var1 = tk.IntVar()
        # self.cbx_is_subgenre = tk.Checkbutton(self.frm_insert_genre, text='Subgenre', variable=var1, onvalue=1, offvalue=0)
        # self.cbx_is_subgenre.grid(column=1, row=1)
        # self.btn_insert_genre = tk.Button(self.frm_insert_genre, text='Inserir')
        # self.btn_insert_genre.grid(column=1, row=2)

        # self.lbl_insert_disk = tk.Label(self.frm_insert_disk, text="Nome do disco: ", background='purple')
        # self.lbl_insert_disk.grid(column=0, row=0)
        # self.ent_insert_disk_name = tk.Entry(self.frm_insert_disk, width=25)
        # self.ent_insert_disk_name.grid(column=1, row=0)

        # self.lbl_insert_disk_author = tk.Label(self.frm_insert_disk, text="Autor: ")
        # self.lbl_insert_disk_author.grid(column=0, row=1)
        # self.ent_insert_disk_author = tk.Entry(self.frm_insert_disk, width=25)
        # self.ent_insert_disk_author.grid(column=1, row=1)

        # self.lbl_gerne = tk.Label(self.frm_insert_disk, text="Genero: ")
        # self.lbl_gerne.grid(column=0, row=2)
        # n = tk.StringVar()
        # self.cbb_genres = ttk.Combobox(self.frm_insert_disk, width=25, textvariable=n)
        # self.cbb_genres['values'] = ('Rock', 'Rap', 'Indie', 'Pagode', 'Samba', 'MPB', 'Neo MPB', 'teste')
        # self.cbb_genres.grid(column=1, row=2)

        # frm_list_view content
        self.ent_generic_search = tk.Entry(self.frm_search, width=15)
        self.ent_generic_search.grid(column=0, row=0)

        to_search_selected_genre = tk.StringVar()
        self.to_search_genre_list = db.search('SELECT DISTINCT genre_name FROM genre')
        self.cbb_to_search_genres = ttk.Combobox(self.frm_search, width=25, textvariable=to_search_selected_genre, values=[data for data, in self.to_search_genre_list])
        self.cbb_to_search_genres.grid(column=2, row=0)

        self.lbl_placeholder_DATEPICKER = tk.Label(self.frm_search, text="ANO", background='pink')
        self.lbl_placeholder_DATEPICKER.grid(column=3, row=0)

        # frm_list_view content

        columns = ["ID", "nome", "autor", "genero", "ano"]
        self.tvw_disk_list = ttk.Treeview(self.frm_list_view, columns=columns, show="headings")
        self.tvw_disk_list.place(rely=0.1, relx=0, relheight=0.7, relwidth=0.95)

        self.tvw_disk_list.heading("ID", text="ID")
        self.tvw_disk_list.heading("nome", text="Nome")
        self.tvw_disk_list.heading("autor", text="Autor")
        self.tvw_disk_list.heading("genero", text="Genero")
        self.tvw_disk_list.heading("ano", text="Ano")

        self.tvw_disk_list.column('ID', minwidth=0, width=3)
        self.tvw_disk_list.column('nome', minwidth=0, width=60)
        self.tvw_disk_list.column('autor', minwidth=0, width=60)
        self.tvw_disk_list.column('genero', minwidth=0, width=60)
        self.tvw_disk_list.column('ano', minwidth=0, width=5)

        def update_view():
            for i in self.tvw_disk_list.get_children():
                self.tvw_disk_list(i)

            #directives
            length = db.search("SELECT DISTINCT COUNT(*) FROM disk, genre, author WHERE fk_author = author.id and fk_genre = genre.id")
            length = ''.join(map(str, (length[0])))
            sql_directive = "SELECT DISTINCT disk.id, disk_name, author_name, genre_name, year FROM disk, genre, author WHERE fk_author = author.id AND fk_genre = genre.id"
            data = db.search(sql_directive)
            # print(data)
            # print(f"total de discos: {length}")
            for item in data:
                self.tvw_disk_list.insert('', tk.END, values=item)
            
        update_view()

        # frm_stock_view content

        self.lbl_resource_income = tk.Label(self.frm_stock_view, text="Ultimas Entradas")
        self.lbl_resource_income.place(relx=0.1, rely=0.05)

        columns2 = ["ID", "produto", "qnt"]
        self.tvw_resource_income = ttk.Treeview(self.frm_stock_view, columns=columns2, show="headings")
        self.tvw_resource_income.place(relx=0.1, rely=0.1, relwidth=0.35, relheight=0.45)

        self.tvw_resource_income.heading("ID", text="ID")
        self.tvw_resource_income.heading("produto", text="Produto")
        self.tvw_resource_income.heading("qnt", text="Qnt")

        self.tvw_resource_income.column("ID",  minwidth=0, width=2)
        self.tvw_resource_income.column("produto", minwidth=0, width=20)
        self.tvw_resource_income.column("qnt", minwidth=0, width=20)


        self.lbl_last_sales = tk.Label(self.frm_stock_view, text="Ultimas vendas")
        self.lbl_last_sales.place(relx=0.1, rely=0.56)

        columns3 = ["ID", "produto", "qnt"]
        self.tvw_last_sales = ttk.Treeview(self.frm_stock_view, columns=columns3, show="headings")
        self.tvw_last_sales.place(relx=0.1, rely=0.61, relwidth=0.35, relheight=0.45)

        self.tvw_last_sales.heading("ID", text="ID")
        self.tvw_last_sales.heading("produto", text="Produto")
        self.tvw_last_sales.heading("qnt", text="Qnt")

        self.tvw_last_sales.column("ID", minwidth=0, width=2)
        self.tvw_last_sales.column("produto", minwidth=0, width=20)
        self.tvw_last_sales.column("qnt", minwidth=0, width=20)


app = tk.Tk()
Screen(app)
app.mainloop()
