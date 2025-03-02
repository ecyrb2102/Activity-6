users = {"admin": "password123", "user1": "mypassword"}  

def login():
    username = input("Enter username: ")
    password = input("Enter password: ")

    if username in users and users[username] == password:
        print("Login successful! Welcome,", username)
    else:
        print("Invalid username or password.")

def register():
    new_username = input("Enter a new username: ")
    if new_username in users:
        print("Username already exists. Try a different one.")
        return
    
    new_password = input("Enter a new password: ")
    users[new_username] = new_password
    print("Registration successful! You can now log in.")

while True:
    print("\n1. Login\n2. Register\n3. Exit")
    choice = input("Choose an option: ")

    if choice == "1":
        login()
    elif choice == "2":
        register()
    elif choice == "3":
        print("Goodbye!")
        break
    else:
        print("Invalid choice. Please try again.")

#This is Push
#This is Commit
#Third Commit