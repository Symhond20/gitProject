from tkinter import *
import customtkinter as ctk
from tkinter import messagebox, ttk
from backend_menu import MenuCreation  
from datetime import datetime

ctk.set_appearance_mode("light")

class MenuGui:
    def __init__(self, root):
        self.root = root
        self.menu = MenuCreation()

        self.search_icon = PhotoImage(file="icons/search.png")
        
        # Main Frames
        self.header_frame = Frame(self.root)
        self.header_frame.pack(fill= X, anchor= "n", pady= 10, padx= 10)
        
        self.features_frame = Frame(self.root)
        self.features_frame.pack(fill= X, padx= 10, pady= 10)

        self.menu_form_frame = Frame(self.root, bg= "white")
        self.menu_form_frame.pack(side = LEFT, anchor="n", padx=10)
        
        self.menu_tree_frame = Frame(self.root)
        self.menu_tree_frame.pack(side= LEFT, anchor= "n", padx= 10)

        # Feature frame contents
        self.search_entry = ctk.CTkEntry(self.features_frame, width= 250, placeholder_text= "Search by name", border_color= "#DADADA", height= 30)
        self.search_entry.pack(side=LEFT)
        self.search_btn = Button(self.features_frame, image= self.search_icon, bd= 0)
        self.search_btn.pack(side= LEFT, padx= 10)

        # Header frame contents
        Label(self.header_frame, text="Menu Management", font=("Times", 27, "bold")).pack(side= LEFT)
        Label(self.header_frame, text=datetime.now().strftime("%A, %d %B %Y"), font=("Times", 12)).pack(anchor= "e") 
        Label(self.header_frame, text=datetime.now().strftime("%I:%M %p"), font=("Times", 11)).pack(anchor= "e")

        # Menu Form Frame contents
        Label(self.menu_form_frame, text="Dish name:", font=("Times", 12)).pack(anchor="w")
        self.name_entry = ctk.CTkEntry(self.menu_form_frame,placeholder_text="Enter name...", width=260)  
        self.name_entry.pack(anchor="w", pady=(0, 25))

        Label(self.menu_form_frame, text="Description:", font=("Times", 12)).pack(anchor="w")
        self.description_entry = ctk.CTkTextbox(self.menu_form_frame, width= 260, height= 100, corner_radius= 3, border_width= 2)
        self.description_entry.pack(anchor= "w", pady= (0, 25))

        Label(self.menu_form_frame, text="Price:", font=("Times", 12)).pack(anchor="w")
        self.price_entry = ctk.CTkEntry(self.menu_form_frame, placeholder_text="Enter price...", width=260)
        self.price_entry.pack(anchor="w", pady=(0, 25))

        # Dropdown menu for Cuisines
        Label(self.menu_form_frame, text="Select Cuisine:", font=("Times", 12)).pack(anchor="w")
        cuisines = self.menu.get_cuisines()
        if isinstance(cuisines, str):
            messagebox.showerror("Error", cuisines)
            cuisine_names = ["No cuisines available"]  
        else:   
            cuisine_names = []
            for c in cuisines:
                cuisine_names.append(c[1])
        self.cuisine_combo = ttk.Combobox(self.menu_form_frame, values=cuisine_names, width=27,state="readonly")
        self.cuisine_combo.pack(anchor="w", pady=(0, 25))

        # Dropdown menu for Courses
        Label(self.menu_form_frame, text="Select Category:", font=("Times", 12)).pack(anchor="w")
        categories = self.menu.get_categories()
        if isinstance(categories, str):
            messagebox.showerror("Error", categories)
            cat_names = ["No Category availlable"]  
        else:
            cat_names = []
            for cat in categories:
                cat_names.append(cat[1])
        self.cat_combo = ttk.Combobox(self.menu_form_frame, values=cat_names, width=27,state="readonly")
        self.cat_combo.pack(anchor="w",  pady=(0, 25))

        Label(self.menu_form_frame, text="Preparation Time (minutes):").pack(anchor="w", pady=5)
        self.prep_entry = ctk.CTkEntry(self.menu_form_frame,placeholder_text="Enter prepartion time...", width=260)
        self.prep_entry.pack(anchor="w", pady=(0, 25))
   
        # Add and cancel btn
        self.add_btn = Button(self.menu_form_frame, text="Add", font=("Times",10), height= 1, width= 10, relief= RIDGE, command=self.add_meal)
        self.add_btn.pack(side=LEFT, padx=5, pady=(25, 0))

        self.cancel_btn = Button(self.menu_form_frame, text="Cancel", font=("Times",10), height= 1, width= 10, relief= RIDGE, command= self.clear_form)
        self.cancel_btn.pack(side=RIGHT , padx=5,  pady=(25, 0))

        self.creatTableTree(self.menu_tree_frame)
        
        Label(self.features_frame,text="Filter by Category:").pack(side=RIGHT, padx=5)
        category_names_filter = ["All"]
        cat_ids = [None]

        if not isinstance(categories, str):
             for cat_id, cat_name in categories:
                category_names_filter.append(cat_name)
                cat_ids.append(cat_id)
        self.cat_combo_filter = ttk.Combobox(self.features_frame, values=category_names_filter, state="readonly", width=20)
        self.cat_combo_filter.set("All")
        self.cat_combo_filter.pack(side=RIGHT, padx=5)
        self.cat_combo_filter.bind("<<ComboboxSelected>>", self.filter_menu)

        self.update_btn= Button(self.features_frame, text="Update", width=10, command=self.open_update_window)
        self.update_btn.pack(side= RIGHT, padx=10)

        self.displayAll()
 
    def creatTableTree(self,parent): #Done
        columns = ("Name", "Price", "Availability", "Preparation Time", "Category", "Cuisine")
        self.table_tree = ttk.Treeview(parent, columns = columns, show="tree headings", height= 30)
        self.table_tree.heading("#0", text= "ID")
        self.table_tree.heading("Name", text= "Name")
        self.table_tree.heading("Price", text= "Price")
        self.table_tree.heading("Availability", text= "Availability")
        self.table_tree.heading("Preparation Time", text= "Preparation Time")
        self.table_tree.heading("Category", text= "Category")
        self.table_tree.heading("Cuisine", text= "Cusine")
        

        self.table_tree.column("#0",  width= 100)
        self.table_tree.column("Name",width= 150,anchor="center")
        self.table_tree.column("Price", width= 150,anchor="center")
        self.table_tree.column("Availability", width= 150,anchor="center")
        self.table_tree.column("Preparation Time", width= 150,anchor="center")
        self.table_tree.column("Category", width= 150,anchor="center")
        self.table_tree.column("Cuisine", width= 150,anchor="center")
        self.table_tree.pack(side= LEFT, fill= Y, expand= TRUE)

        scrollbar = ttk.Scrollbar(parent, orient= "vertical", command= self.table_tree.yview)
        self.table_tree.config(yscrollcommand= scrollbar.set)
        scrollbar.pack(side= RIGHT, fill= Y) 
        self.table_tree.bind("<<TreeviewSelect>>", self.selectedRow)
       
    def selectedRow(self, event): #Done
        selected_data = self.table_tree.selection()
        if not selected_data:
            return
        
        item = selected_data[0]

        for child in self.table_tree.get_children():
            if child != selected_data:
                self.table_tree.item(child, open= FALSE)
        
        if self.table_tree.get_children(item):
            self.table_tree.item(item, open= TRUE)
        else:
            self.table_tree.selection_remove(item)
        
    def displayAll(self, course_id=None):
        for item in self.table_tree.get_children():
            self.table_tree.delete(item)

        meals = self.menu.display(course_id=course_id)
        if isinstance(meals, str):
            messagebox.showerror("Error", meals)
            return

        for meal in meals:
            meal_id, name, description, price, availability, prep_time, cuisine_name, category_name = meal
            avail_text = "Available" if availability else "Not Available"

            parent = self.table_tree.insert("", END, iid=str(meal_id),text= meal_id,values=(name, f"₱ {price}", avail_text, f"{prep_time} mins", category_name, cuisine_name))
            self.table_tree.insert(parent, END,values=("", description,"", "", "", "", ""))
    
    def filter_menu(self, event=None):
        selected_category_name = self.cat_combo_filter.get()
        if selected_category_name == "All":
            selected_category_id = None
        else: 
            all_categories = self.menu.get_categories()
            selected_category_id = None
            
            for category in all_categories:
                if len(category) >= 2 and category[1] == selected_category_name:
                    selected_category_id = category[0]
                    break
        self.displayAll(course_id=selected_category_id)        

    def add_meal(self):
        name = self.name_entry.get().strip()
        description = self.description_entry.get("1.0", "end").strip() 
        price = self.price_entry.get().strip()
        cuisine_name = self.cuisine_combo.get()
        cat_name = self.cat_combo.get()
        prep = self.prep_entry.get().strip()
        
        if not name or not price or not cuisine_name or not cat_name or not description:
            messagebox.showerror("Error", "Name, Price, Description, Cuisine, and Category are required.")
            return
       
        try:
            price = float(price)
            prep = int(prep) if prep else 0
            if price <= 0:
                messagebox.showerror("Error", "Price must be greater than 0.")
                return
        except ValueError:
            messagebox.showerror("Error", "Price and Preparation Time must be numbers.")
            return
            
        status = True
        cuisines = self.menu.get_cuisines()
        cuisine_id = None
        for c in cuisines:
            if c[1] == cuisine_name:
                cuisine_id = c[0]
                break

        categories = self.menu.get_categories()
        cat_id = None
        for cat in categories:
            if cat[1] == cat_name:
                cat_id = cat[0]
                break
        if cuisine_id is None or cat_id is None:
            messagebox.showerror("Error", "Invalid cuisine or category.")
            return
        
        result =self.menu.add_meal(name, description, price, cuisine_id, cat_id, status, prep)
        messagebox.showinfo("Result", result)
        self.displayAll()  
        self.clear_form()

    def open_update_window(self):
        selected = self.table_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a meal to update.")
            return

        item_id = selected[0]
        parent_id = self.table_tree.parent(item_id)
        if parent_id:
            item_id = parent_id

        values = self.table_tree.item(item_id)['values']
        meal_id = int(item_id)
        # Create popup window
        update_win = Toplevel(self.root)
        update_win.title("Update Meal Window")
        update_win.geometry("400x300")
        update_win.resizable(False, False)

        frame = Frame(update_win,bg="white")
        frame.pack(pady=10)


        Label(frame, text=f"Updating this item {values[2]}  price and status.", font=("Times", 14 ),bg="white").pack(anchor="w",pady=(0, 15),padx=10)
        # Price
        Label(frame, text="Price:").pack(anchor="w", padx=10, pady=(10,0))
        price_entry = ctk.CTkEntry(frame, width=200)
        price_entry.pack(anchor="w",padx=10, pady=5)
        price_entry.insert(0, str(values[1]).replace("₱", ""))

        # Availability
        Label(frame, text="Availability:").pack(anchor="w", padx=10, pady=(10,0))
        avail_combo = ttk.Combobox(frame, values=["Available", "Not Available"], state="readonly", width=20)
        avail_combo.pack(anchor="w",padx=10, pady=5)
        avail_combo.set(values[2])

        def save_update():
            try:
                new_price = float(price_entry.get())
            except ValueError:
                messagebox.showerror("Invalid Input", "Price must be a number.")
                return

            if new_price <= 0:
                messagebox.showerror("Invalid Price", "Price must be greater than 0.")
                return
            new_avail = avail_combo.get()
            avail_value = 1 if new_avail == "Available" else 0
            # Update treeview
            result = self.menu.update(meal_id, new_price, avail_value)
            messagebox.showinfo("Result", result)
            update_win.destroy()
            self.displayAll()
        Button(frame, text="Save",bg="#10F000",fg="#ECF1EE", command=save_update, width=10).pack(pady=10)
   
    def clear_form(self):
        self.name_entry.delete(0, END)
        self.price_entry.delete(0, END)
        self.prep_entry.delete(0, END)
        self.description_entry.delete("1.0", "end")
        self.cuisine_combo.set("")
        self.cat_combo.set("")