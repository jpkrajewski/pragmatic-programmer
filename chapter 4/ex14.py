"""Design kitchen blender. It will be a web wersion of a IoT blender,
but for now we only need interface. Blender has a work speed setting
(0 means off, 1-10 means speed of blending). Blender can't be used
when it's empty and a speed can be changed one step at a time.
Here are the methods:

int get_speed() - returns current speed
void set_speed(int speed) - sets speed to given value
boolean is_full() - returns true if blender is full
void fill() - fills blender
void empty() - empties blender

Use Design by Contract paradigmat to specify the behavior of the blender.
"""


def require(lambda_expression, assertion_error_message):
    def decorator(fun):
        def wrapper(*args, **kwargs):
            assert lambda_expression(*args), assertion_error_message
            return fun(*args, **kwargs)

        return wrapper

    return decorator


def ensure(lambda_expression, assertion_error_message):
    def decorator(fun):
        def wrapper(*args, **kwargs):
            print(*args)
            ret = fun(*args, **kwargs)
            assert lambda_expression(*args), assertion_error_message
            return ret

        return wrapper

    return decorator


def invariant_dec(obj, lambda_expression, assertion_error_message):
    def decorator(fun):
        def wrapper(*args, **kwargs):
            ret = fun(*args, **kwargs)
            assert lambda_expression(obj), assertion_error_message
            return ret

        return wrapper

    return decorator


def invariant(lambda_expression, assertion_error_message, cls=None):
    if cls is None:
        return lambda cls: invariant(lambda_expression, assertion_error_message, cls)

    class Decoratable(cls):
        def __init__(self, *args, **kargs):
            super().__init__(*args, **kargs)

        def __getattribute__(self, item):
            value = object.__getattribute__(self, item)
            if callable(value):
                return invariant_dec(self, lambda_expression, assertion_error_message)(
                    value
                )
            return value

    return Decoratable


@invariant(
    lambda self: 0 <= self.speed <= 10, "Speed can't be lower than 0 and higher than 10"
)
class Blender:

    def __init__(self):
        self.speed = 0
        self.is_full = False

    def get_speed(self) -> int:
        return self.speed

    @require(
        lambda obj, speed: abs(obj.get_speed() - speed) == 1,
        "Speed can be changed one step at a time",
    )
    @require(
        lambda obj, speed: 0 <= speed <= 10,
        "Speed can't be lower than 0 and higher than 10",
    )
    @ensure(lambda obj, speed: obj.speed == speed, "Speed not set correctly")
    def set_speed(self, speed: int) -> None:
        self.speed = speed

    def is_full(self) -> bool:
        return self.is_full

    @require(lambda obj: obj.is_full == False, "Blender has to be empty")
    def fill(self) -> None:
        self.is_full = True

    @require(lambda obj: obj.is_full == True, "Blender has to be full to be empitied")
    def empty(self) -> None:
        self.is_full = False
