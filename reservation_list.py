from tkinter import *
from tkinter import ttk, messagebox
import customtkinter as ctk
from datetime import datetime
from backend_reservation import TableManager, ReservationManager
from reservation_page import ReservationPage

ctk.set_appearance_mode("light")

class ViewReservationPage:
    def __init__(self, root):
        self.root = root
        self.reservation_manager = ReservationManager()
        self.table_manger = TableManager()

        # Style
        self.style = ttk.Style()
        self.style.configure("Treeview", font= ("", 10))
        self.style.configure("Treeview.Heading", font= ("Times", 11, "bold"))

        # Icons
        self.search_icon = PhotoImage(file="icons/search.png")
        self.add_icon = PhotoImage(file="icons/add.png")

        # Main Frames
        self.header_frame = Frame(self.root)
        self.header_frame.pack(fill= X, pady= 10, padx= 10)

        self.features_frame = Frame(self.root)
        self.features_frame.pack(fill= X, padx= 10, pady= 0)

        self.reservation_table = Frame(self.root)
        self.reservation_table.pack(side= LEFT, padx= 10)

        # Sub Frame
        self.treeview_frame = Frame(self.reservation_table)
        self.treeview_frame.pack()

        # Header frame contents
        ttk.Label(self.header_frame, text= "Reservation List", font= ("Times", 27, "bold")).pack(side= LEFT, anchor= "w")
        self.create_btn = Button(self.header_frame, image= self.add_icon, text= "Add New Reservations", compound= "left", anchor= "w", padx= 17, height= 27, 
                                 font= ("Times", 9),
                                 command= self.createReservation)
        self.create_btn.pack(side= RIGHT, padx= (10, 20))

        self.date_today = datetime.now().strftime("%A, %d %B %Y")
        Label(self.header_frame, text=self.date_today, font=("Times", 11)).pack(side=RIGHT)

        # Features frame contents
        self.search_btn = Button(self.features_frame, image= self.search_icon, bd= 0, command= self.searchReservation)
        self.search_btn.pack(side= RIGHT, padx= 10)
        self.search_entry = ctk.CTkEntry(self.features_frame, width= 250, placeholder_text= "Search by name", border_color= "#DADADA", height= 30)
        self.search_entry.pack(side=RIGHT)

        self.filter_box = ttk.Combobox(self.features_frame, values=["Date", "Time", "Name", "Cancelled Reservations"], state="readonly", height= 50)  
        self.filter_box.pack(side=RIGHT, padx= (7, 27))
        Label(self.features_frame, text= "Filter By:").pack(side= RIGHT)
        self.filter_box.set("")  
        self.filter_box.bind("<<ComboboxSelected>>", self.filterReservation)

        self.cancel_btn = Button(self.features_frame, text="Cancel Reservations", pady= 5, command= self.cancelReservation)
        self.cancel_btn.pack(side=LEFT, padx= (10, 20))

        self.delete_btn = Button(self.features_frame, text="Delete Reservation", pady= 5, command= self.deleteReservation)
        self.delete_btn.pack(side=LEFT, padx= (10, 20))

        self.view_btn = Button(self.features_frame, text="View Detail", pady= 5, command= self.viewReservation)
        self.view_btn.pack(side=LEFT, padx= (10, 20))

        self.show_all_btn = Button(self.features_frame, text="Show All", font= ("Times", 10), pady= 5, command= self.showAllReservation)
        self.show_all_btn.pack(side=LEFT, padx= (10, 20))

        self.createReservationListView(self.treeview_frame)
        self.reservationTableValue()
    
    def viewReservation(self): # Not done yet
        selected_item = self.reservation_tree.selection()
        if not selected_item:
            messagebox.showerror("No selection", "Please select a reservation from the list first, to view.")
            return
        
        self.order_window = Toplevel(self.root)
        self.order_window.geometry("400x300")
        self.order_window.title("Reservation Detail")
    
    def deleteReservation(self): # Done
        selected_item = self.reservation_tree.selection()
        if not selected_item:
            messagebox.showerror("No selection", "Please a reservation from the list first, to delete.")
            return
        
        selected_item = selected_item[0]
        values = self.reservation_tree.item(selected_item, "values")
        reservation_id = values[0]
        guest_name = values[3]  
        status = values[4]  

        if status.lower() == "deleted":
            messagebox.showerror("Already Deleted", f"The reservation for {guest_name} is already deleted.")
            return
        confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete reservation for {guest_name}?")
        
        if confirm:
            reservation_id = selected_item
            result = self.reservation_manager.removeReservation(reservation_id)  
            if result == "success":
                messagebox.showinfo("Success", "Reservation is successfully deleted.")
                self.reservationTableValue() 
            else:
                messagebox.showerror("Error", f"Failed to delete reservation: {result}")
    
    def showAllReservation(self): # Done
        self.reservationTableValue()
        
    def cancelReservation(self):  # Done
        selected_item = self.reservation_tree.selection()
        if not selected_item:
            messagebox.showerror("No selection", "Please seect a reservation from the list first, to cancel.")
            return

        selected_item = selected_item[0] # for iid i treeview
        values = self.reservation_tree.item(selected_item, "values")
        guest_name = values[3] # gets the name in the treeview (which is in column 4)
        status = values[7] # gets the status in the treeview (which is in column 7)

        if status.lower() == "cancelled":
            messagebox.showerror("Already Cancelled", f"The reservation for {guest_name} is already cancelled.")
            return

        confirm = messagebox.askyesno("Confirm Cancellation", f"Are you sure you want to cancel reservation for {guest_name}?")
        if confirm:
            reservation_id = selected_item
            result = self.reservation_manager.cancelReservation(reservation_id)
            if result == "success":
                messagebox.showinfo("Success", "Reservation cancelled successfully")
                self.reservationTableValue()
            else:
                messagebox.showerror("Error", f"Failed to cancel reservation: {result}")

    def filterReservation(self, event=None):  # Done
        selected_filter = self.filter_box.get()

        if selected_filter == "Date":
            result = self.reservation_manager.viewReservationByDate() 
        elif selected_filter == "Name":
            result = self.reservation_manager.viewReservationByName()  
        elif selected_filter == "Time": 
            result = self.reservation_manager.viewReservationByTime()  
        elif selected_filter == "Cancelled Reservations": 
            result = self.reservation_manager.viewCancelledReservations()
        else:
            result = None  
        self.reservationTableValue(result)

    def searchReservation(self):  # Done
        to_search = self.search_entry.get()

        if not to_search:
            messagebox.showwarning("Warning", "Please enter name to search")
            return
        
        for item in self.reservation_tree.get_children():
            self.reservation_tree.delete(item)
        
        result = self.reservation_manager.searchReservation(to_search)

        if not result:
            messagebox.showinfo("No Results", f"No reservations found for '{to_search}'.")

        for reservation_id, guest_name, contact, selected_date, selected_time, guest_count, table_number, reservation_status, booking_date, cancelled_at  in result:
            try:
                fromatted_time = datetime.strptime(str(selected_time), "%H:%M:%S")
                display_time = fromatted_time.strftime("%I:%M %p").lstrip("0")
            except Exception:
                display_time = str(selected_time)

            if cancelled_at:
                try:
                    formatted_dt = datetime.strptime(str(cancelled_at), "%Y-%m-%d %H:%M:%S")
                    cancelled_at_display = formatted_dt.strftime("%Y-%m-%d    %I:%M %p").lstrip('0')
                except Exception:
                    cancelled_at_display = str(cancelled_at)
            else:
                cancelled_at_display = "N/A"

            self.reservation_tree.insert("", END, iid=str(reservation_id), values=(booking_date, selected_date, display_time, guest_name, guest_count, table_number, contact,  reservation_status, cancelled_at_display))  # Assuming contact is last

    def createReservation(self): # Done
        for widgets in self.root.winfo_children():
            widgets.destroy()

        ReservationPage(self.root)

    def reservationTableValue(self, result=None):  # Done
        for item in self.reservation_tree.get_children():
            self.reservation_tree.delete(item)

        if result is None:  
            result = self.reservation_manager.viewAll()

        for reservation_id, guest_name, contact, reservation_date, reservation_time, guest_count, instructions, table_id, status, created_at, booking_date, cancelled_at in result:
            table_number = f"{table_id}"
            self.reservation_tree.insert("", "end", iid=str(reservation_id), values=(booking_date, reservation_date, reservation_time, guest_name, guest_count, table_number, contact, status, cancelled_at))

    def createReservationListView(self, parent_frame):  # Done
        tree_frame = Frame(parent_frame, width= 700)
        tree_frame.pack(fill=BOTH, expand=True)

        self.reservation_tree = ttk.Treeview(tree_frame, columns=("Booking Date", "Reservation Date", "Reservation Time", "Guest Name", "Number of People", "Reserved Table", "Contact Number",  "Status", "Cancelled Date"), show="headings", height=30, selectmode= "browse")
        self.reservation_tree.heading("Booking Date", text= "Booking Date")
        self.reservation_tree.heading("Reservation Date", text= "Reservation Date")
        self.reservation_tree.heading("Reservation Time", text= "Reservation Time")
        self.reservation_tree.heading("Guest Name", text= "Guest Name")
        self.reservation_tree.heading("Number of People", text= "Number of People")
        self.reservation_tree.heading("Reserved Table", text= "Reserved Table")
        self.reservation_tree.heading("Contact Number", text= "Contact Number")
        self.reservation_tree.heading("Status", text= "Status")
        self.reservation_tree.heading("Cancelled Date", text= "Cancelled Date")

        self.reservation_tree.column("Booking Date", width= 170, anchor= "center")
        self.reservation_tree.column("Reservation Date", width= 170, anchor= "center")
        self.reservation_tree.column("Reservation Time", width= 170, anchor= "center")
        self.reservation_tree.column("Guest Name", width= 170)
        self.reservation_tree.column("Number of People", width= 140, anchor= "center")
        self.reservation_tree.column("Reserved Table", width= 140, anchor= "center")
        self.reservation_tree.column("Contact Number", width= 160, anchor= "center")
        self.reservation_tree.column("Status", width= 160, anchor= "center")
        self.reservation_tree.column("Cancelled Date", width= 190, anchor= "center")
        self.reservation_tree.pack(side=LEFT, fill=BOTH, expand=True)

        y_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.reservation_tree.yview)
        y_scrollbar.pack(side=RIGHT, fill=Y)
        self.reservation_tree.config(yscrollcommand=y_scrollbar.set)

        x_scrollbar = ttk.Scrollbar(parent_frame, orient="horizontal", command=self.reservation_tree.xview)
        x_scrollbar.pack(side=BOTTOM, fill=X)
        self.reservation_tree.config(xscrollcommand=x_scrollbar.set)
