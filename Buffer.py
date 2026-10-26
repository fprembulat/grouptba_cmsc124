# LOADS THE LOL CODE

class Buffer:
    def load_buffer(self):
        with open('program.lol', 'r', encoding='utf-8') as file:
            code = file.read()
        yield code
