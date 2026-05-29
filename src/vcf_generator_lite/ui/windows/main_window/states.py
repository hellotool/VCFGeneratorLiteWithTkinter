from enum import Enum, auto


class GenerationState(Enum):
    IDLE = auto()
    GENERATING = auto()
    STOPPING = auto()
