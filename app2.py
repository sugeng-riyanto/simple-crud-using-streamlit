import streamlit as st
import sqlite3
import pandas as pd
from PIL import Image

# Initialize SQLite database connection
conn = sqlite3.connect('database.db')
c = conn.cursor()

# Create table if not exists
c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fullname TEXT,
        address TEXT,
        signature BLOB
    )
''')
conn.commit()

def insert_user(fullname, address, signature):
    c.execute('''
        INSERT INTO users (fullname, address, signature)
        VALUES (?, ?, ?)
    ''', (fullname, address, signature))
    conn.commit()

def update_user(user_id, fullname, address, signature):
    c.execute('''
        UPDATE users
        SET fullname = ?, address = ?, signature = ?
        WHERE id = ?
    ''', (fullname, address, signature, user_id))
    conn.commit()

def delete_user(user_id):
    c.execute('''
        DELETE FROM users
        WHERE id = ?
    ''', (user_id,))
    conn.commit()

def fetch_all_users():
    c.execute('SELECT * FROM users')
    return c.fetchall()

# Define the pages
def show_home_page():
    st.title('User Data Management - Home')

    # Form for data entry
    with st.form(key='user_form'):
        fullname = st.text_input('Full Name')
        address = st.text_input('Address')
        signature = st.file_uploader('Upload Signature', type=['png', 'jpg', 'jpeg'])

        submit_button = st.form_submit_button(label='Submit')

    if submit_button:
        if signature:
            signature = signature.read()
            insert_user(fullname, address, signature)
            st.success('User added successfully')
        else:
            st.error('Please upload a signature')

def show_manage_page():
    st.title('User Data Management - Manage Users')

    # Display all users
    st.subheader('All Users')
    users = fetch_all_users()
    df = pd.DataFrame(users, columns=['ID', 'Full Name', 'Address', 'Signature'])
    st.dataframe(df)

    # Update user
    st.subheader('Update User')
    user_id_to_update = st.number_input('User ID to update', min_value=1, step=1)
    fullname_to_update = st.text_input('New Full Name')
    address_to_update = st.text_input('New Address')
    signature_to_update = st.file_uploader('Upload New Signature', type=['png', 'jpg', 'jpeg'], key='update')

    if st.button('Update User'):
        if signature_to_update:
            signature_to_update = signature_to_update.read()
            update_user(user_id_to_update, fullname_to_update, address_to_update, signature_to_update)
            st.success('User updated successfully')
        else:
            st.error('Please upload a new signature')

    # Delete user
    st.subheader('Delete User')
    user_id_to_delete = st.number_input('User ID to delete', min_value=1, step=1, key='delete')

    if st.button('Delete User'):
        delete_user(user_id_to_delete)
        st.success('User deleted successfully')

def show_display_page():
    st.title('User Data Management - Display Users')

    # Display all users
    users = fetch_all_users()
    df = pd.DataFrame(users, columns=['ID', 'Full Name', 'Address', 'Signature'])

    if not df.empty:
        st.subheader('All Users')
        for index, row in df.iterrows():
            st.write(f"ID: {row['ID']}")
            st.write(f"Full Name: {row['Full Name']}")
            st.write(f"Address: {row['Address']}")
            st.image(row['Signature'], width=200)
            st.write('---')
    else:
        st.write("No users found.")

# Sidebar for navigation
st.sidebar.title('Navigation')
page = st.sidebar.selectbox('Select a page:', ['Home', 'Manage Users', 'Display Users'])

if page == 'Home':
    show_home_page()
elif page == 'Manage Users':
    show_manage_page()
else:
    show_display_page()

# Close the connection
conn.close()
