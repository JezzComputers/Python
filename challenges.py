from math import pi

# Python Challenge 1: Check if a List is Sorted
def is_sorted(lst) -> bool:
    asc, desc = True, True
    for i in range(len(lst) - 1):
        if lst[i] > lst[i + 1]:
            asc = False
    for i in range(len(lst) - 1):
        if lst[i] < lst[i + 1]:
            desc = False
    return asc or desc

# Python Challenge 2: Convert Binary Numbers to Decimal
def binary2decimal(binary:int) -> int:
    binarylist:list = [int(digit) for digit in str(binary)]
    binarylist.reverse()
    listlen = len(binarylist)
    out:int = 0
    for i in range (listlen):
        out += 2**i * binarylist[i]
    return out

# Python Challenge 3: Loves Me, Loves Me Not
def lovemeLovemenot(n:int) -> list[str]:
    output:list = []
    for i in range (n):
        if n%2 == 0:
            output.append("Loves Me")
        else:
            output.append("Loves Me Not")
    return output

# Python Challenge 4: The Tribonacci Sequence Challenge
def find_nth(nth:int) -> list:
    sequence:list = [0,1,1]
    x:int = 0
    i:int = 0
    for i in range (nth):
        x += (sequence[i] + sequence[i+1] + sequence[i+2])
        sequence.append(x)
        x=0
        i+=3
    return sequence[i-3]

# Python Challenge 5: Hide a Credit Card Number
def hidecrednum(id:int) -> str:
    idlist:list = [int(digit) for digit in str(id)]
    outlist:list = []
    for i in range (0,len(idlist)-3):
        outlist.append(idlist[i])
    for o in range (i, i+3):
        outlist.append("*")
    strings = ''.join(str(x) for x in outlist)
    return strings

# Python Challenge 6: SpongeCase
def spongecase(text:str) -> str:
    outstring:list = []
    for i in range (len(text)):
        if i%2 == 0:
            outstring.append(text[i].upper())
        else:
            outstring.append(text[i].lower())
    output = ''.join(str(x) for x in outstring)
    return output

# Python Challenge 7: Caesar Encryption
def caesarEncryption(text:str, shift:int) -> str:
    result = ""
    for char in text:
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            shifted = (ord(char) - start + shift) % 26 + start
            result += chr(shifted)
        else:
            result += char
    return result

# Python Challenge 8: Is the Product Divisible by the Sum?
def divBySum(values:list) -> bool:
    product:int = 1
    sum:int = 0
    for i in range (len(values)):
        product *= values[i]
        sum += values[i]
    if product % sum == 0:
        return True
    else:
        return False

# Convert Radians To Degrees
def radToDeg(radians:int) -> float:
    degrees = radians*(180/pi)
    return degrees

# Sort a list
def sortList(mylist:list[int], direction:str) -> list[int]:
    if direction == "asc":
        mylist = sorted(mylist)
    elif direction == "desc":
        mylist = sorted(mylist, reverse=True)
    elif direction == "none":
        pass
    else:
        raise ValueError(f"error: value can't be {direction} it can only be asc, desc or none")
    return mylist

# Count the vowels in a string
def vowelsInString(inputString:str) -> int:
    vowelCount:int = 0
    vowels:set[str] = {"a", "e", "i", "o", "u"}
    for char in inputString.lower():
        if char in vowels:
            vowelCount += 1
    return vowelCount

if __name__ == "__main__":
    print(vowelsInString("aeutioo"))
