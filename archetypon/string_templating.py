# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/06_string_templating.ipynb.

# %% auto 0
__all__ = ['get_formatters_from_string', 'string_to_dict', 'StringTemplate']

# %% ../nbs/06_string_templating.ipynb 2
from archetypon.base_model import BaseModel
from pydantic import root_validator,validator
from typing import *
import string
import re

# %% ../nbs/06_string_templating.ipynb 3
def get_formatters_from_string(input_string:str)->List[str]:
    if input_string:
        keys = [tup[1] for tup in string.Formatter().parse(input_string) if tup[1] is not None]
        if len(keys)>0:
            return keys
        else:
            return {}

# %% ../nbs/06_string_templating.ipynb 5
def string_to_dict(string, pattern):
    regex = re.sub(r'{(.+?)}', r'(?P<_\1>.+)', pattern)
    values = list(re.search(regex, string).groups())
    keys = re.findall(r'{(.+?)}', pattern)
    _dict = dict(zip(keys, values))
    return _dict

# %% ../nbs/06_string_templating.ipynb 7
class StringTemplate(BaseModel):
    """String Template Model. 
    
    Define the class with a template and fields, and it can parse a string that matches the template into the attributes of the model
    or accept the attributes and create the string. 
    
    Useful for path operations and partitions. 
    """
    string: Optional[str]=None
    template: str
    
    @classmethod
    def parse_string(cls,string):
        string_format = cls.__fields__['template'].default
        values = string_to_dict(string,string_format)
        return cls(**values)
    
    @validator('template',always=True)
    def validate_template(cls,v):
        template_fields = get_formatters_from_string(v)
        fields = [x for x in cls.__fields__.keys() if x not in ('template','string')]
        assert template_fields == fields,(template_fields,fields)
        return v
    
    @root_validator(skip_on_failure=True)
    def format_template(cls,values):

        values['string'] = values['template'].format(**values)

        return values
    
    def __init__(
        self,
        string=None, # positional only
        /,
        **kwargs
    ):
        if string: 
            obj = self.parse_string(string)
            super().__init__(**obj.dict())
        else:
            super().__init__(**kwargs)
