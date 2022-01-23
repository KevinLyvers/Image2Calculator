from PIL import Image
import pygame
import os
import sys

def get_path(filename):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, filename)
    else:
        return filename

def main():
    filename = input('Please enter your name: ')
    
    #"test.PNG" ###"USA.png","IMG_7391.JPG","kevin.jpeg"
    filename = get_path(filename)
    im = Image.open(filename, 'r')

    global width, height

    width, height = im.size
    if(width<height):
        im  = im.transpose(Image.ROTATE_90)

    im = im.resize((265,165)) ###(width,height)

    width, height = im.size
    pix_val = list(im.getdata()) ###(r,g,b,a), from top left row by row 

    test(pix_val)

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

def test(input_array):
    colorArray = []
    
    for i in range(len(input_array)):
        color = closeTwoColors(input_array[i])
        if color[0]==0:
            colorArray.append(1)
        else:
            colorArray.append(0)

    
    vertLines = findLineVert(colorArray)
    horLines = findLineHor(colorArray)
    
    if vertLines[0]>horLines[0]:
        outputLines = vertLines
    else:
        outputLines = horLines

    for i in outputLines:
        print(i)

    if visualize:
        visualizer(colorArray)


def findLineHor(colorArray):
    outputArray = [] ####in from [lines, type, data.......]

    lines=0
    for i in range(height):
        lastOne = -1
        for j in range(width):
            if(colorArray[(i*width)+j]==1):### if black and new one
                if(lastOne==-1):
                    lastOne=(i*width)+j
                if (j==width-1) or (colorArray[(i*width)+j+1]==0): ###last one is black in a row
                    if(j-(lastOne%width)>1):
                        outputArray.append("For(X,"+str(lastOne%width)+","+str(j)+")\nPxl-On("+str(i)+",X)\nEnd")
                        lines+=3
                    else:
                        for n in range(j-(lastOne%width)+1):
                            outputArray.append("Pxl-On("+str(i)+","+str((lastOne%width)+n)+")")
                        lines+=j-(lastOne%width)+1
                    lastOne=-1
    outputArray.insert(0,lines)
    return outputArray

def findLineVert(colorArray):
    outputArray = [] ####in from [lines, type, data.......]

    lines=0
    for i in range(width):
        lastOne = -1
        for j in range(height):
            if(colorArray[(j*width)+i]==1):### if black and new one
                if(lastOne==-1):
                    lastOne=(j*width)+i
                if (j==height-1) or (colorArray[((j+1)*width)+i]==0): ###last one is black in a row
                    if(j-(int(lastOne/width))>1):
                        outputArray.append("For(X,"+str(int(lastOne/width))+","+str(j)+")\nPxl-On(X,"+str(lastOne%width)+",BLACK)\nEnd")
                        lines+=3
                    else:
                        for n in range(j-(int(lastOne/width))+1):
                            outputArray.append("Pxl-On("+str(int((lastOne/width)+n))+","+str(i)+",BLACK)")
                        lines+=j-(int(lastOne/width))+1
                    lastOne=-1
    outputArray.insert(0,lines)
    return outputArray

def closeTwoColors(input_color): ###finds black or white pixel
    col0 = input_color[0]
    col1 = input_color[1]
    col2 = input_color[2]

    brightness = (col0+col1+col2)/3

    if(brightness>100):
        return(255,255,255)
    else:
        return(0,0,0)

if __name__ == "__main__":
    global visualize 
    visualize = False

    main()