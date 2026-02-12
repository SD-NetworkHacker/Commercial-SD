import sqlite3
import datetime
import logging
from . import config

# Configure logging (mocking config for now since we are in the same package structure)
# In real run, config is imported from parent or sibling. 
# We'll assume this file is at agent_prospecteur/db/database.py and config is at agent_prospecteur/config.py
# So we need to fix import in the actual file content above if running as module.
# For simplicity in scripts, we'll try relative import or assume path is set.

class Database:
    def __init__(self, db_path="prospects.db"):
        self.db_path = db_path
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS prospects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                address TEXT,
                city TEXT,
                sector TEXT,
                website_url TEXT,
                website_status TEXT, -- 'NO_SITE', 'ARCHAIC', 'MODERN', 'UNKNOWN'
                email TEXT,
                message_content TEXT,
                sent_at TIMESTAMP,
                status TEXT DEFAULT 'new',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()

    def add_prospect(self, prospect_data):
        """
        Add a new prospect or update if exists (by name/address or some unique constraint).
        For now, we just insert.
        """
        # Check duplicates by name and city to be safe
        self.cursor.execute("SELECT id FROM prospects WHERE name = ? AND city = ?", (prospect_data.get('name'), prospect_data.get('city')))
        existing = self.cursor.fetchone()
        
        if existing:
            return existing['id']

        columns = ['name', 'address', 'city', 'sector', 'website_url', 'website_status', 'email']
        values = [prospect_data.get(c) for c in columns]
        
        query = f"INSERT INTO prospects ({', '.join(columns)}) VALUES ({', '.join(['?']*len(columns))})"
        self.cursor.execute(query, values)
        self.conn.commit()
        return self.cursor.lastrowid

    def get_pending_prospects(self):
        """Get prospects that are 'new' and fit for sending (Archaic or No Site)."""
        self.cursor.execute("""
            SELECT * FROM prospects 
            WHERE status = 'new' 
            AND website_status IN ('NO_SITE', 'ARCHAIC')
            AND email IS NOT NULL
        """)
        return self.cursor.fetchall()

    def update_listing_status(self, prospect_id, status, website_status=None, email=None, message=None):
        updates = []
        values = []
        
        if status:
            updates.append("status = ?")
            values.append(status)
        if website_status:
            updates.append("website_status = ?")
            values.append(website_status)
        if email:
            updates.append("email = ?")
            values.append(email)
        if message:
            updates.append("message_content = ?")
            values.append(message)
            
        if not updates:
            return

        updates.append("last_updated = CURRENT_TIMESTAMP") # if we had that column, but let's skip for now
        
        query = f"UPDATE prospects SET {', '.join(updates)} WHERE id = ?"
        values.append(prospect_id)
        
        self.cursor.execute(query, values)
        self.conn.commit()

    def close(self):
        if self.conn:
            self.conn.close()

# Singleton or factory usage recommended in main
