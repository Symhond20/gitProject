import mysql.connector

class SystemDB:
    def __init__(self, my_db= "restodb"):
        self.connection = None
        self.cursor = None
        
        try:
            self.connection = mysql.connector.connect(
                host = "127.0.0.1",
                user = "root",
                database = my_db)
            
            if self.connection.is_connected():
                print("Successfully connected to MySQL database")
                self.cursor = self.connection.cursor()
                self.createTables()
        except:
            print("Database error.")
    
    def createTables(self):
        try:
            # Table for RestoTable
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS restaurant_table(
                                table_id INT PRIMARY KEY AUTO_INCREMENT,
                                table_number VARCHAR(10) NOT NULL UNIQUE,
                                capacity INT NOT NULL,
                                table_status VARCHAR(20) NOT NULL DEFAULT 'available',
                                description TEXT)''')       
            # Reservation Table
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS reservations(
                                reservation_id INT PRIMARY KEY AUTO_INCREMENT,
                                guest_name VARCHAR(150) NOT NULL,
                                contact_number VARCHAR(50) NOT NULL,
                                selected_date DATE NOT NULL,
                                selected_time TIME NOT NULL,
                                guest_count INT NOT NULL,
                                instructions TEXT,
                                table_id INT NOT NULL,
                                reservation_status VARCHAR(20) DEFAULT 'confirmed',
                                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                                booking_date DATE NOT NULL DEFAULT (CURRENT_DATE),
                                FOREIGN KEY (table_id) REFERENCES restaurant_table(table_id)
                                )''')
            
            # Cuisine Table
            self.cursor.execute(""" CREATE TABLE IF NOT EXISTS Cuisines(
                                id INT PRIMARY KEY AUTO_INCREMENT,
                                name VARCHAR(100) NOT NULL UNIQUE)""")

            # Courses Table
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS Courses(
                                id INT PRIMARY KEY AUTO_INCREMENT, 
                                name VARCHAR(100) NOT NULL UNIQUE)""")
            # Meals Table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS Meals (
                        id INT PRIMARY KEY AUTO_INCREMENT,
                        name VARCHAR(255) NOT NULL,
                        description TEXT,
                        price DECIMAL(10,2) NOT NULL,
                        Status TINYINT(1) NOT NULL DEFAULT 1,
                        prepTime INT NOT NULL,
                        cuisineID INT NOT NULL,
                        courseID INT NOT NULL,
                        FOREIGN KEY (cuisineID) REFERENCES Cuisines(id),
                        FOREIGN KEY (courseID) REFERENCES Courses(id) 
                    ) 
                """)
           
            # Waiter Table
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS employee(
                                employee_id INT PRIMARY KEY AUTO_INCREMENT,
                                employee_name VARCHAR(150) NOT NULL,
                                tip_recieved FLOAT NOT NULL)""")
            
            # Customer Table
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS customer(
                                customer_id INT PRIMARY KEY AUTO_INCREMENT,
                                guest_name VARCHAR(150) NOT NULL,
                                guest_count INT NOT NULL,
                                arrived_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP)""")
            
            # order Table
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS orders(
                                order_id INT PRIMARY KEY AUTO_INCREMENT,
                                FOREIGN KEY (order_id) REFERENCES Cuisines(id),
                                guest_count INT NOT NULL,
                                arrived_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP)""")
        
            self.connection.commit()
            print("Table is successfully created.")
            
        except Exception as e:
            print(f"Table creation error: {e}.")

    def insertTableData(self): # Done
        
        tables = [('T1', 2, 'Indoor and near entrance'), ('T2', 2, 'Indoor and near entrance'), ('T3', 2, 'Indoor and near entrance'), 
                  ('T4', 2, 'Indoor and Intimate'), ('T5', 2, 'Indoor and Intimate'), 
                  ('T6', 2, 'Indoor and Intimate'), ('T7', 2, 'Indoor and Intimate'), 
                  ('F1', 4, 'Indoor and Near Entrance with Window View'), 
                  ('F2', 4, 'Indoor and near entrance with window view'), 
                  ('F3', 4, 'Indoor/Near entrance with window view'),
                  ('F4', 4, 'Indoor and Near Kitchen'), ('F5', 4, 'Indoor and Near Kitchen'),
                  ('F6', 4, 'Indoor and Near Kitchen'), 
                  ('F7', 4, 'Outdoor in Terrace'),
                  ('S1', 6, 'Indoor Main'), ('S2', 6, 'Indoor Main'),
                  ('S3', 6, 'Outdoor in Terrace'), ('S4', 6, 'Outdoor in Terrace'),
                  ('E1', 8, 'VIP'), ('E2', 8, 'VIP'), ('E3', 8, 'VIP'),]
        
        for table_num, capacity, description in tables:
            self.cursor.execute("SELECT * FROM restaurant_table WHERE table_number = %s", (table_num,))
            result = self.cursor.fetchall()

            if not result:
                self.cursor.execute("INSERT INTO restaurant_table(table_number, capacity, description) VALUES(%s,%s,%s)", (table_num, capacity, description,))
        self.connection.commit()

    def insertCuisine(self): # Done
        cuisines = ["Japanes Cuisine", "Italian Cuisine", "Filipino Cuisine"]
        for cuisine in cuisines:
            self.cursor.execute("SELECT * FROM Cuisines WHERE name = %s", (cuisine,))
            result = self.cursor.fetchall()

            if not result:
                self.cursor.execute("INSERT INTO Cuisines(name) VALUES(%s)", (cuisine,))
        self.connection.commit()

    def insertCourses(self): # Done
        courses = ["Appetizers", "Main Dish", "Dessert", "Drinks"]

        for course in courses:
            self.cursor.execute("SELECT * FROM Courses WHERE name = %s", (course,))
            result = self.cursor.fetchall()

            if not result:
                self.cursor.execute("INSERT INTO Courses(name) VALUES(%s)", (course,))
        self.connection.commit()

    def closeDB(self): # Done
        try:
            if self.cursor is not None:
                self.cursor.close()

            if self.connection is not None and self.connection.is_connected():
                self.connection.close()
                print("MySQL connection closed.")
        except:
            print("Database Error: Can't close the connection.")

app = SystemDB()
app.insertCourses()
