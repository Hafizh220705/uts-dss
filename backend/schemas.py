from pydantic import BaseModel
from typing import List, Literal, Dict, Any

class Criterion(BaseModel):
    Kriteria: str
    Bobot: float
    Tipe: Literal['Benefit', 'Cost']

class DSSPayload(BaseModel):
    method: Literal['saw', 'wp', 'ahp', 'topsis']
    criteria: List[Criterion]
    alternatives: List[Dict[str, Any]]

class AHPPayload(BaseModel):
    comparison_matrix: List[List[float]]