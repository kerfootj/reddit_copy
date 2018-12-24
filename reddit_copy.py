import praw, sys, getpass

def usage():
    print('Usage: "python3 reddit_copy.py -u1 <username> -u2 <username>"')
    print('or')
    print('Usage: "python3 reddit_copy.py -f <filename>"')
    sys.exit()

# Get credentials from a text file
if len(sys.argv) == 3:
    if sys.argv[1] == '-f':
        file_name = sys.argv[2]
        
        try:
            file = open(file_name, 'r')
            credentials = []
            for line in file:
                credentials.append(line[:-1])

            user1 = credentials[0]
            clid1 = credentials[1]
            clsc1 = credentials[2]
            clua1 = credentials[3]

            user2 = credentials[4]
            clid2 = credentials[5]
            clsc2 = credentials[6]
            clua2 = credentials[7]

        except:
            print('failed to open file: %s' % (file_name))
            sys.exit()
    else:
        usage()

# Get credentials from the cmd line
elif len(sys.argv) == 5:
    if sys.argv[1] == '-u1' and sys.argv[3] == '-u2':
        user1 = sys.argv[2]
        user2 = sys.argv[4]

        # Get user 1 credentials
        clid1 = input('User 1 Client id: ')
        clsc1 = input('User 1 Client Secret: ')
        clua1 = input('User 1 User Agent: ')

        # Get user 2 credentials
        clid2 = input('User 2 Client id: ')
        clsc2 = input('User 2 Client Secret: ')
        clua2 = input('User 2 User Agent: ')
    else:
        usage()
else:
    usage()

# Get account passwords and login 
pswd1 = getpass.getpass('User 1 Password: ')
pswd2 = getpass.getpass('User 2 Password: ')

print('logging into account 1')
reddit_from = praw.Reddit(  client_id = clid1, 
                            client_secret = clsc1, 
                            user_agent = clua1,
                            username = user1,
                            password = pswd1)

print('logging into account 2')
reddit_to = praw.Reddit(    client_id = clid2, 
                            client_secret = clsc2, 
                            user_agent = clua2,
                            username = user2,
                            password = pswd2)

total = 0
copied = 0
failed = 0
failed_saves = []

for post in reddit_from.redditor(user1).saved(limit=1000):
    copied += 1
    if post.over_18 == True:
        total += 1
    else:
        try:
            submission = reddit_to.submission(id=post)
            submission.save()
        except:
            failed += 1
            failed_saves.append(submission)
            
print('%d posts failed to save and %d saved successfully' % (failed, copied))
