"""Esquemas de Pydantic para validación y respuesta de la API de actividades."""

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class PreguntaEntrada(BaseModel):
    """Datos de entrada para crear o reemplazar una pregunta."""

    enunciado: str = Field(min_length=1)
    opciones: list[str] = Field(min_length=3, max_length=4)
    respuesta_correcta: str

    @field_validator("enunciado")
    @classmethod
    def validar_enunciado_no_vacio(cls, valor: str) -> str:
        """Verifica que el enunciado no esté compuesto solo por espacios."""
        texto = valor.strip()
        if not texto:
            raise ValueError("El enunciado de la pregunta no puede estar vacío.")
        return texto

    @model_validator(mode="after")
    def validar_respuesta_en_opciones(self) -> "PreguntaEntrada":
        """Comprueba que la respuesta correcta pertenezca a la lista de opciones."""
        if self.respuesta_correcta not in self.opciones:
            raise ValueError("La respuesta correcta debe estar entre las opciones.")
        return self


class PreguntaSalida(BaseModel):
    """Representación de una pregunta devuelta por la API."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    enunciado: str
    opciones: list[str]
    respuesta_correcta: str


class ActividadEntrada(BaseModel):
    """Datos de entrada para crear o actualizar una actividad con sus preguntas."""

    titulo: str = Field(min_length=1)
    descripcion: str = ""
    orden: int = Field(ge=1)
    preguntas: list[PreguntaEntrada] = Field(min_length=5)

    @field_validator("titulo")
    @classmethod
    def validar_titulo_no_vacio(cls, valor: str) -> str:
        """Verifica que el título no esté compuesto solo por espacios."""
        texto = valor.strip()
        if not texto:
            raise ValueError("El título de la actividad no puede estar vacío.")
        return texto


class ActividadSalida(BaseModel):
    """Representación de una actividad con sus preguntas devuelta por la API."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    titulo: str
    descripcion: str
    orden: int
    preguntas: list[PreguntaSalida]
