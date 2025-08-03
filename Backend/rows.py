from typing import Annotated, Optional
from enum import Enum
from fastapi import FastAPI, Query, HTTPException, Path, Depends
from pydantic import BaseModel, Field, AfterValidator

import pandas as pd

class Row(BaseModel):
    box_score: pd.Series
    

