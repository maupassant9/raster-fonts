import re

# only for width < 8
fontfile = "font-4x6"
FONT_WIDTH = 4
FONT_HEIGHT = 6

def isValidLine(str):
    regx = "[ |\t]*0x[0-9A-Fa-f]{2},[ |\t]*/\*[0-1 ]+\*/"
    match = re.search(regx,str)
    return match != None


def getNumber(str):
    regx = "0x[0-9A-Fa-f]{2}"
    match = re.search(regx, str)
    num = int(match.group(), 16)
    return num

def getByteIndex(idx):
    return int(idx % FONT_HEIGHT)

def getBitIndex(idx):
    font_max_width = 8
    return (font_max_width - 1 - int(idx / FONT_HEIGHT))

def convert(ls, width, height):
    templs = [0]*(width*height)
    #get all the number
    #invert width with height
    for i in range(0, width*height):
        val = ls[getByteIndex(i)]
        if (val & (1 << getBitIndex(i))) == 0:
            templs[i] = 0
        else:
            templs[i] = 1
    
    #convert the result to bytes
    cnter = 0
    result = []
    val = 0
    for bit in templs:
        if bit == 1: val += (1 << cnter)
        cnter += 1
        if cnter == 8:
            cnter = 0
            result.append("\t"+hex(val)+",")
            val = 0
    
    result.append("\n")
    return result


cnter = 0
nums2convert = []
convertedstr = []
with open(fontfile+".c", "r") as f:
    fcont = f.readlines()
    for lstr in fcont:
        if isValidLine(lstr):
            cnter += 1
            nums2convert.append(getNumber(lstr))
            if len(nums2convert) == FONT_HEIGHT:
                strs = convert(nums2convert, FONT_WIDTH, FONT_HEIGHT);
                convertedstr = convertedstr+strs
                nums2convert = []
        else:
            convertedstr.append(lstr);
            cnter = 0

#save converted data
with open(fontfile+"_conv.c", "w") as f:
    for lstr in convertedstr:
        f.writelines(lstr)

print("Write everything ok!")
