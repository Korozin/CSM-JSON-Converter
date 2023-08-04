# CSM-JSON-Converter

This script exists because of [@Love🥀](https://www.youtube.com/channel/UC_IfrpabdJiDEiiSHbaPqvw), because they had old CSM Files that they wanted to view in Blockbench again.

### Proper CSM Format
So CSMs are super weird. There's multiple formats of them, and most of them usually work across all versions of PCK Studio. But there can also be several variations of said formats, so it's really hard to make a standard norm, so I'm using a pretty broad format.

```CSM
PckStudio.generateModel+ModelPart
BODY
PckStudio.generateModel+ModelPart
-2
-3
2
1
1
1
0
0
```

to go into more detail, the `PckStudio.generateModel+ModelPart` text doesn't even actually matter. In fact the original CSM I was sent to test this on said `hane` instead, so I'm assuming this text is just acting as a seperator, so the only parts that actually matter are the Bone Types, and Number Values.

To give more context as to what these values actually mean I'll show the following.

```CSM
PckStudio.generateModel+ModelPart <- Separator Text
BODY <- Bone Type
PckStudio.generateModel+ModelPart <- Separator Text
-2 <- X Pos Coord
-3 <- Y Pos Coord
2 <- Z Pos Coord
1 <- X Size Coord
1 <- Y Size Coord
1 <- Z Size Coord
0 < X UV Coord
0 <- Y UV Coord
```

So the CSM could also be something like this

```csm
NonsenseText
ARM0
NonsenseText
-3
-4
2
1
1
1
0
0
```

and it would still get properly converterted, and most likely read in PCK Studio as well.

Basically all the program is doing is every 10 lines or so, it will iterate an entry using an incremented value, and applies those values to a list like so.

```python
['BODY', 'PckStudio.generateModel+ModelPart', '-2', '-3', '2', '1', '1', '1', '0', '0']
```

It reads the bone typing from the first index in the entry, and matches it against a dictionary for proper naming. Then it skips the entry text, and applies the numbers in the correct order to the cube's JSON data, and then it uses the next separator after that to signal that it's time to increment again to a new entry, then rinse and repeat until there's nothing left in the file to convert.

If there are any errors in the conversion process, the program will notify you and then proceed to exit.

If you'd like to see examples of both Input and Output, then you can find them [here](https://github.com/Korozin/CSM-JSON-Converter/tree/main/Example-Output).
