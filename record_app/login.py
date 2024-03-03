import streamlit as st
import sqlite3

# Function to initialize the database
def initialize_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (email TEXT PRIMARY KEY, password TEXT)''')
    conn.commit()
    conn.close()

# Function to validate login credentials
def validate_credentials(email, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''SELECT * FROM users WHERE email=? AND password=?''', (email, password))
    result = c.fetchone()
    conn.close()
    return result is not None

# Function to switch between different pages using session state
def switch_page(page):
    st.query_params["page"] = page
    st.experimental_rerun()

def main():
    # Set page layout to wide
    st.set_page_config(layout="wide")

    # Initialize the database
    initialize_db()

    # Set background image
    set_background("img.jpg")

    # Check query parameters to determine which page to show
    query_params = st.query_params
    page = query_params.get("page", "login")

    if page == "login":
        # Add a title and description for the login page
        st.title("Login Page")
        st.markdown("Please enter your credentials to log in.")

        # Input fields for email and password
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        # Button to submit login credentials
        if st.button("Login"):
            if validate_credentials(email, password):
                st.success("Login successful!")
                switch_page("dashboard")
            else:
                st.error("Invalid email or password. Please try again.")

    elif page == "dashboard":
        # Add a title and description for the dashboard page
        st.title("Dashboard")

        # Search bar and its icon
        search_query = st.text_input("Search", placeholder="Enter search query...")
        search_button = st.button("Search", help="Click to perform search")

        # Display search results if the search button is clicked
        if search_button:
            # Perform search operation here
            st.write(f"Search results for: {search_query}")

        st.write("Welcome to the dashboard!")

def set_background(image_url):
    # Add custom CSS to set background image
    st.markdown(
        f"""
        <style>
        body {{
            background: url("{image_url}") no-repeat center center fixed;
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

if _name_ == "_main_":
    main()