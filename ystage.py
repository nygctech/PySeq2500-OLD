import time

# Move Ystage # number of steps or
# generic command if it's not a positive integer
def move(s, position, f, configuration):
    
    if position.isdigit():
        command = '1D' + position + '\r\n'
        f.write = 'to ystage: ' + command
        s.write(command)
        s.flush()
        response = s.readline()
        #f.write('from ystage: ' + response)
        command = '1G\r\n'
    else:
        command = '1' + position + '\r\n'
    
    f.write = 'to ystage: ' + command
    s.write(command)
    s.flush()
    response = s.readline()
    #f.write('from ystage: ' + response)

    # Make sure Ystage is in the correct position
    if position.isdigit():
        attempt = 1
        correct_position = False
        while correct_position == False and attempt <= 3:
            status(s,f)
            correct_position = check_position(s, f)
            #Retry moving Ystage if not correct
            #Try at least 3 times
            if correct_position == False:
                print('ystage did not reach position on attempt ' + attempt)
                attempt = attempt + 1
                command = '1D' + position + '\r\n'
                f.write = 'to ystage: ' + command
                s.write(command)
                command = '1G\r\n'
                f.write = 'to ystage: ' + command
                s.write(command)
                s.flush()
        if attempt > 3:
            print('Tried moving ystage ' + str(attempt) + ' times but failed')
    else:
        print('from ystage: ' + response)


# Query ystage to see if moving. 1 = moving. 0 = stopped
def status(s,f):
    moving = 1
    while moving == 1:
        command = '1R(MV)\r\n'
        f.write = 'to ystage: ' + command
        s.write(command)
        s.flush()
        moving = int(s.readline()[1:])
        print('moving = ' + str(moving))
       #f.write('from ystage: ' + moving)
        time.sleep(2)

# Query ystage to check if the desired position is reached. 
def check_position(s, f):
    command = '1R(IP)\r\n'
    f.write = 'to ystage: ' + command
    s.write(command)
    s.flush()
    response = int(s.readline()[1:])
    print('in position = ' + str(response))
    #f.write('from ystage: ' + response)
    if response == 1:
        return True
    else:
        return False
    
