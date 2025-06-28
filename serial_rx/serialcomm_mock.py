## Mocked serial port for debugging pourpose
import signal
# import time


class SerialCommMock:
    """
    Mocked Class for serial port handler

    get:
    port: name or route to device ex. /dev/ttyACM0
    velocidad: ex. 9600
    callback: the function where to send the rx port data

    Members
    port_open: boolean

    """

    port_open = False

    def __init__(self, callback, port, velocidad=9600):

        print ('opening mock port: ' + port)
        self.port_open = True
        self.callback = callback
        # check cb function
        import types
        if isinstance(callback, (types.FunctionType, types.BuiltinFunctionType)) != True:
            print('callback not a function!')
            self.callback = self.Callback_Error

        self.counter = 12
        self.Activate_Timeout(self.timeout_handler)
            
    def Write(self, data):
        print ('data to send on serial: ' + str(data))
        self.Answers_for_Write (data)

    def Read(self, datacb):
        print ('data getted on serial')
        self.callback(datacb)

    def Close(self):
        if self.port_open == True:
            print ("close serial port")
            self.port_open = False

    def Answers_for_Write (self, data):
        if data.startswith('uptime'):
            self.Read('uptime hours 60000\r\n')

    def Callback_Error (self, data):
        print('callback not a function, not sended str: ' + str(data)) 

    def Activate_Timeout (self, timeout_handler):
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(2) # Set a 2-second timeout
        
    def timeout_handler(self, signum, frame):
        print(f'counter: {self.counter}')
        if self.counter:
            self.counter -= 1
            signal.alarm(2) # Set a 2-second timeout
            # self.Read("last_10_all,2,0,0,0,2\r\n")
            self.Read("last_10_all,10,0,0,0,10\r\n")            
            # master_meas.csv 2025-06-27 -- 03:57,1,0,0,0,1
        else:
            print('end alarm')
            signal.alarm(0) # Disable the alarm

        
        
