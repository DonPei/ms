
import time
import asyncio
        
        
class MotorBase():

    def __init__(self, board):
        self.board = board

        # Callback data indices
        self.CB_PIN_MODE = 0
        self.CB_PIN = 1
        self.CB_VALUE = 2
        self.CB_TIME = 3

    def print_data(self, data):
        formatted_time = self.format_time(data[self.CB_TIME])
        print(f'Analog Call Input Callback: pin={data[self.CB_PIN]}, '
          f'Value={data[self.CB_VALUE]} Time={formatted_time} '
          f'(Raw Time={data[self.CB_TIME]})')
        
    def format_time(self, raw_time):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(raw_time))
    
    def current_position_callback(self, data):
        msg = (f'current_position_callback returns {data[2]}\n')
        self.base_callback(msg)

    def target_position_callback(self, data):
        msg = (f'target_position_callback returns {data[2]}')
        self.base_callback(msg)

    def distance_to_go_callback(self, data):
        msg = (f'distance_to_go_callback returns {data[2]}\n')
        self.base_callback(msg)
            
    def is_running_callback(self, data):
        msg = (f'is_running_callback returns {data[1]}\n')
        self.base_callback(msg)
    
    def base_callback(self, msg):
        if self.qWidget == None:
            print("widget is None")
            print(msg)
        else:
            self.qWidget.append(msg)
            self.qWidget.append("\n")
    
    def callback_details(self, context):
        print("Task completion received...")
        print("Name of the task:%s"%context.get_name())
        print("Wrapped coroutine object:%s"%context.get_coro())
        print("Task is done:%s"%context.done())
        print("Task has been cancelled:%s"%context.cancelled())
        print("Task result:%s"%context.result())
        print(type(context))
        print(context)

    def callback_base(self, context):
        if self.qWidget == None:
            print("widget is None")
            print("Task result:%s"%context.result())
        else:
            self.qWidget.append(context.result())
            self.qWidget.append("\n")
    
    async def set_motor_info(self, qWidget, motor):
        self.qWidget = qWidget
        
        task1 = await self.board.stepper_set_current_position(motor, 216)
        task1 = await self.board.stepper_move_to(motor, 300)
        task1 = await self.board.stepper_set_current_position(motor, 216)
        
        task1 = await self.board.stepper_is_running(motor, self.is_running_callback)
        task2 = await self.board.stepper_get_current_position(motor, self.current_position_callback)
        task3 = await self.board.stepper_get_target_position(motor, self.target_position_callback)
        task4 = await self.board.stepper_get_distance_to_go(motor, self.distance_to_go_callback)
        task5 = await self.board.stepper_get_speed(motor, self.base_callback)
        task6 = await self.board.stepper_get_max_speed(motor, self.base_callback)

        await asyncio.gather(task1, task2, task3, task4, task5, task6)
        
    async def get_motor_info(self, qWidget):
        self.qWidget = qWidget
        stepPin = 7
        dirPin = 3
        motor = await self.board.set_pin_mode_stepper(interface=1, pin1=stepPin, pin2=dirPin)
        
        task1 = await self.board.stepper_is_running(motor, self.is_running_callback)
        task2 = await self.board.stepper_get_current_position(motor, self.current_position_callback)
        task3 = await self.board.stepper_get_target_position(motor, self.target_position_callback)
        task4 = await self.board.stepper_get_distance_to_go(motor, self.distance_to_go_callback)
        #task5 = await self.board.stepper_get_speed(motor)
        #task6 = await self.board.stepper_get_max_speed(motor)

        await asyncio.gather(task1, task2, task3, task4)

    async def get_motor_info1(self, qWidget):
        self.qWidget = qWidget
        stepPin = 7
        dirPin = 3
        motor = await self.board.set_pin_mode_stepper(interface=1, pin1=stepPin, pin2=dirPin)
        task1 = asyncio.ensure_future(self.retrieve_firmware_version())
        task2 = asyncio.ensure_future(self.retrieve_protocol_version())
        task3 = asyncio.ensure_future(self.retrieve_pymata_version())
        task4 = asyncio.ensure_future(self.retrieve_analog_map())
        task5 = asyncio.ensure_future(self.retrieve_capability_report())

        task1.add_done_callback(self.callback_base)
        task2.add_done_callback(self.callback_base)
        task3.add_done_callback(self.callback_base)
        task4.add_done_callback(self.callback_base)
        task5.add_done_callback(self.callback_base)
        
        task11 = await self.board.stepper_is_running(motor, self.is_running_callback)

        await asyncio.gather(task1, task2, task3, task4, task5)
        
    async def retrieve_firmware_version(self, motor):
        print('Checking if board is running:')
        await self.board.stepper_is_running(motor, self.is_running_callback)
        time.sleep(.2)


        print('\nSetting current position to 216')
        board.stepper_set_current_position(motor, 216)
        board.stepper_get_current_position(motor, current_position_callback)

        time.sleep(.2)

        print('Setting move_to target to 300 (absolute motion.)')
        board.stepper_move_to(motor, 300)
        board.stepper_get_target_position(motor, target_position_callback)
        time.sleep(.2)
        board.stepper_get_distance_to_go(motor, distance_to_go_callback)
        time.sleep(.2)

        print('Setting move_to target to 300 (relative motion.)')
        board.stepper_move(motor, 300)
        board.stepper_get_target_position(motor, target_position_callback)
        time.sleep(.2)
        board.stepper_get_distance_to_go(motor, distance_to_go_callback)
        time.sleep(.2)

        print('Because we set all the parameters to move the motor, but have not started')
        print('it yet, IS_RUNNING reports that the motor is in motion, even though it is not')
        print('actually moving.')
        board.stepper_is_running(motor, is_running_callback)
        time.sleep(.2)
        
        msg = f'retrieve_firmware_version: {await self.board.get_firmware_version()}'
        return msg    
    
    async def retrieve_protocol_version(self):
        msg = f'Protocol Version: {await self.board.get_protocol_version()}'
        return msg
    
    async def retrieve_pymata_version(self):
        msg = f'Pymata Version: {await self.board.get_pymata_version()}'
        return msg
    
    async def retrieve_analog_map(self):
        msg = f'analog map: {await self.board.get_analog_map()}'
        return msg
    
    def format_capability_report(self, data):
        my_list = []
        pin_modes = {0: 'Digital_Input', 1: 'Digital_Output',
                    2: 'Analog_Input', 3: 'PWM', 4: 'Servo',
                    6: 'I2C', 8: 'Stepper',
                    11: 'Digital_Input_Pullup', 12: 'HC-SR04_Sonar', 13: 'Tone',
                    15: 'DHT'}
        x = 0
        pin = 0

        #print('\nCapability Report')
        my_list.append('\nCapability Report\n')
        #print('-----------------\n')
        my_list.append('-----------------\n')
        while x < len(data):
            # get index of next end marker
            #print('{} {}{}'.format('Pin', str(pin), ':'))
            my_list.append('\n{} {}{}'.format('Pin', str(pin), ':'))
            while data[x] != 127:
                mode_str = ""
                pin_mode = pin_modes.get(data[x])
                mode_str += str(pin_mode)
                x += 1
                bits = data[x]
                #print('{:>5}{}{} {}'.format('  ', mode_str, ':', bits))
                my_list.append('\n{:>5}{}{} {}'.format('  ', mode_str, ':', bits))
                x += 1
            x += 1
            pin += 1
        return my_list

    async def retrieve_capability_report(self):
        report = await self.board.get_capability_report()
        return " ".join(self.format_capability_report(report))
    
    async def retrieve_pin_state(self):
        """
        Establish a pin as a PWM pin. Set its value
        to 127 and get the pin state. Then set the pin's
        value to zero and get the pin state again.
        :param my_board: pymata_aio instance
        :return: No values returned by results are printed to console
        """
        await self.board.set_pin_mode_pwm(9)
        await self.board.analog_write(9, 127)
        pin_state = await self.board.get_pin_state(9)
        print('You should see [9, 3, 127] and received: ', pin_state)
        await self.board.analog_write(9, 0)
        pin_state = await self.board.get_pin_state(9)
        print('You should see [9, 3, 0]   and received: ', pin_state)
        return 'finished retrieve_pin_state'
    
    async def retrieve_info1(self):
        await asyncio.gather(self.retrieve_protocol_version(), 
                             self.retrieve_pymata_version(), 
                             self.retrieve_analog_map(),
                             self.retrieve_capability_report(),
                             self.retrieve_firmware_version())
    
    def callback1(self):
        print("Callback result:")

    def callback_details(self, context):
        print("Task completion received...")
        print("Name of the task:%s"%context.get_name())
        print("Wrapped coroutine object:%s"%context.get_coro())
        print("Task is done:%s"%context.done())
        print("Task has been cancelled:%s"%context.cancelled())
        print("Task result:%s"%context.result())
        print(type(context))
        print(context)

    def callback_base(self, context):
        if self.qWidget == None:
            print("widget is None")
            print("Task result:%s"%context.result())
        else:
            self.qWidget.append(context.result())
            self.qWidget.append("\n")

    async def retrieve_info(self, qWidget):
        self.qWidget = qWidget
        task1 = asyncio.ensure_future(self.retrieve_firmware_version())
        task2 = asyncio.ensure_future(self.retrieve_protocol_version())
        task3 = asyncio.ensure_future(self.retrieve_pymata_version())
        task4 = asyncio.ensure_future(self.retrieve_analog_map())
        task5 = asyncio.ensure_future(self.retrieve_capability_report())

        task1.add_done_callback(self.callback_base)
        task2.add_done_callback(self.callback_base)
        task3.add_done_callback(self.callback_base)
        task4.add_done_callback(self.callback_base)
        task5.add_done_callback(self.callback_base)
        
        task11 = await self.board.stepper_is_running(motor, self.is_running_callback)

        await asyncio.gather(task1, task2, task3, task4, task5)

