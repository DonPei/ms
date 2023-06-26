
import time
import asyncio
from telemetrix_motor_base import MotorBase


class Motor(MotorBase):

    def __init__(self, board):
        self.board = board