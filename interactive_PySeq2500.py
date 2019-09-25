import configparser

import open_ports
import make_logfile
import do_hardware

# dictionary of text wrapped serial ports
#keys = name of instrument/hardware (port)
#values = text wrapped serial ports
io_dict = open_ports.open_ports()


# Get configuration
config = configparser.ConfigParser()
config.read('configuration.ini')
config_section = ''
while config_section not in config.sections():
    print('Which configuration do you want to use?')
    print(config.sections())
    print('or DEFAULT')
    config_section = input('configuration: ')
    
# Open log file
f_log = make_logfile.get_log()
 
#Define word to exit interactive session
exit_word = 'bye'

# Get and send commands to dispatch
port = None                                             # port = user input, name of instrument/hardware to send command to                                    
command = None                                          # command = user input, command to send to instrument/hardware
while port == None and command == None:
    port = input('port: ')
    if port in io_dict:
            command = input('command: ')
            if command != exit_word:
                do_hardware.dispatch(port, command, io_dict[port], f_log, config[config_section])
                port = None
                command = None
            else:
                f_log.close()
                break
    elif port == exit_word:
        f_log.close()
        break
    else:
        print('That port does not exist')
        print('Choose from: ', list(io_dict))
        port = None
