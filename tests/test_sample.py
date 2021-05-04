from mylibrary import lib


def test_empty():
    lib.Log.set_config_path('config.yaml')

    @lib.Log(lambda: 'NOOOOOOOOOOOOOOOOOOOOOOOOOOOO', profile='dev')
    def demo(secret: int) -> None:
        raise Exception("OLA BOLA!")

    print(demo(secret='Shhh'))


def test_params():
    lib.Log.set_config_path('config.yaml')

    @lib.Log(profile='dev')
    def demo1(secret: float = 'ok') -> str:
        return secret

    print(demo1(secret='Hacked'))
