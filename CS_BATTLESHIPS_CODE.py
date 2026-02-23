import pygame
import random

class FilePaths:
    """
    this is where the file paths are stored
    i did this to centralise where all the files in the program being used are stored
    probably shouldnt be a class as its instanced once and i dont think it should change
    """
    def __init__(self):

        self.ocean_bg = r"PICTURES\bg_ocean_v2.png"
        self.battleships_homescreen = r"PICTURES\battleships_homescreen.png"
        self.battleships_icon = r"PICTURES\battleships_icon.png"

        self.font = r"FONTS\ITC_Machine_Regular.otf"    
        self.explosion_spritesheet = r"SPRITES\explosion_sprite.png"

        self.background_music = r"SOUNDTRACKS\looped_lobby_music.mp3"
        self.explosion_sound  = r"SOUNDTRACKS\explosion_sound.mp3"


class Configs:
    """
    this is where all the constants are stored
    i did this so changing one setting in configs changes all related code to the constant
    i used a class because i thought i could have different save presets which would be different objects
    """
    def __init__(self):

        self.VIRTUAL_SURFACE = (1920, 1080)
        self.RESOLUTION = (1366, 768)
       
        self.BUTTON_X_ORIGIN = self.VIRTUAL_SURFACE[0] * 0.025
        self.BUTTON_Y_ORIGIN = self.VIRTUAL_SURFACE[1] * 0.5
   

        self.TILE_SIZE = 50
        self.FONT_SIZE = 50 # keep below tile size
        self.BUTTON_SIZE = self.VIRTUAL_SURFACE[1] // 10 # this is the size of the button height, the size of the button width is double this

        # battleships menu name 

        self.GAMENAME_FONT_SIZE = 100
        self.GAMENAME_COLOUR    = (255, 255, 255)

        self.LINE_WIDTH_X = self.TILE_SIZE + 5 # this (5) is the pixel length between each box change the one value to change how thick the lines are (how apart the boxes are)
        self.LINE_WIDTH_Y = self.TILE_SIZE + 5
        self.BUTTON_SPACING = self.BUTTON_SIZE + 20

        self.GAME_BOARD_SIZE = 11 # dont go over 27 cuz then run out of letters so an error, add a cap so volume of ships placed wont be greater then amount of available spaces on board?

        self.TEXT_COLOUR = (255, 0, 0)
        self.HIGHLIGHTED_TEXT_COLOUR = (0, 0, 0)
        self.HELP_TEXT_COLOUR = (0, 0, 0)
        self.READY_TEXT_COLOUR = (0, 0, 0)

        self.TILE_COLOUR = (255, 255, 255)
        self.SCREEN_COLOUR = (174, 198, 207)
        self.BUTTON_COLOUR = (50, 50, 65)

        self.USED_ICON_COLOUR = (200, 200, 200)
        self.BACK_BOARD_COLOUR= (0, 0, 0)
        self.BACK_BOARD_PANEL_COLOUR = (0, 0, 0)
        self.READY_BUTTON_COLOUR = (0, 255, 0)
        self.OVERLAP_COLOUR = (255, 0, 0)
        self.END_SCREEN_TEXT_COLOUR = (0, 0, 0)

        self.COLOURKEY_EXPLOSIONS = (0, 0, 0) # the transparent colour for the explosion spritesheet should prolly be white but then if its white change the background of the sprite sheet to white

        self.BOARD_X_ORIGIN = 150 # the starting x position of the top left tile
        self.BOARD_Y_ORIGIN = self.BOARD_X_ORIGIN # the starting y position of the top left tile

        self.ENEMY_BOARD_X_ORIGIN = self.BOARD_X_ORIGIN + self.LINE_WIDTH_X * self.GAME_BOARD_SIZE + 300
        self.ENEMY_BOARD_Y_ORIGIN = self.BOARD_Y_ORIGIN
       
        # labels on boards

        self.LETTERS = [" ","A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
        self.NUMBERS = [" "] + [str(i) for i in range(1, 27)]

        # margins on the help text screen

        self.HELP_TEXT_X_MARGIN = 25
        self.HELP_TEXT_Y_MARGIN = self.VIRTUAL_SURFACE[1] // 3.5 # prolly change 3.5 to something that scales with the screen
        
        # margins on the end text screen

        self.END_TEXT_X_MARGIN = 25
        self.END_TEXT_Y_MARGIN = self.VIRTUAL_SURFACE[1] // 3.5

        # for animations

        self.ANIMATION_CD = 10 # cooldown between animation frames in ms
        
        self.MAX_ALLOWED_SHIPS = 5

class Sound:
    """
    loads and plays different sounds
    sounds are centralised to avoid repeated coding and seperate audio from logic
    probably shouldnt be a class as theres one instance
    """

    def __init__(self, explosion_sound, background_music):

        self.explosion_sound = pygame.mixer.Sound(explosion_sound)
        self.background_music = background_music

        self.MUSIC_END = pygame.USEREVENT + 1
    
    def load_music(self):
        pygame.mixer.music.load(self.background_music)
    
    def startUP(self):

        self.play_explosion()
        self.play_bg_music()

    def play_bg_music(self):

        pygame.mixer.music.load(self.background_music)
        pygame.mixer.music.play(-1)
    
    def play_explosion(self):

        self.explosion_sound.play()

class Tile:
    """
    represents one individual tile on a board
    each tile has 7 properties
    rect, this is the rect object for the tile its whats drawed to the screen
    grid_pos, this is where the tiles location on the board i.e. (3, 5)
    label, this is where the tile is stored on the board using the boards letter i.e. (3, C)
    colour, this is the current colour of the tile
    is_enemy, this is false when the tile is on the player board and true when it is on the enemy ai board
    ship, this is the ship object stored on the tile. if there is no ship it is None
    hit, this explains if the tile has been hit its False for unhit tiles and True for hit tiles

    tile_update, this changes the colour dependent on if its been hit, if its an enemy owned tile and if it has a ship on it
    """
   
    def __init__(self, rect, grid_pos, label, colour, is_enemy):
       
        self.rect = rect
        self.is_enemy = is_enemy
        self.colour = colour
        self.grid_pos = grid_pos
        self.label = label
        self.ship = None # equal to the class of the thing
        self.hit = False
   
   
    def tile_update(self):

        if self.ship != None and self.hit == True:
            if self.ship.hitTiles == self.ship.size:
                self.colour = (255, 0, 0) # red for if ship is fully destroyed

            else:
                self.colour = (255, 255, 0) # tellow if ship is hit but alive

        elif self.ship == None and self.hit == True: # if tile has no ship but been hit change to light blue
            self.colour = (200, 200, 255)

        elif self.ship != None and self.is_enemy is not True: # if the tile has a ship on it change it to green
            self.colour = (0, 255, 0)
        
        else:
            self.colour = (255, 255, 255) #if nothing make tile white

class SpriteSheet:
    """
    i did this to centralise all the sprite sheets
    theres only one sprite sheet

    get_img this takes 5 inputs frame, width, height, scale and colour
    frame, this is the current frame of the sprite
    width, this is the width of the current sprite on the spritesheet this is needed to cut it up
    height, this is the height of the current sprite on the spritesheet this is needed to cut it up
    scale, this is what the sprite will be changed to. Sprites should only be on square rects. The new resolution will be (scale, scale) where scale are pixels
    colour, this is the colour that will be set to transparent
    """

    def __init__(self, sprite_sheet):

        # if sprite_sheet hasnt been loaded yet load it otherwise dont load it
        if type(sprite_sheet) == str:

                self.sprite_sheet = pygame.image.load(sprite_sheet).convert_alpha()
        else:
            self.sprite_sheet = sprite_sheet
        

    # get image returns a single frame in a sprite sheet
    def get_img(self, frame, width, height, scale, colour):

        # creates a surface the area of the sprite from the sprite sheet and convert it to alpha
        image = pygame.Surface((width, height)).convert_alpha()
        # draw the sprite to the surface frame*width gets the specific sprite to the frame (start at 0)
        image.blit(self.sprite_sheet, (0, 0), ((frame * width), 0, width, height)) # 0 means this will only work with horizontal spritesheets as the y axis doesnt change
        # change the surface to the size of a new square the new proportion is scale x scale in px
        image = pygame.transform.scale(image, (scale, scale))
        # removes the black background of surface
        image.set_colorkey(colour)
        # return the frame
        return image
    
# ships

class Ship:
    """
    i did this so each ship type can inherit the the things it needs
    size, this is how long the ship is in tiles
    type, this is the type of ship that the object is i.e. (cruiser, carrier)
    shipStartingPos, this is where the ship starts i did this as I thought i would make each ship tile have a different image at some point so i would need the head of the ship to know where it starts
                     if there is no ship its None. Its also needed to calculate where the ships position is
    rotated, this is if the ship is rotated. If its False ship orientation is vertical and if its true ship orientation is horizontal

    get_coords_ship_is_on this returns the coords the a ship is on and returns the coords of the ship as a list
    """

    def __init__(self, size, type, shipStartingPos = None):

        self.hitTiles = 0
        self.size = size
        self.type = type
        self.ship_starting_pos = shipStartingPos
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
           
            # if you want to be able to make ships diagonal do it here
       
        return coords
       
class Carrier(Ship):
    """
    This is a set ship. It size is 5 and its a carrier it inherits from the parent ship class
    """

    def __init__(self):

        super().__init__(size = 5, type = Carrier)


class Battleship(Ship):
    """
    This is a set ship. It size is 4 and its a carrier it inherits from the parent ship class
    """

    def __init__(self):

        super().__init__(size = 4, type = Battleship)

class Cruiser(Ship):
    """
    This is a set ship. It size is 3 and its a cruiser it inherits from the parent ship class
    """

    def __init__(self):

        super().__init__(size = 3, type = Cruiser)


class Submarine(Ship):
    """
    This is a set ship. It size is 3 and its a submarine it inherits from the parent ship class
    """

    def __init__(self):

        super().__init__(size = 3, type = Submarine)


class Destroyer(Ship):
    """
    This is a set ship. It size is 2 and its a destroyer it inherits from the parent ship class
    """

    def __init__(self):

        super().__init__(size = 2, type = Destroyer)

class battleship_icons:
    """
    This class creates battleship icons
    Each icon has 
    size, this is the size of the icon in tiles
    column, this is if the icon is on the left or right side of the panel
    row, this is what row each icon appears on
    boat_type, this is the type of boat each icon represents, i.e. (carrier, cruiser)
    rect, this is the rect object of each icon
    colour, this is the colour of each icon

    create_rect, this creates the rectangle object of the icons. It takes 3 inputs rect_panel, margin and tile
    rect_panel, this is the panel that the icons appear on
    margin, this is the distance from the border of the panel that the icons appear on
    tile, this is used to relate icon size to the size of tiles to ensure they dont change if the user changes the size of tiles in settings.
    create_rect returns the rect object of the icon.
    """

    def __init__(self, size, column, row, boat_type, rect_panel, margin, tile):

        self.size = size
        self.column = column
        self.row = row
        self.boat_type = boat_type
        self.rect = self.create_rect(rect_panel, margin, tile)

        self.colour = (0, 0, 255)
    
    def create_rect(self, rect_panel, margin, tile):

        if self.column == "left":
            x = rect_panel.x + margin
        else:
            x = rect_panel.right - tile - margin

        y = rect_panel.y + margin + self.row * (tile * 6)

        rect = pygame.Rect(x, y, tile, tile * self.size)

        return rect

class Panel:
    """
    this represents the panel that appears next to the player board
    it has/uses
    filepaths, filepaths are used to get the font of the text as this create/initialises/loads? the text into memory
    origin, this is the origin of the players board so the panel knows where to position itself in relation to it
    backboard, this it the players back board. The panel gets its height from this

    create_side_panel, this creates all icon objects as well as rendering the text used and the rect objects for the ready button
    it returns: battleship_rects, ready_button, rect_panel, RENDERED_READY_TEXT

    battleship_rects, these are the battleship icons displayed on the panel
    ready_button, this is the ready button that the player uses after setting up their player board
    back_board_panel, this is the panel the tiles on. it is the back of the player board
    rendered_ready_text, this is the text that is displayed on top of the ready button

    back_board_panel_colour, this is the colour of the back board panel the player icons are displayed on
    ready_button_colour, this is the colour of the ready button the player icons are displayed on
    """

    def __init__(self, baseConfigs, filePaths, back_board, origin):

        self.filePaths = filePaths
        self.origin = origin
        self.back_board = back_board
        self.battleship_rects, self.ready_button, self.back_board_panel, self.rendered_ready_text = self.create_side_panel(baseConfigs)

        self.back_board_panel_colour = baseConfigs.BACK_BOARD_PANEL_COLOUR
        self.ready_button_colour = baseConfigs.READY_BUTTON_COLOUR

    def create_side_panel(self, baseConfigs):

        TILE = baseConfigs.TILE_SIZE
        MARGIN = 15
        font = pygame.font.Font(self.filePaths.font, baseConfigs.FONT_SIZE)

        board_x_origin, board_y_origin = self.origin

        # this is the black panel rect

        rect_panel = pygame.Rect(board_x_origin + self.back_board.width,\
                                    (board_y_origin - (baseConfigs.LINE_WIDTH_Y % baseConfigs.TILE_SIZE)),\
                                    (baseConfigs.TILE_SIZE * 4),\
                                    (baseConfigs.LINE_WIDTH_Y * baseConfigs.GAME_BOARD_SIZE) + baseConfigs.LINE_WIDTH_Y % baseConfigs.TILE_SIZE
                                )
        
        # this is for the ship icons on the panel

        # the layout of the buttons on the external pattern left is the size (keep same as the ship sizes or maybe introduce a thing so its like ship_object.size)
        #then its the if the button is on the left or right of the panel then it does that left or right check both put the rect 15px or MARGIN from the boundary
        # the third one is the scale factor for the y axis 

        carrier_icon   = battleship_icons(5, "left",  0, Carrier, rect_panel, MARGIN, TILE)
        battleship_icon= battleship_icons(4, "left",  1, Battleship, rect_panel, MARGIN, TILE)
        cruiser_icon   = battleship_icons(3, "right", 0, Cruiser, rect_panel, MARGIN, TILE)
        submarine_icon = battleship_icons(3, "right", 0.55, Submarine, rect_panel, MARGIN, TILE)
        destroyer_icon = battleship_icons(2, "right", 1.3, Destroyer, rect_panel, MARGIN, TILE)

        battleship_rects = [carrier_icon, battleship_icon, cruiser_icon, submarine_icon, destroyer_icon]

        # this is for the ready button

        ready_button = pygame.Rect(0, rect_panel.bottom - baseConfigs.LINE_WIDTH_Y * 1.5, rect_panel.width - 10, baseConfigs.TILE_SIZE * 1.5)
        ready_button.centerx = rect_panel.centerx

        # this is for the ready button text
        
        ready_text = "READY"
        RENDERED_READY_TEXT = font.render(ready_text, True, baseConfigs.READY_TEXT_COLOUR)

        # center the ready text to the ready button

        RENDERED_READY_TEXT.get_rect(center = ready_button.center)
        
        return battleship_rects, ready_button, rect_panel, RENDERED_READY_TEXT

class Board:
    """
    this class creates the board for the player and enemy
    it has

    filePaths, these are the filepaths i used the for the fonts
    is_enemy , this determines whether the board is an enemy board or player board. if a board is an enemy board the origin changes
    backBoard_colour, this uses the constant from the configs class to get the back board colour
    origin, this is the origin of the board where it is dispalyed

    create_tilemap, it takes baseconfigs as an input and returns RENDERED_LETTERS, RENDERED_NUMBERS, GRID, black_square_rect
    create_tilemap renders the letters, labels and creates the grid using the tile class the black_square_rect is the backboard used for the back of the board
    RENDERED_LETTERS, these are the letters displayed on the baord rendered by the font
    RENDERED_NUMBERS, these are the numbers displayed on the baord rendered by the font
    GRID, this is a 2d list containing all the tiles displayed on the board
    black_square_rect, this is the backboard for the board

    update_board, this function iterates through each tile on the board calling the tile_update function ensuring each button is the correct colour
    """

    def __init__(self, baseConfigs, filePaths, is_enemy):

        self.filePaths = filePaths
        self.is_enemy = is_enemy
        self.backBoard_colour = baseConfigs.BACK_BOARD_COLOUR

        if is_enemy == True:
            self.origin = (baseConfigs.ENEMY_BOARD_X_ORIGIN, baseConfigs.ENEMY_BOARD_Y_ORIGIN)
        else:
            self.origin = (baseConfigs.BOARD_X_ORIGIN, baseConfigs.BOARD_Y_ORIGIN)
        
        self.rendered_letters, self.rendered_numbers, self.grid, self.back_board = self.create_tilemap(baseConfigs)
    

    def create_tilemap(self, baseConfigs):

        board_x_origin, board_y_origin = self.origin

        GRID = []
        
        for y_coordinates in range(baseConfigs.GAME_BOARD_SIZE):

            row = []

            for x_coordinates in range(baseConfigs.GAME_BOARD_SIZE):

                board_x_coordinates = board_x_origin + x_coordinates * baseConfigs.LINE_WIDTH_X
                board_y_coordinates = board_y_origin + y_coordinates * baseConfigs.LINE_WIDTH_Y
            
                row.append(Tile(pygame.Rect(board_x_coordinates, board_y_coordinates, baseConfigs.TILE_SIZE, baseConfigs.TILE_SIZE),
                                (x_coordinates, y_coordinates),
                                (baseConfigs.LETTERS[x_coordinates], baseConfigs.NUMBERS[y_coordinates]),
                                (baseConfigs.TILE_COLOUR),
                                (self.is_enemy)
                            ))

            GRID.append(row)

        font = pygame.font.Font(self.filePaths.font, baseConfigs.FONT_SIZE)

        RENDERED_LETTERS = [font.render(character, True, baseConfigs.TEXT_COLOUR) for character in baseConfigs.LETTERS]
        RENDERED_NUMBERS = [font.render(character, True, baseConfigs.TEXT_COLOUR) for character in baseConfigs.NUMBERS]

        # this is the black square boundary
        black_square_rect = pygame.Rect(board_x_origin - (baseConfigs.LINE_WIDTH_X % baseConfigs.TILE_SIZE),\
                                        board_y_origin - (baseConfigs.LINE_WIDTH_Y % baseConfigs.TILE_SIZE),\
                                        baseConfigs.LINE_WIDTH_X * (baseConfigs.GAME_BOARD_SIZE) + baseConfigs.LINE_WIDTH_X % baseConfigs.TILE_SIZE,\
                                        (baseConfigs.LINE_WIDTH_Y * baseConfigs.GAME_BOARD_SIZE) + baseConfigs.LINE_WIDTH_Y % baseConfigs.TILE_SIZE
                                        )
        
        return RENDERED_LETTERS, RENDERED_NUMBERS, GRID, black_square_rect

    def update_board(self):

        for row in self.grid: # the tilemap should is a square so this will work if its no longer a square there is an error here
            for tile in row:
                
                tile.tile_update()

class Renderer:
    """
    - prolly shouldnt be a class as i think i only reused virtualToReal_window so nothings actually getting reused i also wish i made a class for creating buttons so idk

    renderer, this class is in charge of rendering everything
    virtual_screen, this is the surface everything gets blitted to before its scaled the users res
    window, this is the displayed window it should be the users res / the user can change it

    virtualToReal_window, this function maps the virtual_screen to the window it takes baseConfigs as a parameter

    draw_mainMenu, this draws the main menu. it takes baseconfigs and the mainmenu object as an input
    it blits everything to do with the main menu onto the virtual screen

    draw_endScreen, this function takes baseconfigs and the end screen object as an input
    it blits everything to do with the end screen onto the virtual screen

    draw_helpScreen, this function takes baseconfigs and the help screen object as an input
    it blits everything to do with the help screen onto the virtual screen

    fill_screen, this function fills the virtual screen. it takes baseconfigs as an input. i think i reused this one!!

    draw_board, this function takes a board object as an input and draws it to screen

    draw_labels, this function takes baseConfigs and a board object as an input it draws the labels to their respective boards

    draw_external_player_panel, this function takes self, player_game_panel as an input and draws the player game_panel as well as its buttons to the virtual screen

    highlight_selected_square_placingShips, this function takes the board object and ship_coords_to_be list as inputs. it changes the colour of the tiles on ship_coords_to_be_list i could have probably done this 
                                            in the tile class also 0.75 is hardcoded so it should probably be a constant in the configs class so the user can change it. this function only changes the colour of   
                                            tiles on the player board

    highlight_selected_square, this function takes board object and grid_pos tuple as inputs. it changes the colour of an individual tile only on the enemy board. i probably should have mashed the above function
                                with this function
    """

    def __init__(self, virtual_screen, window):

        self.virtual_screen = virtual_screen
        self.window = window

    # misc renders

    def virtualToReal_window(self, baseConfigs):

        self.window.blit(pygame.transform.smoothscale(self.virtual_screen, baseConfigs.RESOLUTION), (0, 0))

    # main menu renders

    def draw_mainMenu(self, baseConfigs, mainMenu):
        
        # draw buttons

        # this visualises the collidepoint for the rect text
        #for button in buttons:
        #    pygame.draw.rect(virtual_screen, baseConfigs.BUTTON_COLOUR, button)

        # text on buttons

        self.virtual_screen.blit(mainMenu.menu_bg, (0, 0))


        for index, button in enumerate(mainMenu.buttons): # so the text should be the same as the buttons and if its not then theres an issue here

            try:

                currentButtonText = mainMenu.text[index]
                currentButtonPosition = currentButtonText.get_rect(center = button.center)

                self.virtual_screen.blit(currentButtonText, currentButtonPosition)

            except:
                print("more text then buttons, error in draw_mainMenu")
                exit()


        # draw the battleships cover image

        x_coordinate = baseConfigs.VIRTUAL_SURFACE[0] - (mainMenu.cover_image.get_size()[0] - mainMenu.cover_image.get_size()[0] * 0.075)
        y_coordinate = baseConfigs.VIRTUAL_SURFACE[1] - mainMenu.cover_image.get_size()[1]
    
        self.virtual_screen.blit(mainMenu.cover_image, (x_coordinate, y_coordinate))

    # end screen renders
    def draw_endScreen(self, baseConfigs, endScreen):

        x_text = baseConfigs.END_TEXT_X_MARGIN

        # draw end screen text
                # its 0 because there should only be 1 text so 0 index (you win or you lose)
        y_text = (0 * baseConfigs.FONT_SIZE) + baseConfigs.END_TEXT_Y_MARGIN
        self.virtual_screen.blit(endScreen.finalEndText, (x_text, y_text))

        # draw return rect

        x_rect = baseConfigs.VIRTUAL_SURFACE[0] 
        y_rect = baseConfigs.VIRTUAL_SURFACE[1]

        endScreen.returnRect.bottomright = (x_rect, y_rect)
        pygame.draw.rect(self.virtual_screen, baseConfigs.BUTTON_COLOUR, endScreen.returnRect)

        # draw return text
                
        pos = endScreen.rectText.get_rect(center = endScreen.returnRect.center)
        self.virtual_screen.blit(endScreen.rectText, pos)

    # help screen renders
    def draw_helpScreen(self, baseConfigs, helpMenu):

        x_text = baseConfigs.HELP_TEXT_X_MARGIN

        # draw help screen text

        for index, text in enumerate(helpMenu.helpText):

            y_text = (index * baseConfigs.FONT_SIZE) + baseConfigs.HELP_TEXT_Y_MARGIN
            self.virtual_screen.blit(text, (x_text, y_text))

        # draw return rect

        x_rect = baseConfigs.VIRTUAL_SURFACE[0] 
        y_rect = baseConfigs.VIRTUAL_SURFACE[1]

        helpMenu.returnRect.bottomright = (x_rect, y_rect)
        pygame.draw.rect(self.virtual_screen, baseConfigs.BUTTON_COLOUR, helpMenu.returnRect)

        # draw return text
                
        pos = helpMenu.rectText.get_rect(center = helpMenu.returnRect.center)
        self.virtual_screen.blit(helpMenu.rectText, pos)

    # battleship renders
    
    def fill_screen(self, baseConfigs):
        
        self.virtual_screen.fill(baseConfigs.SCREEN_COLOUR) # background colour of battleships game 

    def draw_board(self, board): # takes board object as input and draws it to screen
                
        pygame.draw.rect(self.virtual_screen, board.backBoard_colour, board.back_board) 

        for row in board.grid: # the tilemap should is a square so this will work if its no longer a square there is an error here
            for tile in row:
                
                pygame.draw.rect(self.virtual_screen, tile.colour, tile.rect)

    def draw_labels(self, baseConfigs, board): # takes board object and configs object and displays it to screen
    
        board_x_origin, board_y_origin = board.origin

        for row in board.grid: # the tilemap should is a square so this will work if its no longer a square there is an error here
            for tile in row:
                if tile.rect.y == board_y_origin:

                    columnIndex = (tile.rect.x - board_x_origin) // baseConfigs.LINE_WIDTH_X
                    currentLetter = board.rendered_letters[columnIndex]
                    currentLetterPosition = currentLetter.get_rect(center = tile.rect.center)

                    self.virtual_screen.blit(currentLetter, currentLetterPosition)

                if tile.rect.x == board_x_origin:

                    rowIndex = (tile.rect.y - board_y_origin) // baseConfigs.LINE_WIDTH_Y
                    currentNumber = board.rendered_numbers[rowIndex]
                    currentNumberPosition = currentNumber.get_rect(center = tile.rect.center)
                    self.virtual_screen.blit(currentNumber, currentNumberPosition)

    def draw_external_player_panel(self, player_game_panel):

        # draw back panel and ready button

        pygame.draw.rect(self.virtual_screen, player_game_panel.back_board_panel_colour, player_game_panel.back_board_panel)
        pygame.draw.rect(self.virtual_screen, player_game_panel.ready_button_colour, player_game_panel.ready_button)

        # draw ready button text

        pos = player_game_panel.rendered_ready_text.get_rect(center = player_game_panel.ready_button.center)
        self.virtual_screen.blit(player_game_panel.rendered_ready_text, pos)

        # draw battleship icons
        for battleship_rect in player_game_panel.battleship_rects:
            pygame.draw.rect(self.virtual_screen, battleship_rect.colour, battleship_rect.rect)
    
    def highlight_selected_square_placingShips(self, board, ship_coords_to_be):

        for x, y in ship_coords_to_be:                
            pygame.draw.rect(self.virtual_screen, (board.grid[y][x].colour[0] * 0.75, board.grid[y][x].colour[1] * 0.75, board.grid[y][x].colour[2] * 0.75), board.grid[y][x].rect)
        
    def highlight_selected_square(self, board, grid_pos):

        x, y = grid_pos
        pygame.draw.rect(self.virtual_screen, ((board.grid[y][x].colour[0] * 0.75, board.grid[y][x].colour[1] * 0.75, board.grid[y][x].colour[2] * 0.75)), board.grid[y][x].rect)

class Battleships:
    """
    this class is used in the setup phase. i think its okay being a class because it can be reused when restarting the everything
    it uses

    player_gameBoard, this is the player board object
    player_gamePanel, this is the player panel object
    render, this renders things its the render class object
    grid, this is the grid derived from the player board object
    battleship_rects, ths is derived from the palyer_gamePanel
    battleship_object, this is the current battleship object the player is "holding". the player holds a battleship by clicking on the respective icon. if there is no icon its None
    placed_ship_types, this is the ships placed. i used a set to avoid duplication so the same ship cant be placed multiple times

    get_tile_battleShipGame, function this takes baseConfigs as an input and sometimes specific coordinates (if no specific coords its None). 
                             it returns the grid_pos of the tile clicked on or none if there was no tile. 
                             given coordinates is a useless parameter because i always call this function using realToVirtual_mouse so i dont think it makes any difference and can be removed

    place_ship, this function takes baseConfigs, ship_object, start_pos and place_ship as parameters.
                it returns false if the ship is out of bounds (false placement)
                it returns true if the ship is successfully placed 
                it returns the ship coords if the ship is overlapping with another ship (to colour in the overlapping tile)
    
    highlight_selected_square_placingShips, this function takes baseConfigs and ship_coords_to_be as inputs. its the logic behind the rendering in the render class it does not return anything

    draw_battleship_screen, this function takes baseConfigs as an input and calls all of the rendering functions

    running_battleships_setup, this function takes baseConfigs, events as input it controls what happens in the setup phase.
                                it returns "battleships_game_setup" if nothing has happened
                                it returns "battleShips_game" if the player has placed all ships and pressed the ready button

    get_playerGrid, this function takes nothing as an input and returns the player grid. i dont think i used this i forgot i added it, probably should have instead of .grid this also might have been better in boards???
    """

    def __init__(self, player_gameBoard, player_gamePanel, render):

        self.player_gameBoard = player_gameBoard
        self.player_gamePanel = player_gamePanel

        self.render = render

        self.grid = player_gameBoard.grid
        self.battleship_rects = player_gamePanel.battleship_rects
        self.battleship_object = None
        self.placed_ship_types = set()

    def get_tile_battleShipGame(self, baseConfigs, givenCoordinates = None): # returns the tile that the mouse cursor is on as a class object if given coordinates returns class object touching coordinates
   
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

            return self.grid[grid_y_coordinates][grid_x_coordinates]
    
        else:
            return None
    
    def place_ship(self, baseConfigs, ship_object, start_pos, place_ship = True): # THE GRIDS ORIGIN (upper leftmost tile IS ALWAYS (1, 1) AND LAST POINT IS (GAMEBOARD_SIZE - 1, GAMEBOARD_SIZE - 1))

        ship_object.ship_starting_pos = start_pos
        ship_coords_to_be = ship_object.get_coords_ship_is_on()

        for coord in ship_coords_to_be: # iterate through each coord the ship will be on

            if not ((1 <= coord[0] < baseConfigs.GAME_BOARD_SIZE) and (1 <= coord[1] < baseConfigs.GAME_BOARD_SIZE)):
                return False # the ship will be out of bounds
        
            if self.grid[coord[1]][coord[0]].ship != None: # overlap
 
                self.grid[coord[1]][coord[0]].colour = baseConfigs.OVERLAP_COLOUR
                place_ship = False 


        if place_ship == True:    
            for x, y in ship_coords_to_be:

                self.grid[y][x].ship = ship_object
    
            return True # successful placement
    
        else:
            return ship_coords_to_be

    def highlight_selected_square_placingShips(self, baseConfigs, ship_coords_to_be):

        acceptable_coords = []
        placement = True

        for y in range(baseConfigs.GAME_BOARD_SIZE):
            for x in range(baseConfigs.GAME_BOARD_SIZE):
                if not (self.grid[y][x].grid_pos[0] == 0 or self.grid[y][x].grid_pos[1] == 0):
                    
                        acceptable_coords.append((self.grid[y][x].grid_pos))

        for current_coord in ship_coords_to_be:
        
            if current_coord not in acceptable_coords:
            
                placement = False

        if placement == True:

            self.render.highlight_selected_square_placingShips(self.player_gameBoard, ship_coords_to_be)

    def draw_battleship_screen(self, baseConfigs): # draw player board to screen

        self.render.fill_screen(baseConfigs)
        self.render.draw_board(self.player_gameBoard)
        self.render.draw_labels(baseConfigs, self.player_gameBoard)

        self.render.draw_external_player_panel(self.player_gamePanel)

    def running_battleships_setup(self, baseConfigs, events):


        self.player_gameBoard.update_board()
        self.draw_battleship_screen(baseConfigs)
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
            
                if event.button == 1: # left click 

                    for battleship_rect in self.battleship_rects: # choose a ship to place
                        if battleship_rect.rect.collidepoint(realToVirtual_mouse(baseConfigs)):
                            if battleship_rect.boat_type not in self.placed_ship_types:
                                self.battleship_object = battleship_rect.boat_type()

                if self.battleship_object is not None:
                    tile = self.get_tile_battleShipGame(baseConfigs, realToVirtual_mouse(baseConfigs))
                    
                    if tile is not None:
                        placed = self.place_ship(baseConfigs, self.battleship_object, tile.grid_pos)

                        if placed is True:
                            self.placed_ship_types.add(type(self.battleship_object))
                            
                            for battleship_icon in self.battleship_rects:
                                if battleship_icon.boat_type == getattr(self, "battleship_object").type:
                                    battleship_icon.colour = baseConfigs.USED_ICON_COLOUR

                            self.battleship_object = None
                
                if len(self.placed_ship_types) == baseConfigs.MAX_ALLOWED_SHIPS and \
                self.player_gamePanel.ready_button.collidepoint(realToVirtual_mouse(baseConfigs)):
                    
                    return "battleShips_game"


            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_r: #if key r down, rotate ship

                    if not (self.battleship_object) == None:
                        self.battleship_object.rotated = not self.battleship_object.rotated # change this to like better at saomepoint also prolly make it so it can rotate 360 degrees not just rotate between horizontal and vertical


        # preview of ship object before placing 
        if not (self.battleship_object == None):
            if self.get_tile_battleShipGame(baseConfigs, realToVirtual_mouse(baseConfigs)) != None:
                placeship = self.place_ship(baseConfigs, self.battleship_object, (self.get_tile_battleShipGame(baseConfigs, realToVirtual_mouse(baseConfigs))).grid_pos, False)

                if type(placeship) != bool:
                    self.highlight_selected_square_placingShips(baseConfigs, placeship)


        return "battleships_game_setup"
    
    def get_playerGrid(self):
        return self.player_gameBoard

class EnemySetup:
    """
    this class is what sets up the enemy board. its a class so a new object can be created when all the boards are reset. it takes the enemy board as an input
    enemy_gameBoard, this is the enemy game board
    grid, this is the enemy grid
    shipsToPlace, these are the unplaced ships of the enemy. its a hardcoded constant which should be changed as now if the user changes the amount of ships to place then its not going to change what the enemy places
                    good thing i didnt add that
    
    AI_ship_placement, this function takes baseConfigs as an input it returns the placed enemy ships
    updating_enemyGrid, this function takes baseConfigs as an input. it places the ships returned from AI_ship_placement
    get_Enemy, this returns the enemy board
    """

    def __init__(self, enemy_gameBoard):
        
        self.enemy_gameBoard = enemy_gameBoard
        self.grid = enemy_gameBoard.grid
        self.shipsToPlace = [Carrier, Battleship, Cruiser, Submarine, Destroyer]

    def AI_ship_placement(self, baseConfigs):

        unplaced = True
        enemy_ships = []
        enemy_ship_coords = []

        while unplaced:

            shipChosen = random.randint(0, len(self.shipsToPlace)-1) # choose a random ship from shipsToPlace

            row = random.randint(1, baseConfigs.GAME_BOARD_SIZE -1 ) # choose a random row on the grid
            column = random.randint(1, baseConfigs.GAME_BOARD_SIZE - 1) # choose a random column on the grid
            rotation = random.randint(0, 1) # 0 = Vertical, 1 = Horizontal

            if rotation == 1:
                rotation = True
            else:
                rotation = False

            new_ship = self.shipsToPlace[shipChosen]()

            new_ship.ship_starting_pos = (column, row)
            new_ship.rotated = rotation

            new_ship_coords = new_ship.get_coords_ship_is_on()

            placement = "valid"

            for x, y in new_ship_coords:

                if not (1 <= x < baseConfigs.GAME_BOARD_SIZE) or not (1 <= y < baseConfigs.GAME_BOARD_SIZE): #if ship is out of bounds
                    placement = "invalid"
                
                elif (x, y) in enemy_ship_coords:
                    placement = "invalid"
                
            if placement == "invalid":
                pass

            else:
                enemy_ships.append(new_ship)
                enemy_ship_coords.extend(new_ship.get_coords_ship_is_on())

                self.shipsToPlace.pop(shipChosen)
            
            if len(enemy_ships) == baseConfigs.MAX_ALLOWED_SHIPS:
                unplaced = False

        return enemy_ships

    def updating_enemyGrid(self, baseConfigs):

        enemy_ships = self.AI_ship_placement(baseConfigs)
        for ship in enemy_ships:

            ship_coords = ship.get_coords_ship_is_on()
            
            for x, y in ship_coords:

                self.grid[y][x].ship = ship
    
    def get_Enemy(self):
        return self.enemy_gameBoard

class End:
    """
    this is the end screen 

    baseConfigs, its constants
    filePaths, its where the files are stored
    render, it renders things
    finalEndText, what the text at the end is 

    create_endScreen, takes baseConfigs as an input returns RENDERED_TEXT, RENDERED_RETURN_TEXT, returnRect
    RENDERED_TEXT, this is the text displayed at the end either "you win" or "you lose"
    RENDERED_RETURN_TEXT, this is the text which is displayed over the returnRect 
    returnRect, this is the rect to return to the main menu when clicked

    draw_endScreen, function it calls the render functions from the render object it takes baseConfigs as an input
    display_endMenu, function takes inputs: baseConfigs, events, victor. returns "end_screen" if the returnRect is clicked and "new_game" otherwise

    """

    def __init__(self, baseConfigs, filePaths, render):

        self.filePaths = filePaths
        self.render = render

        self.endText, self.rectText, self.returnRect = self.create_endScreen(baseConfigs)

        # this is what is displayed to screen at the end
        self.finalEndText = None
    
    def create_endScreen(self, baseConfigs):
    
        # create the end text

        font = pygame.font.Font(self.filePaths.font, baseConfigs.FONT_SIZE)

        # "" are spaces inbetween text blocks
        end_text = {
            "win" : "You win",
            "lose" : "You lose",
            }
        
        RENDERED_TEXT = {
            "win" : font.render(end_text["win"], True, baseConfigs.END_SCREEN_TEXT_COLOUR),
            "lose" : font.render(end_text["lose"], True, baseConfigs.END_SCREEN_TEXT_COLOUR)
            }

        # return rect text

        text = "Return"

        RENDERED_RETURN_TEXT = font.render(text, True, baseConfigs.END_SCREEN_TEXT_COLOUR)

        # create the return to main menu rectangle

        returnRect = pygame.Rect(0, 0, baseConfigs.TILE_SIZE * 6, baseConfigs.TILE_SIZE * 2)

        return RENDERED_TEXT, RENDERED_RETURN_TEXT, returnRect
    
    def draw_endScreen(self, baseConfigs):

        self.render.fill_screen(baseConfigs)
        self.render.draw_endScreen(baseConfigs, self)
    
    def display_endMenu(self, baseConfigs, events, victor):
        
        self.finalEndText = self.endText[victor]
        self.draw_endScreen(baseConfigs)

        for event in events:
            
            if event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:

                    if self.returnRect.collidepoint(realToVirtual_mouse(baseConfigs)) == True:
                        
                        return "new_game"
        return "end_screen"

class Help:
    """
    this is the help screen 

    baseConfigs, its constants
    filePaths, its where the files are stored
    render, it renders things

    create_helpScreen, takes baseConfigs as an input returns RENDERED_TEXT, RENDERED_RETURN_TEXT, returnRect
    helpText, this is a lot of text which lists basic instructions on how to play
    rectText, this is the text which is displayed over the returnRect 
    returnRect, this is the rect to return to the main menu when clicked

    draw_helpScreen, function it calls the render functions from the render object it takes baseConfigs as an input
    display_helpMenu, function takes inputs: baseConfigs, events. returns "mainMenu" if the returnRect is clicked and "help" otherwise

    """

    def __init__(self, baseConfigs, filePaths, render):

        self.filePaths = filePaths
        self.render = render

        self.helpText, self.rectText, self.returnRect = self.create_helpScreen(baseConfigs)
    
    def create_helpScreen(self, baseConfigs):
    
        # create the help text

        font = pygame.font.Font(self.filePaths.font, baseConfigs.FONT_SIZE)

        # "" are spaces inbetween text blocks
        help_text = ["Your board is the board on the left.",
                    "Your enemies board is on the right.",
                    "",
                    "To select a ship to place left click on a blue square. That ship is now selected.",
                    "In the base game, each ship can only be placed once.",
                    "Press R to rotate a ship",
                    "After placing all of your ships, press the green rectangle.",
                    "Click on a tile on the right board to attack it",
                    "", 
                    "A yellow square corresponds to a hit tile with a ship on it.",
                    "A light blue square corresponds to a hit tile with no ship on it."
                    ]
        
        RENDERED_TEXT = [font.render(text, True, baseConfigs.HELP_TEXT_COLOUR) for text in help_text]

        # return rect text

        text = "Return"

        RENDERED_RETURN_TEXT = font.render(text, True, baseConfigs.HELP_TEXT_COLOUR)

        # create the return to main menu rectangle

        returnRect = pygame.Rect(0, 0, baseConfigs.TILE_SIZE * 6, baseConfigs.TILE_SIZE * 2)

        return RENDERED_TEXT, RENDERED_RETURN_TEXT, returnRect
    
    def draw_helpScreen(self, baseConfigs):

        self.render.fill_screen(baseConfigs)
        self.render.draw_helpScreen(baseConfigs, self)
    
    def display_helpMenu(self, baseConfigs, events):

        self.draw_helpScreen(baseConfigs)

        for event in events:
            
            if event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:

                    if self.returnRect.collidepoint(realToVirtual_mouse(baseConfigs)) == True:
                        
                        return "mainMenu"
        return "help"
        
class MainMenu:
    """
    this is the main menu class object it takes baseconfigs filepaths and render as inputs
    filepaths, its filepaths
    render, its render

    create_mainMenu, it takes baseConfigs and filePaths as inputs it returns
    BUTTONS, the buttons displayed to the main menu
    COVER_IMAGE, the cover image displayed on the main menu from file paths
    RENDERED_TEXT, the text displayed over buttons 
    RENDERED_TEXT_HIGHLIGHTED, the same text displayed over buttons in a different colour. i wanted to change the colour when a user hovered their mouse over the text but never got round to it
    RENDERED_GAMENAME,  this is the text which should be displayed it says battleships to tell you what youre playing. i dont think i got round to finishign this
    MENU_BG, this is the background iamge of menu scaled to the virtual screne res

    draw_mainMenu takes baseconfigs as input draws things to screen
    get_button_mainMenu, function takes baseConfigs, buttons as inputs. returns the list index of the button clicked

    running_mainMenu takes baseConfigs + events as inputs returns :
        battleships_game_setup 
        settings
        help
        quit
        dependent on the button clicked and mainMenu otherwise
    """

    def __init__(self, baseConfigs, filePaths, render):

        self.filePaths = filePaths
        self.buttons, self.cover_image, self.text, self.highlighted_text, self.rendered_gamename, self.menu_bg = self.create_mainMenu(baseConfigs, filePaths)
        self.render = render

    def create_mainMenu(self, baseConfigs, filePaths):

        #create buttons

        BUTTONS = []

        for button_num in range(4):

            BUTTONS.extend([pygame.Rect(baseConfigs.BUTTON_X_ORIGIN, baseConfigs.BUTTON_Y_ORIGIN + baseConfigs.BUTTON_SPACING * button_num, baseConfigs.BUTTON_SIZE * 4, baseConfigs.BUTTON_SIZE)]) # maybe make the *4 scale to the resolution at some point
    
        # render more text + working on

        mainName = "Battleships"
        font = pygame.font.Font(self.filePaths.font, baseConfigs.GAMENAME_FONT_SIZE)

        RENDERED_GAMENAME = font.render(mainName, True, baseConfigs.GAMENAME_COLOUR)

        # render the button text
    
        buttonText = ["Play", "Settings", "Help", "Quit"] #put this in the baseConfig folder?
        font = pygame.font.Font(self.filePaths.font, baseConfigs.FONT_SIZE)

        RENDERED_TEXT = [font.render(text, True, baseConfigs.TEXT_COLOUR) for text in buttonText]
        RENDERED_TEXT_HIGHLIGHTED = [font.render(text, True, baseConfigs.HIGHLIGHTED_TEXT_COLOUR) for text in buttonText]
                        
        #load image into memory or something

        COVER_IMAGE = pygame.image.load(filePaths.battleships_homescreen).convert_alpha()
        COVER_IMAGE = pygame.transform.scale(COVER_IMAGE, (baseConfigs.VIRTUAL_SURFACE[0] * 0.4, baseConfigs.VIRTUAL_SURFACE[1] * 0.6))

        MENU_BG = pygame.image.load(filePaths.ocean_bg).convert()
        MENU_BG = pygame.transform.scale(MENU_BG, baseConfigs.VIRTUAL_SURFACE)

        return BUTTONS, COVER_IMAGE, RENDERED_TEXT, RENDERED_TEXT_HIGHLIGHTED, RENDERED_GAMENAME, MENU_BG

    def draw_mainMenu(self, baseConfigs):
        
        self.render.draw_mainMenu(baseConfigs, self)

    def get_button_mainMenu(self, baseConfigs, buttons):

        for index, button in enumerate(buttons):
        
            if button.collidepoint(realToVirtual_mouse(baseConfigs)) == True:
            
                return index
            
    def running_mainMenu(self, baseConfigs, events):

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
        
                if event.button == 1:
            
                    buttonChosen = self.get_button_mainMenu(baseConfigs, self.buttons)

                    if buttonChosen == 0:              
                        return "battleships_game_setup"
                
                    elif buttonChosen == 1:
                        return "settings"
                
                    elif buttonChosen == 2:
                        return "help"

                    elif buttonChosen == 3:
                        return "quit"
            
        self.draw_mainMenu(baseConfigs)

        return "mainMenu"

class Match():
    """
    render, this is render
    animation, this is a list of all the sprites from the spritesheet
    last_update, this is when the sprites were last updated
    frame, this is the current frame of the explosion animation
    animation_pos, this is the position of the animation, None otherwise
    animating, True if there are explosions being animated, False otherwise
    enemy, this is the entire enemy_setup object
    enemy_gameBoard, this is the enemy game board
    possible_player_coords, this is every possible coord a ship could be on 
    player_gameBoard, this is the player game board
    turnOver, this is if the player has made a move
    sound, its the sound object

    enemy_turn function, takes nothing as an input it randomly selects a coord from possible_player_coords to hit
    player_turn, takes baseConfigs as an input it returns "valid" if the player successfully makes a move

    animate_clicksOnShip, function, it takes baseconfigs as an input and animates through the animation (returns nothing)
    render_screen it calls all of the rendering functions

    check_wins, function, returns :
        "end_screen", "win", if the enemy runs out of ship tiles
        "end_screen", "lose", if the player runs out of ship tiles
        None, if nothing has happened

    order_of_instructions takes baseConfigs and events as inputs it returns :
        "battleShips_game", None, it returns if nothing is happening (via checkwins). None is returned as no one has won yet



    """

    def __init__(self, baseConfigs, explosion_sprites, enemy_setup, battleship, sound, render):

        self.render = render

        # animations ,frame is the current frame of the animation, 64 is the size of each sprite (fixed), baseConfigs.TILE_SIZE is what the size of each sprite is being changed to
        self.animation = [explosion_sprites.get_img(frame, 64, 64, baseConfigs.TILE_SIZE, baseConfigs.COLOURKEY_EXPLOSIONS) # baseConfigs.COLOURKEY_EXPLOSIONS is the colour thats becoming transparent
                                                                                                    # % 64 removes sprite sheet padding // 64 gets how many sprites are in spritesheet
                           for frame in range((explosion_sprites.sprite_sheet.get_rect().width - (explosion_sprites.sprite_sheet.get_rect().width % 64)) // 64)

                           ]
        self.last_update = pygame.time.get_ticks()
        self.frame = 0
        self.animation_pos = None
        self.animating = False

        # enemy 

        self.enemy = enemy_setup

        self.enemy.AI_ship_placement(baseConfigs)
        self.enemy.updating_enemyGrid(baseConfigs)
        self.enemy_gameBoard = self.enemy.get_Enemy()

        self.possible_player_coords = []
        for x in range(1, baseConfigs.GAME_BOARD_SIZE): 
            for y in range(1, baseConfigs.GAME_BOARD_SIZE):
                self.possible_player_coords.append((x, y))      

        # player

        self.player_gameBoard = battleship.player_gameBoard
        self.turnOver = False

        # sound

        self.sound = sound

    def enemy_turn(self):
        
        chosenCords = random.randint(0, len(self.possible_player_coords) - 1) # prolly add a weighting system and change everything else
        # like give each tile a variable self.weight = 1 and when its hit and its a ship increase the weight around it to like self.weight = 1 and everything else self.weight = 0
        grid_pos = self.possible_player_coords[chosenCords]
        self.possible_player_coords.pop(chosenCords)

        for row in self.player_gameBoard.grid:
            for tile in row:

                if tile.grid_pos == grid_pos:
                    tile.hit = True

                    if tile.ship != None:

                        tile.ship.hitTiles += 1

                        self.animating = True
                        self.sound.play_explosion()
                        self.animation_pos = tile.rect.topleft

    def player_turn(self, baseConfigs):
        
        for row in self.enemy_gameBoard.grid:
            for tile in row:

                if (tile.rect.collidepoint(realToVirtual_mouse(baseConfigs))) == True \
                    and (tile.hit == False) \
                    and ( 1 <= tile.grid_pos[0] < baseConfigs.GAME_BOARD_SIZE) \
                    and ( 1 <= tile.grid_pos[1] < baseConfigs.GAME_BOARD_SIZE): # prevents player from hitting out of bounds + prevents player from hitting already hit squares
                    
                    tile.hit = True

                    if tile.ship != None:
                        tile.ship.hitTiles += 1

                    if tile.rect.collidepoint(realToVirtual_mouse(baseConfigs)) == True and tile.ship != None:
                        
                        self.animating = True
                        self.sound.play_explosion()
                        self.animation_pos = tile.rect.topleft

                    return "valid"
                
    
    def animate_clicksOnShip(self, baseConfigs):

        animation_cd = baseConfigs.ANIMATION_CD

        current_time = pygame.time.get_ticks()

        if current_time - self.last_update >= animation_cd:

            self.frame += 1
            self.last_update = current_time

            if self.frame == len(self.animation):

                self.frame = 0 
                self.animating = False

    def render_screen(self, baseConfigs):
        
        self.render.fill_screen(baseConfigs) # to wipe old screen
        self.render.draw_board(self.player_gameBoard)                # draws player board to screen
        self.render.draw_labels(baseConfigs, self.player_gameBoard)

        self.render.draw_board(self.enemy_gameBoard)                    # draws enemy board to screen
        self.render.draw_labels(baseConfigs, self.enemy_gameBoard)

        for row in self.enemy_gameBoard.grid:
            for tile in row:

                if tile.rect.collidepoint(realToVirtual_mouse(baseConfigs)) == True \
                and 1 <= tile.grid_pos[0] < baseConfigs.GAME_BOARD_SIZE \
                and 1 <= tile.grid_pos[1] < baseConfigs.GAME_BOARD_SIZE:
                    
                    self.render.highlight_selected_square(self.enemy_gameBoard, (tile.grid_pos))
        
        if self.animating == True:
            self.animate_clicksOnShip(baseConfigs)
            self.render.virtual_screen.blit(self.animation[self.frame], self.animation_pos)


    
    def check_wins(self):

        shipTilesLeft_enemy = 0

        for row in self.enemy_gameBoard.grid:
            for tile in row:

                if (tile.ship != None) and (tile.hit == False):

                    shipTilesLeft_enemy += 1

        shipTilesLeft_player = 0

        for row in self.player_gameBoard.grid:
            for tile in row:

                if (tile.ship != None) and (tile.hit == False):
                    shipTilesLeft_player += 1

        if shipTilesLeft_enemy == 0:
            
            return "end_screen", "win" 
            
        elif shipTilesLeft_player == 0:

            return "end_screen", "lose"

        else:
            return None                
                
    def order_of_instructions(self, baseConfigs, events):

        self.enemy_gameBoard.update_board()
        self.player_gameBoard.update_board()
        self.render_screen(baseConfigs)

        validity = "invalid"
        if not self.animating: # only allow a player to click when an animation isnt happening
            for event in events:

                if event.type == pygame.MOUSEBUTTONDOWN:

                    if event.button == 1:
                        
                        validity = self.player_turn(baseConfigs)
                        # if player successfully hits an enemy tile that hasnt been hit yet then turn over
                        if validity == "valid":
                            self.turnOver = True
                
        if getattr(self, "turnOver") and self.animating == False:

            self.enemy_turn()
            self.turnOver = False
        
        
        if self.check_wins() != None and self.animating == False:

            return self.check_wins()
          
        return "battleShips_game", None

class displayed_screen():
    """
    
    render, it renders things its the rendering object
    window, its the user res window
    virtual_screen, its the pretend window which is actually a surface object

    # different screens

    mainMenu, its the mainMenu object
    battleships, its the battleship object
    gameMatch, its the match object
    help, its the help object
    end_screen, its the end_screen object
    
    victor, its who won. None otherwise
    sound, its the sound object
    
    state, its the current state
    running, its if the window is running or not, True or False its a boolean

    run takes baseConfigs, filePaths, explosion_sprites as inputs. its the state controller


    """
    
    def __init__(self, window, virtual_screen, mainMenu, battleships, gameMatch, help, end_screen, sound, render):

        # renders stuff (needed to scale the res to user screen)

        self.render = render

        # displayed and virtual screens

        self.window = window
        self.virtual_screen = virtual_screen

        # different game screens

        self.mainMenu = mainMenu
        self.battleships = battleships
        self.gameMatch = gameMatch
        self.help = help
        self.end_screen = end_screen
        
        # data between screens

        self.victor = None

        # sound

        self.sound = sound

        # running and screen states
        self.state = "mainMenu"
        self.running = True
    
    def run(self, baseConfigs, filePaths, explosion_sprites):

        while self.running == True:

            events = pygame.event.get()

            for event in events:

                if event.type == pygame.QUIT:
                    self.running = False
                
                if event.type == pygame.VIDEORESIZE:

                    baseConfigs.RESOLUTION = event.size
                    self.window = pygame.display.set_mode(baseConfigs.RESOLUTION, pygame.RESIZABLE)

            match self.state:

                case "mainMenu":
                    
                    self.state = self.mainMenu.running_mainMenu(baseConfigs, events)

                case "battleships_game_setup":

                    self.state = self.battleships.running_battleships_setup(baseConfigs, events)
            
                case "battleShips_game":

                    self.state, self.victor = self.gameMatch.order_of_instructions(baseConfigs, events)
            
                case "help":

                    self.state = self.help.display_helpMenu(baseConfigs, events)

                case "settings":

                    print("Add settings later")
                    self.state = "mainMenu"

                case "end_screen":

                    self.state = self.end_screen.display_endMenu(baseConfigs, events, self.victor)

                case "quit":

                    self.running = False

                case "new_game":

                    self.battleships, self.gameMatch = newGame(baseConfigs, filePaths, self.render, explosion_sprites, self.sound)
                    self.state = "mainMenu"
    

                case _:


                    print("error invalid game_state")
                    exit()
                
            
                
            self.render.virtualToReal_window(baseConfigs)
            pygame.display.update()

        exit()

# this maps the window mouse coords to the virtual res mouse coords
def realToVirtual_mouse(baseConfigs): # takes resolution as input and returns x and y mouse coordinates as tuple

    mouse_x_coordinates, mouse_y_coordinates = pygame.mouse.get_pos()

    virtual_x_coordinates = int(round(mouse_x_coordinates * (baseConfigs.VIRTUAL_SURFACE[0] / baseConfigs.RESOLUTION[0])))
    virtual_y_coordinates = int(round(mouse_y_coordinates * (baseConfigs.VIRTUAL_SURFACE[1] / baseConfigs.RESOLUTION[1])))

    return (virtual_x_coordinates, virtual_y_coordinates)

# recreate all the necessary objects inorder to start a new game
def newGame(baseConfigs, filePaths, render, explosion_sprites, sound):

    player_gameBoard = Board(baseConfigs, filePaths, is_enemy = False)                                     # create the player board
    enemy_gameBoard  = Board(baseConfigs, filePaths, is_enemy = True)                                      # create the enemy board
    player_gamePanel = Panel(baseConfigs, filePaths, player_gameBoard.back_board, player_gameBoard.origin) # create player selection panel

    battleship       = Battleships(player_gameBoard, player_gamePanel, render)         # battleship screen
    enemy_setup      = EnemySetup(enemy_gameBoard)                                     # enemy setup time



    game_match       = Match(baseConfigs, explosion_sprites, enemy_setup, battleship, sound, render)             # playing against the AI

    return battleship, game_match

def loadStartUp():

    pygame.init()                                                               #initalise pygame

    filePaths = FilePaths()                                                     # creates file paths preset
    baseConfigs = Configs()                                                     # creates config preset     / maybe make read from a file

    sound = Sound(filePaths.explosion_sound, filePaths.background_music)
    sound.startUP()

    window = pygame.display.set_mode(baseConfigs.RESOLUTION, pygame.RESIZABLE)  # create display window
    virtual_screen = pygame.Surface(baseConfigs.VIRTUAL_SURFACE)                # create fixed window
    gameIcon = pygame.image.load(filePaths.battleships_icon)                    # load window icon

    render = Renderer(virtual_screen, window)
    explosion_sprites = SpriteSheet(filePaths.explosion_spritesheet)

    pygame.display.set_icon(gameIcon)                                           # display the game icon
    pygame.display.set_caption("Battleships")                                   # name the window icon

    mainMenu = MainMenu(baseConfigs, filePaths, render)                         # create the main menu
    help_Menu        = Help(baseConfigs, filePaths, render)                     # create the help menu
    end_screen = End(baseConfigs, filePaths, render)                            # create the end screen

    battleship, game_match = newGame(baseConfigs, filePaths, render, explosion_sprites, sound)

    game = displayed_screen(window, virtual_screen, mainMenu, battleship, game_match, help_Menu, end_screen, sound, render) # creates game controller
    game.run(baseConfigs, filePaths, explosion_sprites)                                                               # runs the game

loadStartUp()
