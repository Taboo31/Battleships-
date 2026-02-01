import pygame

# settings code

class FilePaths:
    def __init__(self):

        self.ocean_bg = r"PICTURES\bg_ocean_v2.png"
        self.battleships_homescreen = r"PICTURES\battleships_homescreen.png"
        self.battleships_icon = r"PICTURES\battleships_icon.png"


class Configs:
    def __init__(self):

        self.VIRTUAL_SURFACE = (1920, 1080)
        self.RESOLUTION = (1366, 768)

        self.BOARD_X_ORIGIN = 150 # the starting x position of the top left tile
        self.BOARD_Y_ORIGIN = self.BOARD_X_ORIGIN # the starting y position of the top left tile

        self.BUTTON_X_ORIGIN = self.VIRTUAL_SURFACE[0] * 0.025
        self.BUTTON_Y_ORIGIN = self.VIRTUAL_SURFACE[1] * 0.5

        self.TILE_SIZE = 50
        self.FONT_SIZE = 50 # keep below tile size
        self.BUTTON_SIZE = self.VIRTUAL_SURFACE[1] // 10 # this is the size of the button height, the size of the button width is double this

        self.LINE_WIDTH_X = self.TILE_SIZE + 5 # this (5) is the pixel length between each box change the one value to change how thick the lines are (how apart the boxes are)
        self.LINE_WIDTH_Y = self.TILE_SIZE + 5
        self.BUTTON_SPACING = self.BUTTON_SIZE + 20

        self.GAME_BOARD_SIZE = 11 # dont go over 27 cuz then run out of letters so an error

        self.TEXT_COLOUR = (0, 0, 0)
        self.TILE_COLOUR = (255, 255, 255)
        self.SCREEN_COLOUR = (174, 198, 207)
        self.BUTTON_COLOUR = (50, 50, 65)

       
        self.LETTERS = [" ","A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
        self.NUMBERS = [" "] + [str(i) for i in range(1, 27)]

class Tile:
   
    def __init__(self, rect, grid_pos, label, colour):
       
        self.rect = rect
        self.colour = colour
        self.grid_pos = grid_pos
        self.label = label
        self.ship = None # equal to the class of the thing
        self.hit = False
    
    
    def self_check(self):
        
        if self.ship != None: # if the tile has been clicked change it to this colour
            self.colour = (255, 0, 0)




# creation code




def create_tilemap_battleShipGame(baseConfigs):

    GRID = []

    for y_coordinates in range(baseConfigs.GAME_BOARD_SIZE):

        row = []

        for x_coordinates in range(baseConfigs.GAME_BOARD_SIZE):

            board_x_coordinates = baseConfigs.BOARD_X_ORIGIN + x_coordinates * baseConfigs.LINE_WIDTH_X
            board_y_coordinates = baseConfigs.BOARD_Y_ORIGIN + y_coordinates * baseConfigs.LINE_WIDTH_Y
           
            row.append(Tile(pygame.Rect(board_x_coordinates, board_y_coordinates, baseConfigs.TILE_SIZE, baseConfigs.TILE_SIZE),
                            (x_coordinates, y_coordinates),
                            (baseConfigs.LETTERS[x_coordinates], baseConfigs.NUMBERS[y_coordinates]),
                            ((255, 255, 255))
                        ))


        GRID.append(row)

    font = pygame.font.Font(None, baseConfigs.FONT_SIZE)

    RENDERED_LETTERS = [font.render(character, True, baseConfigs.TEXT_COLOUR) for character in baseConfigs.LETTERS]
    RENDERED_NUMBERS = [font.render(character, True, baseConfigs.TEXT_COLOUR) for character in baseConfigs.NUMBERS]

    return RENDERED_LETTERS, RENDERED_NUMBERS, GRID





def create_mainMenu(baseConfigs, filePaths, virtual_screen):

    #create buttons

    BUTTONS = []

    for button_num in range(4):

        BUTTONS.extend([pygame.Rect(baseConfigs.BUTTON_X_ORIGIN, baseConfigs.BUTTON_Y_ORIGIN + baseConfigs.BUTTON_SPACING * button_num, baseConfigs.BUTTON_SIZE * 4, baseConfigs.BUTTON_SIZE)]) # maybe make the *4 scale to the resolution at some point
   
    # render more text

    mainName = "Battleships"

    # render the button text
   
    buttonText = ["Play", "Settings", "Help", "Quit"] #put this in the baseConfig folder
    font = pygame.font.Font(None, baseConfigs.FONT_SIZE)
    RENDERED_TEXT = [font.render(text, True, baseConfigs.TEXT_COLOUR) for text in buttonText]
                     
    #load image into memory

    COVER_IMAGE = pygame.image.load(filePaths.battleships_homescreen).convert_alpha()
    COVER_IMAGE = pygame.transform.scale(COVER_IMAGE, (0, 0))
   
    return BUTTONS, COVER_IMAGE, RENDERED_TEXT




# drawing code




def draw_tilemap_battleShipGame(baseConfigs, rendered_letters, rendered_numbers, GRID, virtual_screen):

                                        # change this (0, 255, 0) to something else in baseconfigs at somepoint
    pygame.draw.rect(virtual_screen, (0, 255, 0), (baseConfigs.BOARD_X_ORIGIN - (baseConfigs.LINE_WIDTH_X % baseConfigs.TILE_SIZE),\
                                                    baseConfigs.BOARD_Y_ORIGIN - (baseConfigs.LINE_WIDTH_Y % baseConfigs.TILE_SIZE),\
                                                    baseConfigs.LINE_WIDTH_X * (baseConfigs.GAME_BOARD_SIZE + 4),\
                                                    (baseConfigs.LINE_WIDTH_Y * baseConfigs.GAME_BOARD_SIZE) + baseConfigs.LINE_WIDTH_Y % baseConfigs.TILE_SIZE ) # +3 is the offset on the right
                    )

    for row in GRID: # the tilemap should is a square so this will work if its no longer a square there is an error here
        for tile in row:
            
            tile.self_check()
            pygame.draw.rect(virtual_screen, tile.colour, tile.rect)
            #text_rect = rendered_letters[index].get_rect(center=(tile.centerx, baseConfigs.BOARD_Y_ORIGIN))

            if tile.rect.y == baseConfigs.BOARD_Y_ORIGIN:

                columnIndex = (tile.rect.x - baseConfigs.BOARD_X_ORIGIN) // baseConfigs.LINE_WIDTH_X
                currentLetter = rendered_letters[columnIndex]
                currentLetterPosition = currentLetter.get_rect(center = tile.rect.center)

                virtual_screen.blit(currentLetter, currentLetterPosition)

            if tile.rect.x == baseConfigs.BOARD_X_ORIGIN:

                rowIndex = (tile.rect.y - baseConfigs.BOARD_Y_ORIGIN) // baseConfigs.LINE_WIDTH_Y
                currentNumber = rendered_numbers[rowIndex]
                currentNumberPosition = currentNumber.get_rect(center = tile.rect.center)

                virtual_screen.blit(currentNumber, currentNumberPosition)
    
    




           
def draw_mainMenu(baseConfigs , buttons, cover_image, virtual_screen, rendered_text):

    # draw buttons

    for button in buttons:
        pygame.draw.rect(virtual_screen, baseConfigs.BUTTON_COLOUR, button)

    # text on buttons

    for index, button in enumerate(buttons): # so the text should be the same as the buttons and if its not then theres an issue here
        try:
            currentButtonText = rendered_text[index]
            currentButtonPosition = currentButtonText.get_rect(center = button.center)

            virtual_screen.blit(currentButtonText, currentButtonPosition)
        except:
            pass


    # draw image
    x_coordinate = baseConfigs.VIRTUAL_SURFACE[0] - (cover_image.get_size()[0] - cover_image.get_size()[0] * 0.075)
    y_coordinate = baseConfigs.VIRTUAL_SURFACE[1] - cover_image.get_size()[1]
   
    virtual_screen.blit(cover_image, (x_coordinate, y_coordinate))


def get_button_mainMenu(baseConfigs, buttons):
   
    for index, button in enumerate(buttons):
       
        if button.collidepoint(realToVirtual_mouse(baseConfigs)) == True:
           
            return index    
   
def buttonLogic_mainMenu(baseConfigs, buttonChosen, rendered_items, window, virtual_screen):
   
    if buttonChosen == 0:
        battleShipsGame(baseConfigs, rendered_items, window, virtual_screen)
   
    if buttonChosen == 1:
       
        print("Settings") # call functions
   
    if buttonChosen == 2:
       
        print("Help") # call functions
       
    if buttonChosen == 3: # put code you want to happen before exit here
        exit()
       




   
def get_tile_battleShipGame(baseConfigs, grid, givenCoordinates = None): # returns the tile that the mouse cursor is on as a class object if given coordinates returns class object touching coordinates
   
    if givenCoordinates == None: # if you find another pixel position to input add it to this if stuff
        pixelPosition = realToVirtual_mouse(baseConfigs)
    else:
        pixelPosition = givenCoordinates
   
    x_coordinates = pixelPosition[0] - baseConfigs.BOARD_X_ORIGIN #make the coordinates relative to the board origin
    y_coordinates = pixelPosition[1] - baseConfigs.BOARD_Y_ORIGIN

    if (x_coordinates % baseConfigs.LINE_WIDTH_X > baseConfigs.TILE_SIZE) or (y_coordinates % baseConfigs.LINE_WIDTH_Y > baseConfigs.TILE_SIZE): #check if the mouse is in the line width gap

        return None

    grid_x_coordinates = x_coordinates // baseConfigs.LINE_WIDTH_X
    grid_y_coordinates = y_coordinates // baseConfigs.LINE_WIDTH_Y

    if (0 < grid_x_coordinates < baseConfigs.GAME_BOARD_SIZE) and ( 0 < grid_y_coordinates < baseConfigs.GAME_BOARD_SIZE): #check if in board

        return grid[grid_y_coordinates][grid_x_coordinates]
   
    else:
        return None
    

# btw this doesnt work at all
def place_ship(baseConfigs, rendered_items, ship_object, start_pos, place_ship = True): # THE GRIDS ORIGIN (upper leftmost tile IS ALWAYS (1, 1) AND LAST POINT IS (GAMEBOARD_SIZE - 1, GAMEBOARD_SIZE - 1))

    ship_object.ship_starting_pos = start_pos
    ship_coords_to_be = ship_object.get_coords_ship_is_on()

    for coord in ship_coords_to_be: # iterate through each coord the ship will be on

        if not ((1 <= coord[0] < baseConfigs.GAME_BOARD_SIZE) and (1 <= coord[1] < baseConfigs.GAME_BOARD_SIZE)):
            return False # the ship will be out of bounds
        
        if rendered_items[2][coord[1]][coord[0]].ship != None:

            return False # the ship that will be placed is overlapping with an already placed ship

    if place_ship == True:    
        for x, y in ship_coords_to_be:

            rendered_items[2][y][x].ship = ship_object
    
        return True # successful placement
    
    else:
        return ship_coords_to_be
    



        




    







def highlight_selected_square(baseConfigs, rendered_items, virtual_screen):

        for x in range(baseConfigs.GAME_BOARD_SIZE): # iterate through all tiles on board
            for y in range(baseConfigs.GAME_BOARD_SIZE):
                if (rendered_items[2][y][x].rect.collidepoint(realToVirtual_mouse(baseConfigs)) == True) and\
                    not (rendered_items[2][y][x].grid_pos[0] == 0 or rendered_items[2][y][x].grid_pos[1] == 0): # line above checks if mouse on tile, line below check if tile on board

                    pygame.draw.rect(virtual_screen, ((rendered_items[2][y][x].colour[0] * 0.75, rendered_items[2][y][x].colour[1] * 0.75, rendered_items[2][y][x].colour[2] * 0.75)), rendered_items[2][y][x].rect) 
                    # by doing rendered_items[2][x][y].colour[0] you change/dampen the colour no matter what colour is underneath so its goated

def highlight_selected_square_placingShips(baseConfigs, ship_coords_to_be, rendered_items, virtual_screen): #working on

    acceptable_coords = []
    placement = True

    for y in range(baseConfigs.GAME_BOARD_SIZE):
        for x in range(baseConfigs.GAME_BOARD_SIZE):
            if not (rendered_items[2][y][x].grid_pos[0] == 0 or rendered_items[2][y][x].grid_pos[1] == 0):
                    
                    acceptable_coords.append((rendered_items[2][y][x].grid_pos))

    for current_coord in ship_coords_to_be:
        
        if current_coord not in acceptable_coords:
            
            placement = False
    
    if placement == True:

        for y, x in ship_coords_to_be:                
            pygame.draw.rect(virtual_screen, (rendered_items[2][x][y].colour[0] * 0.75, rendered_items[2][x][y].colour[1] * 0.75, rendered_items[2][x][y].colour[2] * 0.75), rendered_items[2][x][y].rect) 

               
class Ship:

    def __init__(self, size):

        self.hitTiles = 0
        self.size = size
        self.ship_starting_pos = (0, 0) #no idea if this should start with anything
        self.rotated = False  # False = Vertical, True = Horizontal
    
    def get_coords_ship_is_on(self):
        
        coords = []
        for i in range(self.size):
            if self.rotated == False:

                new_coords = (self.ship_starting_pos[0], self.ship_starting_pos[1] + i)
                coords.append(new_coords)
            
            elif self.rotated == True:

                new_coords = (self.ship_starting_pos[0] + i, self.ship_starting_pos[1])
                coords.append(new_coords)
            
            # if you want to be able to make ships diagonal do it here also fuck you
        
        return coords
        



class Carrier(Ship):

    def __init__(self):

        super().__init__(size = 5)


class Battleship(Ship):

    def __init__(self):

        super().__init__(size = 4)

class Cruiser(Ship):

    def __init__(self):

        super().__init__(size = 3)


class Submarine(Ship):

    def __init__(self):

        super().__init__(size = 3)


class Destroyer(Ship):

    def __init__(self):

        super().__init__(size = 2)


# main menu code








# scaling code

def virtualToReal_window(baseConfigs, virtual_screen, window):

    window.blit(pygame.transform.smoothscale(virtual_screen, baseConfigs.RESOLUTION), (0, 0))

def realToVirtual_mouse(baseConfigs):

    mouse_x_coordinates, mouse_y_coordinates = pygame.mouse.get_pos()

    virtual_x_coordinates = int(round(mouse_x_coordinates * (baseConfigs.VIRTUAL_SURFACE[0] / baseConfigs.RESOLUTION[0])))
    virtual_y_coordinates = int(round(mouse_y_coordinates * (baseConfigs.VIRTUAL_SURFACE[1] / baseConfigs.RESOLUTION[1])))

    return (virtual_x_coordinates, virtual_y_coordinates)

















# screens code

testbattleship = Carrier()
def battleShipsGame(baseConfigs, rendered_items, window, virtual_screen):

    running = True

    while running:
   
        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                running = False
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                
                if event.button == 1: # left click to get the tile object
                    
                    if get_tile_battleShipGame(baseConfigs, rendered_items[2], realToVirtual_mouse(baseConfigs)) != None:
                        print(get_tile_battleShipGame(baseConfigs, rendered_items[2], realToVirtual_mouse(baseConfigs)).ship)

                if event.button == 3: # right click to place ship

                    if (get_tile_battleShipGame(baseConfigs, rendered_items[2])) != None:
                        place_ship(baseConfigs, rendered_items, testbattleship, (get_tile_battleShipGame(baseConfigs, rendered_items[2], realToVirtual_mouse(baseConfigs))).grid_pos)

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_r: #if key r down rotates ship

                    testbattleship.rotated = not testbattleship.rotated # change this to like better at saomepoint also prolly make it so it can rotate 360 degrees not just rotate between horizontal and not

            if event.type == pygame.VIDEORESIZE:

                baseConfigs.RESOLUTION = event.size
                window = pygame.display.set_mode(baseConfigs.RESOLUTION, pygame.RESIZABLE)
       

        virtual_screen.fill(baseConfigs.SCREEN_COLOUR)

        #RENDERED_ITEMS = [RENDERED_LETTERS, RENDERED_NUMBERS, GRID] this is what rendered items looks like
        draw_tilemap_battleShipGame(baseConfigs, rendered_items[0], rendered_items[1], rendered_items[2], virtual_screen)

    #testing here
        if get_tile_battleShipGame(baseConfigs, rendered_items[2], realToVirtual_mouse(baseConfigs)) != None:
            placeship = place_ship(baseConfigs, rendered_items, testbattleship, (get_tile_battleShipGame(baseConfigs, rendered_items[2], realToVirtual_mouse(baseConfigs))).grid_pos, False)

            if type(placeship) != bool:
                highlight_selected_square_placingShips(baseConfigs, placeship, rendered_items, virtual_screen)

    #testing ends here
        highlight_selected_square(baseConfigs, rendered_items, virtual_screen)

        virtualToReal_window(baseConfigs, virtual_screen, window)

        pygame.display.update()





def mainMenu(baseConfigs, filePaths, virtual_screen, BUTTONS, COVER_IMAGE, window, rendered_text, rendered_items):

    running = True
    bg = pygame.image.load(filePaths.ocean_bg).convert()
    bg = pygame.transform.scale(bg, baseConfigs.VIRTUAL_SURFACE)

    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
               
                running = False
                exit()
           
            if event.type == pygame.MOUSEBUTTONDOWN:
               
                if event.button == 1:
                   
                    buttonChosen = get_button_mainMenu(baseConfigs, BUTTONS)
                    buttonLogic_mainMenu(baseConfigs, buttonChosen, rendered_items, window, virtual_screen)

           
            if event.type == pygame.VIDEORESIZE:

                baseConfigs.RESOLUTION = event.size
                window = pygame.display.set_mode(baseConfigs.RESOLUTION, pygame.RESIZABLE)


        virtual_screen.blit(bg,(0,0))
        draw_mainMenu(baseConfigs, BUTTONS, COVER_IMAGE, virtual_screen, rendered_text)

        virtualToReal_window(baseConfigs, virtual_screen, window)

        pygame.display.update()




def loadStartUp():

    pygame.init()

    filePaths = FilePaths()
    baseConfigs = Configs()

    window = pygame.display.set_mode(baseConfigs.RESOLUTION, pygame.RESIZABLE)
    virtual_screen = pygame.Surface(baseConfigs.VIRTUAL_SURFACE)
    gameIcon = pygame.image.load(filePaths.battleships_icon)

    pygame.display.set_icon(gameIcon)
    pygame.display.set_caption("Battleships")




    BUTTONS, COVER_IMAGE, RENDERED_TEXT = create_mainMenu(baseConfigs, filePaths, virtual_screen)
    RENDERED_LETTERS, RENDERED_NUMBERS, GRID = create_tilemap_battleShipGame(baseConfigs)

   
    RENDERED_LETTERS, RENDERED_NUMBERS, GRID = create_tilemap_battleShipGame(baseConfigs)    
    RENDERED_ITEMS = [RENDERED_LETTERS, RENDERED_NUMBERS, GRID]
   
    mainMenu(baseConfigs, filePaths, virtual_screen, BUTTONS, COVER_IMAGE, window, RENDERED_TEXT, RENDERED_ITEMS)
    #battleShipsGame(baseConfigs, RENDERED_ITEMS, window, virtual_screen)
   
    #return baseConfigs, filePaths, virtual_screen, window, RENDERED_LETTERS, RENDERED_NUMBERS, GRID, BUTTONS, COVER_IMAGE
#baseConfigs, filePaths, virtual_screen, window, RENDERED_LETTERS, RENDERED_NUMBERS, GRID, BUTTONS, COVER_IMAGE = loadStartUp()


loadStartUp()