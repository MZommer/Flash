from BinaryHelper import BinaryReader, Endianess
from dataclasses import dataclass


def getString(reader):
    returnString = b""
    while (char := reader.read(1)) != b"\x00":
        returnString += char
    return returnString.decode()


class BadPackFile(Exception):
    pass


@dataclass(frozen=True)
class File:
    pointer: int
    length: int
    path: str


class Pack:
    def __init__(self, path):
        self.binaryreader = BinaryReader(path=path, endianess=Endianess.BIG)

        if self.binaryreader.read(4) != b"PACK":
            raise BadPackFile("File is not a pac file")

        if self.binaryreader.uint32() != 1:
            self.binaryreader.flip_endianess()

        fileCount = self.binaryreader.uint32()
        self.binaryreader.uint32()  # Unknown 0x00

        self.filelist = [File(self.binaryreader.uint32(), self.binaryreader.uint32(), getString(self.binaryreader))
                         for _ in range(fileCount)]

    def extractall(self, path=""):
        for file in self.filelist:
            self.binaryreader.seek(file.pointer)
            with open(f"{path}{'/' if not path.endswith('/') else ''}{file.path}", "wb") as f:
                f.write(self.binaryreader.read(file.length))

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.binaryreader.close()

    def __enter__(self):
        return self
