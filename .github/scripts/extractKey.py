import re
import sys

VAR_REGEX = re.compile(r"\w+ = (\w+)")
chunked = lambda list, count: [list[i:i + count] for i in range(0, len(list), count)]

def toInt(num: str) -> int:
    if num.startswith("0x"):
        return int(num, 16)
    return int(num)

def getPairs(file: str) -> list[list[int]]:
    with open(file, "r+", encoding="utf-8") as script:
        scriptText = script.read()
        switchIndex = scriptText.rindex("switch")
        breakIndex = scriptText.index(" = partKey")
        switchCode = scriptText[switchIndex:breakIndex]
        indexes = []
        for variable in VAR_REGEX.findall(switchCode):
            regex = re.compile(rf" {variable} = (\w+)[,|;|\n]")
            match = regex.search(scriptText)
            if match is not None:
                indexes.append(toInt(match.group(1)))
        return chunked(indexes, 2)

if len(sys.argv) == 3:
    input = sys.argv[1]
    output = sys.argv[2]
    with open(output, "w+", encoding="utf-8") as out:
        pairs = getPairs(input)
        out.write(str(pairs))
