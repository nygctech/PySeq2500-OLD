import serial

def valve(hardware, s, command, f):
    f.write('to ' + hardware + ': ' + command +'\n')
    s.write(command)
    s.flush()
    response = s.readline()
    print(hardware + ' response: ' + response)
    f.write('from ' + hardware + ': ' + response + '\n')
