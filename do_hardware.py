import valve
import pump
import xstage
import ystage
import zstage
import fpga


def dispatch(hardware, command, serial_port, f_log, configuration):

    ####################################################################
    ### hardware specific options for command ##########################
    ####################################################################
    
    # send command to valve
    def do_valve(hardware, port, command, f):
        valve.valve(hardware, port, command, f)


    # send command to pump
    def do_pump(hardware, port, command, f):
        
        vol = configuration['ChamberVolume']    
        speed = 0
        while speed < 0.1 or speed > 20 :
            speed = float(input('speed (0.1 -20 mL/min): '))
        #convert speed from mL/min to steps per second
        speed = int(float(speed) / 60 / 8 / 250 * 48000 * 1000)    
        pump.pump(hardware, port, command, vol, speed, f)

    # send command to xstage
    def do_xstage(hardware, port, command, f):
        xstage.move(port, command, f, configuration)

    # send command to ystage
    def do_ystage(hardware, port, command, f):
        ystage.move(port, command, f, configuration)

    # send command to zstage         
    def do_zstage(hardware, port, command, f):
        zstage.move(port, command, f, configuration)

    # send command to zstage                
    def do_fpga(hardware, port, command, f):
        fpga.fpga(port, command, f, configuration)
        
    ####################################################################
    ####################################################################
    ####################################################################
        
    # Dispatch Dictionary
    dispatch_dict = {'ARM9CHEM': None,
                'ARM9DIAG': None,
                'FPGAcommand': do_fpga,
                'FPGAresponse': do_fpga,
                'KLOEHNA': do_pump,
                'KLOEHNB': do_pump,
                'Laser1': None,
                'Laser2': None,
                'PCcamera': None,
                'PCIO': None,
                'TESTport': None,
                'VICIA1': do_valve,
                'VICIA2': do_valve,
                'VICIB1': do_valve,
                'VICIB2': do_valve,
                'XSTAGE': do_xstage,
                'YSTAGE': do_ystage,
                'ZSTAGE': do_zstage,
                }

    # Send basic command to different piecses of hardware 
    dispatch_dict[hardware](hardware, serial_port, command, f_log)
