# =====importing libraries===========
'''This is the section where you will import libraries'''

# ===========================Login============================================

# initialising empty lists and opening user.txt as read only.
file = open("user.txt", "r")
user_list = []
user_pass = []

# asks user for their login details, opens the database of current login
# details and sorts the username and password into separate lists (using a
# for loop to iterate through each line and split the entries by ',') if the
# login and password are present in both lists, log in, else try again.
while True:
    login_username = input("Enter your username: ")
    login_password = input("Enter your password: ")

    for line in file:
        line_split = line.split(",")
        user_list.append(line_split[0].strip())
        user_pass.append(line_split[1].strip())

    if login_username in user_list and login_password in user_pass:
        print("You have successfully logged in!")
        file.close()
        break

    else:
        print("That username or password does not match, please try again.\n")

# =================================MENU=======================================
# Using a while loop to display a menu to the user, there are conditional
# statements for each option in the menu and each of them do different tasks,
# to break the loop you need to enter 'e' for exit.
while True:
    menu = input('''\nSelect one of the following Options below:
r   - Registering a user
a   - Adding a task
va  - View all tasks
vm  - view my task
s   - statistics (admin only)
e   - Exit

Option: ''').lower()

    # this option is only for the user logged in as admin, it uses an if
    # statement to check if the login details are the same as the known
    # admin account, it then opens two external files and reads the data
    # within - calculating the number of times a line is present and
    # printing the results. It will return to the menu once complete or if
    # the user is not the admin will give an error message and return to the
    # menu.
    if menu == 's':
        while True:
            if login_username == "admin" and login_password == "adm1n":

                with open("user.txt", "r") as file_user:
                    file_user_count = len(file_user.readlines())
                    print("\nThe number of users registered: ",
                          file_user_count)

                with open("tasks.txt", "r") as file_tasks:
                    file_tasks_count = len(file_tasks.readlines())
                    print("\nThe number of tasks assigned: ", file_tasks_count)
                    break
            else:
                print("You do not have administrative privileges to access "
                      "that information.")
                break

    # responsible for registering new users and can only be accessed by an
    # admin account. Once it has checked the user is 'admin' it opens the
    # user.txt file with append functionality (this way it doesn't overwrite
    # the data but adds to it) and asks the user for input.
    elif menu == 'r':
        while True:
            if login_username == "admin":
                file = open("user.txt", "a")
                username = input("Please enter a new username: ")
                password = input("Please enter a new password: ")
                password_confirm = input("Please confirm your password: ")

                # condition statement within the main if statement that
                # checks if the passwords entered match and then writes the
                # data to the external file using .write() closes the file
                # and returns to the menu.
                if password_confirm == password:
                    file.write(username + ", " + password + "\n")
                    print("Password confirmed, you have registered a new "
                          "account.\n")
                    file.close()
                    break

                else:
                    print("Those passwords don't match please try "
                          "registering again.\n")

            else:
                print("You do not have administrative permissions to "
                      "register new users.\n")
                break

    # opens external file in file_task variable, asks for user input and
    # appends the input to the file, prints a confirmation message at the
    # end and closes the file.
    elif menu == 'a':
        file_task = open("tasks.txt", "a")
        user_task_assign = input("Enter the username of the person you want "
                                 "to assign the task to: ")
        task_title = input("Enter the title of the task: ")
        task_description = input("Please describe what the task requirements "
                                 "are: ")
        task_due_date = input("When is this task due? (example format: 02 "
                              "oct 2022) ")
        current_date = input("What is the current date? ")
        task_status = "No"

        file_task.write(user_task_assign + ", " + task_title + ", " +
                        task_description + ", " + task_due_date + ", " +
                        current_date + ", " + task_status + "\n")

        file_task.close()

        print("\nThank you! The task has been registered.\n")

    # opens the file_task as read only and uses a for loop to iterate over
    # the words in each line splitting them by ',' and storing them as a
    # list variable task_sort. Then a number of print statements format the
    # data in a professional clear to read way using the index values of the
    # list to sort the data in the right place.
    elif menu == 'va':
        file_task = open("tasks.txt", "r")

        for line in file_task:
            task_sort = line.strip().split(", ")
            print("Task:\t\t\t\t" + task_sort[1])
            print("Assigned to:\t\t" + task_sort[0])
            print("Date assigned:\t\t" + task_sort[3])
            print("Due date:\t\t\t" + task_sort[4])
            print("Task complete?\t\t" + task_sort[5])
            print("Task description:\n" + "\t" + task_sort[2] + "\n")

        file_task.close()

    # similar to the above block of code we open the file as read only and
    # use a for loop to read through the data in each line, splitting it
    # into a list by separating by ',' but this time the conditional if
    # statement only prints the data when the username that is currently
    # logged in matches the task assignment username.
    elif menu == 'vm':
        file_task = open("tasks.txt", "r")
        for line in file_task:
            task_sort = line.strip().split(", ")

            if login_username == task_sort[0]:
                print("Task:\t\t\t\t" + task_sort[1])
                print("Assigned to:\t\t" + task_sort[0])
                print("Date assigned:\t\t" + task_sort[3])
                print("Due date:\t\t\t" + task_sort[4])
                print("Task complete?\t\t" + task_sort[5])
                print("Task description:\n" + "\t" + task_sort[2] + "\n")

    # the only way to exit out of the menu while loop, prints a goodbye
    # message and closes the program.
    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    # if the user enters anything other than the stated options this error
    # message is shown and the loop cyles again.
    else:
        print("You have made a wrong choice, Please Try again")

file_task.close()
