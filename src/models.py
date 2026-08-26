from pydantic import BaseModel, Field

class CellStructure(BaseModel):
    cell_type: str = Field(
        description="Tipo de celda: 'markdown' para explicaciones teóricas o 'code' para código ejecutable."
    )
    content: str = Field(
        description="El texto en formato Markdown o las líneas de código Python correspondientes."
    )

class NotebookFullResponse(BaseModel):
    summary: str = Field(description="Breve resumen de los cambios o contenido creado.")
    notebook_cells: list[CellStructure] = Field(
        description="Lista completa de celdas que compondrán el cuaderno final en orden lógico."
    )
