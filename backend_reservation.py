from storage import SystemDB
from abc import ABC, abstractmethod
from datetime import datetime

class Manager(ABC):
    def __init__(self):
        self._storage = SystemDB()
    
    @abstractmethod
    def viewAll(self, date):
        pass

    @abstractmethod
    def changeStatus(self, new_status):
        pass

class TableManager(Manager):
    def __init__(self):
        super().__init__()

    def viewAll(self, date): # Done
        self._storage.cursor.execute('''SELECT restaurant_table.table_id, restaurant_table.table_number, restaurant_table.capacity, restaurant_table.table_status, reservations.selected_time, restaurant_table.description 
                                  FROM restaurant_table 
                                  LEFT JOIN reservations 
                                  ON restaurant_table.table_id = reservations.table_id AND reservations.selected_date = %s ORDER BY reservations.selected_time''', (date,))
        
        result = self._storage.cursor.fetchall()
        return result

    def viewFilteredTable(self, date, guest_count): # Done
        self._storage.cursor.execute('''SELECT restaurant_table.table_id, restaurant_table.table_number, restaurant_table.capacity, 
                                     restaurant_table.description, restaurant_table.table_status,
                                     reservations.selected_time
                                     FROM restaurant_table LEFT JOIN reservations
                                     ON restaurant_table.table_id = reservations.table_id 
                                     AND reservations.selected_date = %s WHERE restaurant_table.capacity >= %s''', (date, guest_count))
        result = self._storage.cursor.fetchall()
        return result
    
    def changeStatus(self, new_status, table_id): # Done
        try:
            self._storage.cursor.execute("UPDATE restaurant_table SET table_status = %s WHERE table_id = %s", (new_status, table_id))
            self._storage.connection.commit()
            return "success"
        except Exception as e:
            print(f"Error updating table status: {e}")
            self._storage.connection.rollback()
            return "error"
        
class ReservationManager(Manager):
    def __init__(self):
        super().__init__()

    def addReservation(self, name, contact, date, time, guest_count, notes, table_number): # Done
        if not name or not contact or not date or not time or not guest_count or not table_number:
            return "empty_fields"
        
        # Validates the date and time input
        try:
            datetime.strptime(date, '%Y-%m-%d')
            datetime.strptime(time, '%H:%M')
        except ValueError:
            return "Invalid_format"
        
        # Validates the guest_count input
        try:
            guest_count_int = int(guest_count)
            if guest_count_int < 0:
                return "invalid_guest_count"
        except ValueError:
            return "invalid_guest_count"
        
        self._storage.cursor.execute("SELECT table_id, capacity FROM restaurant_table WHERE table_number = %s", (table_number,))
        table_result = self._storage.cursor.fetchone()
        
        if not table_result:
            return "invalid_table"  
        
        table_id, capacity = table_result
        if guest_count_int > capacity:
            return "exceeds_capacity"
        
        # Checks for duplicate reservation on same table/date/time/contact
        self._storage.cursor.execute("SELECT * FROM reservations WHERE table_id = %s AND selected_date = %s AND selected_time = %s AND contact_number = %s", (table_id, date, time, contact))
        result = self._storage.cursor.fetchall()
        
        # Inserts Reservation if there's no duplicate found
        if not result:
            self._storage.cursor.execute("INSERT INTO reservations(guest_name, contact_number, selected_date, selected_time, guest_count, instructions, table_id) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                                      (name, contact, date, time, guest_count_int, notes, table_id))
            self._storage.connection.commit()

            table_manager = TableManager()
            status_update = table_manager.changeStatus(table_id, 'reserved')

            if status_update == "error":
                return "error_updating_status"
            return "success"

        else:
            return "already_exists"
        
    def viewInfo(self, date=""): # Done
        self._storage.cursor.execute("SELECT reservations.reservation_id, reservations.selected_time, restaurant_table.table_number, reservations.guest_count, reservations.reservation_status FROM reservations INNER JOIN restaurant_table ON reservations.table_id = restaurant_table.table_id WHERE reservations.booking_date = %s AND reservation_status != 'deleted'", (date,))
        
        result = self._storage.cursor.fetchall()
        return result
    
    def viewAll(self, date=""): # Done
        self._storage.cursor.execute("SELECT * FROM reservations WHERE reservation_status != 'deleted'")
        result = self._storage.cursor.fetchall()
        return result

    def searchReservation(self, name): # Done
        self._storage.cursor.execute('''SELECT reservations.reservation_id, reservations.guest_name, reservations.contact_number, 
                                     reservations.selected_date, reservations.selected_time, 
                                     reservations.guest_count, restaurant_table.table_number, 
                                     reservations.reservation_status, reservations.booking_date, reservations.cancelled_at
                                     FROM reservations INNER JOIN restaurant_table ON reservations.table_id = restaurant_table.table_id WHERE reservations.reservation_status != 'deleted' AND reservations.guest_name LIKE %s''', 
                                  ("%" + name + "%",))
        result = self._storage.cursor.fetchall()
        return result
    
    def removeReservation(self, reservation_id): # Done
        try:
            self._storage.cursor.execute("SELECT reservation_status FROM reservations WHERE reservation_id = %s", (reservation_id,))
            result = self._storage.cursor.fetchone()
            
            if not result:
                return "Reservation not found."
            if result == 'deleted':
                return "Reservation is already deleted."
            
            self._storage.cursor.execute("UPDATE reservations SET reservation_status = 'deleted' WHERE reservation_id = %s", (reservation_id,))
            self._storage.connection.commit()
            return "success"
        
        except Exception as e:
            self._storage.connection.rollback()         
            print(f"Error deleting reservation {reservation_id}: {str(e)}") 
            return "An error occurred while deleting the reservation. Please try again."

    def cancelReservation(self, reservation_id): # Done
        try:
            self._storage.cursor.execute("UPDATE reservations SET reservation_status = 'cancelled', cancelled_at = CURRENT_TIMESTAMP WHERE reservation_id = %s", (reservation_id,))
            self._storage.connection.commit()
            return "success"
        except Exception as e:
            self._storage.connection.rollback()
            return str(e)    

    def viewReservationByDate(self): # Done
        self._storage.cursor.execute("SELECT * FROM reservations WHERE reservation_status != 'deleted' ORDER BY selected_date DESC")
        result = self._storage.cursor.fetchall()
        return result
    
    def viewReservationByTime(self): # Done
        self._storage.cursor.execute("SELECT * FROM reservations WHERE reservation_status != 'deleted' ORDER BY selected_time ASC")
        result = self._storage.cursor.fetchall()
        return result
    
    def viewReservationByName(self): # Done
        self._storage.cursor.execute("SELECT * FROM reservations WHERE reservation_status != 'deleted' ORDER BY guest_name ASC")
        result = self._storage.cursor.fetchall()
        return result
    
    def viewCancelledReservations(self): # Done
        self._storage.cursor.execute("SELECT * FROM reservations WHERE reservation_status = 'cancelled'")
        result = self._storage.cursor.fetchall()
        return result
    

    def changeStatus(self, new_status):
        pass
        
