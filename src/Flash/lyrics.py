from BinaryHelper import BinaryWriter, BinaryReader, Endianess


class LyricData:
    @staticmethod
    def Serialize(data, path=None, filestream=None):  # not tested
        def getEntryCount(_data):
            _entryCount = 0
            for entry in _data.values():
                _entryCount = max(entryCount, len(entry))
            return _entryCount

        binaryWriter = BinaryWriter(path=path, buffer=filestream, endianess=Endianess.BIG)
        entryCount = getEntryCount(data)
        binaryWriter.uint32(entryCount)

        if isinstance(data, list):
            for line in data:
                binaryWriter.ushort(len(line))
                binaryWriter.write(line.encode("utf-16-be"))
            return

        data = {
            "en": data.get("en", []),
            "fr": data.get("fr", []),
            "it": data.get("it", []),
            "de": data.get("de", []),
            "es": data.get("es", []),
            "la": data.get("la", []),
            "nl": data.get("nl", []),
            "da": data.get("da", []),
            "fi": data.get("fi", []),
            "no": data.get("no", []),
            "sv": data.get("sv", []),
            "pt": data.get("pt", []),
        }
        # To fill the missing data
        for loc in data.values():
            for arr in loc:
                if not arr:
                    arr = ["" for _ in range(entryCount)]
                for line in arr:
                    binaryWriter.ushort(len(line))
                    binaryWriter.write(line.encode("utf-16-be"))

    @staticmethod
    def Deserialize(path=None, filestream=None, legacy=False):
        getString = lambda reader: reader.read(reader.ushort() * 2).decode("utf-16-be", "backslashreplace")

        binaryReader = BinaryReader(path=path, buffer=filestream, endianess=Endianess.BIG)

        entryCount = binaryReader.uint32()
        if legacy:  # older versions of the engine have the data in separate files
            return [getString(binaryReader) for _ in range(entryCount)]

        return {
            "en": [getString(binaryReader) for _ in range(entryCount)],  # English
            "fr": [getString(binaryReader) for _ in range(entryCount)],  # French
            "it": [getString(binaryReader) for _ in range(entryCount)],  # Italian
            "de": [getString(binaryReader) for _ in range(entryCount)],  # German
            "es": [getString(binaryReader) for _ in range(entryCount)],  # Spain Spanish
            "la": [getString(binaryReader) for _ in range(entryCount)],  # Latam Spanish
            "nl": [getString(binaryReader) for _ in range(entryCount)],  # Dutch
            "da": [getString(binaryReader) for _ in range(entryCount)],  # Danish
            "fi": [getString(binaryReader) for _ in range(entryCount)],  # Finnish
            "no": [getString(binaryReader) for _ in range(entryCount)],  # Norwegian
            "sv": [getString(binaryReader) for _ in range(entryCount)],  # Swedish
            "pt": [getString(binaryReader) for _ in range(entryCount)],  # Portuguese
            "pl": [getString(binaryReader) for _ in range(entryCount)],  # Polish
            # ? in the binary claims here goes polish? untested
        }


class LyricScript:
    def __init__(self):
        self.endBeat = 0
        self.clips = []

    def Serialize(self, path=None, filestream=None): # Not tested
        binaryWriter = BinaryWriter(path=path, buffer=filestream, endianess=Endianess.BIG)

        binaryWriter.float32(len(self.clips))
        binaryWriter.float32(self.endBeat)
        binaryWriter.float32(0)
        for clip in self.clips:
            binaryWriter.float32(clip["id"])
            binaryWriter.float32(clip["duration"] / 100)
            binaryWriter.float32(clip["startTime"] / 100)
            binaryWriter.float32(clip["sing"])

    @staticmethod
    def Deserialize(path=None, filestream=None):
        self = LyricScript()
        binaryReader = BinaryReader(path=path, buffer=filestream, endianess=Endianess.BIG)

        entryCount = int(binaryReader.float32())
        self.endBeat = binaryReader.float32()  # Seconds
        karaoke = binaryReader.float32()

        for _ in range(entryCount):
            self.clips.append({
                "id": int(binaryReader.float32()),
                "duration": round(binaryReader.float32() * 100),
                "startTime": round(binaryReader.float32() * 100),
                "sing": int(binaryReader.float32())
            })

        return self

    def makeBlueStar(self, data, lang="en"):
        clips = []
        if isinstance(data, dict):
            data = data[lang]
        for clip in self.clips:
            try:
                text = data[clip["id"] + 1]
            except IndexError:
                text = "\t"
            clips.append({
                "time": clip["startTime"],
                "duration": clip["duration"],
                "text": text,
                "isLineEnding": 1
            })
        for index, clip in enumerate(clips):
            if index >= len(clips) - 1:
                continue
            next_clip = clips[index + 1]
            if clip['time'] + clip['duration'] > next_clip['time']:
                clip['duration'] -= clip['time'] + clip['duration'] - next_clip['time'] + 1
        return clips
