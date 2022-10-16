from email import message
import imghdr
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from turtle import color
import sqlite3
from sqlite3 import Error, connect
from datetime import date
import webbrowser
import db_directives as db

#DONE
# relações importantes
# todos os cruds 
# busca na tvw principal
# log simplificado
# exibição do historico


# TO DO


class Screen():
    def __init__(self, master, selected_mont=None):
        self.window = master
        self.window.title('HighDisk')
        self.window.geometry('750x850')
        self.window.minsize(1250, 850)
        self.window.state('zoomed')

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

        def about_dev():
            self.info_toplv = tk.Toplevel()
            self.info_toplv.geometry('550x300')
            self.info_toplv.title("About me")

            self.text_about_me = tk.Text(self.info_toplv, width= 60, height= 30)
            self.text_about_me.insert(INSERT, "Crhistopher Ric Coelho Saar, 28yo, natural from Brazil.\nGraduating in IT at UFAC(Federal University of Acre).\nCurrently working with angular 13 and mainly with python(django 3.1)")
            self.text_about_me.place(relx=0, rely=0)
            self.text_about_me.configure(state='disabled')
            
            

        def reach_me():
            def path(url):
                webbrowser.open_new(url)
            self.info_toplv = tk.Toplevel()
            self.info_toplv.geometry('300x300')
            self.info_toplv.title("Contact me")

            self.lbl_explain = tk.Label(self.info_toplv, text="A few links and ways to contact me:")
            self.lbl_explain.place(rely=0, relx=0)

            self.lbl_cont1 = tk.Label(self.info_toplv, text='Email: ')
            self.lbl_cont1.place(rely=0.1, relx=0.05)

            self.lbl_contact1 = tk.Label(self.info_toplv, text='cristophersaar@gmail.com', fg='#0000EE')
            self.lbl_contact1.place(rely=0.1, relx=0.21)
            self.lbl_contact1.bind("<Button-1>", lambda e: path("http://mailto:cristophersaar@gmail.com"))

            self.lbl_cont2 = tk.Label(self.info_toplv, text='phone: ')
            self.lbl_cont2.place(rely=0.2, relx=0.05)
            self.lbl_contact2 = tk.Label(self.info_toplv, text='+55 68 999310080', fg='#0000EE')
            self.lbl_contact2.place(rely=0.2, relx=0.21)
            self.lbl_contact2.bind("<Button-1>", lambda e: path("https://wa.me/5568999310080"))
        
            self.lbl_cont3 = tk.Label(self.info_toplv, text='Github: ')
            self.lbl_cont3.place(rely=0.3, relx=0.05)
            self.lbl_contact3 = tk.Label(self.info_toplv, text="cCoelhos", fg='#0000EE')
            self.lbl_contact3.place(rely=0.3, relx=0.21)
            self.lbl_contact3.bind("<Button-1>", lambda e: path("https://github.com/crcoelhos"))



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
            self.btn_create_genre.grid(column=1, row=4)

        
        def remove_genre():
            current_name = self.cbb_genres_to_update.get()
            if current_name:
                validacao = messagebox.askyesno(title='Excluir?', message='Tem certeza que deseja remover?')
                if validacao:
                    sql_directive = f'DELETE FROM genre WHERE genre_name="{current_name}";'
                    db.delete(sql_directive)
                    messagebox.showinfo('Aviso', 'Genero removido com sucesso!')
                    self.genre_update_toplv.destroy()
                else:
                    self.genre_update_toplv.deiconify()


            else:
                messagebox.showerror("Aviso", "Necessario selecionar algum item para exclusão")
                self.genre_update_toplv.deiconify()
        
        def genre_update():
            self.genre_update_toplv = tk.Toplevel()
            self.genre_update_toplv.geometry("250x250")
            self.genre_update_toplv.title("Atualizar genero")
            
            selected_genre = tk.StringVar()
            self.lbl_insert_genre = tk.Label(self.genre_update_toplv, text="Genero: ")
            self.lbl_insert_genre.grid(column=0, row=0)
            genre_list = db.search('SELECT DISTINCT genre_name FROM genre')
            self.cbb_genres_to_update = ttk.Combobox(self.genre_update_toplv, width=25, textvariable=selected_genre, state="readonly" ,values = [data_genre for data_genre, in genre_list])            
            self.cbb_genres_to_update.grid(column=1, row=0)

            self.lbl_new_name = tk.Label(self.genre_update_toplv, text="Novo nome")
            self.lbl_new_name.grid(column=0, row=1)

            self.ent_new_genre_name = tk.Entry(self.genre_update_toplv, width=28)
            self.ent_new_genre_name.grid(column=1, row=1)

            self.btn_new_name = tk.Button(self.genre_update_toplv, text="Atualizar", command=confirm_new_genre_name)
            self.btn_new_name.grid(column=1, row=2)

            
            self.btn_remove_genre = tk.Button(self.genre_update_toplv, text='Remover', command=remove_genre)
            self.btn_remove_genre.grid(column=1, row=3)
        
        def confirm_new_genre_name():
            new_name = self.ent_new_genre_name.get()
            current_name = self.cbb_genres_to_update.get()
            sql_directive = f'UPDATE genre SET genre_name="{new_name}" WHERE genre_name="{current_name}";'
            if new_name:
                db.update(sql_directive)
                messagebox.showinfo('Aviso', 'Genero atualizado com sucesso!')
                self.genre_update_toplv.destroy()
            else:
                messagebox.showwarning('Aviso', 'Nome invalido, refaça a operação!')
                self.genre_update_toplv.destroy()



            

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
        
        
        def author_update():
            selected_author = tk.StringVar()
            self.author_update_toplv = tk.Toplevel()
            self.author_update_toplv.geometry("250x250")
            self.author_update_toplv.title("Atualizar autor")

            self.lbl_insert_disk_author_to_update = tk.Label(self.author_update_toplv, text="Autor: ")
            self.lbl_insert_disk_author_to_update.grid(column=0, row=0)
            author_list = db.search('SELECT DISTINCT author_name FROM author')
            self.cbb_authors_to_update = ttk.Combobox(self.author_update_toplv, 
                                                width=25, 
                                                textvariable=selected_author, 
                                                state="readonly",
                                                values = [data_author for data_author, in author_list])
            self.cbb_authors_to_update.grid(column=1, row=0)

            self.lbl_new_name = tk.Label(self.author_update_toplv, text="Novo nome")
            self.lbl_new_name.grid(column=0, row=1)

            self.ent_new_name = tk.Entry(self.author_update_toplv, width=28)
            self.ent_new_name.grid(column=1, row=1)

            self.btn_new_name = tk.Button(self.author_update_toplv, text="Atualizar", command=confirm_new_author_name)
            self.btn_new_name.grid(column=1, row=2)
           
            self.btn_delete_author = tk.Button(self.author_update_toplv, text="Remover", command=remove_author)
            self.btn_delete_author.grid(column=1, row=3)


        def remove_author():
            current_name = self.cbb_authors_to_update.get()
            if current_name:
                validacao = messagebox.askyesno(title='Excluir?', message='Tem certeza que deseja remover?')
                if validacao:
                    sql_directive = f'DELETE FROM author WHERE author_name="{current_name}";'
                    db.delete(sql_directive)
                    messagebox.showinfo('Aviso', 'Autor removido com sucesso!')
                    self.author_update_toplv.destroy()
                else:
                    self.author_update_toplv.deiconify()


            else:
                messagebox.showerror("Aviso", "Necessario selecionar algum item para exclusão")
                self.author_update_toplv.deiconify()


        def confirm_new_author_name():
            new_name = self.ent_new_name.get()
            current_name = self.cbb_authors_to_update.get()
            sql_directive = f'UPDATE author SET author_name="{new_name}" WHERE author_name="{current_name}";'
            if new_name:
                db.update(sql_directive)
                messagebox.showinfo('Aviso', 'Autor atualizado com sucesso!')
                self.author_update_toplv.destroy()
            else:               
                messagebox.showwarning('Aviso', 'Nome invalido, refaça a operação!')
                self.author_update_toplv.destroy()

        

        def product_registration():
            disk_name = self.ent_insert_disk_name.get()

            author_id = db.search(f"SELECT id FROM author WHERE author_name LIKE '{self.cbb_authors.get()}';")
            right_author_id = ''.join(map(str, (author_id[0])))

            genre_id_query = f"SELECT id FROM genre WHERE genre_name = '{self.cbb_genres.get()}';"
            genre_id = db.search(genre_id_query)
            right_genre_id = ''.join(map(str, (genre_id[0])))
            # print(right_author_id, right_genre_id)



            year = ''.join(map(str,{self.ent_insert_disk_release_date.get()}))

            if author_id == '' and genre_id == '':
                messagebox.showwarning('Aviso', 'Necessario um nome e um genero principal!')
            else:
                sql_directive = f"INSERT INTO disk VALUES(NULL,'{disk_name}', 0, '{right_author_id}', '{right_genre_id}', '{year}');"
                db.insert(sql_directive)
                update_view()
                
                messagebox.showinfo('Aviso', 'Disco inserido com sucesso!')
                # self.ent_insert_disk_author.delete(0, 'end')
                # self.cbb_genres.delete(0, 'end')
                self.product_toplv.destroy()

        def product_create_product():
            self.product_toplv = tk.Toplevel()
            self.product_toplv.geometry("250x250")
            self.product_toplv.title("Criar Produto")
            selected_genre = tk.StringVar()
            selected_author = tk.StringVar()

            self.lbl_insert_disk_name = tk.Label(self.product_toplv, text="Nome: ")
            self.lbl_insert_disk_name.grid(column=0, row=0)
            self.ent_insert_disk_name = tk.Entry(self.product_toplv, width=28)
            self.ent_insert_disk_name.grid(column=1, row=0)

            self.lbl_insert_disk_author = tk.Label(self.product_toplv, text="Autor: ")
            self.lbl_insert_disk_author.grid(column=0, row=1)
            author_list = db.search('SELECT DISTINCT author_name FROM author')
            self.cbb_authors = ttk.Combobox(self.product_toplv, width=25, textvariable=selected_author, state="readonly" ,values = [data_author for data_author, in author_list])
            self.cbb_authors.grid(column=1, row=1)

            self.lbl_genre = tk.Label(self.product_toplv, text="Genero: ")
            self.lbl_genre.grid(column=0, row=2)
            genre_list = db.search('SELECT DISTINCT genre_name FROM genre')
            self.cbb_genres = ttk.Combobox(self.product_toplv, width=25, textvariable=selected_genre, state="readonly", values = [data_genre for data_genre, in genre_list])
            self.cbb_genres.grid(column=1, row=2)

            self.lbl_insert_disk_release_date = tk.Label(self.product_toplv, text="Ano: ")
            self.lbl_insert_disk_release_date.grid(column=0, row=3)
            self.ent_insert_disk_release_date = tk.Entry(self.product_toplv, width=4)
            self.ent_insert_disk_release_date.grid(column=1, row=3)

            # directive = f'INSERT INTO product {}'
            self.btn_create_product = tk.Button(self.product_toplv, text='Inserir', command=product_registration)
            self.btn_create_product.grid(column=1, row=4, columnspan=2)


        def remove_product():
            current_name = self.cbb_products_to_update.get()
            if current_name:
                validacao = messagebox.askyesno(title='Excluir?', message='Tem certeza que deseja remover?')
                if validacao:
                    sql_directive = f'DELETE FROM disk WHERE disk_name="{current_name}";'
                    db.delete(sql_directive)
                    messagebox.showinfo('Aviso', 'Disco removido com sucesso!')
                    update_view()
                    self.edit_product_toplv.destroy()
                else:
                    self.edit_product_toplv.deiconify()


        def product_edit_product():
            self.edit_product_toplv = tk.Toplevel()
            self.edit_product_toplv.geometry("250x250")
            self.edit_product_toplv.title("Editar Produto")

            selected_product = tk.StringVar()

            self.lbl_get_product_to_update = tk.Label(self.edit_product_toplv, text="Disco: ")
            self.lbl_get_product_to_update.grid(column=0, row=0)
            disk_list = db.search('SELECT DISTINCT disk_name FROM disk')
            self.cbb_products_to_update = ttk.Combobox(self.edit_product_toplv, 
                                                width=25, 
                                                textvariable=selected_product, 
                                                state="readonly",
                                                values = [data_disk for data_disk, in disk_list])
            self.cbb_products_to_update.grid(column=1, row=0)

            self.lbl_new_product_name = tk.Label(self.edit_product_toplv, text="Novo nome")
            self.lbl_new_product_name.grid(column=0, row=1)

            self.ent_new_product_name = tk.Entry(self.edit_product_toplv, width=28)
            self.ent_new_product_name.grid(column=1, row=1)

            self.btn_new_name = tk.Button(self.edit_product_toplv, text="Atualizar", command=confirm_new_disk_name)
            self.btn_new_name.grid(column=1, row=2)

            self.btn_remove_product = tk.Button(self.edit_product_toplv, text="Remover", command=remove_product)
            self.btn_remove_product.grid(column=1, row=3)

        def confirm_new_disk_name():
            new_name = self.ent_new_product_name.get()
            current_name = self.cbb_products_to_update.get()
            sql_directive = f'UPDATE disk SET disk_name="{new_name}" WHERE disk_name="{current_name}";'
            if new_name:
                db.update(sql_directive)
                messagebox.showinfo('Aviso', 'Disco atualizado com sucesso!')
                self.edit_product_toplv.destroy()
                update_view()
            else:               
                messagebox.showwarning('Aviso', 'Nome invalido, refaça a operação!')
                self.edit_product_toplv.destroy()

        def product_add_product():
            self.product_toplv = tk.Toplevel()
            self.product_toplv.geometry("400x250")
            self.product_toplv.title("Inserir Produto")
            # n = tk.StringVar()
            selected_disks = tk.StringVar()
            

            disk_list = db.search('SELECT DISTINCT disk_name FROM disk')
            self.cbb_disks = ttk.Combobox(self.product_toplv, width=25, textvariable=selected_disks, state="readonly", values = [data_disk for data_disk, in disk_list])
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
            self.cbb_disks = ttk.Combobox(self.product_toplv, width=25, textvariable=selected_disks, state="readonly", values = [data_disk for data_disk, in disk_list])
            self.cbb_disks.grid(column=0, row=0)

            self.lbl_quantity = tk.Label(self.product_toplv, text="Quantidade: ")
            self.lbl_quantity.grid(column=1, row=0)
            self.ent_quantity = tk.Entry(self.product_toplv, width=5)
            self.ent_quantity.grid(column=2, row=0)

            # in_stock = db.search(f"SELECT quantity FROM disk WHERE disk_name = '{self.cbb_disks.get()}'")
            # print(in_stock)

            # self.lbl_current_quantity = tk.Label(self.product_toplv, text="Quantidade em estoque")
            # self.lbl_current_quantity.grid(column=0, row=1, columnspan=1)

            # self.lbl_value = tk.Label(self.product_toplv, text=f"{in_stock}")
            # self.lbl_current_quantity.grid(column=1, row=1, columnspan=1)


            self.btn_insert_genre = tk.Button(self.product_toplv, text='Vender', command=confirm_sell_product)
            self.btn_insert_genre.grid(column=1, row=2)


        def confirm_add_product():
            income = int(self.ent_quantity.get())
            disk_name = self.cbb_disks.get()   
            old_quantity = db.search(f'SELECT quantity FROM disk WHERE disk_name="{disk_name}";')
            right_old_quantity = int(''.join(map(str, (old_quantity[0]))))
            disk_reference = db.search(f'SELECT id FROM disk WHERE  disk_name="{disk_name}";')
       
            parsed_disk_Reference = int(''.join(map(str, (disk_reference[0]))))

            
            today = date.today()
            parsed_date = today.strftime(f"%d/%m/%Y")
            price = db.search("SELECT price FROM")

            quantity = right_old_quantity+income

            sql_directive = f'UPDATE disk SET quantity={quantity} WHERE disk_name="{disk_name}";'
            change_directive = f'INSERT INTO changes VALUES(NULL, "{income} UNIDADES ADICIONADAS", "compra", "{parsed_date}",{quantity},{parsed_disk_Reference});'
            db.update(sql_directive)
            db.update(change_directive)
            messagebox.showinfo("Quantidade inserida", "Disco adicionado ao estoque!")
            income_update_view()

            self.product_toplv.destroy()


        def confirm_sell_product():
            sell_quantity = int(self.ent_quantity.get())
            disk_name = self.cbb_disks.get()   
            old_quantity = db.search(f'SELECT quantity FROM disk WHERE disk_name="{disk_name}";')

            disk_reference = db.search(f'SELECT id FROM disk WHERE  disk_name="{disk_name}";')       
            parsed_disk_Reference = int(''.join(map(str, (disk_reference[0]))))

            right_old_quantity = int(''.join(map(str, (old_quantity[0]))))
            
            quantity = right_old_quantity-sell_quantity

            today = date.today()
            parsed_date = today.strftime(f"%d/%m/%Y")
            sql_directive = f'UPDATE disk SET quantity={quantity} WHERE disk_name="{disk_name}";' 
            change_directive = f'INSERT INTO changes VALUES(NULL, "{sell_quantity} UNIDADES VENDIDAS", "venda", "{parsed_date}",{quantity}, {parsed_disk_Reference});'
            
            if (quantity>0):
                
                db.update(sql_directive)
                db.update(change_directive)
                messagebox.showinfo("Venda", "Venda realizada com sucesso!")
                sales_update_view()
                self.product_toplv.destroy()

            elif (quantity==0):
                db.update(sql_directive)
                db.update(change_directive)
                messagebox.showinfo("Venda", "Venda realizada com sucesso! \n Quantidade em estoque: 0, necessario reposição;")
                sales_update_view()
                self.product_toplv.destroy()

            else:
                failed_sale_record = f'INSERT INTO changes VALUES(NULL, "VENDA NÃO EFETUADA POR INSUFICIENCIA NO ESTOQUE", "falha", "{parsed_date}", {quantity}, {parsed_disk_Reference});'
                db.update(failed_sale_record)
                sales_update_view()
                messagebox.showwarning("Aviso", "Quantidade solicitada indisponivel no estoque!" )



        def tvw_search():
            self.tvw_disk_list.selection()
            fetchdata = self.tvw_disk_list.get_children()
            for f in fetchdata:
                self.tvw_disk_list.delete(f)
        
            name = self.ent_generic_search.get()
            genre = self.cbb_to_search_genres.get()
        
            if name:
                if genre:
                    sql = f"SELECT DISTINCT disk.id, disk_name, author_name, genre_name, year FROM disk, genre, author WHERE fk_author = author.id AND fk_genre = genre.id AND disk_name LIKE '%{name}%' AND genre_name LIKE '%{genre}%' "
                    data = db.search(sql)
                    for d in data:
                        self.tvw_disk_list.insert("", END, values=d)
                else:
                    sql = f"SELECT DISTINCT disk.id, disk_name, author_name, genre_name, year FROM disk, genre, author WHERE fk_author = author.id AND fk_genre = genre.id AND disk_name LIKE '%{name}%'"
                    data = db.search(sql)
                    for d in data:
                        self.tvw_disk_list.insert("", END, values=d)
            elif genre:
                if name:
                    sql = f"SELECT DISTINCT disk.id, disk_name, author_name, genre_name, year FROM disk, genre, author WHERE fk_author = author.id AND fk_genre = genre.id AND disk_name LIKE '%{name}%' AND genre_name LIKE '%{genre}%' "
                    data = db.search(sql)
                    for d in data:
                        self.tvw_disk_list.insert("", END, values=d)
                else:
                    sql = f"SELECT DISTINCT disk.id, disk_name, author_name, genre_name, year FROM disk, genre, author WHERE fk_author = author.id AND fk_genre = genre.id AND genre_name LIKE '%{genre}%' "
                    data = db.search(sql)
                    for d in data:
                        self.tvw_disk_list.insert("", END, values=d)
                
            else:
                update_view()
        
        def tvw_search_filter_reset():
            self.cbb_to_search_genres.set('')
            self.ent_generic_search.delete(0, END)
            update_view()
            

            
        #menu

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
        self.genre_menu.add_command(label="Editar genero", command=genre_update)
        self.menu_bar.add_cascade(label="Generos", menu=self.genre_menu)

        self.author_menu = Menu(self.menu_bar, tearoff=0)
        self.author_menu.add_command(label="Adicionar autor", command=author_registration)
        self.author_menu.add_command(label="Editar autor", command=author_update)
        self.menu_bar.add_cascade(label="Autor", menu=self.author_menu)

        self.user_menu = Menu(self.menu_bar, tearoff=0)
        self.user_menu.add_command(label="Sobre", command=about_dev)
        self.user_menu.add_command(label="Contato", command=reach_me)
        self.menu_bar.add_cascade(label="Info", menu=self.user_menu)






        #content

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
        self.cbb_to_search_genres = ttk.Combobox(self.frm_search, width=25, textvariable=to_search_selected_genre, values=[data for data, in self.to_search_genre_list])
        self.cbb_to_search_genres.grid(column=2, row=0)

        self.btn_search_on_tvw = tk.Button(self.frm_search, text="Procurar", command=tvw_search)
        self.btn_search_on_tvw.grid(column=3, row=0)

        self.gambiarra = tk.Label(self.frm_search)
        self.gambiarra.grid(column=4, row=0)
        self.gambiarra2 = tk.Label(self.frm_search)
        self.gambiarra2.grid(column=5, row=0)

       
        self.btn_search_on_tvw = tk.Button(self.frm_search, text="Atualizar", command=tvw_search_filter_reset)
        self.btn_search_on_tvw.grid(column=6, row=0)

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

            #directives
            length = db.search("SELECT DISTINCT COUNT(*) FROM disk, genre, author WHERE fk_author = author.id and fk_genre = genre.id")
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
        self.tvw_resource_income.heading("QUANTIA", text="Quantidade")

        self.tvw_resource_income.column("DISCO",  minwidth=0, width=1)
        self.tvw_resource_income.column("QUANTIA", minwidth=20, width=20)

        def income_update_view():
            for i in self.tvw_resource_income.get_children():
                self.tvw_resource_income.delete(i)

            sql_directive = "SELECT DISTINCT disk_name, SUBSTR(stamp,  1, 3) FROM changes, disk WHERE fk_disk = disk.id AND changes.type ='compra'"
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
        self.tvw_last_sales.heading("QUANTIA", text="Quantidade")

        self.tvw_last_sales.column("DISCO",  minwidth=0, width=2)
        self.tvw_last_sales.column("QUANTIA", minwidth=0, width=20)

        def sales_update_view():
            for i in self.tvw_last_sales.get_children():
                self.tvw_last_sales.delete(i)

            sql_directive = "SELECT DISTINCT disk_name, SUBSTR(stamp,  1, 3) FROM changes, disk WHERE fk_disk = disk.id AND changes.type ='venda'"
            data = db.search(sql_directive)
            for item in data:
                self.tvw_last_sales.insert('', tk.END, values=item)
            
        sales_update_view()

app = tk.Tk()
Screen(app)
app.mainloop()
