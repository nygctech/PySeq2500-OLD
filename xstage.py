import time

# Move xstage # number of steps or
# generic command if it's not a positive integer
def move(s, position, f, configuration):
    
    if position.isdigit():
        command = 'MA ' + position + '\r'
    else:
        command = position + '\r'
    
    f.write = 'to xstage: ' + command
    s.write(command)
    s.flush()
    response = s.readline()
    #f.write('from xstage: ' + str(response))

    # Make sure Xstage is in the correct position
    if position.isdigit():
        attempt = 1
        correct_position = False
        while correct_position == False and attempt <= 3:
            status(s,f)
            correct_position = check_position(position, s, f)
            #Retry moving 4iXstage if not correct
            #Try at least 3 times
            if correct_position == False:
                print('xstage did not reach position on attempt ' + str(attempt))
                attempt = attempt + 1
                f.write = 'to xstage: ' + command
                s.write(command)
                s.flush()
                response = s.readline()
                status(s,f)
                correct_position = check_position(position,s,f)
                #f.write('from xstage: ' + response)
        if attempt > 3:
            print('Tried moving xstage ' + str(attempt) + ' times but failed')
    else:
        print('from xstage: ' + response)


# Query Xstage to see if moving. 1 = moving. 0 = stopped
def status(s,f):
    moving = 1
    while moving == 1:
        command = 'PR MV\r'
        f.write = 'to xstage: ' + command
        s.write(command)
        s.flush()
        moving = int(s.readline())
        #f.write('from xstage: ' + str(moving))
        time.sleep(2)

# Query Xstage to check if the desired position is reached. 
def check_position(position, s, f):
    command = 'PR P\r'
    f.write = 'to xstage: ' + command
    s.write(command)
    s.flush()
    response = s.readline()
    #f.write('from xstage: ' + response)
    if int(position) == int(response):
        return True
    else:
        return False
    
    
        
    
    
