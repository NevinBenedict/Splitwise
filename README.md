This project is a **Splitwise-like Expense Sharing Application** designed to help users manage group expenses and settlements. It allows users to create groups, add expenses, split costs among group members, and track balances and settlements. Below is a detailed description of the project's functionality and components:

---

### **Key Features**
1. **User Management**:
   - Users can register, log in, and log out.
   - Each user has a profile with basic details like username and email.

2. **Group Management**:
   - Users can create groups and invite other users to join.
   - Group creators can manage members, including removing members if necessary.
   - Groups are used to organize expenses among specific sets of users.

3. **Expense Management**:
   - Users can add expenses to a group, specifying the total amount, description, and payer.
   - Expenses can be split among group members using one of the following methods:
     - **Equal Split**: The total amount is divided equally among all members.
     - **Exact Split**: Specific amounts are assigned to each member.
     - **Percentage Split**: The total amount is split based on percentages assigned to each member.

4. **Expense Tracking**:
   - Users can view a list of expenses for a group, including details like the payer, total amount, and split amounts.
   - Each user's balance is tracked, showing how much they owe or are owed.

5. **Settlements**:
   - Users can settle balances by making payments to other group members.
   - Settlements are recorded and reduce the outstanding balances.

6. **Email Notifications**:
   - Email notifications are sent to group members when expenses are added or balances are updated.

7. **Dashboard**:
   - Users can view an overview of their groups, expenses, and settlements.
   - The dashboard provides a summary of total amounts owed and paid.

---





### **Technologies Used**
1. **Backend**:
   - Django (Python) for handling business logic and database interactions.
   - Django ORM for database operations.

2. **Frontend**:
   - HTML, CSS, and Bootstrap for responsive UI design.
   - Django templates for rendering dynamic content.

3. **Database**:
   - SQLite (default Django database) for development.
   - Can be switched to PostgreSQL or MySQL for production.

4. **Email**:
   - Django's `send_mail` function for sending email notifications.
   - SMTP server (e.g., Gmail) for email delivery.

---

### **How It Works**
1. **Creating a Group**:
   - A user creates a group and invites other users to join.
   - The group creator can manage members and expenses.

2. **Adding an Expense**:
   - A user adds an expense to the group, specifying the total amount, payer, and split type.
   - The system calculates how much each member owes and creates `ExpenseSplit` records.

3. **Tracking Balances**:
   - Each user's balance is updated based on the expenses they owe or have paid.

4. **Settling Balances**:
   - Users can settle balances by making payments to other members.
   - Settlements are recorded, and balances are updated accordingly.

5. **Viewing Reports**:
   - Users can view detailed reports of expenses, balances, and settlements for each group.

---

### **Example Use Case**
1. Alice creates a group called "Vacation Trip" and invites Bob and Charlie.
2. Alice adds an expense of $300 for hotel booking, which she paid for. The expense is split equally among the three members.
3. The system calculates that Bob and Charlie each owe $100 to Alice.
4. Bob makes a payment of $100 to Alice through the app. The system records the settlement and updates the balances.
5. Charlie can view his remaining balance and settle it later.

---

This project provides a robust foundation for managing group expenses and can be extended with additional features to enhance usability and functionality.
