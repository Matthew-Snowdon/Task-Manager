# importing libraries
import datetime
from datetime import datetime
import os


# functions

# The main menu function asks for the users input and returns the value, I'm
# using casefold() instead of lower() because it's more aggressive
def menu():
    selection = input('''\nSelect one of the following Options below:
r   - Registering a user
a   - Adding a task
va  - View all tasks
vm  - View my task
gr  - Generate reports
s   - Statistics
e   - Exit

Option: ''').casefold()
    return selection


# responsible for registering new users and can only be accessed by an
# admin account. Once it has checked the user is 'admin' it opens the
# user.txt file with append functionality (this way it doesn't overwrite
# the data but adds to it) and asks the user for input.
def reg_user():
    while True:
        if login_username == "admin":
            file = open("user.txt", "a")
            username = input("Please enter a new username: ")
            password = input("Please enter a new password: ")
            password_confirm = input("Please confirm your password: ")

            if username not in user_list:
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
                print("That username already exists please enter another one.")

        else:
            print("\nYou do not have administrative permissions to "
                  "register new users.\n")
            break
    return


# opens external file in task_file variable, asks for user input and
# appends the input to the file, prints a confirmation message at the
# end and closes the file.
def add_task():
    task_file = open("tasks.txt", "a")

    user_task_assign = input("\nEnter the username of the person you want "
                             "to assign the task to: ")
    task_title = input("Enter the title of the task: ")
    task_description = input("Please describe what the task requirements "
                             "are: ")
    task_due_date = input("When is this task due? (example format: 02 "
                          "oct 2022) ")
    current_date = input("What is the current date? ")
    task_status = "No\n"

    task_file.write(user_task_assign + ", " + task_title + ", " +
                    task_description + ", " + task_due_date + ", " +
                    current_date + ", " + task_status)

    task_file.close()

    print("\nThank you! The task has been registered.\n")
    return


# opens the tasks.txt file as read only and uses a for loop to iterate over
# the words in each line splitting them by ',' and storing them as a list
# variable sort_task. Then using an f string print the statements a clear
# to read way using the index values of the list to sort the data in the right
# place.
def view_all():
    with open("tasks.txt", "r") as view_file:
        for sentence in view_file:
            sort_task = sentence.strip().split(", ")
            print(f'''
Task:                   {sort_task[1]}
Assigned to:            {sort_task[0]}
Date assigned:          {sort_task[3]}
Due date:               {sort_task[4]}
Task complete?          {sort_task[5]}
Task description:       {sort_task[2]} 
''')
    return


# open tasks.txt as read only and using enumerate(), we iterate
# through the file with two variables, count and lines. Count holds the index
# value and lines holds all the data on each line. Then we create a variable
# that splits the data by "," and strips the /n characters, this way we have
# created a list of all the information we need to display, below we can call
# the count variable to assign the current task with the index value and then
# print the data in a neat format calling the index's of the list.
def view_mine():
    with open("tasks.txt", "r") as file_task:
        for count, lines in enumerate(file_task):
            task_sort = lines.strip().split(", ")

            if login_username == task_sort[0]:
                print(f'''                
Task number:            {str(count)}
Task:                   {task_sort[1]}
Assigned to:            {task_sort[0]}
Date assigned:          {task_sort[3]}
Due date:               {task_sort[4]}
Task complete?          {task_sort[5]}
Task description:       {task_sort[2]}
                ''')

    with open("tasks.txt", "r+") as f:
        contents = f.readlines()

    # declaring a number of options for the user to choose between
    first_option = int(input('''
Please choose an option:

1. Select a task for editing.
-1. Return to the main menu

option: '''))
    # If the user wants to edit, we ask which task they want to edit and the
    # corresponding line in contents is split. There's a condition that won't
    # allow you to edit that task if it has already been marked complete.
    if first_option == 1:
        task_num = int(input("\nPlease select the task number: "))
        split_data = contents[task_num].split(", ")

        if split_data[5] == "Yes\n":
            print("\nThis task has already been marked complete and "
                  "therefore cannot be edited, "
                  "returning to main menu.")
            return

    elif first_option == -1:
        return
    else:
        print("You've entered an incorrect option, please try again")

    # once a task num has been selected we present the user with three more
    # options that each do different things to the targeted task
    second_option = int(input("""\nPlease enter an option:
    
1. Mark the selected task complete.
2. Change who the selected task is assigned to.
3. Change the selected task due date.

option: """))

    # this block of code is responsible for marking the task as complete
    # there is a warning message to tell the user that they can't edit after
    # they have marked the task complete, if "No" is selected you are returned
    # to the main menu however if yes is selected we target the task and split
    # the contents into a list and using the specific index swap the value no
    # with yes, rejoin the contents and write it to the file.
    if second_option == 1:
        double_check = input(
            "\nOnce the task has been marked complete "
            "you will not be able to edit it, do you "
            "want to continue? (y/n): ")

        if double_check == "y".casefold():
            split_data = contents[task_num].split(", ")
            split_data[5] = "Yes\n"
            join_data = ", ".join(split_data)
            contents[task_num] = join_data
            f = open("tasks.txt", "w")

            for line in contents:
                f.write(line)
            f.close()

            # notification message saying the task has been completed and then
            # a preview of the task is printed
            print(f"\nTask: {task_num} has been edited, "
                  f"returning to main menu.\n")
            print(f"Preview of edited task: {task_num}")
            print(f''' 
==============================================================================                           
Task number:            {str(task_num)}
Task:                   {split_data[1]}
Assigned to:            {split_data[0]}
Date assigned:          {split_data[3]}
Due date:               {split_data[4]}
Task complete?          {split_data[5]}
Task description:       {split_data[2]}
==============================================================================
            ''')

        else:
            print("\nReturning to main menu...")
            return

    # using the same method this option changes split_data[0] which is the user
    # who is assigned the task and then writes the change to the file
    elif second_option == 2:
        split_data = contents[task_num].split(", ")
        split_data[0] = input(
            "\nPlease enter the name of the user you "
            "wish to reassign the task to: ")
        join_data = ", ".join(split_data)
        contents[task_num] = join_data
        f = open("tasks.txt", "w")

        for line in contents:
            f.write(line)
        f.close()

        # confirmation message and preview of the edited task
        print(f"\nTask: {task_num} has been edited, "
              f"returning to main menu.\n")
        print(f''' 
==============================================================================                           
Task number:            {str(task_num)}
Task:                   {split_data[1]}
Assigned to:            {split_data[0]}
Date assigned:          {split_data[3]}
Due date:               {split_data[4]}
Task complete?          {split_data[5]}
Task description:       {split_data[2]}
==============================================================================
                    ''')
    # the last option changes the due date and asks the user to enter a
    # specific format of date, using the same method we split/edit/rejoin and
    # write the new data to the external file
    elif second_option == 3:
        split_data = contents[task_num].split(", ")
        split_data[4] = input("\nPlease enter a new due date in the "
                              "following format 02 oct 2022: ")
        join_data = ", ".join(split_data)
        contents[task_num] = join_data
        f = open("tasks.txt", "w")

        for line in contents:
            f.write(line)
        f.close()

        # a confirmation message and preview of the edited task
        print(f"\nTask: {task_num} has been edited, "
              f"returning to main menu.\n")
        print(f''' 
==============================================================================                           
Task number:            {str(task_num)}
Task:                   {split_data[1]}
Assigned to:            {split_data[0]}
Date assigned:          {split_data[3]}
Due date:               {split_data[4]}
Task complete?          {split_data[5]}
Task description:       {split_data[2]}
==============================================================================
                    ''')
    return


# this function is responsible for reading data from our user and task files
# and running calculations to present the total number of users or a percentage
# of task completed and displays it in a neat format.
def generate_report():
    # total number of assigned tasks, with the file open we can use
    # .readlines() to count how many tasks there are in the file because each
    # task is printed on a separate line and readlines() counts by line, to get
    # a numeric value we use len() function to count, we then write the result
    # to another file.
    with open("tasks.txt", "r") as file_tasks:
        total_count = len(file_tasks.readlines())
        with open("task_overview.txt", "w") as file:
            file.write(f"Total number of tasks: {total_count}\n")

    # total number of completed tasks, uses a count variable and iterates
    # through the tasks looking for the value "yes", if it finds one then it
    # + 1 to the counter, calling the variable outside the loop in a print
    # statement will return how many times it found the value in the file
    file = open("task_overview.txt", "a")
    with open("tasks.txt", "r") as file_tasks:
        completed_count = 0
        for task in file_tasks:
            task_sort = task.strip().split(", ")
            if task_sort[5] == "Yes":
                completed_count += 1
        file.write(f"Total number of completed tasks: {completed_count}\n")
    file.close()

    # total number of uncompleted tasks, same method as completed tasks, using
    # a step counter to add the values found within the file
    file = open("task_overview.txt", "a")
    with open("tasks.txt", "r") as file_tasks:
        uncompleted_count = 0
        for task in file_tasks:
            task_sort = task.strip().split(", ")
            if task_sort[5] == "No":
                uncompleted_count += 1
        file.write(f"Total number of uncompleted tasks: {uncompleted_count}\n")
    file.close()

    # total number of overdue tasks not completed, because we are checking if
    # the task is overdue we have to compare today's date with the due date and
    # if today's date is bigger than the due date it means the task is overdue.
    file = open("task_overview.txt", "a")
    with open("tasks.txt", "r") as file_tasks:
        # grabbing today's date using the datetime module
        date_today = datetime.now()
        # setting the desired format of today's date
        date_today = date_today.strftime("%Y%m%d")
        # initialising counter
        overdue_count = 0

        # for loop iterates through all the tasks
        for task in file_tasks:
            task_sort = task.strip().split(", ")
            # coverts task_sort[4] into a date object
            due_date = datetime.strptime(task_sort[4], '%d %b %Y')
            # converts our date object into a new format year/month/day
            # which gives a 6-digit number that can be compared numerically
            due_date = due_date.strftime("%Y%m%d")

            # if overdue and not complete plus 1 to the counter
            if date_today > due_date and task_sort[5] == "No":
                overdue_count += 1
        file.write(
            f"Total number of uncompleted tasks that are now overdue: "
            f"{overdue_count} out of {total_count}\n")

    # percentage of tasks incomplete, simple calculation to turn the incomplete
    # task count variable into a percentage
    file = open("task_overview.txt", "a")
    percentage = uncompleted_count / total_count * 100
    file.write(f"The Percentage of incomplete tasks: {percentage}% \n")

    # percentage of tasks overdue, same calculation but calculating the number
    # of overdue tasks with the overdue_count variable we created earlier
    file = open("task_overview.txt", "a")
    overdue_percentage = overdue_count / total_count * 100
    file.write(f"The Percentage of overdue tasks: {overdue_percentage}%\n")
    file.close()

    # total number of users registered, same method as with tasks count, using
    # readlines() and len() functions
    file = open("user_overview.txt", "w")

    with open("user.txt", "r") as file_users:
        total_users = len(file_users.readlines())
        file.write(f"The total number of users: {total_users}\n")
    file.close()

    # total number of tasks that have been generated
    file = open("user_overview.txt", "a")

    with open("tasks.txt", "r") as file_tasks:
        total_count = len(file_tasks.readlines())
        file.write(f"The total number of tasks: {total_count}\n")
    file.close()

    # total number of tasks assigned to current user, using a count variable,
    # we + 1 everytime the task_sort[0] == the current user logged in
    file = open("user_overview.txt", "a")
    with open("tasks.txt", "r") as file_tasks:
        user_task_count = 0
        for task in file_tasks:
            task_sort = task.strip().split(", ")
            if task_sort[0] == login_username:
                user_task_count += 1
        file.write(f"Total number of tasks assigned to current user: "
                   f"{user_task_count}\n")
    file.close()

    # percentage of total number of tasks assigned to that user, same
    # percentage calculation used before, we take the task count variable and
    # divide it by the total amount of tasks and * 100 to give the percentage
    file = open("user_overview.txt", "a")
    percentage = user_task_count / total_count * 100
    file.write(f"The percentage of total number of tasks assigned to current"
               f" user: {percentage}%\n")

    # percentage of completed tasks, assigned to that user, + 1 to a count
    # variable every time the if statement is met whilst running through the
    # loop, then outside the loop we use the count variable in the percentage
    # equation
    file = open("user_overview.txt", "a")
    with open("tasks.txt", "r") as file_tasks:
        current_count = 0
        for task in file_tasks:
            task_sort = task.strip().split(", ")
            if login_username == task_sort[0] and task_sort[5] == "Yes":
                current_count += 1
        percentage = current_count / total_count * 100
        file.write(f"The percentage of completed tasks assigned to the current"
                   f" user: {percentage}%\n")
    file.close()

    # percentage of tasks assigned to current user that must be completed, the
    # same method but instead of looking for the value yes it searches for no
    file = open("user_overview.txt", "a")
    with open("tasks.txt", "r") as file_tasks:
        uncompleted_tasks = 0
        for task in file_tasks:
            task_sort = task.strip().split(", ")
            if login_username == task_sort[0] and task_sort[5] == "No":
                uncompleted_tasks += 1
        percentage = uncompleted_tasks / total_count * 100
        file.write(f"The percentage of uncompleted tasks assigned to the"
                   f" current user: {percentage}%\n")

    # percentage of tasks not complete and overdue, assigned to that user, this
    # borrows the same code as above but converts the uncompleted counter into
    # a percentage, also we only + 1 if both conditions are met in the if
    # statement.
    file = open("user_overview.txt", "a")
    with open("tasks.txt", "r") as file_tasks:
        uncompleted_tasks = 0
        for task in file_tasks:
            task_sort = task.strip().split(", ")
            due_date = datetime.strptime(task_sort[4], '%d %b %Y')
            due_date = due_date.strftime("%Y%m%d")
            if login_username == task_sort[0] and date_today > due_date and \
                    task_sort[5] == "No":
                uncompleted_tasks += 1
        percentage = uncompleted_tasks / total_count * 100
        file.write(f"The percentage of uncompleted tasks, that are overdue,"
                   f" assigned to the current user: {percentage}%\n")

    print("\nThe reports have been generated, returning to main menu.")
    return


# admin only option, it checks to see if the admin is the current user, returns
# to main menu if not. if the first check passes it creates two files and
# checks the file size using the getsize() function from the os module. If the
# files are empty runs the code to generate the reports and the prints them.
def view_stats():
    while True:
        if login_username == "admin" and login_password == "adm1n":
            create_user_file = open("user_overview.txt", "w")
            create_task_file = open("task_overview.txt", "w")

            if os.path.getsize("task_overview.txt") == 0 or \
                    os.path.getsize("user_overview.txt") == 0:
                generate_report()

            with open("task_overview.txt", "r") as file_task_overview:
                file_task_read = file_task_overview.read()
                print(f"\n{file_task_read}")

            with open("user_overview.txt", "r") as file_user_overview:
                file_user_read = file_user_overview.read()
                print(file_user_read)
                break
        else:
            print("\nYou do not have administrative privileges to access "
                  "that information.")
            break
    return


# ===========================Login============================================
# initialising empty lists and opening user.txt as read only.
# asks user for their login details, opens the database of current login
# details and sorts the username and password into separate lists (using a
# for loop to iterate through each line and split the entries by ',') if the
# login and password are present in both lists, log in, else try again.
while True:
    login_username = input("Enter your username: ")
    login_password = input("Enter your password: ")
    user_file = open("user.txt", "r")
    user_list = []
    user_pass = []
    for data in user_file:
        data_split = data.split(",")
        user_list.append(data_split[0].strip())
        user_pass.append(data_split[1].strip())

    if login_username in user_list and login_password in user_pass:
        print("You have successfully logged in!")
        user_file.close()
        break

    else:
        print(
            "That username or password does not match, please try again.\n")

# =================================MENU=======================================
# Using a while loop to display a menu to the user, there are conditional
# statements for each option in the menu, each call a different function.

while True:
    user_choice = menu()

    if user_choice == 'r':
        reg_user()

    elif user_choice == 'a':
        add_task()

    elif user_choice == 'va':
        view_all()

    elif user_choice == 'vm':
        view_mine()

    elif user_choice == 'gr':
        generate_report()

    elif user_choice == 's':
        view_stats()

    elif user_choice == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")
