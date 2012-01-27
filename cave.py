import random

# initializes/returns a rectangular list of dimensions x,y full of 0
def initmap(x,y):
    _map = [[0]*x for i in range(y)]
    return _map

# print a rectangular list all pretty like
def printmap(m):
    s = ''
    for i in m:
        print s
        s=''
        for j in i:
            s=s+str(j)
    print s
    
# fill the map with noise
def seedmap(m):
    ybound = len(m)-1
    xbound = len(m[1])-1
    
    for i in range(len(m)):
        for j in range(len(m[i])):
            if (i == 0) or (j == 0):
                m[i][j] = 1
            elif (i == ybound) or (j == xbound):
                m[i][j] = 1
            else:
                m[i][j] = random.randint(0,1)
    return m

# < 4 neighbors and the cell dies,
# 5+ and the cell is born
# takes/returns a rectangular list
def carve(a):
    x = []
    y = []
    ybound = len(a)-1
    xbound = len(a[1])-1
    # j=x i=y
    for i in range (1,ybound):
        for j in range (1,xbound):
            count = 0
            if a[i-1][j-1] == 1: count = count + 1
            if a[i-1][j] == 1: count = count + 1
            if a[i-1][j+1] == 1: count = count + 1
            if a[i+1][j-1] == 1: count = count + 1
            if a[i+1][j] == 1: count = count + 1
            if a[i+1][j+1] == 1: count = count + 1
            if a[i][j-1] == 1: count = count + 1
            if a[i][j+1] == 1: count = count + 1
            if (count >= 5) and a[j][i] == 0:
                x.append(j)
                y.append(i)
            if (count < 4) and a[j][i] == 1:
                x.append(j)
                y.append(i)
    if len(x) != 0:
        for k in range(len(x)):
            if (a[x[k]][y[k]] == 0):
                a[x[k]][y[k]] = 1
            elif(a[x[k]][y[k]] == 1):
                a[x[k]][y[k]] = 0
    return a

# generate a map
def generatecave(x,y):
    cavemap = initmap(x,y)
    cavemap = seedmap(cavemap)
    for i in range(5):
        cavemap = carve(cavemap)
    return cavemap
        

class caveroom(object):
    
    def __init__(self,x,y,lmap):
        self._size = 0
        self.xbounds = [] # parallel lists: open space next to a wall
        self.ybounds = []
        self.lmap = lmap # the map this room exists on
        self.testx = x
        self.testy = y
        self.allcoords = [] # every tile this room has
        self.defineroom(x,y,lmap)

    def getsize(self):
        return self._size
    def setsize(self, value):
        self._size = value
    def delsize(self):
        del self._size
    size = property(getsize, setsize, delsize, "area of the room")
    
    # this function, aka 4 direction flood fill, counts all contiguous space,
    # originating from x,y. it also populates the xbounds and ybounds lists,
    # which hold the coordinates of all locations next to a wall.
    def defineroom(self,x,y,lmap): 
        boundtile = False
        self.allcoords.append((x,y));
        if not self.allcoords.count((x,y+1)):
            if (lmap[y+1][x] == 0):
                self.defineroom(x,y+1,lmap)
            else: boundtile = True
            
        if not self.allcoords.count((x,y-1)):
            if (lmap[y-1][x] == 0):
                self.defineroom(x,y-1,lmap)
            else: boundtile = True

        if not self.allcoords.count((x+1,y)):
            if (lmap[y][x+1] == 0):
                self.defineroom(x+1,y,lmap)
            else: boundtile = True

        if not self.allcoords.count((x-1,y)):
            if (lmap[y][x-1] == 0):
                self.defineroom(x-1,y,lmap)
            else: boundtile = True
        
        self._size = self._size + 1
        
        if boundtile:
            self.xbounds.append(x)
            self.ybounds.append(y)
            
    # does the room contain the point x,y?
    
    def contains(self,x,y):
        for i in range(len(self.xbounds)):
            if x == self.xbounds[i] and y == self.ybounds[i]:
                return True
        
        if self.lmap[y][x] == 1:
            return False
        
        xupper = False;
        count = 0
        while xupper == False:
            count = count + 1
            for i in range(len(self.xbounds)):
                if (x+count == self.xbounds[i]) and (y == self.ybounds[i]):
                    xupper = True
                elif(self.lmap[y][x+count] == 1):
                    return False
        xlower = False
        count = 0
        while xlower == False:
            count = count - 1
            for i in range(len(self.xbounds)):
                if (x+count == self.xbounds[i]) and (y == self.ybounds[i]):
                    xlower = True
                elif(self.lmap[y][x+count] == 1):
                    return False
        yupper = False
        count = 0
        while yupper == False:
            count = count + 1
            for i in range(len(self.ybounds)):
                if (y+count == self.ybounds[i]) and (x == self.xbounds[i]):
                    yupper = True
                elif(self.lmap[y+count][x] == 1):
                    return False
        ylower = False
        count = 0
        while ylower == False:
            count = count - 1
            for i in range(len(self.ybounds)):
                if (y+count == self.ybounds[i]) and (x == self.xbounds[i]):
                    ylower = True
                elif(self.lmap[y+count][x] == 1):
                    return False
        return True

    def fillroom(self):
        for i in self.allcoords:
            self.lmap[i[1]][i[0]] = 1
    
def detectrooms(lmap):
    roomlist = []
    for i in range(len(lmap)):
        for j in range(len(lmap[i])):
            if lmap[i][j] == 0:
                if roomlist == []: #no rooms? make one.
                    roomlist.append(caveroom(j,i,lmap))
                makearoom = True
                for k in roomlist:
                    if k.contains(j,i):
                        makearoom = False
                if makearoom:
                    roomlist.append(caveroom(j,i,lmap))
    return roomlist



cave = generatecave(64,64)
printmap(cave)
roomlist = detectrooms(cave)

