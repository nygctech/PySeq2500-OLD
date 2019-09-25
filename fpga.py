import serial

def fpga(s, command, f, configuration):
    f.write('to fpga: ' + command)
    command = command + '\n'
    s.write(command)
    s.flush()
    response = s.readline()
    print('response: ' + response)
    #f.write('from fpga: ' + response)
