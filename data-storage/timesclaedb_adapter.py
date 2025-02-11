import psycopg2

db_config = {
    "dbname": "ovd",
    "user": "admin",
    "password": "admin",
    "host": "timescaledb_ovd",
    "port": 5432 
}

def get_database_info():
    try:
        # Establishing the connection
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        # 1. Number of tables
        cursor.execute("""
            SELECT count(*)
            FROM information_schema.tables
            WHERE table_schema = 'public';
        """)
        num_tables = cursor.fetchone()[0]

        # 2. Number of rows (sum of all table row counts)
        cursor.execute("""
            SELECT SUM(reltuples::BIGINT)
            FROM pg_class
            WHERE relkind='r' AND relnamespace IN (
                SELECT oid FROM pg_namespace WHERE nspname = 'public'
            );
        """)
        num_rows = cursor.fetchone()[0] or 0

        # 3. Size of the database
        cursor.execute("SELECT pg_size_pretty(pg_database_size(current_database()));")
        db_size = cursor.fetchone()[0]

        # 4. Number of fields (columns)
        cursor.execute("""
            SELECT count(*)
            FROM information_schema.columns
            WHERE table_schema = 'public';
        """)
        num_fields = cursor.fetchone()[0]

        # Closing the cursor and connection
        cursor.close()
        conn.close()

        return num_tables, num_rows, db_size#, num_fields
    
    except Exception as error:
        print(f"Error at timescaledb_adapter: {error}")



if __name__ == "__main__":

    print(get_database_info()[1])