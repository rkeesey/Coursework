class Note:

    def __init__(self, p="a file path"):
        self.p = p

    def __str__(self):
        return f"{self.p}"

    def save_note(self, usr_inpt=""):
        # create path obj to notes storage file
        p = self.p

        # check if storage file exists, if not create it.
        if not p.exists():
            p.touch(exist_ok=True)
        
        # open and write user note to file
        f = p.open('a')
        f.write(str(usr_inpt) + '\n')
        f.close()
    
    def read_notes(self):
        p = self.p
        
        # check if storage file exists, if not return.
        if not p.exists():
            return
        
        # open and write user note to file
        f = p.open()

        lines = []
        for line in f:
            line_str = line.replace('\n', '')
            lines.append(line_str)
        f.close()

        return lines
    
    def remove_note(self, remove_id=''):
        p = self.p

        # check if storage file exists, if not return.
        if not p.exists():
            return
        
        lines = []
        # print each note with an id and store each line in a list
        f = p.open()
        for line in f:
            lines.append(line)
        f.close()

        # open as write to overwrite existing notes, add notes back while skipping user selection 
        f = p.open('w')
        removed_note = ""

        id = 0
        for line in lines:
            if id == int(remove_id):
                removed_note = line
            else:
                f.write(line)
            id = id+1
        f.close()

        return removed_note