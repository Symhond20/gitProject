from tkinter import * 
from reservation_page import ReservationPage, ViewReservationPage
from tkinter import ttk

window = Tk()
window.geometry("1500x900")
window.title("Restaurant Ordering System")

class SidebarMenu:
    def __init__(self, root):
        self.root = root
        
        # Load Icons
        self.dashboard_icon = PhotoImage(file="icons/dashboard.png")
        self.order_icon = PhotoImage(file="icons/order.png")
        self.reservation_icon = PhotoImage(file="icons/reservation.png")
        self.report_icon = PhotoImage(file="icons/report.png")
        self.foodMenu_icon = PhotoImage(file="icons/menu-food.png")
        self.logout_icon = PhotoImage(file="icons/logout.png")


        # ------------- Main frames ---------------
        self.sidebar_frame = Frame(self.root, bg='#D9D9D9')
        self.sidebar_frame.pack(side= LEFT, fill= Y)

        self.page_frame = Frame(self.root, bg='#D9D9D9')
        self.page_frame.pack(side= LEFT, fill= Y, padx= 30, pady= 10, anchor= "center")
        # ------------------------------------------

        
        # Side bar buttons
        self.dashboard_btn = Button(self.sidebar_frame, image=self.dashboard_icon, text="Dashboard", 
                                    font=('Helvetica', 10), bd= 0, bg="#DADADA",
                                    compound="left", anchor= "w", padx= 20,
                                    command=self.homePage)
        self.dashboard_btn.pack(fill=X, pady=(170, 50))

        self.customer_btn = Button(self.sidebar_frame, image=self.dashboard_icon, text="Customer", 
                                   font=('Helvetica', 10), bd= 0, bg="#DADADA",
                                   compound="left", anchor= "w", padx= 20,
                                   command=self.customerPage)
        self.customer_btn.pack(fill=X, pady=(0, 50))

        # Reservation buttons main frame
        self.reservation_btn_frame = Frame(self.sidebar_frame, bg="#DADADA")
        self.reservation_btn_frame.pack(fill=X, anchor="w")

        # Reservation subframe
        self.reservation_btn_subframe = Frame(self.reservation_btn_frame, bg="#DADADA")

        self.reservation_btn = Button(self.reservation_btn_frame, image=self.reservation_icon, text="Reservation", 
                                      font=('Helvetica', 10), bd=0, bg="#DADADA",
                                      compound="left", anchor="w", padx=20, 
                                      command=self.reservationOnClick)
        self.reservation_btn.pack(fill=X, anchor= 'w')

        # Reservation button sub buttons (make and view reservation)
        self.make_reservation_btn = Button(self.reservation_btn_subframe, text="Make Reservation", 
                                           font=('Helvetica', 10), bd=0, bg="#DADADA",
                                           command=self.addReservationPage)
        self.make_reservation_btn.pack(fill=X, pady=(5, 10))

        self.view_reservation_btn = Button(self.reservation_btn_subframe, text="View Reservations", 
                                           font=('Helvetica', 10), bd=0, bg="#DADADA",
                                           command=self.viewReservationPage)  # Fixed typo: removed extra space
        self.view_reservation_btn.pack(fill=X, pady=(0, 20))

        # Order buttons main frame
        self.order_btn_frame = Frame(self.sidebar_frame, bg="#DADADA")
        self.order_btn_frame.pack(fill=X, anchor="w")

        # Order button subframe
        self.order_btn_subframe = Frame(self.order_btn_frame, bg="#DADADA")

        self.order_btn = Button(self.order_btn_frame, image=self.order_icon, text="Order", 
                                font=('Helvetica', 10), bd=0, bg="#DADADA",
                                compound="left", anchor="w", padx= 20, 
                                command=self.orderOnClick)
        self.order_btn.pack(fill=X, anchor= "w", pady= (50, 0))

        # Order button sub buttons (view order and payment & billing)
        self.view_order_btn = Button(self.order_btn_subframe, text="View Orders", 
                                     font=('Helvetica', 10), bd=0, bg="#DADADA", 
                                     command= self.viewOrdersPage)
        self.view_order_btn.pack(fill=X, pady=(5, 10))

        self.billing_btn = Button(self.order_btn_subframe, text="Payment & Billing", 
                                  font=('Helvetica', 10), bd=0, bg="#DADADA",
                                  command= self.paymentPage)
        self.billing_btn.pack(fill=X, pady=(0, 10))
        
        # Continuation of sidebar buttons
        self.menu_btn = Button(self.sidebar_frame, image=self.foodMenu_icon, text="Menu", 
                               font=('Helvetica', 10), bd=0, bg="#DADADA",
                               compound= "left", anchor= "w", padx= 20, 
                               command=self.menuPage)
        self.menu_btn.pack(fill=X, pady= 50)

        report_btn = Button(self.sidebar_frame, image=self.report_icon, text="Report", 
                            font=('Helvetica', 10), bd=0, bg="#DADADA",
                            compound= "left", anchor= "w", padx= 20, 
                            command=self.reportPage)
        report_btn.pack(fill=X, pady=(0, 50))

    def homePage(self):
        for widgets in self.page_frame.winfo_children():
            widgets.destroy()

        

    def customerPage(self):
        for widgets in self.page_frame.winfo_children():
            widgets.destroy()

      

    def reservationOnClick(self):
        if self.order_btn_subframe.winfo_viewable():
            self.order_btn_subframe.pack_forget()
            self.order_btn.pack_configure(pady=(50, 0))
            self.menu_btn.pack_configure(pady=50)
        
        if self.reservation_btn_subframe.winfo_viewable():
            self.reservation_btn_subframe.pack_forget()
            self.order_btn.pack_configure(pady=(50, 0))
        else:
            self.reservation_btn_subframe.pack(fill=X, pady=(5, 0))
            self.order_btn.pack_configure(pady=0)
    
    def addReservationPage(self):
        for widgets in self.page_frame.winfo_children():
            widgets.destroy()

        ReservationPage(self.page_frame)

    def viewReservationPage(self):
        for widgets in self.page_frame.winfo_children():
            widgets.destroy()
        
        ViewReservationPage(self.page_frame)
    def tableManagerPage(self):
        for widgets in self.page_frame.winfo_children():
            widgets.destroy()
        # Title
        Label(self.page_frame, text="Table Manager", font=('Helvetica', 16, 'bold'), bg='#D9D9D9').pack(pady=10)
        # Create Treeview for displaying tables
        columns = ('ID', 'Table Number', 'Capacity', 'Status', 'Description')
        tree = ttk.Treeview(self.page_frame, columns=columns, show='headings', height=20)
        
        # Define column headings
        tree.heading('ID', text='ID')
        tree.heading('Table Number', text='Table Number')
        tree.heading('Capacity', text='Capacity')
        tree.heading('Status', text='Status')
        tree.heading('Description', text='Description')
        
        # Define column widths
        tree.column('ID', width=50, anchor='center')
        tree.column('Table Number', width=100, anchor='center')
        tree.column('Capacity', width=80, anchor='center')
        tree.column('Status', width=100, anchor='center')
        tree.column('Description', width=300, anchor='w')
        
        # Fetch and insert data

    def orderOnClick(self):
        if self.reservation_btn_subframe.winfo_viewable():
            self.reservation_btn_subframe.pack_forget()
            self.order_btn.pack_configure(pady=(50, 0))
        
        if self.order_btn_subframe.winfo_viewable():
            self.order_btn_subframe.pack_forget()  
            self.order_btn.pack_configure(pady=(50, 0))
            self.menu_btn.pack_configure(pady=50)
        else:
            self.order_btn_subframe.pack(fill=X, pady=(5, 10))  
            self.menu_btn.pack_configure(pady=(0, 50))

    def viewOrdersPage(self):
        for widgets in self.page_frame.winfo_children():
            widgets.destroy()

        

    def paymentPage(self):
        for widgets in self.page_frame.winfo_children():
            widgets.destroy()

        Label(self.page_frame, text= "Payment & Billing").pack()

    def menuPage(self):
        for widgets in self.page_frame.winfo_children():
            widgets.destroy()

        

    def reportPage(self):
        for widgets in self.page_frame.winfo_children():
            widgets.destroy()

        Label(self.page_frame, text= "Reports").pack()

sidebar = SidebarMenu(window)
window.mainloop()