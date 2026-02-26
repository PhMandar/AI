import psycopg2
from psycopg2 import OperationalError, ProgrammingError

def check_table_access(db_name, user, password, host, port, table_name):
    """
    Checks if a specific PostgreSQL table is accessible.
    """
    conn = None
    try:
        # Establish connection to the database
        conn = psycopg2.connect(
            dbname=db_name,
            user=user,
            password=password,
            host=host,
            port=port
        )
        print(f"Connection to database '{db_name}' established successfully.")

        # Create a cursor object
        cur = conn.cursor()

        # SQL query to check if the table exists using information_schema
        # Using EXISTS is efficient as it stops searching after finding the first match
        query = """
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_schema = 'public' AND table_name = %s
        );
        """
        cur.execute(query, (table_name,))
        table_exists = cur.fetchone()[0]

        if table_exists:
            print(f"Table '{table_name}' exists and is accessible in the 'public' schema.")
            return True
        else:
            print(f"Table '{table_name}' does not exist in the 'public' schema.")
            return False

    except OperationalError as e:
        print(f"An OperationalError occurred: {e}")
        print("Please check your connection parameters or database/user permissions.")
    except ProgrammingError as e:
        print(f"A ProgrammingError occurred: {e}")
        print("Please check the SQL query or table name.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        if conn:
            cur.close()
            conn.close()
            print("Database connection closed.")

# --- Usage Example ---
if __name__ == '__main__':
    # Replace with your PostgreSQL credentials and table name
    DB_PARAMS = {
        'db_name': 'postgres',
        'user': 'postgres',
        'password': 'postgres',
        'host': 'localhost',
        'port': '5432',
    }
    TARGET_TABLE = 'user_vault'

    is_accessible = check_table_access(
        DB_PARAMS['db_name'],
        DB_PARAMS['user'],
        DB_PARAMS['password'],
        DB_PARAMS['host'],
        DB_PARAMS['port'],
        TARGET_TABLE
    )

    if is_accessible:
        print(f"Access check for '{TARGET_TABLE}' succeeded.")
    else:
        print(f"Access check for '{TARGET_TABLE}' failed or the table does not exist.")

