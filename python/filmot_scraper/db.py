import sqlite3
import uuid

# Database file
DB_FILE = "data.db"


# Create or connect to SQLite database
def create_connection():
  conn = sqlite3.connect(DB_FILE)
  return conn


# Create the database tables if they don't exist
def create_tables():
  conn = create_connection()
  cursor = conn.cursor()

  # Create "poems" table
  cursor.execute("""
      CREATE TABLE IF NOT EXISTS poems (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          poem TEXT NOT NULL,
          timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
          latitude REAL,
          longitude REAL
      )
    """)

  # Create "mp3_files" table
  cursor.execute("""
      CREATE TABLE IF NOT EXISTS mp3_files (
          id TEXT PRIMARY KEY,
          file_path TEXT NOT NULL,
          keywords TEXT,
          video_id TEXT,
          timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
      )
    """)

  # Create an index separately
  cursor.execute("""
      CREATE INDEX IF NOT EXISTS idx_keywords ON mp3_files (keywords);
  """)

  conn.commit()
  conn.close()


# Insert a new poem entry
def insert_poem(poem, latitude=None, longitude=None):
  conn = create_connection()
  cursor = conn.cursor()

  cursor.execute(
    """
        INSERT INTO poems (poem, latitude, longitude)
        VALUES (?, ?, ?)
    """,
    (poem, latitude, longitude),
  )

  conn.commit()
  conn.close()


# Insert a new MP3 file entry
def insert_mp3(file_path, keywords=None, video_id=None):
  conn = create_connection()
  cursor = conn.cursor()

  mp3_id = str(uuid.uuid4())  # Generate a new UUID for the mp3

  cursor.execute(
    """
        INSERT INTO mp3_files (id, file_path, keywords, video_id)
        VALUES (?, ?, ?, ?)
    """,
    (mp3_id, file_path, keywords, video_id),
  )

  conn.commit()
  conn.close()
  return mp3_id


# Fetch current (latest) poem
def fetch_current_poem():
  conn = create_connection()
  cursor = conn.cursor()

  cursor.execute("SELECT * FROM poems ORDER BY timestamp DESC LIMIT 1")
  poem = cursor.fetchone()

  conn.close()
  return poem


# Fetch poems
def fetch_poems():
  conn = create_connection()
  cursor = conn.cursor()

  cursor.execute("SELECT * FROM poems")
  poems = cursor.fetchall()

  conn.close()
  return poems


# Fetch MP3 files
def fetch_mp3_files():
  conn = create_connection()
  cursor = conn.cursor()

  cursor.execute("SELECT * FROM mp3_files")
  mp3_files = cursor.fetchall()

  conn.close()
  return mp3_files


# Fetch a specific poem by ID
def fetch_poem_by_id(poem_id):
  conn = create_connection()
  cursor = conn.cursor()

  cursor.execute("SELECT * FROM poems WHERE id=?", (poem_id,))
  poem = cursor.fetchone()

  conn.close()
  return poem


# Fetch a specific MP3 file by UUID
def fetch_mp3_by_id(mp3_id):
  conn = create_connection()
  cursor = conn.cursor()

  cursor.execute("SELECT * FROM mp3_files WHERE id=?", (mp3_id,))
  mp3 = cursor.fetchone()

  conn.close()
  return mp3


def fetch_mp3_by_keyword(keyword):
  conn = create_connection()
  cursor = conn.cursor()

  cursor.execute("SELECT * FROM mp3_files WHERE keywords = ?", (keyword,))
  mp3_files = cursor.fetchall()  # Fetch all matching entries

  conn.close()
  return mp3_files  # Returns a list of matching MP3 entries
