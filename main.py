import imghdr
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from turtle import color
import sqlite3
from sqlite3 import Error, connect
from datetime import date
import db_directives as db


# DONE
# todos os cruds 
# log simplificado
# relações importantes
# exibição do historico


# TO DO

# todas as telas de edits
# valores dos discos
# insert on tvw das vendas e compras
# busca na tvw de disk_list

class Screen():
    def __init__(self, master, selected_mont=None):
        self.window = master
        self.window.title('HighDisk')
        self.window.geometry('750x850')
        self.window.minsize(1250, 850)
        # self.window.state('zoomed')

        # frames
        self.frm_logo_view = tk.Frame(self.window)
        self.frm_logo_view.place(rely=0, relx=0, relwidth=0.758, relheight=0.164)

        self.frm_insert_on_tvw = tk.Frame(self.window)
        self.frm_insert_on_tvw.place(rely=0.28, relx=0.01, relwidth=0.15, relheight=0.35)

        self.frm_list_view = tk.Frame(self.window)
        self.frm_list_view.place(rely=0.28, relx=0.22, relwidth=0.5, relheight=0.55)

        self.frm_stock_view = tk.Frame(self.window)
        self.frm_stock_view.place(rely=0.01, relx=0.70, relwidth=0.50, relheight=0.85)

        # subframes
        self.frm_market = tk.Frame(self.frm_insert_on_tvw)
        self.frm_market.place(rely=0, relx=0, relwidth=0.80)

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
                # self.ent_insert_disk_author.delete(0, 'end')
                # self.cbb_genres.delete(0, 'end')
                self.new_genre_toplv.destroy()

        def author_insertion():
            author_name = self.ent_insert_new_author.get()
            if author_name == '':
                messagebox.showwarning('Aviso', 'Necessario um nome e um artista principal!')
            else:
                sql_directive = f"INSERT INTO author VALUES(NULL, '{author_name}');"
                db.insert(sql_directive)
                messagebox.showinfo('Aviso', 'Artista cadastrado com sucesso!')
                self.new_author_toplv.destroy()

        def genre_registration():
            self.new_genre_toplv = tk.Toplevel()
            self.new_genre_toplv.geometry("250x250")
            self.new_genre_toplv.title("Cadastrar gênero")

            self.lbl_insert_new_genre = tk.Label(self.new_genre_toplv, text="Nome: ")
            self.lbl_insert_new_genre.grid(column=0, row=0)
            self.ent_insert_new_genre = tk.Entry(self.new_genre_toplv, width=25)
            self.ent_insert_new_genre.grid(column=1, row=0)

            self.btn_create_genre = tk.Button(self.new_genre_toplv, text='Inserir', command=genre_insertion)
            self.btn_create_genre.grid(column=1, row=4, columnspan=2)

        def author_registration():
            self.new_author_toplv = tk.Toplevel()
            self.new_author_toplv.geometry("250x250")
            self.new_author_toplv.title("Cadastrar artista")

            self.lbl_insert_new_author = tk.Label(self.new_author_toplv, text="Nome: ")
            self.lbl_insert_new_author.grid(column=0, row=0)
            self.ent_insert_new_author = tk.Entry(self.new_author_toplv, width=25)
            self.ent_insert_new_author.grid(column=1, row=0)

            self.btn_create_author = tk.Button(self.new_author_toplv, text='Inserir', command=author_insertion)
            self.btn_create_author.grid(column=1, row=4, columnspan=2)

        def product_registration():
            disk_name = self.ent_insert_disk_name.get()
            price = self.ent_insert_disk_price.get()

            author_id = db.search(f"SELECT id FROM author WHERE author_name LIKE '{self.cbb_authors.get()}';")

            right_author_id = ''.join(map(str, (author_id[0])))
            genre_id_query = f"SELECT id FROM genre WHERE genre_name = '{self.cbb_genres.get()}';"
            genre_id = db.search(genre_id_query)
            right_genre_id = ''.join(map(str, (genre_id[0])))
            # print(right_author_id, right_genre_id)

            year = ''.join(map(str, {self.ent_insert_disk_release_date.get()}))

            if author_id == '' and genre_id == '':
                messagebox.showwarning('Aviso', 'Necessario um nome e um genero principal!')
            else:
                sql_directive = f"INSERT INTO disk VALUES(NULL,'{disk_name}', 0, {price}, '{right_author_id}', '{right_genre_id}', '{year}');"
                print(sql_directive)
                db.insert(sql_directive)
                update_view()

                messagebox.showinfo('Aviso', 'Disco inserido com sucesso!')
                self.product_toplv.destroy()

        def product_create_product():
            self.product_toplv = tk.Toplevel()
            self.product_toplv.geometry("450x450")
            self.product_toplv.title("Criar Produto")
            selected_genre = tk.StringVar()
            selected_author = tk.StringVar()

            self.lbl_insert_disk_name = tk.Label(self.product_toplv, text="Nome: ")
            self.lbl_insert_disk_name.grid(column=0, row=0)
            self.ent_insert_disk_name = tk.Entry(self.product_toplv, width=25)
            self.ent_insert_disk_name.grid(column=1, row=0)

            self.lbl_insert_disk_author = tk.Label(self.product_toplv, text="Autor: ")
            self.lbl_insert_disk_author.grid(column=0, row=1)
            author_list = db.search('SELECT DISTINCT author_name FROM author')
            self.cbb_authors = ttk.Combobox(self.product_toplv, width=25, textvariable=selected_author,
                                            state="readonly", values=[data_author for data_author, in author_list])
            self.cbb_authors.grid(column=1, row=1)

            self.lbl_genre = tk.Label(self.product_toplv, text="Genero: ")
            self.lbl_genre.grid(column=0, row=2)
            genre_list = db.search('SELECT DISTINCT genre_name FROM genre')
            self.cbb_genres = ttk.Combobox(self.product_toplv, width=25, textvariable=selected_genre, state="readonly",
                                           values=[data_genre for data_genre, in genre_list])
            self.cbb_genres.grid(column=1, row=2)

            self.lbl_insert_disk_release_date = tk.Label(self.product_toplv, text="Ano: ")
            self.lbl_insert_disk_release_date.grid(column=0, row=3)
            self.ent_insert_disk_release_date = tk.Entry(self.product_toplv, width=4)
            self.ent_insert_disk_release_date.grid(column=1, row=3)

            self.lbl_insert_disk_price = tk.Label(self.product_toplv, text="Preço: ")
            self.lbl_insert_disk_price.grid(column=0, row=4)
            self.ent_insert_disk_price = tk.Entry(self.product_toplv, width=15)
            self.ent_insert_disk_price.grid(column=1, row=4)

            self.btn_create_product = tk.Button(self.product_toplv, text='Inserir', command=product_registration)
            self.btn_create_product.grid(column=1, row=5, columnspan=2)

        def product_edit_product():
            self.product_toplv = tk.Toplevel()
            self.product_toplv.geometry("450x450")
            self.product_toplv.title("Criar Produto")

        def product_add_product():
            self.product_toplv = tk.Toplevel()
            self.product_toplv.geometry("400x250")
            self.product_toplv.title("Inserir Produto")
            # n = tk.StringVar()
            selected_disks = tk.StringVar()

            disk_list = db.search('SELECT DISTINCT disk_name FROM disk')
            self.cbb_disks = ttk.Combobox(self.product_toplv, width=25, textvariable=selected_disks, state="readonly",
                                          values=[data_disk for data_disk, in disk_list])
            self.cbb_disks.grid(column=0, row=0)

            self.lbl_quantity = tk.Label(self.product_toplv, text="Quantidade: ")
            self.lbl_quantity.grid(column=1, row=0)
            self.ent_quantity = tk.Entry(self.product_toplv, width=5)
            self.ent_quantity.grid(column=2, row=0)

            self.btn_insert_genre = tk.Button(self.product_toplv, text='Inserir', command=confirm_add_product)
            self.btn_insert_genre.grid(column=1, row=1, columnspan=1)

        def product_sell_product():
            self.product_toplv = tk.Toplevel()
            self.product_toplv.geometry("400x250")
            self.product_toplv.title("Vender Produto")
            # n = tk.StringVar()
            selected_disks = tk.StringVar()

            disk_list = db.search('SELECT DISTINCT disk_name FROM disk')
            self.cbb_disks = ttk.Combobox(self.product_toplv, width=25, textvariable=selected_disks, state="readonly",
                                          values=[data_disk for data_disk, in disk_list])
            self.cbb_disks.grid(column=0, row=0)

            self.lbl_quantity = tk.Label(self.product_toplv, text="Quantidade: ")
            self.lbl_quantity.grid(column=1, row=0)
            self.ent_quantity = tk.Entry(self.product_toplv, width=5)
            self.ent_quantity.grid(column=2, row=0)

            self.btn_insert_genre = tk.Button(self.product_toplv, text='Vender', command=confirm_sell_product)
            self.btn_insert_genre.grid(column=1, row=1, columnspan=1)

        def confirm_add_product():
            income = int(self.ent_quantity.get())
            disk_name = self.cbb_disks.get()
            old_quantity = db.search(f'SELECT quantity FROM disk WHERE disk_name="{disk_name}";')
            right_old_quantity = int(''.join(map(str, (old_quantity[0]))))
            disk_reference = db.search(f'SELECT id FROM disk WHERE  disk_name="{disk_name}";')


            parsed_disk_Reference = int(''.join(map(str, (disk_reference[0]))))

            today = date.today()
            parsed_date = today.strftime(f"%d/%m/%Y")

            quantity = right_old_quantity + income

            sql_directive = f'UPDATE disk SET quantity={quantity} WHERE disk_name="{disk_name}";'
            change_directive = f'INSERT INTO changes VALUES(NULL, "{income} UNIDADES ADICIONADAS", "compra", "{parsed_date}",{income} , 0, {parsed_disk_Reference});'
            db.update(sql_directive)
            db.update(change_directive)
            messagebox.showinfo("Quantidade inserida", "Disco adicionado ao estoque!")
            self.product_toplv.destroy()

        def confirm_sell_product():
            sell_quantity = int(self.ent_quantity.get())
            disk_name = self.cbb_disks.get()
            old_quantity = db.search(f'SELECT quantity FROM disk WHERE disk_name="{disk_name}";')

            disk_reference = db.search(f'SELECT id FROM disk WHERE  disk_name="{disk_name}";')
            parsed_disk_Reference = int(''.join(map(str, (disk_reference[0]))))

            right_old_quantity = int(''.join(map(str, (old_quantity[0]))))

            disk_price = db.search(f'SELECT price FROM disk where disk_name="{disk_name}";')
            disk_price = float(''.join(map(str, (disk_price[0]))))
            total_price = disk_price*sell_quantity
            print(type(total_price))

            quantity = right_old_quantity - sell_quantity

            today = date.today()
            parsed_date = today.strftime(f"%d/%m/%Y")
            sql_directive = f'UPDATE disk SET quantity={quantity} WHERE disk_name="{disk_name}";'
            change_directive = f'INSERT INTO changes VALUES(NULL, "{sell_quantity} UNIDADES VENDIDAS", "venda", "{parsed_date}", {sell_quantity} ,{total_price},{parsed_disk_Reference});'

            if (quantity > 0):

                db.update(sql_directive)
                db.update(change_directive)
                messagebox.showinfo("Venda", "Venda realizada com sucesso!")
                self.product_toplv.destroy()

            elif quantity == 0:
                db.update(sql_directive)
                db.update(change_directive)
                messagebox.showinfo("Venda", "Venda realizada com sucesso! \n Quantidade em estoque: 0, necessario reposição;")
                self.product_toplv.destroy()

            else:
                failed_sale_record = f'INSERT INTO changes VALUES(NULL, "VENDA NÃO EFETUADA POR INSUFICIENCIA NO ESTOQUE", "falha", "{parsed_date}", {parsed_disk_Reference});'
                db.update(failed_sale_record)
                messagebox.showwarning("Aviso", "Quantidade solicitada indisponivel no estoque!")

        # menu

        self.menu_bar = Menu(self.window)
        self.window.config(menu=self.menu_bar)

        self.config_menu = Menu(self.menu_bar, tearoff=0)
        self.config_menu.add_command(label="Sair", command=self.window.quit)
        self.menu_bar.add_cascade(label="Configurações", menu=self.config_menu)

        self.product_menu = Menu(self.menu_bar, tearoff=0)
        self.product_menu.add_command(label="Criar produto", command=product_create_product)
        self.product_menu.add_command(label="Editar produto", command=product_edit_product)
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

        # content

        # logo_view content
        # with Image.open('disky.png') as im:
        #     im.rotate(45).show()
        self.img_logo = tk.PhotoImage(file="compact-disk-64.png")
        self.lbl_logo = tk.Label(self.frm_logo_view, image=self.img_logo)
        self.lbl_logo.place(rely=0.1, relx=0.01, relheight=0.9, relwidth=0.55)
        self.img_prod_name = tk.PhotoImage(file="highdisk-wnobg.png")
        self.lbl_bus_name = tk.Label(self.frm_logo_view, image=self.img_prod_name)
        self.lbl_bus_name.place(rely=0.1, relx=0.35, relheight=0.9, relwidth=0.55)

        # frm_insert_on_tvw content
        self.btn_buy_disk = tk.Button(self.frm_market, text="Inserir", width=15, command=product_add_product)
        self.btn_buy_disk.grid(column=0, row=0)

        self.btn_buy_disk = tk.Button(self.frm_market, text="Vender", width=15, command=product_sell_product)
        self.btn_buy_disk.grid(column=0, row=1)

        # frm_list_view content
        self.ent_generic_search = tk.Entry(self.frm_search, width=15)
        self.ent_generic_search.grid(column=0, row=0)

        to_search_selected_genre = tk.StringVar()
        self.to_search_genre_list = db.search('SELECT DISTINCT genre_name FROM genre')
        self.cbb_to_search_genres = ttk.Combobox(self.frm_search, width=25, textvariable=to_search_selected_genre,
                                                 values=[data for data, in self.to_search_genre_list])
        self.cbb_to_search_genres.grid(column=2, row=0)

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
                self.tvw_disk_list.delete(i)

            # directives
            length = db.search(
                "SELECT DISTINCT COUNT(*) FROM disk, genre, author WHERE fk_author = author.id and fk_genre = genre.id")
            length = ''.join(map(str, (length[0])))
            sql_directive = "SELECT DISTINCT disk.id, disk_name, author_name, genre_name, year FROM disk, genre, author WHERE fk_author = author.id AND fk_genre = genre.id"
            data = db.search(sql_directive)
            for item in data:
                self.tvw_disk_list.insert('', tk.END, values=item)

        update_view()

        # frm_stock_view content

        self.lbl_resource_income = tk.Label(self.frm_stock_view, text="Ultimas entradas no estoque")
        self.lbl_resource_income.place(relx=0.1, rely=0.05)

        columns2 = ["DISCO", "QUANTIA"]
        self.tvw_resource_income = ttk.Treeview(self.frm_stock_view, columns=columns2, show="headings")
        self.tvw_resource_income.place(relx=0.1, rely=0.1, relwidth=0.45, relheight=0.45)

        self.tvw_resource_income.heading("DISCO", text="Disco")
        self.tvw_resource_income.heading("QUANTIA", text="Quantia")

        self.tvw_resource_income.column("DISCO", minwidth=0, width=1)
        self.tvw_resource_income.column("QUANTIA", minwidth=20, width=20)

        def income_update_view():
            for i in self.tvw_resource_income.get_children():
                self.tvw_resource_income.delete(i)

            sql_directive = "SELECT DISTINCT disk_name, changes.quantity FROM changes, disk WHERE fk_disk = disk.id AND changes.type ='compra'"
            data = db.search(sql_directive)
            for item in data:
                self.tvw_resource_income.insert('', tk.END, values=item)

        income_update_view()

        self.lbl_last_sales = tk.Label(self.frm_stock_view, text="Ultimas vendas")
        self.lbl_last_sales.place(relx=0.1, rely=0.56)

        columns3 = ["DISCO", "QUANTIA"]
        self.tvw_last_sales = ttk.Treeview(self.frm_stock_view, columns=columns3, show="headings")
        self.tvw_last_sales.place(relx=0.1, rely=0.61, relwidth=0.45, relheight=0.45)

        self.tvw_last_sales.heading("DISCO", text="Disco")
        self.tvw_last_sales.heading("QUANTIA", text="Quantia")

        self.tvw_last_sales.column("DISCO", minwidth=0, width=2)
        self.tvw_last_sales.column("QUANTIA", minwidth=0, width=20)

        def sales_update_view():
            for i in self.tvw_last_sales.get_children():
                self.tvw_last_sales.delete(i)

            sql_directive = "SELECT DISTINCT disk_name, changes.quantity FROM changes, disk WHERE fk_disk = disk.id AND changes.type ='venda'"
            data = db.search(sql_directive)
            for item in data:
                self.tvw_last_sales.insert('', tk.END, values=item)

        sales_update_view()


app = tk.Tk()
Screen(app)
app.mainloop()
