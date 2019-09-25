import time
import serial
import sys

#function automatically switch pump valve and flow through x chamber volume (uL) of fluid
def pump(hardware, s, command, vol, speed, f):
        
        #draw fluid into syringe
        command_pos = int(command) * vol * 48000 / 8 / 250   # convert command in chamber volume units to steps
        command = '/1IV' + str(speed) + 'A' + str(int(command_pos)) + 'R\r'
        f.write('to ' + hardware + ': ' + str(command) + '\n')   # write command to log
        s.write(command)
        s.flush()                                            #it is buffering. required to get the data out *now*
        response = s.readline()
        print(hardware + ' response: ' + response)
        f.write('from ' + hardware + ': ' + response + '\n')
        check_pump(hardware, s,command_pos,f)

        #switch pump valve to output
        f.write('to ' + hardware + ': /1OR\r')
        std_command = '/1OR\r'
        s.write(std_command)
        s.flush()
        response = s.readline()
        f.write('from ' + hardware + ': ' + response + '\n')
        
        #push fluid out of syringe to waste and return to 0 position
        command_pos = 0
        f.write('to ' + hardware + ': /1OV7000A0R\r')
        std_command = '/1OV7000A0R\r'
        s.write(std_command)
        s.flush()
        response = s.readline()
        f.write('from ' + hardware + ': ' + response + '\n')
        check_pump(hardware, s,command_pos,f)
        
        #switch pump valve to input
        f.write('to ' + hardware + ': /1IR\r')
        std_command = '/1IR\r'
        s.write(std_command)
        s.flush()
        response = s.readline()
        f.write('from ' + hardware + ': ' + response + '\n')

#function to check status of pump and hold if busy
def check_pump(hardware, s,command_pos,f):
        status_code = '@'
        busy = '@'
        ready = '`'
        # initialize status code as busy
        while status_code[0] != ready : 
                command = '/1\r'                                                # query pump status
                f.write('to ' + hardware + ': ' + command)                      # write command to log
                s.write(command)
                s.flush()
                response = s.readline()
                f.write('from ' + hardware + ': ' + response + '\n')            # write response to log
                status_code = str(response.split('0')[1])                       # parse status code
                if status_code[0] == busy :
                        time.sleep(2)
                elif status_code[0] == ready:
                    check_pos(hardware,command_pos,f)
                elif status_code[0] != ready :
                        print(hardware + 'pump error')
                        sys.exit()

#function to check pump is at correct position
def check_pos(hardware, s,command_pos,f):
    f.write('to ' + hardware + ': /1?\r')                    # Query pump position
    s.write('/1?\r')
    s.flush()
    response = s.readline()
    f.write('from ' + hardware + ': ' + response + '\n')
    response = response.split('`')[1]                        # get position, end code, and new line
    response = int(response.split('\x03')[0])                # get position, convert to integer
    # Resend command if not at correct position
    if response != command_pos:
        command = '/1A' + str(command_pos) + 'R\r'
        f.write('to ' + hardware + ': ' + str(command))      # write command to log
        s.write(command)
        s.flush()                                            #it is buffering. required to get the data out *now*
        response = s.readline()
        f.write('from ' + hardware + ': ' + response + '\n') # write response to log
        print('pump not at correction position, retrying...')
        check_pump(hardware,command_pos,f)
