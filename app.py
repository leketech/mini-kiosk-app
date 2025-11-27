from flask import Flask, jsonify
import os
import psycopg2
import time

app = Flask(__name__)

def get_db_connection():
    host = os.getenv('DB_HOST', 'localhost')
    database = os.getenv('DB_NAME', 'kioskdb')
    user = os.getenv('DB_USER', 'kioskuser')
    password = os.getenv('DB_PASS', 'securepass123')
    
    print(f"Connecting to database: host={host}, database={database}, user={user}")
    conn = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password
    )
    return conn

def init_db():
    """Wait for the DB to be ready and initialize the table."""
    for i in range(10):  # retry up to 10 times
        try:
            print(f"Attempting to connect to database... (attempt {i+1}/10)")
            conn = get_db_connection()
            cur = conn.cursor()
            print("Creating visits table if it doesn't exist...")
            cur.execute('''
                CREATE TABLE IF NOT EXISTS visits (
                    id SERIAL PRIMARY KEY,
                    count INT DEFAULT 1
                );
            ''')
            cur.execute('SELECT COUNT(*) FROM visits;')
            count = cur.fetchone()[0]
            print(f"Found {count} rows in visits table")
            if count == 0:
                print("Inserting initial row...")
                cur.execute('INSERT INTO visits (count) VALUES (0);')
            conn.commit()
            cur.close()
            conn.close()
            print("✅ Database initialized successfully")
            return
        except Exception as e:
            print(f"⚠️ Waiting for database... ({i+1}/10): {e}")
            time.sleep(2)
    print("❌ Database not reachable after retries. Exiting.")
    exit(1)

def ensure_db_initialized():
    """Ensure database is initialized without exiting the application."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS visits (
                id SERIAL PRIMARY KEY,
                count INT DEFAULT 1
            );
        ''')
        cur.execute('SELECT COUNT(*) FROM visits;')
        if cur.fetchone()[0] == 0:
            cur.execute('INSERT INTO visits (count) VALUES (0);')
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"⚠️ Database initialization failed: {e}")
        return False

@app.route('/')
def home():
    try:
        # Try to ensure DB is initialized
        if not ensure_db_initialized():
            return "Database connection error", 500
            
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('UPDATE visits SET count = count + 1 WHERE id = 1 RETURNING count;')
        new_count = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return f"Hello from Kiosk! You are visitor #{new_count}"
    except Exception as e:
        return f"Database error: {str(e)}", 500

@app.route('/health')
def health():
    try:
        conn = get_db_connection()
        conn.close()
        db_ok = True
    except Exception as e:
        print(f"Health check failed: {e}")
        db_ok = False
    return jsonify(status="ok", db_connected=db_ok)

if __name__ == '__main__':
    print("Starting Kiosk application...")
    init_db()  # ✅ call this directly, not with a decorator
    print("Starting Flask server...")
    app.run(host='0.0.0.0', port=5000, debug=True)