# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/05_formatting.ipynb.

# %% auto 0
__all__ = ['format_factory', 'big_number', 'big_dollars', 'as_multiple', 'format_minutes', 'Formatter']

# %% ../nbs/05_formatting.ipynb 2
from typing import (
    Union,
    Callable,
    TypeVar,
    Literal,
    List
)
from archetypon.base_model import *
from pydantic import root_validator
from pydantic.color import Color
import math
from pandas import isnull
import pandas as pd
import datetime as dt

# %% ../nbs/05_formatting.ipynb 5
FormatterT = TypeVar("FormatterT",str,Callable)

# %% ../nbs/05_formatting.ipynb 6
def format_factory(
    string_or_callable:FormatterT,
    null_format:str = '',
    **kwargs
)->Callable:
    """
    Returns a function factory to format a given value. 
    """
    if callable(string_or_callable):
        def _formatter(val,*args):

            if val=='' or isnull(val):
                return null_format
            return string_or_callable(val,*args,**kwargs)
        
        return _formatter
    
    def _formatter(val):
        if val=='' or isnull(val):
            return null_format

        return string_or_callable.format(val)
    return _formatter

# %% ../nbs/05_formatting.ipynb 10
def big_number(num:float,decimal_places:int=2)->str:
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    # add more suffixes if you need them
    formatted = f'%.{decimal_places}f%s' % (num, ['', 'K', 'M', 'B', 'T', 'P'][magnitude])
    return formatted

# %% ../nbs/05_formatting.ipynb 11
def big_dollars(num:float,decimal_places:int=2)->str:
    formatted = big_number(num,decimal_places)
    return f"${formatted}"

# %% ../nbs/05_formatting.ipynb 12
def as_multiple(num:float)->str:
    if abs(num) < 0.005:
        return '-'
    else:
        return '{:.2f}x'.format(num)

# %% ../nbs/05_formatting.ipynb 14
def format_minutes(time:float)->str:
    """Takes in minutes as a float and converts to MM:SS"""
    if type(time)==dt.time:
        return time.strftime("%M:%S")
    minutes = math.floor(time)
    seconds = (time * 60) % 60
    return "%02d:%02d" % (minutes, seconds)

# %% ../nbs/05_formatting.ipynb 16
class Formatter():
    """
    A customizable object for applying string formats. 
    
    Any additional attributes passed during instantion must have a name ending in "_format". 
    Values can be either a formattable string (e.g. "{:.0f}") or a callable.  
    """
    def __init__(
        self,
        null_format: str = '',
        dollars_format: FormatterT = "${:,.0f}",
        percent_format: FormatterT = "{:.0%}",
        percent2dp_format: FormatterT = "{:.2%}",
        number_format: FormatterT = "{:,.0f}",
        small_number_format: FormatterT = "{:.2f}",
        big_number_format: FormatterT = big_number,
        big_dollars_format: FormatterT = big_dollars,
        multiple_format: FormatterT = as_multiple,
        minutes_format: FormatterT = format_minutes,
        **kwargs
    ):
        self.null_format = null_format
        self.dollars_format=dollars_format
        self.percent_format=percent_format
        self.percent2dp_format=percent2dp_format
        self.number_format=number_format
        self.small_number_format=small_number_format
        self.big_number_format=big_number_format
        self.big_dollars_format=big_dollars_format
        self.multiple_format = multiple_format
        self.minutes_format = minutes_format
        
        #add anything extra
        for k,v in kwargs.items():
            if not k.split('_')[-1]=='format':
                raise ValueError(f"Keyword arguments passed to the Formatter must end in '_format' ")
            setattr(self,k,v)
        
        # create methods from string_formats
        items = [(k,v) for k,v in self.__dict__.items()]
        for k,v in items:
            if not k.startswith('null'):
                method = '_'.join([x for x in k.split('_')][:-1]) # remove "_format" from the end of the attribute when setting the method
                if type(v)==tuple:
                    setattr(
                        self,
                        method,
                        format_factory(
                            v[0],
                            null_format = self.null_format,
                            **v[1]
                        )
                    )
                else:
                    setattr(
                        self,
                        method,
                        format_factory(v,null_format=self.null_format)
                    )
