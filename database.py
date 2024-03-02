# from get_data import get_paper_info
import sqlite3


def insert_or_update_database(data):
    total_rows_affected = 0  # Initialize a counter to track affected rows
    try:
        # Using a context manager to handle the database connection
        with sqlite3.connect("data/papers.db") as conn:
            c = conn.cursor()
            # Create table
            c.execute(
                """CREATE TABLE IF NOT EXISTS papers
                        (url TEXT PRIMARY KEY, title TEXT, arxiv_link TEXT, published DATE, authors TEXT, summary TEXT )"""
            )
            for paper in data:
                # Check if the record already exists
                c.execute("SELECT 1 FROM papers WHERE url = :url", {'url': paper['url']})
                if not c.fetchone():
                    # Prepare SQL query to insert or replace records
                    sql_query = """INSERT OR REPLACE INTO papers (url, title, arxiv_link, published, authors, summary) 
                                VALUES (:url, :title, :arxiv_link, :published, :authors, :summary)"""

                    # Execute SQL query
                    c.execute(sql_query, paper)

                    total_rows_affected += c.rowcount

            # Commit changes automatically due to the context manager

    except sqlite3.DatabaseError as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

    print(f"Total rows affected (inserted or updated): {total_rows_affected}")

# Update data base with new data
# insert_or_update_database(get_paper_info())
