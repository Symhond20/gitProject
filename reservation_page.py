from tkinter import *
from tkinter import ttk, messagebox
import customtkinter as ctk
from datetime import datetime

ctk.set_appearance_mode("light")

class ReservationPage:
    def __init__(self, root):
        self.root = root

        

        # Main Frames 
        self.header_frame = Frame(self.root) 
        self.header_frame.pack(fill= X, pady= 20)

        self.form_frame = Frame(self.root)
        self.form_frame.pack(side= LEFT, anchor= "nw", padx= (0, 20))

        self.table_frame = Frame(self.root)
        self.table_frame.pack(side= LEFT, anchor= "n", padx= (0, 10))

        self.reservation_frame = Frame(self.root)
        self.reservation_frame.pack(side= LEFT, anchor= "n", padx= (20, 15))
    
        Label(self.header_frame, text= "Make a Reservation", font= ("Times", 27, "bold")).pack(side= LEFT, anchor= "w")
        
        current_date = datetime.now().strftime("%A, %d %B %Y")
        current_time = datetime.now().strftime("%I:%M %p")
        
        Label(self.header_frame, text= current_time, font= ("Times", 12)).pack(side= RIGHT, padx= (0, 20))
        Label(self.header_frame, text= current_date, font= ("Times", 12)).pack(side= RIGHT, padx= 15)

        # Form Section
        Label(self.form_frame, text= "Full Name:", font= ("Times", 9)).pack(anchor= "w")
        self.name_entry = ctk.CTkEntry(self.form_frame, width= 260)
        self.name_entry.pack(anchor= "w", pady = (0, 25))

        Label(self.form_frame, text= "Contact Number:", font= ("Times", 9)).pack(anchor= "w")
        self.contact_entry = ctk.CTkEntry(self.form_frame, width= 260)
        self.contact_entry.pack(anchor= "w", pady = (0, 25))

        Label(self.form_frame, text= "Selected Date:", font= ("Times", 9)).pack(anchor= "w")
        self.date_entry = ctk.CTkEntry(self.form_frame, width= 260)
        self.date_entry.pack(anchor= "w", pady = (0, 25))

        Label(self.form_frame, text= "Select Time:", font= ("Times", 9)).pack(anchor= "w")
        self.time_entry = ctk.CTkEntry(self.form_frame, width= 260)
        self.time_entry.pack(anchor= "w", pady = (0, 25))

        Label(self.form_frame, text= "Guest Count:", font= ("Times", 9)).pack(anchor= "w")
        self.guest_count_entry = ctk.CTkEntry(self.form_frame, width= 260)
        self.guest_count_entry.pack(anchor= "w", pady = (0, 25))
       
        Label(self.form_frame, text= "Special Instructions:", font= ("Times", 9)).pack(anchor= "w")
        self.requests = ctk.CTkTextbox(self.form_frame, border_width= 2, width= 260)
        self.requests.pack(anchor= "w", pady= (0, 25)) 

        self.cancel_btn = ctk.CTkButton(self.form_frame, text= "Cancel", width= 100,
                                        fg_color= "#FFFFFF", font= ("Times", 12), text_color= "#000000",
                                        border_width= 2, border_color= "#DADADA", 
                                        command= self.clearForm)
        self.cancel_btn.pack(side= LEFT, anchor= "w")
        
        self.btns_frame = Frame(self.table_frame)
        self.btns_frame.pack(anchor= "w")

        Label(self.btns_frame, text= "Select Table", font= ("Times", 13)).pack(anchor= "w", pady= (0, 15))
    
        self.create_table_view(self.table_frame, "2nd Floor")

        Label(self.reservation_frame, text= "Reservations Created Today", font=('Times', 15)).pack(anchor= "w", pady= (0, 15))

        # Current reservation frame for table
        self.reservation_sub_page = Frame(self.reservation_frame)
        self.reservation_sub_page.pack(fill= BOTH, expand= True)

        self.create_reservation_view(self.reservation_sub_page)

        self.add_btn = ctk.CTkButton(self.reservation_frame, text= "Add", width= 100,
                                        fg_color= "#FFFFFF", font= ("Times", 12), text_color= "#000000",
                                        border_width= 2, border_color= "#DADADA", 
                                        command= self.clearForm)
        self.add_btn.pack(anchor= "e", padx= (0, 16))

    def submitForm(self):
        name = self.name_entry.get()
        phone = self.contact_entry.get()
        date = self.date_entry.get()
        time = self.time_entry.get()
        guest_count = int(self.guest_count_entry.get())
        requests = self.requests.get("1.0", END).strip()

        if not name or not phone or not date or not time or not guest_count:
            messagebox.showerror("Error", "Please fill in all required fields.")
            return
        
    def clearForm(self):
        self.name_entry.delete(0, END)
        self.contact_entry.delete(0, END)
        self.date_entry.delete(0, END)
        self.time_entry.delete(0, END)
        self.guest_count_entry.delete(0, END)
        self.requests.delete("1.0", END)

    def create_table_view(self, parent_frame, floor_name):
        self.table_tree = ttk.Treeview(parent_frame, columns= ("Table Number", "Capacity", "Status", "Time"), show= "headings", height= 20)
        self.table_tree.heading("Table Number", text= "Table Number")
        self.table_tree.heading("Capacity", text= "Capacity")
        self.table_tree.heading("Status", text= "Status")
        self.table_tree.heading("Time", text= "Time")

        self.table_tree.column("Table Number", width= 100, anchor= "center")
        self.table_tree.column("Capacity", width= 80, anchor= "center")
        self.table_tree.column("Status", width= 130, anchor= "center")
        self.table_tree.column("Time", width= 130, anchor= "center")
        self.table_tree.pack(side= LEFT, fill= BOTH, expand= True)

        scrollbar = ttk.Scrollbar(parent_frame, orient= "vertical", command= self.table_tree.yview)
        self.table_tree.config(yscrollcommand= scrollbar.set)
        scrollbar.pack(side= RIGHT, fill= Y)
    
    def create_reservation_view(self, parent_frame):
        self.reservation_tree = ttk.Treeview(parent_frame, columns= ("Time", "Table Number", "Capacity", "Status"), show="headings", height= 25)
        self.reservation_tree.heading("Time", text= "Time")
        self.reservation_tree.heading("Table Number", text= "Table Number")
        self.reservation_tree.heading("Capacity", text= "Capacity")
        self.reservation_tree.heading("Status", text= "Status")

        self.reservation_tree.column("Time", width= 150, anchor= "center")
        self.reservation_tree.column("Table Number", width= 130, anchor= "center")
        self.reservation_tree.column("Capacity", width= 100, anchor= "center")
        self.reservation_tree.column("Status", width= 150, anchor= "center")
        self.reservation_tree.pack(side= LEFT, fill= BOTH, expand= True, pady= (0, 25))

        scrollbar = ttk.Scrollbar(parent_frame, orient= "vertical", command= self.reservation_tree.yview)
        self.reservation_tree.config(yscrollcommand= scrollbar.set)
        scrollbar.pack(side= RIGHT, fill= Y)

class ViewReservationPage:
    def __init__(self, root):
        self.root = root

        # Load Icon
        self.search_icon = PhotoImage(file= "icons/search.png")

        #---------------- Main Frame ----------------
        self.header_frame = Frame(self.root)
        self.header_frame.pack(fill= X)

        self.features_frame = Frame(self.root)
        self.features_frame.pack(fill= X)

        self.reservation_table = Frame(self.root)
        self.reservation_table.pack(padx= 10, pady= (0, 10))
        #-------------------------------------------

        Label(self.header_frame, text="Reservation List", font=("Times", 27, "bold")).pack(side= LEFT, anchor= "w", padx= (5, 0),pady= (0, 10))

        current_date = datetime.now().strftime("%A, %d %B %Y")
        current_time = datetime.now().strftime("%I:%M %p")
        
        Label(self.header_frame, text= current_time, font= ("Times", 10)).pack(side= RIGHT, padx= (0, 20))
        Label(self.header_frame, text= current_date, font= ("Times", 12)).pack(side= RIGHT, padx= 15)

        self.search_entry = ctk.CTkEntry(self.features_frame, width= 250, placeholder_text="Search",
                                         border_color= "#DADADA")
        self.search_entry.pack(side= LEFT, anchor="w", padx= (10, 5))

        self.search_btn = Button(self.features_frame, image=self.search_icon, bd= 0, 
                                 command=self.searchReservation)
        self.search_btn.pack(side= LEFT)

        self.filter_box = ttk.Combobox(self.features_frame)
        self.filter_box.pack(side= RIGHT,anchor= "e", pady= (0, 10))

        self.cancelled_btn = ctk.CTkButton(self.features_frame, text= "Cancelled Reservations", width= 140, height= 30,
                                        fg_color= "#FFFFFF", font= ("Times", 12), text_color= "#000000",
                                        border_width= 2, border_color= "#DADADA")
        self.cancelled_btn.pack(side= RIGHT, anchor= "e", padx= (0, 16), pady= (0, 10))

        self.create_reservation_list_view(self.reservation_table)

    def create_reservation_list_view(self, parent_frame):
        # Treeview
        self.reservation_tree = ttk.Treeview(parent_frame, columns=("Booking Date", "Reservation Date", "Reservation Time", "Guest Name", "Number of People", "Reserved Table", "Contact Number"), show= "headings", height= 30)
        self.reservation_tree.heading("Booking Date", text= "Booking Date")
        self.reservation_tree.heading("Reservation Date", text= "Reservation Date")
        self.reservation_tree.heading("Reservation Time", text= "Reservation Time")
        self.reservation_tree.heading("Guest Name", text= "Guest Name")
        self.reservation_tree.heading("Number of People", text= "Number of People")
        self.reservation_tree.heading("Reserved Table", text= "Reserved Table")
        self.reservation_tree.heading("Contact Number", text= "Contact Number")

        self.reservation_tree.column("Booking Date", width= 200)
        self.reservation_tree.column("Reservation Date", width= 200)
        self.reservation_tree.column("Reservation Time", width= 200)
        self.reservation_tree.column("Guest Name", width= 200)
        self.reservation_tree.column("Number of People", width= 140)
        self.reservation_tree.column("Reserved Table", width= 140)
        self.reservation_tree.column("Contact Number", width= 200)

        self.reservation_tree.pack()

        scrollbar = ttk.Scrollbar(parent_frame, orient= "vertical", command= self.reservation_tree.yview)
        self.reservation_tree.configure(yscrollcommand= scrollbar.set)
        self.reservation_tree.pack(side= "left", fill= "y")
        scrollbar.pack(side= "right", fill= "y")

    def searchReservation(self):
        query = self.search_entry.get()
        messagebox.showinfo("Search", f"You searched for: {query}")


    





      





