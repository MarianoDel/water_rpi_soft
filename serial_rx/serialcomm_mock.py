## Mocked serial port for debugging pourpose


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
        # check cb function
        import types
        if isinstance(callback, (types.FunctionType, types.BuiltinFunctionType)) != True:
            print('callback not a function!')

    def Write(self, data):
        print ('data to send on serial: ' + str(data))

    def Read(self):
        print ('data getted on serial')

    def Close(self):
        if self.port_open == True:
            print ("close serial port")
            self.port_open = False

