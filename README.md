## Flash Engine
Just Dance Kids games uses Flash Player,
this games uses bundles in the Pack format (.pac)
For the Wii versions, the engine uses `.arc` files (commonly used in nintendo games).
You can extract this `arc` files with [BrawlCreate](https://github.com/soopercool101/BrawlCrate)

The module has a Pack extractor

Example usage:
```python
from PAC import Pack

with Pack("dance_script.pac") as pac:
    pac.extractall("/output")
```

Inside this 'bundles' there are mutiple files, `binaries`, `swf`, `lmc` and `gesture` files
The swf files are a common flash type. This files can be explored with [JPEXS](https://github.com/jindrapetrik/jpexs-decompiler)

The binaries can be parsed with the Flash module.

The lyrics have 2 files, the `script` and the `data`.
The script having the times and the data having the actual lyrics.
This because the engine supports diferent languages.
This datas are separated into diferent files, but newer versions of the engine have them all packed into a single file.
This files can be deserialized with the `LyricDeserializer.py` file. Lyrics also have support for `serialization`.

Then the `script` is what has the movement and pictogram times.
