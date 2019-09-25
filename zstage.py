import time

# Move Tilt Motors # number of steps or
# generic command if it's not a positive integer
def move(s, position, f, configuration):
    
    if position.isdigit():
        for n in range(1,3):
            command = 'T' + str(n) + 'MOVETO ' + position + '\n'
            f.write = 'to zstage: ' + command
            s.write(command)
            s.flush()
            response = s.readline()
            #f.write('from zstage: ' + response)
        
    else:
        command = position + '\n'
        f.write = 'to zstage: ' + command
        s.write(command)
        s.flush()
        response = s.readline()
        #f.write('from zstage: ' + response)

    # Make sure Zstage is in the correct position
    if position.isdigit():
        attempts = 1
##        correct_position = False
##        while correct_position == False and attempt <= 3:
##            status(s,f)
##            correct_position = check_position(position, s, f)
##            #Retry moving Zstage if not correct
##            #Try at least 3 times
##            if correct_position == False
##                print('Zstage did not reach position on attempt ' + attempt)
##                attempt = attempt + 1
##                f.write = 'to Zstage: ' + command
##                s.write(command)
##                s.flush()
##                response = s.readline()
##                f.write('from Zstage: ' + response)
##        if attempts > 3
##            print('Tried moving Zstage ' + attempts + ' times but failed')
    else:
        print('from Zstage: ' + response)


# Query zstage to see if moving. 1 = moving. 0 = stopped
def status(s,f):
    moving = 1
    while moving == 1:
        for n in range(1,3):
            command = 'T'+ n + 'RD\n'
            f.write = 'to zstage: ' + command
            s.write(command)
            s.flush()
            position1 = s.readline()
            #f.write('from zstage: ' + position)
            time.sleep(2)
            command = 'T' + n + 'RD\n'
            f.write = 'to zstage: ' + command
            s.write(command)
            s.flush()
            position2 = s.readline()
            if position1 == position2:
                moving = 0
        

# Query zstage to check if the desired position is reached. 
def check_position(position, s, f):
    in_position = [False,False,False]
    for n in range(1,3):
        command = 'T' + str(n) + 'RD\n'
        f.write = 'to zstage: ' + command
        s.write(command)
        s.flush()
        response = s.readline()
        #f.write('from zstage: ' + response)
        if response == position[n-1]:
            in_position[n-1] = True
        
