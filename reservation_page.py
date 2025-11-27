from tkinter import *
from datetime import datetime
import customtkinter as ctk
from tkinter import ttk, messagebox
from backend_reservation import TableManager, ReservationManager

ctk.set_appearance_mode("light")

class ReservationPage:
    def __init__(self, root):
        self.root = root
        self.table_manager = TableManager()
        self.reservation_manager = ReservationManager()

        self.style = ttk.Style()
        self.style.configure("Treeview", font= ("", 9))
        self.style.configure("Treeview.Heading", font= ("Times", 10, "bold"))

        self.add_icon = PhotoImage(file="icons/add.png")
        
        # Main Frames
        self.page_header_frame = Frame(self.root, bg=  "#3c5070")
        self.page_header_frame.pack(fill= X, anchor= "n", pady= 10, padx= 25)

        self.form_frame = Frame(self.root, bg= "white")
        self.form_frame.pack(side= LEFT, anchor= "n", padx= 25)

        self.table_view_frame = Frame(self.root, bg= "white")
        self.table_view_frame.pack(side= LEFT, anchor= "n", padx= 10)

        self.reservation_view_frame = Frame(self.root, bg= "white")
        self.reservation_view_frame.pack(side= LEFT, anchor= "n", padx= 10)

        # Sub Frames
        self.table_header = Frame(self.table_view_frame, bg= "white")
        self.table_header.pack(fill= X, anchor= "e")

        self.table_frame = Frame(self.table_view_frame, bg= "white")
        self.table_frame.pack()

        self.order_frame = Frame(self.table_view_frame, width= 440, height= 700, bg= "white", highlightbackground= "gray", highlightthickness= 2)
        self.order_frame.pack_propagate(False)
        self.order_frame.pack(anchor= "w", pady= 30)

        self.reservation_header = Frame(self.reservation_view_frame, bg= "white")
        self.reservation_header.pack(fill= X, anchor= "e")

        self.reservation_frame = Frame(self.reservation_view_frame, bg= "white")
        self.reservation_frame.pack()

        # Contents
        Label(self.page_header_frame, text= "Make a Reservation", font= ("Times", 27, "bold"), bg=  "#3c5070", fg= "#f5f0e9").pack(side= LEFT)
        Label(self.page_header_frame, text= datetime.now().strftime("%A, %d %B %Y"), font= ("Times", 12), bg=  "#3c5070", fg= "#f5f0e9").pack(anchor= "e")
        Label(self.page_header_frame, text= datetime.now().strftime("%I:%M %p"), font= ("Times", 11), bg=  "#3c5070", fg= "#f5f0e9").pack(anchor= "e")

        # Form Section
        Label(self.form_frame, text= "Full Name:", font= ("Times", 11)).pack(anchor= "w")
        self.name_entry = ctk.CTkEntry(self.form_frame, width= 260, corner_radius= 3)
        self.name_entry.pack(anchor= "w", pady= (0, 25))

        Label(self.form_frame, text= "Contact Number:", font= ("Times", 11)).pack(anchor= "w")
        self.contact_entry = ctk.CTkEntry(self.form_frame, width= 260, corner_radius= 3)
        self.contact_entry.pack(anchor= "w", pady= (0, 25))

        Label(self.form_frame, text= "Selected Date (YYYY-MM-DD):", font= ("Times", 11)).pack(anchor= "w")
        self.date_entry = ctk.CTkEntry(self.form_frame, width= 260, corner_radius= 3)
        self.date_entry.pack(anchor= "w", pady= (0, 25))

        Label(self.form_frame, text= "Selected Time (HH:MM AM/PM):", font= ("Times", 11)).pack(anchor= "w")
        self.time_entry = ctk.CTkEntry(self.form_frame, width= 260, corner_radius= 3)
        self.time_entry.pack(anchor= "w", pady= (0, 25))

        Label(self.form_frame, text= "Guest Count:", font= ("Times", 11)).pack(anchor= "w")
        self.guest_count_entry = ctk.CTkEntry(self.form_frame, width= 260, corner_radius= 3)
        self.guest_count_entry.pack(anchor= "w", pady= (0, 25))

        Label(self.form_frame, text= "Special Instructions:", font= ("Times", 11)).pack(anchor= "w")
        self.notes_entry = ctk.CTkTextbox(self.form_frame, width= 260, corner_radius= 3,  border_width= 2)
        self.notes_entry.pack(anchor= "w", pady= (0, 25))

        self.cancel_btn = Button(self.form_frame, text= "Cancel", height= 1, width= 20, relief= RIDGE, command= self.clearForm)
        self.cancel_btn.pack(anchor= "w")

        Label(self.table_header, text= "Selected Table:", font= ("Times", 11)).pack(side= LEFT, anchor= "w", pady= (0, 5))
        self.table_entry = ctk.CTkEntry(self.table_header, width= 40, corner_radius= 3, state="readonly")
        self.table_entry.pack(side= LEFT, anchor= "w", pady= (0, 7), padx= 10)

         # Calls the Table View
        self.creatTableTreeview(self.table_frame)

        # Table frame buttons
        self.show_btn = Button(self.table_header, text= "Show Tables", height= 1, width= 10, relief= RAISED, command= self.showAllTable)
        self.show_btn.pack(side= RIGHT, pady= (0, 5), padx= (10, 15))

        self.filter_btn = Button(self.table_header, text= "Filter Tables", height= 1, width= 10, relief= RAISED, command= self.showFilteredTable)
        self.filter_btn.pack(side= RIGHT, pady= (0, 5), padx= 10)

        # Advanced Order Button
        Label(self.order_frame, text= "Advanced Order", font= ("Times", 12), bg= "white").pack(pady= 10)
        self.advanced_order_btn = Button(self.order_frame, image= self.add_icon, text= "Advanced Order", relief= RAISED, compound= "left", padx= 5, pady= 5,
                                         command= self.orderWindow)
        self.advanced_order_btn.pack(side= BOTTOM, anchor= "e", padx= 10, pady= 10)
        
        # Advanced Order Items
        self.order_summary = None
        self.view_order_mode = False

        Label(self.reservation_header, text= "Current Reservations Today", font= ("Times", 12)).pack(anchor= "w", pady= (0, 12))
        
        # Calls the Reservation view
        self.createReservationTreeview(self.reservation_frame)

        self.add_btn = Button(self.reservation_view_frame, text= "Add Reservation", height= 1, width= 20, relief= RAISED, command= self.submitReservation)
        self.add_btn.pack(anchor= "e", pady= (25, 0))

        # Uses the curreny date
        self.showAllTable()
        self.showCurrentReservation()

        self.table_tree.bind("<<TreeviewSelect>>", self.selectedRow)

    def orderWindow(self): 
        self.order_window = Toplevel(self.root)
        self.order_window.geometry("400x300")
        self.order_window.title("Advanced Order")
    
    def clearForm(self): # Done
        self.name_entry.delete(0, 'end')
        self.contact_entry.delete(0, 'end')
        self.date_entry.delete(0, 'end')
        self.time_entry.delete(0, 'end')
        self.guest_count_entry.delete(0, 'end')
        self.notes_entry.delete("1.0", 'end')
        self.table_entry.configure(state="normal")
        self.table_entry.delete(0, 'end')
        self.table_entry.configure(state="readonly")
    
    def creatTableTreeview(self, parent): # Done
        self.table_tree = ttk.Treeview(parent, columns= ("Capacity", "Status", "Time"), show= "tree headings", height= 20, selectmode= "browse")
        self.table_tree.heading("#0", text= "Table Number")
        self.table_tree.heading("Capacity", text= "Capacity")
        self.table_tree.heading("Status", text= "Status")
        self.table_tree.heading("Time", text= "Time")

        self.table_tree.column("#0", width= 140)
        self.table_tree.column("Capacity", width= 90)
        self.table_tree.column("Status", width= 90)
        self.table_tree.column("Time", width= 100, anchor= "center")
        self.table_tree.pack(side= LEFT, fill= BOTH, expand= TRUE)

        scrollbar = ttk.Scrollbar(parent, orient= "vertical", command= self.table_tree.yview)
        self.table_tree.config(yscrollcommand= scrollbar.set)
        scrollbar.pack(side= RIGHT, fill= Y)     

    def createReservationTreeview(self, parent): # Done
        tree_frame = Frame(parent)
        tree_frame.pack(fill= BOTH, expand= True)

        self.reservation_tree = ttk.Treeview(tree_frame, columns= ("Reservation ID", "Selected Time", "Table Number", "Guest Count", "Reservation Status"), show= "headings", height= 27) 
        self.reservation_tree.heading("Reservation ID", text= "Reservation ID")
        self.reservation_tree.heading("Selected Time", text= "Selected Time")
        self.reservation_tree.heading("Table Number", text= "Table Number")
        self.reservation_tree.heading("Guest Count", text= "Guest Count")
        self.reservation_tree.heading("Reservation Status", text= "Reservation Status")

        self.reservation_tree.column("Reservation ID", width= 130, anchor= "center")
        self.reservation_tree.column("Selected Time", width= 130, anchor= "center")
        self.reservation_tree.column("Table Number", width= 120, anchor= "center")
        self.reservation_tree.column("Guest Count", width= 100, anchor= "center")
        self.reservation_tree.column("Reservation Status", width= 130, anchor= "center")
        self.reservation_tree.pack(side= LEFT, fill= BOTH, expand= True)

        yscrollbar = ttk.Scrollbar(tree_frame, orient= "vertical", command= self.reservation_tree.yview)
        yscrollbar.pack(side= RIGHT, fill= Y)   
        self.reservation_tree.config(yscrollcommand= yscrollbar.set)

        xscrollbar = ttk.Scrollbar(parent, orient= "horizontal", command= self.reservation_tree.xview)
        xscrollbar.pack(side= BOTTOM, fill= X)   
        self.reservation_tree.config(xscrollcommand= xscrollbar.set)

    def selectedRow(self, event): # Done
        selected_data = self.table_tree.selection()
        if not selected_data:
            return
        
        item = selected_data[0]

        for child in self.table_tree.get_children():
            if child != selected_data:
                self.table_tree.item(child, open= FALSE)
        
        if self.table_tree.get_children(item):
            self.table_tree.item(item, open= TRUE)
            table_number = self.table_tree.item(item, "text")
            self.table_entry.configure(state= "normal")
            self.table_entry.delete(0, 'end')
            self.table_entry.insert(0, table_number)
            self.table_entry.configure(state= "readonly")
        else:
            self.table_tree.selection_remove(item)

    def showAllTable(self, date=None): # Done
        for item in self.table_tree.get_children():
            self.table_tree.delete(item)

        if date is None:
            formatted_date = datetime.now().strftime("%Y-%m-%d")
            view = self.table_manager.viewAll(formatted_date)
        else:
            view = self.table_manager.viewAll(date)
        
        for id, table_number, capacity, status, time, description in view:
            if time:
                try:
                    formatted_time = datetime.strptime(str(time), "%H:%M:%S")
                    display_time = formatted_time.strftime("%I:%M %p").lstrip("0")
                except Exception:
                    display_time = str(time)
            else:
                display_time = "N/A"
            
            status_display = "reserved" if time else "available"
            parent = self.table_tree.insert("", "end", iid= str(id), text= table_number, values= (capacity, status_display, display_time))
            self.table_tree.insert(parent, "end", text= description, values= ("","",""))

    def showFilteredTable(self): # Done
        try:
            date = self.date_entry.get().strip()
            guest = self.guest_count_entry.get()
            
            if not date and not guest:
                messagebox.showwarning("No Input Error", "Please enter date and guest count.")
                return
            if not guest:
                messagebox.showwarning("Input Error", "Please enter guest count (number).")
                return
            if not date:
                messagebox.showwarning("Input Error", "Please enter a date.")
                return
         
            guest_count_int = int(guest)
            if guest_count_int <= 0:
                messagebox.showwarning("Input Error", "Please enter valid input guest count (no zero and negative number).")
                return
            datetime.strptime(date, "%Y-%m-%d")
                
        except ValueError:
            messagebox.showwarning("Input Error", "Please enter valid date format (YYYY-MM-DD) and guest count (number)")
            return
        
        for item in self.table_tree.get_children():
            self.table_tree.delete(item)

        filtered_data = self.table_manager.viewFilteredTable(date, guest_count_int)

        for table_id, table_num, capacity, description, status, time in filtered_data:
            if time:
                try:
                    formatted_time = datetime.strptime(str(time), "%H:%M:%S")
                    display_time = formatted_time.strftime("%I:%M %p").lstrip("0")
                except Exception:
                    display_time = str(time)
            else:
                display_time = "-"

            status_display = "reserved" if time else "available"
            parent = self.table_tree.insert("", "end", iid= str(table_id), text= table_num, values= (capacity, status_display, display_time))
            self.table_tree.insert(parent, "end", text= f" Description: {description}", values= ("", "", ""))

    def submitReservation(self): # Done
        name = self.name_entry.get().title() 
        contact = self.contact_entry.get()
        date = self.date_entry.get()
        time = self.time_entry.get()
        guest_count = self.guest_count_entry.get()
        notes = self.notes_entry.get("1.0", "end").strip()
        table_number = self.table_entry.get()

        if not name or not contact or not date or not time or not guest_count or not table_number:
            messagebox.showwarning("Input Error", "Please fill up required entries.")
            return
        
        # Checks the guest count
        try:
            guest_count_int = int(guest_count) # Converts guest count to integer
            if guest_count_int <= 0:
                messagebox.showwarning("Input Error", "Please enter valid input guest count (no zero and negative number).")
                return
        except ValueError:
            messagebox.showwarning("Input Error", "Please enter valid guest count (numeric characters only).")
            return
        # Checks the contact nunmber
        if not contact.isdigit():
            messagebox.showwarning("Input Error", "Contact number must oonly contain numeric chracters.")
            return

        if len(contact) != 11:
            messagebox.showwarning("Input Error", "Contact number must be 11 digits and numeric only (e.g., 09122919463)")
            return
        if not contact.startswith('09'):
            messagebox.showwarning("Input Error", "Contact must start with '09', (e.g., 09122919463)")
            return
        # checks the contact number 
        try:
            contact_number = int(contact)
        except ValueError:
            messagebox.showwarning("Input Error", "Invalid contact number format.")
        # Checks the date format
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            messagebox.showwarning("Invalid Date Format", "Plaese enter a valid date format YYYY-MM-DD.") 
            return
        # Checks the time format    
        try:
            input_time = datetime.strptime(time, "%I:%M %p").time() # If the format is not like this 
        except ValueError:
            messagebox.showwarning("Invalid Time Format", "Plaese enter a valid time format HH:MM AM/PM (e.g., 9:00 AM)") 
            return
        
        input_hour = input_time.hour
        input_minute = input_time.minute
        opening_hour = 8
        opening_minute = 0
        cutoff_hour = 22
        cutoff_minute = 0

        if (input_hour < opening_hour) or (input_hour == opening_hour and input_minute < opening_minute):
            messagebox.showwarning("Input Error", "Reservations are not allowed before 8:00 AM (opening time).")
            return
        if input_hour == 0 and input_minute == 0:
            messagebox.showwarning("Input Error", "Reservations cannot be made for 12:00 AM (midnight). Please select a different time.")
            return
        if (input_hour > cutoff_hour) or (input_hour == cutoff_hour and input_minute >= cutoff_minute):
            messagebox.showwarning("Input Error", "Reservations are not allowed after or at 10:00 PM (closing time is 11:00 PM).")
            return
        
        time_24h = input_time.strftime("%H:%M")

        result = self.reservation_manager.addReservation(name, contact, date, time_24h, guest_count, notes, table_number)

        if result == "success":
            messagebox.showinfo("Success", "Reservation is successfully added.")
            self.table_tree.selection_remove(self.table_tree.selection())
            self.clearForm()
            self.showAllTable()
            self.showCurrentReservation()
        elif result == 'empty_fields':
            messagebox.showwarning("Input Error", "Fill in all required fields.")
        elif result == "already_exists":
            messagebox.showerror('Duplicate Error', "A reservtion with the same details already exists.")
        else:
            print(f"Debug {result}")
            messagebox.showerror("Error", "An unexpected error occurred.")
        
    def showCurrentReservation(self, date=""): # Done
        for item in self.reservation_tree.get_children():
            self.reservation_tree.delete(item)

        if date == "":
            date = datetime.now().strftime("%Y-%m-%d")

        reservations = self.reservation_manager.viewInfo(date)

        for reservation_id, time, table_num, guest_count, status  in reservations:
            if time:
                try:
                    formatted_time = datetime.strptime(str(time), "%H:%M:%S")
                    display_time = formatted_time.strftime("%I:%M %p").lstrip("0")
                except Exception:
                    display_time = str(time)
            else:
                display_time = "N/A"
            
            self.reservation_tree.insert("", "end", values=(reservation_id, display_time, table_num, guest_count, status))