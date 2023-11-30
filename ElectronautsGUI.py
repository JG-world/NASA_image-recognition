
from cgitb import text
from pkgutil import get_loader
import serial
import pygame
import math
import time

# Initialize Pygame
pygame.init()

clock = pygame.time.Clock() 

# Set colors
black = (0, 0, 0)
red = (255, 0, 0)
white = (255, 255, 255)
blue = (57, 77, 96)
green = (0, 128, 0)
purp = (128, 0, 128)
# Set up the display
cell_size = 20  # Size of each grid cell
grid_width, grid_height = 40, 30  # Number of grid cells in width and height
width, height = cell_size * grid_width, cell_size * grid_height

# Font and text
font = pygame.font.Font(None, 35)  # You can change the font and size
NoConn = "No Connection."
connecting = "Connecting..."
record = "Record"
start = "Start Rec"
stop = "Stop Rec"
live = "Live"
playback = "Playback"
Exit = "EXIT"



# Calculate the text size and position
text_NoConn = font.render(NoConn, True, black)
text_connecting = font.render(connecting, True, white)
text_rec = font.render(record, True, white)
text_start = font.render(start, True, white)
text_stop = font.render(stop, True, white)
text_live = font.render(live, True, black)
text_playback = font.render(playback, True, white)
text_exit = font.render(Exit, True, white)

#text box
#textBox = pygame.Rect(100,100,140,32)
#inputText = ''
#waiting = True


# Open a text file for writing data
file_path = "TSGC.txt"

# Global Variables
Record = False
Live = True

#enter polar circle
polarC = pygame.image.load('PolarCircle.png')
polarCScale = pygame.transform.scale(polarC,(440,440))
polarC_rect = polarCScale.get_rect()


class CrewMem:
    # The __init__ method is called when an instance of the class is created.
    def __init__(self):
        self.cam = 0  # This attribute stores the person's name.
        self.x = 0  # This attribute stores the person's name.
        self.y = 0    # This attribute stores the person's age.

    # This is a method to greet the person.
    def updateData(self,cam,x,y):
        self.cam = cam  # This attribute stores the person's name.
        self.x = x  # This attribute stores the person's name.
        self.y = y    # This attribute stores the person's age.

# Waits for serial connection from COM4
def Connect():
    global CDBser

    isConnected = True

    while isConnected:

        
        screen.fill(black)
        screen.blit(text_connecting, (150,150))
        #Home Button
        home_button_rect = pygame.draw.rect(screen, red, (600, 420, 120, 50))
        screen.blit(text_exit, (630,435))
        pygame.display.flip()
        time.sleep(1)

        try:
            # Define the serial port and its configuration
            serial_port = "COM4"
            baud_rate = 115200

            # Open the serial port
            CDBser = serial.Serial(serial_port, baud_rate) #Central Data Base Serial
        except:
            screen.fill(white)
            screen.blit(text_NoConn, (150,150))
            #Home Button
            home_button_rect = pygame.draw.rect(screen, red, (600, 420, 120, 50))
            screen.blit(text_exit, (630,435))
            pygame.display.flip()
            time.sleep(1)
        else:
            isConnected = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if home_button_rect.collidepoint(event.pos):
                        Startup()
                        isConnected = False

# Reads from serial and stores it in crewinfo
def readSerial():
      global crewInfo

      try:
            #Read the crew info being sent from the CDB
            crewInfo = CDBser.readline().decode('utf-8')   
      except:
            Connect()
      else:
            if(Record):
                with open(file_path, "a") as file:
                    file.write(crewInfo)

            if crewInfo and len(crewInfo) >= 2:
                if(crewInfo[0] == '0'):
                    
                    UpdateCrew()

                    #converts potion into (x,y) corddintes 
                    xcord1 = (distance1 * 10) * math.cos(math.radians(obsAng1))
                    print(xcord1)
                    ycord1 = (distance1 * 10) * math.sin(math.radians(obsAng1)) 
                    print(ycord1)
                    xcord2 = ((distance2 * 10)) * math.cos(math.radians(obsAng2))
                    print(xcord2)
                    ycord2 = (distance2 * 10) * math.sin(math.radians(obsAng2)) 
                    print(ycord2)

# Creates the background
def CreateBackground():
    #Clear the screen
    screen.fill(black)

    #display boundary circle of radius 20
    #pygame.draw.circle(screen, blue, (220,220), 200)
    #pygame.draw.circle(screen, black, (220,220), 40)
    
    #screen.blit(scaled_image,(0,0))
    screen.blit(polarCScale, (0,0))
                               #(cplor),[center],radius,thickness
    pygame.draw.circle(screen, black, [220, 220], 310, 105)
    pygame.draw.circle(screen, black, (220,221), 40)

    pygame.draw.line(screen, white, (450, 0), (450, height),5)



# Creates the start up menu with Live and Playback button
def Startup():
    running = True
    global Live

    # Creates instances of 4 crew members
    for i in range(1, 5):
        global crewi
        crewi = CrewMem()

    # Stays on home screen until option is chossen
    while running:
        CreateBackground()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("we quit")
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if white_button_rect.collidepoint(event.pos):
                    running = False
                    Live = True
                elif black_button_rect.collidepoint(event.pos):
                    running = False
                    Live = False

        # Draw buttons
        white_button_rect = pygame.draw.rect(screen, white, (455, 50, 120, 50))
        black_button_rect = pygame.draw.rect(screen, blue, (580, 50, 120, 50))

        # Add text to buttons
        font = pygame.font.Font(None, 36)
        screen.blit(text_live, (480, 65))
        screen.blit(text_playback, (590, 65))

        pygame.display.flip()

# Decodes serial data and updates 
def UpdateCrew():
    global patchID1
    global distance1
    global obsAng1
    global asmAng1
    global crewInfo

    global patchID2
    global distance2
    global obsAng2
    global asmAng2

    global patchID3
    global distance3
    global obsAng3
    global asmAng3

    global patchID4
    global distance4
    global obsAng4
    global asmAng4

    print(crewInfo)
    
    #Extracts the data from serial and saves to crew 1
    distance1 = int(crewInfo[1:4]) / 30.48
    obsAng1 = int(crewInfo[4:7])
    asmAng1 = int(crewInfo[7:10])
    print("this is crew1)")
    print(distance1);
    print(obsAng1);
    print(asmAng1);

    #Extracts the data from serial and saves to crew 2
    distance2 = int(crewInfo[10:13]) / 30.48
    obsAng2 = int(crewInfo[13:16])
    asmAng2 = int(crewInfo[16:19])
    print("this is crew2)")
    print(distance2);
    print(obsAng2);
    print(asmAng2);
    #Extracts the data from serial and saves to crew 3
    distance3 = int(crewInfo[19:22]) / 30.48
    obsAng3 = int(crewInfo[22:25])
    asmAng3 = int(crewInfo[25:28])
    print("this is crew3)")
    print(distance3);
    print(obsAng3);
    print(asmAng3);
    #Extracts the data from serial and saves to crew 1
    distance4 = int(crewInfo[28:31]) / 30.48
    obsAng4 = int(crewInfo[31:34])
    asmAng4 = int(crewInfo[34:37])
    print("this is crew4)")
    print(distance4);
    print(obsAng4);
    print(asmAng4);
    
def takeInput():
    #takes input for playback file

    global file_path

    textBox = pygame.Rect(500,240,140,32)
    inputText = ''
    waiting = True
    active = True

    while waiting:
        print("waiting")

        for event in pygame.event.get():
        #if event.type == pygame.MOUSEBUTTONDOWN:
            #if textBox.collidepoint(event.pos):
            #    active = not active
            #else:
            #    active = False
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        file_path = inputText
                        inputText = ''
                        waiting = False
                    elif event.key == pygame.K_BACKSPACE:
                        inputText = inputText[:-1]
                    else:
                        inputText += event.unicode

        txt_surface = font.render(inputText, True, white)
        width = max(200, txt_surface.get_width()+10)
        textBox.w = width
        # Blit the text.
        screen.blit(txt_surface, (textBox.x+5, textBox.y+5))
        # Blit the input_box rect.
        pygame.draw.rect(screen, white, textBox, 2)

        pygame.display.flip()
        clock.tick(30)


#initializing angle values for triangle models later
angle = 0;
angle2 = 0;
angle3 = 0;
angle4 = 0;

#create display
screen = pygame.display.set_mode((750, 500))
pygame.display.set_caption("Crew1 Position Test")

bg = pygame.image.load('HERA1.png')
scaled_image = pygame.transform.scale(bg,(600,600))

test_surface = pygame.image.load('patch1_triangle.png')
test_surface2 = pygame.image.load('patch2_triangle.png')
test_surface3 = pygame.image.load('patch4_triangle.png')
test_surface4 = pygame.image.load('patch3_triangle.png')


scaled_image1 = pygame.transform.scale(test_surface,(50,50))
scaled_image2 = pygame.transform.scale(test_surface2,(50,50))
scaled_image3 = pygame.transform.scale(test_surface3,(50,50))
scaled_image4 = pygame.transform.scale(test_surface4,(50,50))



# print(Live)

Startup()

# print(Live)

TravRow = 0
readInput = True

# main code
while True:
    global CBDser
    global CrewInfo
    global asmAng1
    EOF = False


    # print(Live)

    # print("we in here")
    xcord1 = 10000
    ycord1 = 10000
    xcord2 = 10000
    ycord2 = 10000
    xcord3 = 10000
    ycord3 = 10000
    xcord4 = 10000
    ycord4 = 10000

    if(Live):
        try:
            #Read the crew info being sent from the CDB
            crewInfo = CDBser.readline().decode('utf-8')  
            print(crewInfo)
        except:
            Connect()
        else:
            if(Record):
                with open(file_path, "a") as file:
                    file.write(crewInfo)

            if crewInfo and len(crewInfo) >= 2:
                if(crewInfo[0] == 'x'):
                    
                    UpdateCrew()

                    angle = asmAng1 - 45
                    angle2 = asmAng2 - 45
                    angle3 = asmAng3 - 45
                    angle4 = asmAng4 - 45
    
                   

                    #converts potion into (x,y) corddintes 
                    xcord1 = ((distance1 * 20)) * math.cos(math.radians(obsAng1))-180
                    ycord1 = ((distance1 * 20)) * math.sin(math.radians(obsAng1)) +80
                    xcord2 = ((distance2 * 20)) * math.cos(math.radians(obsAng2))-180
                    ycord2 = ((distance2 * 20)) * math.sin(math.radians(obsAng2)) +80
                    xcord3 = ((distance3 * 20)) * math.cos(math.radians(obsAng3))-180
                    ycord3 = ((distance3 * 20)) * math.sin(math.radians(obsAng3)) +80
                    xcord4 = ((distance4 * 20)) * math.cos(math.radians(obsAng4))-180
                    ycord4 = ((distance4 * 20)) * math.sin(math.radians(obsAng4)) +80
   
    # if not live
    else:

        #this is where the file select should be

        if readInput:
            takeInput()
            readInput = False

        ###

        try:
            file = open(file_path)
        except:
            EOF = True

        for _ in range(TravRow):
            try:
                next(file)
            except:
                print("End of File Reached")
                TravRow = 0
                EOF = True
                readInput = True
                Startup()
            else:
                EOF = False
        
        if(EOF == False):
            crewInfo = file.readline()
            print("this is crewInfo:",crewInfo)

            #TravRow = 1
            TravRow = TravRow + 1

            time.sleep(.25)

            if crewInfo and len(crewInfo) >= 2:
                if(crewInfo[0] == 'x'):
                    
                    UpdateCrew()

                    angle = asmAng1 - 45
                    angle2 = asmAng2 - 45
                    angle3 = asmAng3 - 45
                    angle4 = asmAng4 - 45

                    #test prints
                    print("distance 3:",distance3)


                   #converts potion into (x,y) corddintes 
                    xcord1 = ((distance1 * 20)) * math.cos(math.radians(obsAng1))-180
                    ycord1 = ((distance1 * 20)) * math.sin(math.radians(obsAng1)) +80
                    xcord2 = ((distance2 * 20)) * math.cos(math.radians(obsAng2))-180
                    ycord2 = ((distance2 * 20)) * math.sin(math.radians(obsAng2)) +80
                    xcord3 = ((distance3 * 20)) * math.cos(math.radians(obsAng3))-180
                    ycord3 = ((distance3 * 20)) * math.sin(math.radians(obsAng3)) +80
                    xcord4 = ((distance4 * 20)) * math.cos(math.radians(obsAng4))-180
                    ycord4 = ((distance4 * 20)) * math.sin(math.radians(obsAng4)) +80

                    print("distance of distance 3 after math conv:",(distance3 * 20))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if Live:
                if Record_button_rect.collidepoint(event.pos):
                        Record = not Record
                        print("Now Recording")
            if home_button_rect.collidepoint(event.pos):
                    Startup()
                    Record = False
                    readInput = True
                    TravRow = 0
            if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                # Toggle fullscreen mode
                pygame.display.toggle_fullscreen()



    CreateBackground()
   
    # creating rotated images based on scaled images
    rotated_image1 = pygame.transform.rotate(scaled_image1, angle)
    rotated_image2 = pygame.transform.rotate(scaled_image2, angle2)
    rotated_image3 = pygame.transform.rotate(scaled_image3, angle3)
    rotated_image4 = pygame.transform.rotate(scaled_image4, angle4)

    # creating
    original_rect2 = rotated_image2.get_rect()
    original_rect3 = rotated_image3.get_rect()
    original_rect4 = rotated_image4.get_rect()
    original_rect1 = rotated_image1.get_rect()

    
    image_rect2 = original_rect2.copy()
    image_rect3 = original_rect3.copy()
    image_rect4 = original_rect4.copy()
    image_rect1 = original_rect1.copy()


    # Set the image position
  
    image_rect2.center = (width // 2 + xcord2, height // 2 - ycord2)
    image_rect3.center = (width // 2 + xcord3, height // 2 - ycord3)
    image_rect4.center = (width // 2 + xcord4, height // 2 - ycord4)
    image_rect1.center = (width // 2 + xcord1, height // 2 - ycord1)

    
    rotated_rect2 = rotated_image1.get_rect(center=image_rect2.center)
    rotated_rect3 = rotated_image1.get_rect(center=image_rect3.center)
    rotated_rect4 = rotated_image1.get_rect(center=image_rect4.center)
    print("this is center of yellow: ",image_rect4.center)
    rotated_rect1 = rotated_image1.get_rect(center=image_rect1.center)
    print("this is center of green: ",image_rect1.center)


   # pygame.draw.polygon(screen, red, TRIANGLE_VERTICES)
    screen.blit(rotated_image2, rotated_rect2)
    screen.blit(rotated_image3, rotated_rect3)
    screen.blit(rotated_image4, rotated_rect4)
    screen.blit(rotated_image1, rotated_rect1)

    pygame.draw.circle(screen, black, (220,221), 40)

    #Home Button
    home_button_rect = pygame.draw.rect(screen, red, (600, 420, 120, 50))
    screen.blit(text_exit, (630,435))

    if(Live):
        if(Record):
            Record_button_rect = pygame.draw.rect(screen, red, (475, 420, 120, 50))
            screen.blit(text_stop, (480,435))
        else:
            Record_button_rect = pygame.draw.rect(screen, blue, (475, 420, 120, 50))
            screen.blit(text_start, (480,435))


    # Update the display
    pygame.display.flip()
    #clock.tick(60) 

file.close()

# Quit Pygame
pygame.quit()
