#!/usr/bin/env python3
import sqlite3
import sys

def main(db_file):
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        print(f"Connected to {db_file}. Type '.help' for commands.")
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        sys.exit(1)

    while True:
        try:
            query = input("sqlite> ").strip()
            
            if not query:
                continue
            
            if query.lower() in ['.exit', '.quit']:
                print("Exiting...")
                break
            elif query.lower() == '.help':
                print("Commands:\n  .help       Show this message\n  .tables     List tables\n  .exit/.quit Exit")
                continue
            elif query.lower() == '.tables':
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                print("\n".join([t[0] for t in tables]) if tables else "No tables found.")
                continue
            
            # Execute SQL
            cursor.execute(query)
            
            if query.lower().startswith("select"):
                rows = cursor.fetchall()
                for row in rows:
                    print(row)
            else:
                conn.commit()
                print(f"{cursor.fetchall()}")
                print(f"{cursor.rowcount} rows affected.")
            
        except sqlite3.Error as e:
            print(f"SQL error: {e}")
        except KeyboardInterrupt:
            print("\nInterrupted. Use '.exit' to quit.")
        except EOFError:
            print("\nExiting...")
            break

    conn.close()

if __name__ == "__main__":
    db_name = input("Podaj lokalizacje chuju: ")
    main(db_name)
