import ctypes
# paste code here
#             |
#             V
code = """
typedef struct {
  WORD wYear;
  WORD wMonth;
  WORD wDayOfWeek;
  WORD wDay;
  WORD wHour;
  WORD wMinute;
  WORD wSecond;
  WORD wMilliseconds;
} _SYSTEMTIME, SYSTEMTIME, PSYSTEMTIME, LPSYSTEMTIME;
"""
def listToStr(listArray):
    d = ""
    for it in listArray: d += it
    return d
def listToLineStr(listArray):
    d = ""
    for it in listArray: d += it + '\n'
    return d[:-2]


if code.splitlines()[1] == "typedef struct {":
    args = code.splitlines()[len(code.splitlines())-1].replace('} ','').replace('*','').replace(';','').split(', ')
    firstArg = args[0]
    args.remove(firstArg)
    codedx = code.splitlines()[2:-1]
    codedx.insert(0, 'typedef struct ' + firstArg + ' {')
    argFixed = [arg + ', ' for arg in args]
    codedx.append('} ' + listToStr(argFixed)[:-2] + ';')
    code = '\n' + listToLineStr(codedx) + '\n'
   #  print(code)
    
code = code.replace('typedef struct', 'class').replace('  ', '        ').replace(' {','(ctypes.Structure):\n    _fields_ = [').replace('}','    ]\n')
codeLines = code.splitlines()
for i in range(len(codeLines)):
    line = codeLines[i]
    if line.startswith('        '):
        li = line.replace('        ','').replace(';','').split()[::-1]
        if not codeLines[i+1].startswith('    ]'): cm = ','
        else: cm = ''
        codeLines[i] = '        (\'' + li[0] + '\', ' + li[1] + ')' + cm
v = ""
cLast = codeLines[len(codeLines)-1].replace('*','').replace(';','').split(', ')
ls = code.splitlines()[1].replace('(ctypes.Structure):','').replace('class ', '')
cLast[0] = cLast[0][1:]
for i in range(len(cLast)):
    cLast[i] = cLast[i] + ' = ' + ls + '\n'
for i in range(len(codeLines)-1):
    v += codeLines[i] + '\n'
for i in range(len(cLast)):
    v += cLast[i]
print(v[1:])
