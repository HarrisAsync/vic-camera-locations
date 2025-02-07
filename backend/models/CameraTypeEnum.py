from enum import Enum
class CameraType(Enum):
    MOBILE=1
    PHONE=2
if __name__ == "__main__":
    print(CameraType(1).value)
    print(CameraType["MOBILE"].value)
    print(CameraType(2).name)
    print(CameraType["PHONE"].name)