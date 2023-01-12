# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/02_base_model.ipynb.

# %% auto 0
__all__ = ['BaseModel', 'GenericModel']

# %% ../nbs/02_base_model.ipynb 1
from typing import *
from pydantic import BaseModel as PydanticBaseModel
from pydantic.generics import GenericModel as PydanticGenericModel
import json
from json2html import json2html
from IPython.display import HTML,JSON
import inspect
import yaml
from archetypon.delegates import delegates

# %% ../nbs/02_base_model.ipynb 3
def dict_to_yaml(data: dict) -> str:
    # convert the dictionary to a yaml string
    yaml_str = yaml.dump(data,sort_keys = False)

    return yaml_str

# %% ../nbs/02_base_model.ipynb 4
def pydantic_to_dbt(model: Type[PydanticBaseModel]) -> dict:
    # convert the model to a dictionary
    model_dict = model.schema()

    # create a dictionary for the dbt model
    dbt_model = {
        "version": 2,
        "name": model.__name__.lower(),  # use the model's class name as the table name
        "description":model_dict.get('description'),
        "columns": []
    }
    dbt_model = {k:v for k,v in dbt_model.items() if v or k=='columns'}

    # add the columns from the pydantic model to the dbt model
    for field_name, field in model_dict["properties"].items():

        column = {
            "name": field_name,
            "description":field.get('description'),
            "type": field["type"],
        }
        dbt_model["columns"].append({k:v for k,v in column.items() if v})
    return dbt_model


# %% ../nbs/02_base_model.ipynb 5
class Base():
    """
    Custom implementation of Pydantic's Base Model.

    Includes `_repr_json_` and `_repr_html_` methods for nice displays in Jupyter Lab and Jupyter Notebook, respectively.

    json_encoders are set in the Config class.
    """
    @delegates(PydanticBaseModel.json)
    def display_json(self,**kwargs):
        """Helper function to display json in jupyter lab using kwargs passed to pydantic's .json() method"""
        return JSON(
            json.loads(self.json(**kwargs))
        )

    @classmethod
    @delegates(PydanticBaseModel.schema_json)
    def display_schema_json(cls,**kwargs):
        """Helper function to display schema json in jupyter lab using kwargs passed to pydantic's .json() method"""
        return JSON(
            json.loads(cls.schema_json(**kwargs))
        )

    @classmethod
    @delegates(PydanticBaseModel.schema_json)
    def schema_html(cls,**kwargs):
        return HTML(
            json2html.convert(cls.schema_json(**kwargs))
        )

    @classmethod
    @delegates(PydanticBaseModel.schema)
    def schema_yml(cls,**kwargs):
        dbt = pydantic_to_dbt(cls)

        return dict_to_yaml(dbt)

    def _repr_html_(self):
        try:
            return json2html.convert(
                self.json(**self.Display.html)
            )
        except:
            pass

    def _repr_json_(self):
        try:
            return json.loads(
                self.json(**self.Display.json)
            )
        except Exception as e:
            print(e)
            pass

    class Display:
        json = {}
        html = {}
        

# %% ../nbs/02_base_model.ipynb 6
class BaseModel(PydanticBaseModel,Base):
    pass

# %% ../nbs/02_base_model.ipynb 7
class GenericModel(PydanticGenericModel,Base):
    pass