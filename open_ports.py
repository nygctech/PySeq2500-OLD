import os
import serial
import io

def open_ports():
    #dictionary of portnames as keys with baudrate as values
    port_baud_rate_dict = {'ARM9CHEM': 115200,
                'ARM9DIAG': 9600,               #assumed
                'FPGAcommand': 115200,
                'FPGAresponse': 115200,
                'KLOEHNA': 9600,
                'KLOEHNB': 9600,
                'Laser1': 9600,
                'Laser2': 9600,
                'PCcamera': 9600,               #assumed
                'PCIO': 115200,
                'TESTport': 9600,               #assumed
                'VICIA1': 9600,
                'VICIA2': 9600,
                'VICIB1': 9600,
                'VICIB2': 9600,
                'XSTAGE': 9600,
                'YSTAGE': 9600,
                'ZSTAGE': 9600,                 #assumed
                }

    #dictionary of io streams as values with portnames as keys
    io_dict = dict.fromkeys(list(port_baud_rate_dict))


    # loop over ports, open serial port and then wrap in text
    for port in port_baud_rate_dict:
            com_port = os.environ.get(port)                                                     #get COM port #
            if com_port != None:
                com_port = com_port[com_port.find('(')+1:com_port.find(')')]                    #remove parenthesis from (COM#)
                serial_port = serial.Serial(com_port,                                           #open serial port
                            baudrate = port_baud_rate_dict[port],
                            timeout = 1)
                # If not FPGA, use the same port input and output
                if port.find('FPGA') == -1:
                    io_dict[port] = io.TextIOWrapper(io.BufferedRWPair(serial_port, serial_port),
                                encoding = 'ascii',
                                errors = 'ignore')
                elif port == 'FPGAcommand':
                    fpga_in = serial_port
                elif port == 'FPGAresponse':
                    fpga_out = serial_port
                    
 
    # Initialize Pumps
    if io_dict['KLOEHNA'] != None:
        io_dict['KLOEHNA'].write('/1W4R\r')
        io_dict['KLOEHNA'].flush()
        response = io_dict['KLOEHNA'].readline()
    if io_dict['KLOEHNB'] != None:
        io_dict['KLOEHNB'].write('/1W4R\r')
        io_dict['KLOEHNB'].flush()
        response = io_dict['KLOEHNB'].readline()
    
    # Initialize X-Stage
    if io_dict['XSTAGE'] != None:
        #Initialize X-Stage
        io_dict['XSTAGE'].write('\x03\r')
        io_dict['XSTAGE'].flush()
        response = io_dict['XSTAGE'].readline()
        print('xstage: ' + response)
        #Change echo mode to respond only to print and list commands 
        io_dict['XSTAGE'].write('EM=2\r')
        io_dict['XSTAGE'].flush()
        response = io_dict['XSTAGE'].readline()
        print('xstage: ' + response)
        #Enable Encoder
        io_dict['XSTAGE'].write('EE=1\r')
        #Set Initial Velocity
        io_dict['XSTAGE'].write('VI=40\r')
        io_dict['XSTAGE'].flush()
        #Set Max Velocity
        io_dict['XSTAGE'].write('VM=1000\r')
        io_dict['XSTAGE'].flush()
        #Set Acceleration
        io_dict['XSTAGE'].write('A=4000\r')
        io_dict['XSTAGE'].flush()
        #Set Deceleration
        io_dict['XSTAGE'].write('D=4000\r')
        io_dict['XSTAGE'].flush()
        #Set Home
        io_dict['XSTAGE'].write('S1=1,0,0\r')
        io_dict['XSTAGE'].flush()
        #Set Neg. Limit
        io_dict['XSTAGE'].write('S2=3,1,0\r')
        io_dict['XSTAGE'].flush()
        #Set Pos. Limit
        io_dict['XSTAGE'].write('S3=2,1,0\r')
        io_dict['XSTAGE'].flush()
        #Set Stall Mode = stop motor
        io_dict['XSTAGE'].write('SM=0\r')
        io_dict['XSTAGE'].flush()
        # limit mode = stop if sensed
        io_dict['XSTAGE'].write('LM=1\r')
        io_dict['XSTAGE'].flush()
        #Encoder Deadband
        io_dict['XSTAGE'].write('DB=8\r')
        io_dict['XSTAGE'].flush()
        #Debounce home
        io_dict['XSTAGE'].write('D1=5\r')
        io_dict['XSTAGE'].flush()
        # Set hold current
        io_dict['XSTAGE'].write('HC=20\r')
        io_dict['XSTAGE'].flush()
        # Set run current
        io_dict['XSTAGE'].write('RC=100\r')
        io_dict['XSTAGE'].flush()
        # Set run current
        io_dict['XSTAGE'].write('RC=100\r')
        io_dict['XSTAGE'].flush()
        # Home stage
        io_dict['XSTAGE'].write('PG 1\r')
        io_dict['XSTAGE'].write('HM 1\r')
        io_dict['XSTAGE'].write('H\r')
        io_dict['XSTAGE'].write('P=30000\r')
        io_dict['XSTAGE'].write('E\r')
        io_dict['XSTAGE'].write('PG\r')
        io_dict['XSTAGE'].flush()
        io_dict['XSTAGE'].write('EX 1\r')
        io_dict['XSTAGE'].flush()
    
    # Initialize Y-Stage
    if io_dict['YSTAGE'] != None:
        io_dict['YSTAGE'].write('1Z\r\n')
        io_dict['YSTAGE'].flush()
        response = io_dict['YSTAGE'].readline()
        print('ystage: ' + response)
        io_dict['YSTAGE'].write('1W(EX,0)\r\n')
        io_dict['YSTAGE'].flush()
        response = io_dict['YSTAGE'].readline()
        print('ystage: ' + response)
        io_dict['YSTAGE'].write('1W(CQ,1)\r\n')                                         #Pause until commans are complete
        io_dict['YSTAGE'].write('1MA\r\n')                                              #Set Absolute Positioning mode
        io_dict['YSTAGE'].write('1GAINS(5,10,7,1.5,0)\r\n')                             #Set gains
        io_dict['YSTAGE'].write('1LIMITS(0,1,0,1000.0)\r\n')                            #Set Limits
        io_dict['YSTAGE'].write('1W(EW,2500)\r\n')                                      #Set position error window
        io_dict['YSTAGE'].write('1W(IT,100)\r\n')                                       #Set Settling time
        io_dict['YSTAGE'].write('1HOME1(-,0,+0.4,0.1,3)\r\n')                           #Setup Homing
        io_dict['YSTAGE'].write('1W(HF,0.1)\r\n')                                       #Set homing final velocity
        io_dict['YSTAGE'].write('1MOTOR(49420,1.6,1300000,138,80,4.75,1.8,4.5)\r\n')    #Configure motor
        io_dict['YSTAGE'].flush()
        io_dict['YSTAGE'].write('1ON\r\n')                                              #Energize Motor
        io_dict['YSTAGE'].flush()
        io_dict['YSTAGE'].write('1GH\r\n')                                              #Go Home
        io_dict['YSTAGE'].write('1W(PA,0)\r\n')                                         #Zero out
        io_dict['YSTAGE'].flush()
        
        #response = io_dict['YSTAGE'].readline()
        #print('ystage: ' + response)

   
    # Initialize FPGA
    if 'fpga_in' in locals() and 'fpga_out' in locals() :
        # Wrap fpga input/output with seperate serial ports
        io_dict['FPGAcommand'] = io.TextIOWrapper(io.BufferedRWPair(fpga_out, fpga_in),
                                encoding = 'ascii',
                                errors = 'ignore')
        ##    io_dict['FPGAresponse'] = io.TextIOWrapper(io.BufferedRWPair(fpga_out, fpga_in),
        ##                                encoding = 'ascii',
        ##                                errors = 'ignore')
   
        io_dict['FPGAcommand'].write('RESET\n')
        io_dict['FPGAcommand'].flush()
        response = io_dict['FPGAcommand'].readline()
        print('fgpa: ' + response)

    #Initialize Tilt Motors
    io_dict['ZSTAGE'] = io_dict['FPGAcommand']
    io_dict['ZSTAGE'].write('T1HM\n')
    io_dict['ZSTAGE'].write('T2HM\n')
    io_dict['ZSTAGE'].write('T3HM\n')
    io_dict['ZSTAGE'].flush()
    
    return io_dict
