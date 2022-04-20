import pwd

users = pwd.getpwall()
for user in users:
    print(user.pw_name, user.pw_shell)
