import time
import copy
import turtle

SIZE = 20 # size of the 2D cellular automaton
work = []
tmp = []


def printSep():
    """
    Print a separator
    """
    print('-' * (SIZE+2))


def printEachRow(world, row_num):
    """
    Return one row as string
    :param world: result of work
    :param row_num: interested row number
    :return: one row as string
    """
    string_append = '|'
    for i in world_size:
        if world[row_num][i]:
            string_append += 'x'    # Mean being alive
        else:
            string_append += ' '
    return string_append + '| row ' + str(row_num)


def printWorld(world):  # Changed HJ
    """
    Print one generation.
    Must use printSep() above to print the separators.
    """
    # # Test code
    # test_file.write('-'*(SIZE+2)+'\n')
    printSep()

    for i in world_size:
        # # Test code
        # assist_string = printEachRow(world, i)
        # test_file.write(assist_string+'\n')
        print(printEachRow(world, i))

    # # Test code
    # test_file.write('-'*(SIZE+2)+'\n')
    printSep()

    # Intensive time sleep
    time.sleep(TIME)


def cellSum(world_tmp, y, x):
    """
    Get sum of around cells alive, including interested cell itself
    :param world_tmp: work
    :param y: location
    :param x: location
    :return: sum as integer
    """
    result = 0
    for i in [y-1, y, y+1]:
        if i in world_size:    # Edge limitation
            for j in [x-1, x, x+1]:
                if not(i == y and j == x) and j in world_size:
                    result += world_tmp[i][j]
    return result


def cellDiscriminator(cell_state, sum_up):
    """
    Discriminate whether cell is going to be alive or dead
    :param cell_state: recent state of interested cell
    :param sum_up: sum by cellSum()
    :return: alive = 1, dead = 0
    """
    if str(sum_up) in RULE[1 - cell_state]:   # About survive
        return 1    # Mean being alive
    else:
        return 0    # Mean being dead


def getRule(default):
    """
    Get RULE
    :param default: Conway default 23/3
    :return: RULE
    """
    form = (
        ('Diamoeba', '5678/35678'),
        ('Seeds', '/2'),
        ('Serviettes', '/234'),
        ('Maze', '12345/3'),
        ('Mazectric', '1234/3'),
        ('2x2', '125/36'),
        ('Replicator', '1357/1357'),
        ('Amoeba', '1358/357'),
        ('Conway\'s game of life', '23/3'),
        ('Highlife', '23/36'),
        ('Stains', '235678/3678'),
        ('Coagulations', '235678/378'),
        ('Pseudo life', '238/357'),
        ('Move', '245/368'),
        ('34 Life', '34/34'),
        ('Day & Night', '34678/3678'),
        ('Coral', '45678/3'),
        ('Long life', '5/346'),
        ('Assimilation', '4567/345'),
        ('Life without death', '012345678/3'),
        ('Gnarl', '1/1'),
        ('Walled cities', '2345/45678'),
        ('Pylamid', '/12345678'),
        ('Sponge cells', '01234567/456'),
        ('wired life', '23/3678'),
        ('1 life', '13/3'),
        ('drill', '245678/3'),
        ('h tree', '012345678/1'),
        ('rats in maze', '1234/37'),
        ('repilcater2', '02468/1357'),
        ('wired life 37', '23/37')
    )
    getter = str(input('Rule (survive/birth): ')).strip().lower()

    for i in form:
        if getter == i[0].lower() or getter == i[1]:
            return i[1].split('/')

    if '/' not in getter:
        return default

    result = ['','']
    for i in [0, 1]:
        for ch in getter.split('/')[i]:
            if ch.isdigit() and ch not in result[i]:
                result[i] += ch

    return result


def getSize(default):
    """
    Get SIZE
    :param default: SIZE default 20
    :return: SIZE
    """
    try:
        inp_size = int(input('Grid sidelength (default 20): '))
        return inp_size if inp_size > default else default
    except:
        return default  # Use default(global SIZE)


def getGeneration():
    """
    Get GENE
    This function can call itself(recursive)
    :return: GENE or this function itself
    """
    try:
        inp_generation = int(input('Max generation: '))
        return inp_generation if inp_generation > 0 else getGeneration()
    except:
        return getGeneration()  # Call itself(recursive)


def getGenerationDefault():
    """
    Get GENE
    This function can call itself(recursive)
    :return: GENE or this function itself
    """
    print('### DEFAULT MODE ### ', 'Max generation: ', 9999999, sep='')
    return 9999999


def getTime(default):
    """
    Get TIME
    :param default: sec. default 1
    :return: TIME
    """
    try:
        return float(input('Sleep time (sec. default 1): '))
    except:
        return default   # Use default(1 sec.)


def setDrawer(drawer, square_size, cell, x, y):
    """
    Set drawer
    :param drawer: turtle
    :param square_size: size of square
    :param cell: cell state
    :param x: location
    :param y: location
    :return: none
    """
    # For turtle
    drawer.penup()
    drawer.shape('square')
    if cell:
        drawer.showturtle()
    drawer.resizemode('user')
    drawer.turtlesize((square_size - 1 - 0) / 20, (square_size - 1 - 0) / 20)
    drawer.color(255, 255, 255)
    # drawer.fillcolor(0, 0, 0)
    drawer.fillcolor(0, 255 - int(60 * (x+y) // SIZE), 0)
    drawer.speed(0)
    drawer.setposition(square_size * x, square_size * y)


def toggleDrawer(drawer, work, tmp):
    """

    :param drawer:
    :param work: work cell list
    :param tmp: deepcopied work cell list
    :return: none
    """
    for y in world_size:
        for x in world_size:
            drawer[y][x].fillcolor(200, 200, 200)
            if work[y][x] == 0:
                drawer[y][x].showturtle()
            turtle.update()
            # cell = \
            #     cellDiscriminator(tmp[y][x], cellSum(tmp, y, x))
            # work[y][x] = cell
            # drawer[y][x].fillcolor(cell, cell, cell)
            # drawer[y][x].fillcolor(work[y][x], work[y][x], work[y][x])
            cell = \
                cellDiscriminator(tmp[y][x], cellSum(tmp, y, x))
            work[y][x] = cell
            if cell == 1:
                drawer[y][x].fillcolor(0, 255 - int(60 * (x+y) // SIZE), 0)
            else:
                drawer[y][x].hideturtle()
            turtle.update()
    # turtle.update()
    time.sleep(TIME)


#
# Main program
#

# # Test code
# print(work)

#
# # Test code
#
# # Initialize work
#
# read_file = open('cellular_automaton\\SampleOutput.txt')
# read_file.readline()
# for r in range(0, 20):
#     temp_string = read_file.readline()
#     temp_string = temp_string.replace(' ', '0')
#     temp_string = temp_string.replace('x', '1')
#     temp_list = []
#     for r2 in range(1, 21):
#         temp_list.append(int(temp_string[r2]))
#     work.append(temp_list)
# read_file.close()
#

# Compute:
RULE = getRule(['23', '3']) # Conway's default 23/3
SIZE = getSize(SIZE)    # default global SIZE
# GENE = getGeneration()
GENE = getGenerationDefault()
TIME = getTime(1)   # default 1 sec.

#
# # Test code
# Output file
# test_file = open('lab11_p2_output_test\\lab11_p2_output s'+str(SIZE)+' g'+str(GENE)+'.txt', 'w')
#

# Initialize work
world_size = [x for x in range(SIZE)]

for i in world_size[0:3]:
    work.append([0, 1] + [0] * (SIZE - 2))
for i in world_size[3:10]:
    work.append([0] * SIZE)
work.append([0] * 10 + [1] * 3 + [0] * (SIZE - 13))
work.append([0] * 10 + [1] + [0] * (SIZE - 11))
work.append([0] * 10 + [1] * 3 + [0] * (SIZE - 13))
for i in world_size[13:]:
    work.append([0] * SIZE)

window_size = 600
square_size = window_size / SIZE

# Append work
if SIZE > 20:
    for r in range(0, 20):
        for r2 in range(20, SIZE):
            work[r].append(0)
    for r3 in range(20, SIZE):
        work.append([0]*SIZE)

# Turtle
turtle.setup(window_size+2*square_size, window_size-20)
turtle.screensize(window_size, window_size-20)
turtle.setworldcoordinates(0, window_size-20, window_size+2*square_size, 0)
turtle.tracer(0, 0)
window = turtle.Screen()
turtle.colormode(255)

# Row number.
# Made on 6.5 Wed. 22:35.
point = turtle.Turtle()
point.penup()
point.hideturtle()
for i in world_size:
    point.setposition(window_size, int(i*square_size+square_size//6))
    point.write(' row '+str(i), font = ('Times New Roman', int(square_size/2), 'bold'))

drawer = []
# Make turtles and draw gene 0
for y in world_size:
    drawer.append([])
    for x in world_size:
        drawer[y].append(turtle.Turtle())
        drawer[y][x].hideturtle()
        setDrawer(drawer[y][x], square_size, work[y][x], x, y)
turtle.update()
time.sleep(TIME)

window.listen()

# # Print gene 0
# printWorld(work)

# Print gene 1 ~ GENE
while GENE:
    tmp = copy.deepcopy(work)

    # Now discrimination is by variable tmp
    # Now mutation is to variable work
    toggleDrawer(drawer, work, tmp)

    # # Print cells
    # printWorld(work)

    GENE -= 1


# turtle.mainloop()
# # Test code
# Output file
# test_file.close()
