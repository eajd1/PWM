import keyboard
from msvcrt import getch

class Edit:

    text = []
    position = 0
    editing = True
    prev = 0
    typing = False

    def __init__(self, text : str):
        self.text = text.splitlines()

    def println(self):
        print(' ' * len(self.text[self.prev]), end = '\r')
        print(self.text[self.position], end = '\r')

    def printHelp(self):
        print('')
        print("Controls:")
        print("Up/Down Arrows to navigate")
        print("Esc to exit")
        print("Enter/Return for new line")
        print("Backspace to edit line")
        print('')

    def edit_mode(self):
        self.printHelp()

        keyboard.on_press_key("esc", self.stop)
        keyboard.on_press_key("up_arrow", self.up)
        keyboard.on_press_key("down_arrow", self.down)
        keyboard.on_press_key("enter", self.addLine)
        keyboard.on_press_key("backspace", self.type)

        self.println()
        while(self.editing):
            if (self.typing):
                print(self.text[self.position])
                self.text[self.position] = input("Enter text to replace line above: ")
                self.typing = False
                self.println()

            getch()
            continue

    def stop(self, event):
        self.editing = False

    def up(self, event):
        self.prev = self.position
        self.position = self.position - 1
        if (self.position < 0):
            self.position = len(self.text) - 1

        self.println()

    def down(self, event):
        self.prev = self.position
        self.position = self.position + 1
        if (self.position >= len(self.text)):
            self.position = 0
        
        self.println()

    def addLine(self, event):
        if (self.typing): # Dont add a line while the user pressed enter to submit text
            return
        
        new_pos = self.position + 1
        if (new_pos < len(self.text)):
            self.text.insert(new_pos, '')
        else:
            self.text.append('')
        
        self.down(None)

    def type(self, event):
        self.typing = True

    def get_text(self) -> str:
        return '\n'.join(self.text)
    

# test = Edit("""0
# 1
# 2
# 3
# 4
# 5
# 6
# 7
# 8
# 9""")
# test.edit_mode()