import os
import sys
import pygame
from PIL import Image

def get_path(filename): ###helper function to read file while EXE
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, filename)
    else:
        return filename

def colored(r, g, b, text): ###print color text to terminal
    return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)

def optionSlicer(options): ###experimental option slicer Takes in option=value
    i = options.split("=") 
    
    if "vis" in i[0] and "1" in i[1]:
        global visualize
        visualize = True
    if "bri" in i[0]:
        global brightnessValue
        brightnessValue = int(i[1])

def optionHandler(options): ###experimental option handler
    if "help" in options:
        print(colored(255,0,0,"\nPossible Modifications:"))
        print(colored(0,255,0,"   vis = \"1 or 0\" 1 enables visualizer"))
        print(colored(0,255,0,"   *space multiple modifications with a siingle space*"))
        print("\n")
        return 1
    
    for thing in options.split(" "):
        optionSlicer(thing)
    return 1

def main():
    filename = input('Enter name of image: ')
    
    while 1:###re-asks mod questions if help is asked
        options = input('Enter any modifications(or "help"): ')
        if optionHandler(options):
            break
    
    filename = get_path(filename) 
    im = Image.open(filename, 'r') 

    global width, height 

    width, height = im.size
    if(width<height): ### if image is vertial make it horizontal
        im  = im.transpose(Image.ROTATE_90)

    im = im.resize((265,165)) ###(width,height)

    width, height = im.size
    pix_val = list(im.getdata()) ###(r,g,b,a), from top left row by row 

    colorArray = []
    
    for i in range(len(pix_val)): ###loops through each pixel in image
        color = closeTwoColors(pix_val[i])
        if color[0]==0:
            colorArray.append(1) ###one represents black pixel
        else:
            colorArray.append(0)

    
    vertLines = findLineVert(colorArray)
    horLines = findLineHor(colorArray)
    
    if vertLines[0]>horLines[0]:
        outputLines = vertLines
    else:
        outputLines = horLines

    f = open("calcOutput.txt", "w")

    for i in range(1,len(outputLines)):
        f.write(str(outputLines[i]))
    f.close()
        
    if visualize:
        visualizer(colorArray)

###Pxl-On(0,0)->(164,264) (height,width)

def visualizer(input_array):
    run = 1
    pygame.init()
  
    # Initializing surface
    surface = pygame.display.set_mode((width,height))
    
    # Drawing Rectangle
    for i in range(len(input_array)):
        if input_array[i] == 1:
            pygame.draw.rect(surface, (0,0,0), pygame.Rect(i%width, int(i/width), 1, 1))
        else:
            pygame.draw.rect(surface, (255,255,255), pygame.Rect(i%width, int(i/width), 1, 1))
    pygame.display.flip()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = 0;

def findLineHor(colorArray):
    outputArray = [] ####in from [lines, data.......]

    lines=0
    for i in range(height):
        lastOne = -1
        for j in range(width):
            if(colorArray[(i*width)+j]==1):### if black and new one
                if(lastOne==-1):
                    lastOne=(i*width)+j
                if (j==width-1) or (colorArray[(i*width)+j+1]==0): ###last one is black in a row
                    if(j-(lastOne%width)>1):
                        outputArray.append("For(X,"+str(lastOne%width)+","+str(j)+")\nPxl-On("+str(i)+",X)\nEnd\n")
                        lines+=3
                    else:
                        for n in range(j-(lastOne%width)+1):
                            outputArray.append("Pxl-On("+str(i)+","+str((lastOne%width)+n)+")\n")
                        lines+=j-(lastOne%width)+1
                    lastOne=-1
    outputArray.insert(0,str(lines)+"\n")
    return outputArray

def findLineVert(colorArray):
    outputArray = [] ####in from [lines, data.......]

    lines=0
    for i in range(width):
        lastOne = -1
        for j in range(height):
            if(colorArray[(j*width)+i]==1):### if black and new one
                if(lastOne==-1):
                    lastOne=(j*width)+i
                if (j==height-1) or (colorArray[((j+1)*width)+i]==0): ###last one is black in a row
                    if(j-(int(lastOne/width))>1):
                        outputArray.append("For(X,"+str(int(lastOne/width))+","+str(j)+")\nPxl-On(X,"+str(lastOne%width)+",BLACK)\nEnd\n")
                        lines+=3
                    else:
                        for n in range(j-(int(lastOne/width))+1):
                            outputArray.append("Pxl-On("+str(int((lastOne/width)+n))+","+str(i)+",BLACK)\n")
                        lines+=j-(int(lastOne/width))+1
                    lastOne=-1
    outputArray.insert(0,str(lines)+"\n")
    return outputArray

def closeTwoColors(input_color): ###finds black or white pixel
    col0 = input_color[0]
    col1 = input_color[1]
    col2 = input_color[2]
    global brightnessValue

    brightness = (col0+col1+col2)/3
    if(brightness>brightnessValue):
        return(255,255,255)
    else:
        return(0,0,0)

if __name__ == "__main__":
    global visualize 
    visualize = False
    global brightnessValue
    brightnessValue = 120

    main()