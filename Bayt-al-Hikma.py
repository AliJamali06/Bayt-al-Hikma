import sqlite3
import streamlit as st

# database setup


def create_database():
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
                   title TEXT,
                   author TEXT,
                   year INTEGER,
                   genre TEXT,
                   read_status INTEGER                 
    )
""")
    conn.commit()
    


create_database()


# streamlit ui
st.title("Bayt al-Hikma: Personal Library")

# connect to database

conn = sqlite3.connect("library.db")
cursor = conn.cursor()

# Add Book Section
st.header("Add a New Book")
title = st.text_input("Enter Book Title")
author = st.text_input("Enter Author")
year = st.number_input("Enter Publication Year",
                       min_value=1000, max_value=2100, step=1)
genre = st.text_input("Enter Genre")
read_status = st.radio("Have you this book?", ["Yes", "No", ])
read_status_bool = 1 if read_status == "Yes" else 0

if st.button("Add Book"):
    cursor.execute("INSERT INTO books (title, author, year, genre, read_status) VALUES (?, ?, ?, ?, ?)",
                   (title, author, year, genre, read_status_bool))
    conn.commit()
    st.success("Book added successfully!")

    # display books section
    st.header("Your Library")
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    if books:
        st.write("Here are your books:")
        st.table(books)
    else:
        st.write("No books in the library yet.")

     # search book section
    st.header("Search for a book")
    search_query = st.text_input("Enter title or author name to search")

    if st.button("Search"):
        cursor.execute("Select * From books Where title LIKE ? OR author LIKE ?",
                       (f"%{search_query}%", f"{search_query}%"))
        search_results = cursor.fetchall()
        if search_results:
            st.table("No matching books found.")

    # Remove book section
    st.header("Remove a Book")
    book_id_to_remove = st.number_input(
        "Enter Book ID to remove", min_value=1, step=1)
    if st.button("Remove Book"):
        cursor.execute("DELETE FROM books WHERE id = ?", (book_id_to_remove))
        conn.commit()
        st.success("Book remove successfully!")

    # display statistics
    st.header("Library Statistics")
    cursor.execute("SELECT COUNT(*) FROM books")
    total_books = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM books WHERE read_status = 1")
    read_books = cursor.fetchone()[0]
    percentage_read = (read_books / total_books) * \
        100 if total_books > 0 else 0

    st.write(f"Total Books: {total_books}")
    st.write(f"Read Books: {read_books}")
    st.write(f"Percentage Read: {percentage_read:.2f}%")

    # close db connection
    conn.close()
