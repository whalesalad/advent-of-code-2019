commands = {
    '1': 'add',
    '2': 'multiply',
    '99': 'exit'
}

ADD, MULTIPLY = [1, 2]


class TerminateException(Exception):
    pass


def do_add(state, a, b, output):
    state[state[output]] = state[state[a]] + state[state[b]]
    return state


def do_multiply(state, a, b, output):
    state[state[output]] = state[state[a]] * state[state[b]]
    return state


class Computer(object):
    def __init__(self, boot):
        self.state = [int(i) for i in boot.strip().split(',')]
        self.current_position = 0

    def get(self, idx):
        return self.state[idx]

    @property
    def current(self):
        return self.get(self.current_position)

    def goto(self, new_position):
        self.current_position = new_position

    def read(self):
        value = self.current

        print(f'read, value:{value}, state:{self.state}')

        if value == ADD:
            # read ahead 2 positions for args
            self.state = do_add(
                state=self.state.copy(),
                a=self.current_position + 1,
                b=self.current_position + 2,
                output=self.current_position + 3
            )
            return self.goto(self.current_position + 4)

        if value == MULTIPLY:
            self.state = do_multiply(
                state=self.state.copy(),
                a=self.current_position + 1,
                b=self.current_position + 2,
                output=self.current_position + 3
            )
            return self.goto(self.current_position + 4)

        if value == 99:
            raise TerminateException()
            return

    def run(self):
        try:
            while True:
                self.read()

        except TerminateException as e:
            print('terminating')
            pass

        print('state', self.state)

        return self.state


def main(data):
    c = Computer(data)
    c.run()


if __name__ == '__main__':
    boot = '1,9,10,3,2,3,11,0,99,30,40,50'
    print(main(boot))
