from BinaryHelper import BinaryWriter, BinaryReader


class Script:
    def __init__(self):
        self.pictos = []
        self.moves = [[], []]

    @staticmethod
    def Deserialize(path=None, filestream=None):
        def existPictoTime(time):
            for picto in self.pictos:
                if picto["startTime"] == time:
                    return True
            return False

        self = Script()
        if path:
            filestream = open(path, "rb")
        binaryReader = BinaryReader("BIG", filestream)
        _ = binaryReader.float32()
        self.songLength = int(binaryReader.float32() * 1000)
        _ = binaryReader.float32()
        entryCount = int(binaryReader.float32())

        for _ in range(entryCount):
            __class = int(binaryReader.float32())

            if __class == 10:  # beat section?
                _ = binaryReader.float32()
                _ = binaryReader.float32()
                self.beatOffset = int(binaryReader.float32() * 100)
                _ = binaryReader.float32()
                _ = binaryReader.float32()
                self.delay = int(binaryReader.float32() * 100)
            elif __class in (21, 22):  # Picto
                startTime = int(binaryReader.float32() * 100)
                _ = int(binaryReader.float32() * 100)
                endTime = int(binaryReader.float32() * 100)
                _ = int(binaryReader.float32() * 100)
                name = str(int(binaryReader.float32()))
                if not existPictoTime(startTime):
                    self.pictos.append({
                        "startTime": startTime,
                        "endTime": endTime,
                        "name": name
                    })
                binaryReader.seek(0x14, 1)
            elif __class == 25:  # Move
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
                if not existPictoTime(startTime) and _ == 21:  # for 2 coaches songs, don't repeat the pictos
                    self.pictos.append({
                        "startTime": startTime,
                        "endTime": endTime,
                        "name": name
                    })
                binaryReader.seek(0x3C, 1)
        return self

    def makeBlueStar(self, codename=""):
        codename = codename.lower()
        return {
            "beats": list(range(self.beatOffset, self.songLength, self.delay)),
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
