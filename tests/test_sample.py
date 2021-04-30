from mylibrary import sample


def test_empty():
    @sample.log()
    def demo(secret):
        print(secret)

    demo('Shhh')


def test_params():
    @sample.log('I am in!', 'Bye!')
    def demo(secret):
        print(secret)

    demo('Hacked')
