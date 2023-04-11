from BinaryHelper import BinaryWriter, BinaryReader, Endianess


class Script:
    def __init__(self):
        self.endbeat: float = 0
        self.startbeat: float = 0
        self.delay: float = 1000
        self.showUi: float = 0
        self.pictos: list[dict] = []
        self.moves: list[list[dict]] = [[], []]

    
    def existPictoTime(self, time):
        for picto in self.pictos:
            if picto["startTime"] == time:
                return True
        return False

    @staticmethod
    def Deserialize(path=None, filestream=None):

        self = Script()
        binaryReader = BinaryReader(path=path, buffer=filestream, endianess=Endianess.BIG)
        _ = binaryReader.float32()  # always 600, maybe an identifier?
        self.endbeat = int(binaryReader.float32() * 1000)
        _ = binaryReader.float32()  # always 0?
        entryCount = int(binaryReader.float32())

        for _ in range(entryCount):
            __class = int(binaryReader.float32())
            if __class == 10:  # beat
                self._parseBeatSection(binaryReader)
            elif __class == 13:  # Virtual Start
                self._parseVirtualStart(binaryReader)
            elif __class in (21, 22):  # Picto
                self._parsePictoClip(binaryReader, __class)
            elif __class == 25:  # Move
               self._parseMoveClip(binaryReader)
            else:
                pass # print("Unknown class: ", __class)
        return self

    def _parseBeatSection(self, binaryReader):
        _ = binaryReader.float32()
        _ = binaryReader.float32()
        _ = binaryReader.float32()
        _ = binaryReader.float32()
        _ = binaryReader.float32()
        self.delay = int(binaryReader.float32() * 100)
    def _parseVirtualStart(self, binaryReader):
        _ = binaryReader.float32()
        _ = binaryReader.float32()
        self.startbeat = int(binaryReader.float32() * 100)
        self.showUi = int(binaryReader.float32() * 100)
        _ = binaryReader.float32()
    
    def _parsePictoClip(self, binaryReader, __class=21):
        startTime = int(binaryReader.float32() * 100)
        _ = int(binaryReader.float32())
        endTime = int(binaryReader.float32() * 100)
        _ = int(binaryReader.float32() * 100)
        name = str(int(binaryReader.float32()))
        if not self.existPictoTime(startTime):
            self.pictos.append({
                "startTime": startTime,
                "endTime": endTime,
                "name": name
            })
        binaryReader.seek(0x14, 1)
    
    def _parseMoveClip(self, binaryReader):
        startTime = int(binaryReader.float32() * 100)
        _ = int(binaryReader.float32())
        endTime = int(binaryReader.float32() * 100)
        binaryReader.seek(0xC, 1)
        name = str(int(binaryReader.float32()))
        coach = int(binaryReader.float32())
        self.moves[coach].append({
            "startTime": startTime,
            "endTime": endTime,
            "name": name
        })
        if not self.existPictoTime(startTime) and _ == 21:  # for 2 coaches songs, don't repeat the pictos
            self.pictos.append({
                "startTime": startTime,
                "endTime": endTime,
                "name": name
            })
        binaryReader.seek(0x3C, 1)

    def makeBlueStar(self, codename=""):
        codename = codename.lower()
        return {
            "beats": list(range(self.startbeat, self.endbeat, self.delay)),
            "pictos": [{
                "name": picto['name'],
                "time": picto["startTime"],
                "duration": picto["endTime"] - picto["startTime"],
            } for picto in self.pictos],
            "moves": [
                [{
                    "name": f"{codename}{'_' if codename else ''}{clip['name']}",
                    "time": clip["startTime"],
                    "duration": clip["endTime"] - clip["startTime"],
                } for clip in move] for move in self.moves]
        }
