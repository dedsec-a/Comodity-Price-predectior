
import sys 
from my_logger import logging

def error_message_detail(error , error_message_details:sys):
    type,value,exc_tb = error_message_details.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    error_message = "Error Occured in Pyhton Script at [{0}] at line Number[{1}] Error Message [{2}]".format(
        file_name , exc_tb.tb_lineno , str(error)
    )

    return error_message


class CustomException(Exception):
    def __init__(self, error_message, error_message_details:sys):
        super().__init__(error_message)
        self.error_message = error_message_detail(error= error_message , error_message_details= error_message_details)

    def __str__(self):
        return self.error_message
    




        

