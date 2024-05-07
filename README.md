Task 1 - Welcome Card Implementation
The welcome card implementation utilizes the Discord.py library to handle new member
events and send welcome messages.

1. The key steps in this task are as follows:
2. Set up the Discord.py bot and connect it to the Discord server.
3. Implement an event handler for the on_member_join event.
4. When a new member joins, send a welcome message in a specific channel using
the send method.
5. Initiate a direct message to the new member using the send method.
The implementation ensures error handling for any potential exceptions that may occur
during the process.

Task 2 – Word Counting
In this task, you want to count each word that is sent to a guild, and by using
commands, show which words are used the most. Also, implement a command which
gives the most used words by a user.
Key Steps:
1. Set up a MySQL database.
2. Create a table named 'user_words' with two columns: 'discord_id' and 'word'.
3. Implement an event handler for on_message. When a message is received,
extract all words in the message and store them in the database with the
sender's user ID.
4. Next, Implement two commands:
a. /word-status: Gives the 10 most used words.
b. /user-status <user>: Gives the 10 most used words by the specified user.

Task 3 – User Role Selection Implementation
In this task use Discord.py library to implement a feature allowing users to select their
roles via a select menu.
Key Steps:
1. Create a table named "user_role" with columns: discord_id and role. This table will
store Discord user IDs alongside their selected roles.
2. Implement a slash command /select-role, which sends a message containing a
select menu as a response to the command, The select menu should contain
available roles to choose from.
3. Upon a user's selection of a role from the menu, update the role of the user in the
database.
4. Also grant the selected role to the user on Discord.
