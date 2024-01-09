__all__ = ["CartesianVector"]


@dataclass
class CartesianVector:  # defined elsewhere?
    x: float
    y: float
    z: float


@dataclass
class MagneticField:
    Bx: float
    By: float
    Bz: float


class VectorObservation:
    def __init__(self, x, y, z, Bx, By, Bz):
        self.x = x
        self.y = y
        self.z = z
        self.Bx = Bx
        self.By = By
        self.Bz = Bz



def get_mesocenter(positions: Iterable[CartesianVector]):



def get_volumetric_tensor(positions: list[Vector]):
