from dataClasses import Media, Franchise
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog as fd
import random
from datetime import datetime
from PIL import Image
from shutil import copyfile
import os

################################################################################
RATINGS = {0:"S", 1:"A+ or above", 2:"A or above", 3:"B+ or above", 4: "B or above", 5:"C or above", 6:"D or above"}

################################################################################
### Utility Functions
def parseName(oldName):
    """Will return media title without any space or colons

    Returns:
        name (str): Parsed media title
    """
    name = oldName
    name = name.replace(" ", "")
    name = name.strip(":")
    name = name.strip("+")
    return name

def ratingConversion(rating: float):
    """Will convert float into letter grade equivalent

    Args:
        rating (float): Rating of media

    Returns:
        letterGrade (str): Letter grade equivalent of rating 
    """
    letterGrade = ""

    if rating >= 9:
        letterGrade = "S"
    elif rating >= 8.5:
        letterGrade = "A+"
    elif rating >= 8.0:
        letterGrade = "A"
    elif rating >= 7.5:
        letterGrade = "B+"
    elif rating >= 7.0:
        letterGrade = "B"
    elif rating >= 6.0:
        letterGrade = "C"
    else:
        letterGrade = "D"

    return letterGrade

def getScreenSize():
    """Will return dimensions of the screen

    Returns:
        screen_width (int): width of screen
        screen_height (int): height of screen
    """
    root = ctk.CTk()  # Use CTk from customtkinter
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.destroy()  # Destroy the CTk instance since it's not needed anymore
    return screen_width, screen_height

def getAgeClassificationImage(ageClassification: int):
    match ageClassification:
        case 0:
            ratingPath = f"imgsrc/ausRating/gsquare.png"
        case 1:
            ratingPath = f"imgsrc/ausRating/pgsquare.png"
        case 2:
            ratingPath = f"imgsrc/ausRating/msquare.png"
        case 3:
            ratingPath = f"imgsrc/ausRating/ma15square.png"
        case 4:
            ratingPath = f"imgsrc/ausRating/r18square.png"
    return ratingPath

################################################################################
### Preload Image
infoImage = ctk.CTkImage(light_image=Image.open("imgsrc/util/darkInfo2.png"),
                            dark_image=Image.open("imgsrc/util/whiteInfo.png"),
                            size=(30, 30))

################################################################################
##### App Class #####
class cardApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        ### Create default appearance scheme
        self.title("The Movie Card Application")
        globals()["maxWidth"], globals()["maxHeight"] = getScreenSize()
        text = f"{globals()["maxWidth"]}x{globals()["maxHeight"]}"
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("green")
        self.geometry(text)

        # Configure the grid layout to make the controlBar fill the left-hand side
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)  # Control bar fixed width
        self.grid_columnconfigure(1, weight=1)  # Main content fills the rest

        self.controlBar = controlBarFrame(self)
        self.controlBar.grid(row = 0, column = 0, padx=10, pady= (10, 10), sticky="nsew")

        self.mainContent = mainContentFrame(self)
        self.mainContent.grid(row = 0, column = 1, padx=10, pady= (10, 10), sticky = "nsew")
    
    def showHomeFrame(self):
        print("At Home")
        self.mainContent.displayHome()
        self.mainContent.grid(row = 0, column = 1, padx=10, pady=(10, 10), sticky="nsew")
    
    def showMediaListFrame(self):
        print("At Media List")
        self.mainContent.displayMediaList()
        self.mainContent.grid(row = 0, column = 1, padx=10, pady=(10, 10), sticky="nsew")

    def showFranchiseListFrame(self):
        print("At Franchise List")
        self.mainContent.displayFranchiseList()
        self.mainContent.grid(row = 0, column = 1, padx=10, pady=(10, 10), sticky="nsew")

    def showRandomMediaFrame(self):
        print("At Random")
        
        # # Random Media Picker
        # mediaListLength = len(mediaList)
        # random.seed(datetime.now().timestamp())
        # randomNumber = random.randint(0, mediaListLength-1)
        # randomMedia = mediaList[randomNumber]
        # print(randomMedia.name)

        # Update Frame
        self.mainContent.displayRandom()
        self.mainContent.grid(row = 0, column = 1, padx=10, pady=(10, 10), sticky="nsew")

    def showRandomFranchiseFrame(self):
        print("At Random")
        
        # Random Media Picker
        franchiseListLength = len(franchiseList)
        if franchiseListLength > 0:
            random.seed(datetime.now().timestamp())
            randomNumber = random.randint(0, franchiseListLength-1)
            randomFranchise = franchiseList[randomNumber]
            print(randomFranchise.name)

            # Update Frame
            self.mainContent.displayFranchise(randomFranchise)
            self.mainContent.grid(row = 0, column = 1, padx=10, pady=(10, 10), sticky="nsew")

    def showAddMediaFrame(self):
        print("At Add")
        self.mainContent.displayNewMediaFrame()
        self.mainContent.grid(row = 0, column = 1, padx=10, pady=(10, 10), sticky="nsew")

    def showAddFranchiseFrame(self):
        print("At Add Franchise")
        self.mainContent.displayNewFranchiseFrame()
        self.mainContent.grid(row = 0, column = 1, padx=10, pady=(10, 10), sticky="nsew")
    
    def closeApp(self):
        self.destroy()

################################################################################
##### Static Frame #####
### Control Bar on Left
class controlBarFrame(ctk.CTkFrame):
    def __init__(self, master: cardApp):
        super().__init__(master, height=globals()["maxHeight"])

        self.label = ctk.CTkLabel(self, text = "Control Bar",fg_color="gray30", corner_radius=6, width = 230, height = 50, font = ("Ariel", 30, "bold"))
        self.label.grid(row=0, column = 0, padx = 10, pady = (10,25), sticky = "ew")

        self.homeButton = ctk.CTkButton(self, text= "Home", command = master.showHomeFrame, width = 230, height = 50, font = ("ArielBold", 24))
        self.homeButton.grid(row=1, column = 0, padx = 10, pady = (0,25), sticky = "w")

        self.mediaListButton = ctk.CTkButton(self, text= "Media List", command = master.showMediaListFrame, width = 230, height = 50, font = ("ArielBold", 24))
        self.mediaListButton.grid(row=2, column = 0, padx = 10, pady = (0,25), sticky = "w")

        self.franchiseListButton = ctk.CTkButton(self, text= "Franchise List", command = master.showFranchiseListFrame, width = 230, height = 50, font = ("ArielBold", 24))
        self.franchiseListButton.grid(row=3, column = 0, padx = 10, pady = (0,25), sticky = "w")

        self.randomMediaButton = ctk.CTkButton(self, text= "Random Media", command = master.showRandomMediaFrame, width = 230, height = 50, font = ("ArielBold", 24))
        self.randomMediaButton.grid(row=4, column = 0, padx = 10, pady = (0,25), sticky = "w")

        self.randomFranchiseButton = ctk.CTkButton(self, text= "Random Franchise", command = master.showRandomFranchiseFrame, width = 230, height = 50, font = ("ArielBold", 24))
        self.randomFranchiseButton.grid(row=5, column = 0, padx = 10, pady = (0,25), sticky = "w")

        self.addMediaButton = ctk.CTkButton(self, text= "Add Media", command = master.showAddMediaFrame, width = 230, height = 50, font = ("ArielBold", 24))
        self.addMediaButton.grid(row=6, column = 0, padx = 10, pady = (0,25), sticky = "w")

        self.addFranchiseButton = ctk.CTkButton(self, text= "Add Franchise", command = master.showAddFranchiseFrame, width = 230, height = 50, font = ("ArielBold", 24))
        self.addFranchiseButton.grid(row=7, column = 0, padx = 10, pady = (0,25), sticky = "w")

        self.closeAppButton = ctk.CTkButton(self, text= "Exit Program", command = master.closeApp, width = 230, height = 50, font = ("ArielBold", 24), hover_color="#c33d3b", fg_color="#ff8886")
        self.closeAppButton.grid(row=8, column = 0, padx = 10, pady = (0,10), sticky = "ws")

        self.grid_rowconfigure(8,weight=1)

### Main Content Frame
class mainContentFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.displayedFrame = homeFrame(self)
        self.displayedFrame.grid(row=0,column=0,pady=10,padx=10,sticky="nsew")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def displayHome(self):
        self.displayedFrame.destroy()
        self.displayedFrame.pack_forget()
        self.displayedFrame = homeFrame(self)
        self.displayedFrame.update()
        self.displayedFrame.update_idletasks()
        self.displayedFrame.grid(row=0,column=0,pady=10,padx=10,sticky="nsew")

    def displayRandom(self):
        self.displayedFrame.destroy()
        self.displayedFrame.pack_forget()
        self.displayedFrame = randomFrame(self)
        self.displayedFrame.update()
        self.displayedFrame.update_idletasks()
        self.displayedFrame.grid(row=0,column=0,pady=10,padx=10,sticky="nsew")

    def displayNewMediaFrame(self):
        self.displayedFrame.destroy()
        self.displayedFrame.pack_forget()
        self.displayedFrame = newMediaFrame(self)
        self.displayedFrame.update()
        self.displayedFrame.update_idletasks()
        self.displayedFrame.grid(row=0,column=0,pady=10,padx=10,sticky="nsew")

    def displayNewFranchiseFrame(self):
        self.displayedFrame.destroy()
        self.displayedFrame.pack_forget()
        self.displayedFrame = newFranchiseFrame(self)
        self.displayedFrame.update()
        self.displayedFrame.update_idletasks()
        self.displayedFrame.grid(row=0,column=0,pady=10,padx=10,sticky="nsew")

    def displayMediaList(self):
        self.displayedFrame.destroy()
        self.displayedFrame.pack_forget()
        self.displayedFrame = mediaListFrame(self)
        self.displayedFrame.update()
        self.displayedFrame.update_idletasks()
        self.displayedFrame.grid(row=0,column=0,pady=10,padx=10,sticky="nsew")

    def displayFranchiseList(self):
        self.displayedFrame.destroy()
        self.displayedFrame.pack_forget()
        self.displayedFrame = franchiseListFrame(self)
        self.displayedFrame.update()
        self.displayedFrame.update_idletasks()
        self.displayedFrame.grid(row=0,column=0,pady=10,padx=10,sticky="nsew")

    def displayMedia(self, media: Media):
        self.displayedFrame.destroy()
        self.displayedFrame.pack_forget()
        self.displayedFrame = mediaFrame(self, media)
        self.displayedFrame.update()
        self.displayedFrame.update_idletasks()
        self.displayedFrame.grid(row=0,column=0,pady=10,padx=10,sticky="nsew")

    def displayFranchise(self, franchise: Franchise):
        self.displayedFrame.destroy()
        self.displayedFrame.pack_forget()
        self.displayedFrame = franchiseFrame(self, franchise)
        self.displayedFrame.update()
        self.displayedFrame.update_idletasks()
        self.displayedFrame.grid(row=0,column=0,pady=10,padx=10,sticky="nsew")
    
    def displayEditMedia(self, media: Media):
        self.displayedFrame.destroy()
        self.displayedFrame.pack_forget()
        self.displayedFrame = editMediaFrame(self, media)
        self.displayedFrame.update()
        self.displayedFrame.update_idletasks()
        self.displayedFrame.grid(row=0,column=0,pady=10,padx=10,sticky="nsew")
    
    def displayDeleteMedia(self, media: Media):
        self.displayedFrame.destroy()
        self.displayedFrame.pack_forget()
        self.displayedFrame = deleteMediaFrame(self, media)
        self.displayedFrame.update()
        self.displayedFrame.update_idletasks()
        self.displayedFrame.grid(row=0,column=0,pady=10,padx=10,sticky="nsew")    

    def removeMedia(self, removedMedia: Media):
        self.displayHome()
        mediaList.remove(removedMedia)

        for franchise in franchiseList:
            try:
                franchise.media.remove(removedMedia)
            except ValueError:
                print(f"Media not in franchise {franchise.name}")
        
        updateAllFranchise()
        fullUpdateMasterFranchise()

        # Specify the path to the file
        file_path = f"filmData/{parseName(removedMedia.name)}.txt"
        cover_path = f"imgsrc/media/{parseName(removedMedia.name)}.jpg"
        poster_path = f"imgsrc/media/{parseName(removedMedia.name)}Poster.jpg"

        pathList = [file_path, cover_path, poster_path]

        # Check if the file exists before attempting to remove it
        for path in pathList:
            if os.path.exists(path):
                os.remove(path)  # Remove the file
                print(f"{path} has been deleted.")
            else:
                print(f"{path} does not exist.")

        fullUpdateMasterMedia()
        del removedMedia

    def displayDeleteFranchise(self, franchise: Franchise):
        self.displayedFrame.destroy()
        self.displayedFrame.pack_forget()
        self.displayedFrame = deleteFranchiseFrame(self, franchise)
        self.displayedFrame.update()
        self.displayedFrame.update_idletasks()
        self.displayedFrame.grid(row=0,column=0,pady=10,padx=10,sticky="nsew")    

    def removeFranchise(self, removedFranchise: Franchise):
        self.displayHome()
        franchiseList.remove(removedFranchise)

        file_path = f"franchiseData/{parseName(removedFranchise.name)}.txt"

        if os.path.exists(file_path):
            os.remove(file_path)  # Remove the file
            print(f"{file_path} has been deleted.")
        else:
            print(f"{file_path} does not exist.")
        
        fullUpdateMasterFranchise()
        del removedFranchise

################################################################################
##### Main Content Frames #####
### Home Frame ###
class homeFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight = 1)

        self.grid_rowconfigure(0, weight = 0)
        self.grid_rowconfigure(1, weight = 1)

        #### Title
        homeName = ctk.CTkLabel(self, text = "The Media Card Library Program", fg_color="black", corner_radius=6, height = 80, width=1600, font = ("Ariel", 30, "bold"))
        homeName.grid(row = 0, column = 0, pady=(10,0), padx=10, sticky = "nsew")

        textFrame = ctk.CTkFrame(self, fg_color='#2b2b2b')
        textFrame.grid(row = 1, column = 0, pady=(10,10), padx=10, sticky = "nsew")

        ### Introduction
        introFrame = ctk.CTkFrame(textFrame, fg_color='transparent')
        introFrame.grid(row = 0, column = 0, pady=(5,0), sticky = "nsew")
        introFrame.grid_rowconfigure(1, weight = 1)

        introTextLabel = ctk.CTkLabel(introFrame, text = "Welcome!!!", wraplength = 1720, font = ("Ariel", 24, 'bold'), compound="left", justify="left", anchor="nw", text_color="#2fa572")
        introTextLabel.grid(row = 0, column = 0, pady=(10,0), padx=10, sticky = "nsw")

        introText = ctk.CTkLabel(introFrame, text = "This is my way of recording down every unique piece of media I have in my collection. This software will allow you to create new Media and Franchises, upload images for them, find something to watch and more!!!", 
                                 wraplength = 1720, font = ("Ariel", 20), compound="left", justify="left", anchor="nw")
        introText.grid(row = 1, column = 0, pady=(5,0), padx=10, sticky = "nsw")

        ### Definitions of Labels
        definitionFrame = ctk.CTkFrame(textFrame, fg_color='transparent')
        definitionFrame.grid(row = 1, column = 0, pady=(10,0), sticky = "nsew")

        definitionLabel = ctk.CTkLabel(definitionFrame, text = "Definitions:", wraplength = 1720, font = ("Ariel", 23, 'bold'), compound="left", justify="left", anchor="w", text_color="#2fa572")
        definitionLabel.grid(row = 0, column = 0, pady=(10,0), padx=10, sticky = "nsw")

        definitionIntroText = ctk.CTkLabel(definitionFrame, text = "In this software, there are two key terms which you need to know about:",
                                       wraplength = 1720, font = ("Ariel", 20), compound="left", justify="left", anchor="w")
        definitionIntroText.grid(row = 1, column = 0, pady=(5,0), padx=10, sticky = "nsw")

        definitionMediaIntroText = ctk.CTkLabel(definitionFrame, text = "- Media: This refers to any film, television show, special or OVA. Note that each of these media have to be standalone and will be decided on individual case-by-case.",
                                       wraplength = 1700, font = ("Ariel", 20), compound="left", justify="left", anchor="w")
        definitionMediaIntroText.grid(row = 2, column = 0, pady=(5,0), padx=(20,10), sticky = "nsw")
        definitionMediaIntroExample = ctk.CTkLabel(definitionFrame, text = 'For example, Dragon Ball and Dragon Ball Z are considered independant, but something like Attack on Titan and Attack on Titan: The Final Chapters would not be considered independant.',
                                       wraplength = 1700, font = ("Ariel", 20), compound="left", justify="left", anchor="w")
        definitionMediaIntroExample.grid(row = 3, column = 0, pady=(0,0), padx=(32,10), sticky = "nsw")
        # definitionMediaCount = ctk.CTkLabel(definitionFrame, text = f'Currently, there are {len(mediaList)} unique pieces of media in the collection.',
        #                                wraplength = 1700, font = ("Ariel", 20), compound="left", justify="left", anchor="w")
        # definitionMediaCount.grid(row = 4, column = 0, pady=(0,0), padx=(32,10), sticky = "nsw")

        definitionFranchiseIntroText = ctk.CTkLabel(definitionFrame, text = "- Franchise: This refers to any grouping of media. Each individual media is capable of belonging to multiple franchises as well.",
                                                    wraplength = 1700, font = ("Ariel", 20), compound="left", justify="left", anchor="w")
        definitionFranchiseIntroText.grid(row = 4, column = 0, pady=(5,0), padx=(20,10), sticky = "nsw")
        definitionFranchiseIntroExample = ctk.CTkLabel(definitionFrame, text = "For example, Dragon Ball Z could fit into the Dragon Ball franchise as well as the Shonen Jump franchise, the Toei Franchise etc...",
                                                    wraplength = 1700, font = ("Ariel", 20), compound="left", justify="left", anchor="w")
        definitionFranchiseIntroExample.grid(row = 5, column = 0, pady=(0,0), padx=(32,10), sticky = "nsw")
        # definitionFranchiseCount = ctk.CTkLabel(definitionFrame, text = f'Currently, there are {len(franchiseList)} unique franchises in the collection.',
        #                                wraplength = 1700, font = ("Ariel", 20), compound="left", justify="left", anchor="w")
        # definitionFranchiseCount.grid(row = 7, column = 0, pady=(0,0), padx=(32,10), sticky = "nsw")
        
        ### Ratings Explained
        ratingFrame = ctk.CTkFrame(textFrame, fg_color='transparent')
        ratingFrame.grid(row = 2, column = 0, pady=(10,0), sticky = "nsew")

        ratingLabel = ctk.CTkLabel(ratingFrame, text = "Ratings Explained:", wraplength = 1720, font = ("Ariel", 23, 'bold'), compound="left", justify="left", anchor="w", text_color="#2fa572")
        ratingLabel.grid(row = 0, column = 0, pady=(10,0), padx=10, sticky = "nsw")

        ratingIntroText = ctk.CTkLabel(ratingFrame, text = "This system uses two types of rating, being a letter grade and a more accurate numeric score.",
                                       wraplength = 1720, font = ("Ariel", 20), compound="left", justify="left", anchor="w")
        ratingIntroText.grid(row = 1, column = 0, pady=(5,0), padx=10, sticky = "nsw")

        ratingScoreText = ctk.CTkLabel(ratingFrame, text = "The numeric scores have been gathered from popular review sites. In particular, the rating given to anime was collected from MyAnimeList, whilst non-anime was collected from IMDB.",
                                       wraplength = 1720, font = ("Ariel", 20), compound="left", justify="left", anchor="w")
        ratingScoreText.grid(row = 2, column = 0, pady=(5,0), padx=10, sticky = "nsw")

        ratingGradeText = ctk.CTkLabel(ratingFrame, text = "The letter scores were calculated from the numeric score, based on the reference below:",
                                       wraplength = 1720, font = ("Ariel", 20), compound="left", justify="left", anchor="w")
        ratingGradeText.grid(row = 3, column = 0, pady=(5,0), padx=10, sticky = "nsw")

        ratingPath = "imgsrc/util/ratingGraphic.png"
        width = 1600
        with Image.open(ratingPath) as ratingScale:
                imgRatio = width / ratingScale.width
                ratingScaleImage = ctk.CTkImage(
                    light_image=ratingScale.copy(),
                    dark_image=ratingScale.copy(),
                    size=(width, ratingScale.height * imgRatio)
                )

        ratingGradeImage = ctk.CTkLabel(ratingFrame, text = "", image = ratingScaleImage)
        ratingGradeImage.grid(row = 4, column = 0, pady=(15,0), padx=10, sticky = "nesw")

### Card Frames ###
class mediaFrame(ctk.CTkScrollableFrame):
    """
    At current, it can correctly read the attributes. It needs to be correctly 'decorated'.
    """
    def __init__(self, master, media: Media):
        super().__init__(master, width = 1600, height = 1000)
        self.media = media
        attributes = self.media.__dict__
        posterHeight = 480
        self.grid_rowconfigure(4, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Movie Image
        # self.posterImage = f"imgsrc/media/{parseName(attributes["name"])}Poster.jpg"
        # posterRatio = 480/Image.open(self.posterImage).height
        # posterImage = ctk.CTkImage(light_image=Image.open(self.posterImage),
        #                           dark_image=Image.open(self.posterImage),
        #                           size=(Image.open(self.posterImage).width*posterRatio, posterHeight))
        
        # self.contentImage = f"imgsrc/media/{parseName(attributes["name"])}.jpg"
        # aspectRatio = posterHeight/Image.open(self.contentImage).height
        # contentImage = ctk.CTkImage(light_image=Image.open(self.contentImage),
        #                           dark_image=Image.open(self.contentImage),
        #                           size=(Image.open(self.contentImage).width * aspectRatio, posterHeight))

        # Define poster image path
        self.posterImage = f"imgsrc/media/{parseName(attributes['name'])}Poster.jpg"

        # Open poster image once and calculate ratio
        with Image.open(self.posterImage) as poster_img:
            posterRatio = posterHeight / poster_img.height
            posterImage = ctk.CTkImage(
                light_image=poster_img.copy(),
                dark_image=poster_img.copy(),
                size=(poster_img.width * posterRatio, posterHeight)
            )

        # Define content image path
        self.contentImage = f"imgsrc/media/{parseName(attributes['name'])}.jpg"

        # Open content image once and calculate ratio
        with Image.open(self.contentImage) as content_img:
            aspectRatio = posterHeight / content_img.height
            contentImage = ctk.CTkImage(
                light_image=content_img.copy(),
                dark_image=content_img.copy(),
                size=(content_img.width * aspectRatio, posterHeight)
        ) 

        ## Display media attributes
        # Media Title
        labelname = ctk.CTkLabel(self, text = f'{attributes["name"]} ({attributes["yearRelease"]})',  fg_color="black", corner_radius=6, height = 80, width=1500, font = ("Ariel", 30, "bold"))
        labelname.grid(row = 0, column = 0, pady=(10,0), padx=10, sticky = "we")
        
        # Media Images
        imageFrame = ctk.CTkFrame(self,  fg_color="transparent")
        imageFrame.grid(row=1, column = 0, pady=(10,5), padx=10, sticky = "we" )
        imageFrame.grid_columnconfigure(0, weight=1)
        imageFrame.grid_columnconfigure(1, weight=1)

        labelPosterImage = ctk.CTkLabel(imageFrame, image=posterImage, text="") # Poster Image
        labelPosterImage.grid(row=0, column = 0, pady=10, padx=10, sticky = "e")

        labelContentImage = ctk.CTkLabel(imageFrame, image=contentImage, text="") # Scenc Image
        labelContentImage.grid(row=0, column = 1, pady=10,padx=10, sticky = "w")

        # Media Details
        mediaDetails = ctk.CTkFrame(self, width = 1400)
        mediaDetails.grid(row=2, column=0, pady=(0,5), padx=10, sticky = "we")
        mediaDetails.grid_columnconfigure(0, weight=0)
        mediaDetails.grid_columnconfigure(1, weight=1, uniform = "red")
        mediaDetails.grid_columnconfigure(2, weight=1, uniform = "red")
        mediaDetails.grid_columnconfigure(3, weight=1, uniform = "red")
        mediaDetails.grid_columnconfigure(4, weight=1, uniform = "red")
        mediaDetails.grid_rowconfigure(0, weight=1)

        # Age Rating Image
        ageFrame = ctk.CTkFrame(mediaDetails, width = 200, corner_radius=6)
        ageFrame.grid(row=0,column=0, padx = 10, pady = 10, sticky = "nswe")
        ageFrame.grid_rowconfigure(0, weight=1)

        ratingPath = getAgeClassificationImage(attributes["ageClassification"])
        ratingImage = ctk.CTkImage(light_image=Image.open(ratingPath),dark_image=Image.open(ratingPath), size = (50,50))
        self.ageClassification = ctk.CTkLabel(ageFrame, image=ratingImage, text="", bg_color="transparent")
        self.ageClassification.grid(row = 0, column = 0, padx = (10,10), pady = (10,10), sticky = "we")

        ageNotes = attributes["ageNote"]
        self.ageNotes = ctk.CTkLabel(ageFrame, text=ageNotes, wraplength=200, text_color="white", font = ("CTkFont",13, 'bold'))
        self.ageNotes.grid(row = 0, column = 1, padx = (10,10), pady = (10,10), sticky = "w")

        # Media Type
        mediaTypeFrame = ctk.CTkFrame(mediaDetails, corner_radius=6)
        mediaTypeFrame.grid(row = 0, column = 1, pady=10, padx=10, sticky = "nsew")
        mediaTypeFrame.grid_columnconfigure(0, weight = 1)
        mediaTypeFrame.grid_rowconfigure(1, weight=1)

        titlemediaType = ctk.CTkLabel(mediaTypeFrame, text="Media Type", fg_color="transparent", font = ("CTkFont",14, 'bold'), text_color="#2fa572")
        titlemediaType.grid(row = 0, column = 0, pady=(5,0),padx=10, sticky = "ew")

        labelmediaType = ctk.CTkLabel(mediaTypeFrame, text=str(Media.MEDIATYPE[attributes["mediaType"]]), fg_color="transparent",  font = ("CTkFont",22))
        labelmediaType.grid(row = 1, column = 0, pady=(0,10),padx=10, sticky = "nsew")
        
        # Grade Rating
        gradeRating = ratingConversion(attributes["rating"])
        rating = f'{attributes["rating"]} ({gradeRating})'

        gradeFrame = ctk.CTkFrame(mediaDetails, corner_radius=6)
        gradeFrame.grid(row = 0, column = 2, pady=10, padx=10, sticky = "nsew")
        gradeFrame.grid_columnconfigure(0, weight = 1)
        gradeFrame.grid_rowconfigure(1, weight=1)

        titlerating = ctk.CTkLabel(gradeFrame, text="Rating", fg_color="transparent", font = ("CTkFont",14, 'bold'), text_color="#2fa572")
        titlerating.grid(row = 0, column = 0, pady=(5,0),padx=10, sticky = "ew")

        labelrating = ctk.CTkLabel(gradeFrame, text=rating, fg_color="transparent", font = ("CTkFont",22))
        labelrating.grid(row = 1, column = 0, pady=(0,10),padx=10, sticky = "nsew")

        # Episode Count/Runtime
        runtimeFrame = ctk.CTkFrame(mediaDetails, corner_radius=6)
        runtimeFrame.grid(row=0, column = 3, pady=10, padx=10, sticky = "nsew")
        runtimeFrame.grid_columnconfigure(0, weight = 1)
        runtimeFrame.grid_rowconfigure(1, weight=1)

        titleruntime = ctk.CTkLabel(runtimeFrame, text="Runtime", fg_color="transparent", font = ("CTkFont",14, 'bold'), text_color="#2fa572")
        titleruntime.grid(row = 0, column = 0, pady=(5,0),padx=10, sticky = "ew")

        if attributes["mediaType"] == 1:
            labelruntime = ctk.CTkLabel(runtimeFrame, text=f'{attributes["episodeCount"]} Episodes\n{attributes["runtime"]} min', fg_color="transparent", font = ("CTkFont",16))
            labelruntime.grid(row = 1, column = 0, pady=(0,10),padx=10, sticky = "nsew")
        
        else: 
            labelruntime = ctk.CTkLabel(runtimeFrame, text=f'{attributes["runtime"]} min', fg_color="transparent", font = ("CTkFont",22))
            labelruntime.grid(row = 1, column = 0, pady=(0,10),padx=10, sticky = "nsew")
        
        # Media Format
        mediaFormatFrame = ctk.CTkFrame(mediaDetails, corner_radius=6)
        mediaFormatFrame.grid(row=0, column = 4, pady=10, padx=10, sticky = "nsew")
        mediaFormatFrame.grid_columnconfigure(0, weight = 1)
        mediaFormatFrame.grid_rowconfigure(1, weight = 1)

        titlemediaFormat = ctk.CTkLabel(mediaFormatFrame, text="Format", fg_color="transparent", font = ("CTkFont",14, 'bold'), text_color="#2fa572")
        titlemediaFormat.grid(row = 0, column = 0, pady=(5,0),padx=10, sticky = "ew")

        index = 0
        formatText=""

        for item in attributes["mediaFormat"]:
            formatText+=Media.MEDIAFORMAT[item]
            formatText+='\n'
            index += 1
        
        formatText = formatText[:-1]

        labelmediaFormats=ctk.CTkLabel(mediaFormatFrame, text=f'{formatText}', fg_color = "transparent", font = ("CTkFont",22-6*(index-1)))
        labelmediaFormats.grid(row=1, column = 0, pady=(0,10), padx = 10,sticky = "ew")
        
        ### Genres
        genreFrame = ctk.CTkFrame(self)
        genreFrame.grid(row = 3, column = 0, padx=10, pady = 0, sticky = "nswe")

        genreList = list(attributes["genre"])
        genres = []

        for index in range(len(genreList)):
            genres.append(ctk.CTkLabel(genreFrame, text=Media.GENRE[genreList[index]],fg_color='#333333',corner_radius=10,font=("CTkFont",12,"bold"), width = 150))
            genres[index].grid(row=0, column=index, pady=5, padx=(4,0), sticky = "we")
            genreFrame.columnconfigure(index, weight = 0, uniform = "black")
        
        # Main Text
        textFrame = ctk.CTkFrame(self, width = int(self.winfo_width()/3))
        textFrame.grid(row = 4, column = 0, padx = 10, pady = 5, sticky = "nswe")
        textFrame.grid_columnconfigure(0, weight = 0)
        textFrame.grid_columnconfigure(1, weight = 1)
        textFrame.grid_rowconfigure(0, weight = 1)

        ## Description Frame
        desFrame = ctk.CTkFrame(textFrame)
        desFrame.grid(row=0, column = 0, pady=10, padx = 10, sticky = "nswe")
        desFrame.grid_columnconfigure(0, weight = 0)

        ### Tagline        
        tagline = attributes["tagline"].replace("’", "'").replace("“", "\"").replace("”", "\"")  
        labeltagline = ctk.CTkLabel(desFrame, text=tagline, fg_color="transparent",font = ("Ariel",20, "bold"), text_color="#2fa572")
        labeltagline.grid(row = 0, column = 0, pady=(0,0), padx=200, sticky = "we")
        
        ### Description
        description = attributes["description"]
        description = description.replace("\n", "\n\n")
        labeldescription = ctk.CTkLabel(desFrame, text=description, wraplength=600, fg_color="transparent", font =("CTkFont",16))
        labeldescription.grid(row = 1, column = 0, pady=10,padx=200, sticky = "nswe")
        
        ### Media Notes
        viewingNoteFrame = ctk.CTkFrame(textFrame, fg_color="transparent", width = int(self.winfo_width()/3))
        viewingNoteFrame.grid(row = 0, column = 1, padx = 10, pady = 10, sticky = "nswe")
        viewingNoteFrame.grid_columnconfigure(0, weight = 1)
        viewingNoteFrame.grid_rowconfigure(0, weight = 0)
        viewingNoteFrame.grid_rowconfigure(1, weight = 1)

        sourceFrame = ctk.CTkFrame(viewingNoteFrame, width = int(self.winfo_width()/3), height=100, corner_radius=6, fg_color="#333333")
        sourceFrame.grid(row = 0, column = 0, padx = 10, pady = (0,5), sticky = "nwe")
        sourceFrame.grid_columnconfigure(0, weight = 1)
        sourceFrame.grid_rowconfigure(1, weight=1)

        labelsource = ctk.CTkLabel(sourceFrame, text="Where Can I Watch This?", fg_color="transparent", corner_radius=6, text_color="#2fa572", font = ("Ariel",18, "bold"))
        labelsource.grid(row = 0, column = 0,pady=(0,0) ,padx=(0,0), sticky = "nswe")

        sourceText = ""

        for source in attributes["source"]:
            sourceText += source
            sourceText += '\n'
        
        sourceText = sourceText[:-1]

        viewingSource = ctk.CTkLabel(sourceFrame, text=sourceText, fg_color="transparent", font =("CTkFont",16))
        viewingSource.grid(row = 1, column = 0,pady=(5,5),padx=10, sticky = "nswe")

        noteFrame = ctk.CTkFrame(viewingNoteFrame, width = int(self.winfo_width()/3), corner_radius=6, fg_color="#333333")
        noteFrame.grid(row = 1, column = 0, padx = 10, pady = (5,0), sticky = "nswe")
        noteFrame.grid_columnconfigure(0, weight = 1)
        noteFrame.grid_rowconfigure(1, weight=1)

        labelviewingNote = ctk.CTkLabel(noteFrame, text="Viewing Notes", fg_color="transparent",  corner_radius=6, text_color="#2fa572", font = ("Ariel",18, "bold"))
        labelviewingNote.grid(row = 0, column = 0,pady=(0,0) ,padx=(0,0), sticky = "we")
        
        comments = attributes["viewingNote"].replace("\n","\n\n")

        viewingNote = ctk.CTkLabel(noteFrame, text=comments, fg_color="transparent", wraplength=400, font =("CTkFont",16))
        viewingNote.grid(row = 1, column = 0,pady=(5,10),padx=10, sticky = "nswe")

        ##### Button Frame #####
        buttonFrame = ctk.CTkFrame(self, width = 1400,corner_radius=6)
        buttonFrame.grid(row=5, column=0, pady=(10,5), padx=10, sticky = "we")
        buttonFrame.grid_columnconfigure(0, weight = 1, uniform = "acacia")
        buttonFrame.grid_columnconfigure(1, weight = 1, uniform = "acacia")

        ### Edit Button
        editButton = ctk.CTkButton(buttonFrame, corner_radius=6, text="Edit Media", command = lambda cancelledMedia = self.media : master.displayEditMedia(cancelledMedia))
        editButton.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = "ew")

        ### Delete Button
        deleteButton = ctk.CTkButton(buttonFrame, corner_radius=6, text="Delete Media", command = lambda deletedMedia = self.media : master.displayDeleteMedia(deletedMedia), hover_color="#c33d3b", fg_color="red")
        deleteButton.grid(row = 0, column = 1, padx = 10, pady = 10, sticky = "ew")

class franchiseFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, franchise: Franchise):
        super().__init__(master,  width = 1600, height = 1000)
        self.franchise = franchise
        attributes = self.franchise.__dict__

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)

        self.grid_rowconfigure(0, weight = 0)
        self.grid_rowconfigure(1, weight = 0)
        self.grid_rowconfigure(2, weight = 0)
        self.grid_rowconfigure(3, weight = 0)
        self.grid_rowconfigure(4, weight = 1)
        self.grid_rowconfigure(5, weight = 0)

        title = ctk.CTkLabel(self, text = f'{attributes["name"]} Franchise ({franchise.earliestMedia()})',  fg_color="black", corner_radius=6, height = 80, width=1600, font = ("Ariel", 30, "bold"))
        title.grid(row = 0, column = 0, columnspan = 2,  pady = 10, padx=10, sticky = "nsew")

        ################################################################################
        ### Description Frame
        description = ctk.CTkFrame(self, fg_color= 'transparent')
        description.grid(row = 1, column = 0, columnspan = 2,  pady = 10, padx=10, sticky = "ew")
        description.grid_columnconfigure(1, weight = 1)
        description.grid_rowconfigure(0, weight=1)

        ### Image
        randomNumber = random.randint(0,attributes["count"] - 1)
        randomMedia = attributes["media"][randomNumber]

        self.imgPath = f"imgsrc/media/{parseName(randomMedia.name)}.jpg"
        coverWidth = 750
        
        # Open the image file once and ensure it's properly managed
        with Image.open(self.imgPath) as img:
            posterRatio = coverWidth / img.width
            refImage = ctk.CTkImage(
                light_image=img.copy(),
                dark_image=img.copy(),
                size=(coverWidth, img.height * posterRatio)
            )

        # Create the label and set the image
        img = ctk.CTkLabel(description, image=refImage, text="")
        img.grid(row=0, column=0, padx=(0, 10), pady=(10, 10), sticky="nse")

        ### Text Frame
        textFrame = ctk.CTkFrame(description)
        textFrame.grid(row = 0, column = 1,  pady = 10, padx=(10,0), sticky = "nsew")
        textFrame.grid_columnconfigure(0, weight = 1)
        textFrame.grid_rowconfigure(1, weight=1)

        ### Tagline
        tagline = attributes["tagline"].replace("’", "'").replace("“", "\"").replace("”", "\"")  
        labeltagline = ctk.CTkLabel(textFrame, text=tagline, fg_color="transparent",font = ("Ariel",20, "bold"), text_color="#2fa572")
        labeltagline.grid(row = 0, column = 0, pady= 10, padx=0, sticky = "we")

        ### Viewing Notes
        viewingNotes = ctk.CTkLabel(textFrame, text = attributes["viewingNotes"], wraplength=600)
        viewingNotes.grid(row = 1, column = 0, pady=10, padx=10, sticky = "new")

        ################################################################################
        ### Media Listing Section
        count = ctk.CTkLabel(self, text = f'Items in Franchise: {attributes["count"]}', fg_color="#2b2b2b", corner_radius=6, height = 60, width=1400, font = ("ArielBold", 24, "bold"))
        count.grid(row = 3, column = 0, pady=10, padx=10, sticky = "nsew")

        media = ctk.CTkFrame(self, width = 1600, fg_color="#565b5e")
        media.grid(row = 4, column = 0, pady=10, padx=10, sticky = "nsew")
        media.grid_columnconfigure(0, weight = 1)

        media.options = []
        media.buttons = []
        for i in range(attributes["count"]):
            media.options.append(mediaListing(media, attributes["media"][i]))
            media.options[i].grid(row = i, column = 0, padx = 10, pady=(10, 10), sticky = "ew")

            media.buttons.append(ctk.CTkButton(media, text=f'More Info', width = 120, height = 50, font = ("ArielBold", 18), command = lambda mediaChoice=attributes["media"][i]: master.displayMedia(mediaChoice)))
            media.buttons[i].grid(row = i, column = 1, padx = (30,10), pady = (10,10))

        ##### Button Frame #####
        buttonFrame = ctk.CTkFrame(self, width = 1400,corner_radius=6)
        buttonFrame.grid(row=5, column=0, pady=(10,5), padx=10, sticky = "we")
        buttonFrame.grid_columnconfigure(0, weight = 1, uniform = "acacia")
        buttonFrame.grid_columnconfigure(1, weight = 1, uniform = "acacia")

        ### Edit Button
        editButton = ctk.CTkButton(buttonFrame, corner_radius=6, text="Edit Franchise", command = lambda cancelledFranchise = self.franchise : master.displayEditFranchise(cancelledFranchise))
        editButton.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = "ew")

        ### Delete Button
        deleteButton = ctk.CTkButton(buttonFrame, corner_radius=6, text="Delete Franchise", command = lambda deletedFranchise = self.franchise : master.displayDeleteFranchise(deletedFranchise), hover_color="#c33d3b", fg_color="red")
        deleteButton.grid(row = 0, column = 1, padx = 10, pady = 10, sticky = "ew")

### Edit Object Frames ###
class editMediaFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, media: Media):
        super().__init__(master, width = 1600, height = 1000)
        self.media = media
        self.master = master
        self.grid_columnconfigure(0, weight=1)

        self.grid_rowconfigure(0, weight = 0)
        self.grid_rowconfigure(1, weight = 1)
        self.grid_rowconfigure(2, weight = 1)
        self.grid_rowconfigure(3, weight = 0)
        
        #### Title
        newMediaTitle = ctk.CTkLabel(self, text = "Edit Media", fg_color="black", corner_radius=6, height = 80, width=1600, font = ("Ariel", 30, "bold"))
        newMediaTitle.grid(row = 0, column = 0, pady=(10,5), padx=10, sticky = "nsew")

        #### Click Options
        options = ctk.CTkFrame(self, corner_radius=6, width=1600, height = 800)
        options.grid(row = 1, column = 0, pady=(5,5), padx=10, sticky = "nsew")

        options.grid_rowconfigure(0, weight = 1)
        options.grid_columnconfigure(0, weight = 0, uniform = "green")
        options.grid_columnconfigure(1, weight = 1)
        options.grid_columnconfigure(2, weight = 0, uniform = "green")

        ### Option Selector ###
        #########################################################################
        ##### Left Column #####
        leftColumn = ctk.CTkFrame(options, fg_color = "transparent")
        leftColumn.grid(row=0, column=0, pady=(10,0), padx=10, sticky = "nsew")

        leftColumn.grid_columnconfigure(0, weight=1)
        leftColumn.grid_rowconfigure(5, weight = 1)

        ### Name (Input) ###
        nameFrame = ctk.CTkFrame(leftColumn, corner_radius=6, fg_color="#333333")
        nameFrame.grid(row = 0, column = 0, columnspan = 2, pady = (5,0), padx=10, sticky = "nsew")
        nameFrame.grid_columnconfigure(0, weight = 1)
        nameFrame.grid_rowconfigure(6, weight = 1)

        nameTitle = ctk.CTkLabel(nameFrame, corner_radius=6, fg_color="black", text = "Name")
        nameTitle.grid(row=0, column=0, sticky = "ew")
        
        self.nameEntry=ctk.CTkEntry(nameFrame, fg_color="#2b2b2b")
        self.nameEntry.grid(row=1,column=0, padx = 10, pady=(10,10), sticky = "nsew")        
        self.nameEntry.insert("0",self.media.name)
        
        ### Year (Input) ###
        yearFrame = ctk.CTkFrame(leftColumn, corner_radius=6, fg_color="#333333")
        yearFrame.grid(row = 1, column = 0, pady = (10,0), padx=10, sticky = "nsew")
        yearFrame.grid_columnconfigure(0, weight = 1)
        yearFrame.grid_rowconfigure(1, weight = 1)

        yearTitle = ctk.CTkLabel(yearFrame, corner_radius=6, fg_color="black", text = "Year of Release")
        yearTitle.grid(row=0, column=0, sticky = "ew")
        
        self.yearEntry=ctk.CTkEntry(yearFrame, fg_color="#2b2b2b")
        self.yearEntry.grid(row=1,column=0, padx = 10, pady=(10,10), sticky = "nsew")
        self.yearEntry.insert("0", self.media.yearRelease)
        
        ### Community Rating Filter (Radio Button) ###
        communityRatingFrame = ctk.CTkFrame(leftColumn,corner_radius=6, width = 300, fg_color="#333333")
        communityRatingFrame.grid(row = 1, column = 1, pady=(10,0), padx=10, sticky = "nsew")
        communityRatingFrame.grid_columnconfigure(0, weight=1)

        communityRatingTitle = ctk.CTkLabel(communityRatingFrame, corner_radius=6, fg_color="black", text = "Community Rating")
        communityRatingTitle.grid(row=0, column=0, columnspan = 2, sticky = "ew")
        
        self.communityRatingEntry = ctk.CTkEntry(communityRatingFrame, placeholder_text="", fg_color="#2b2b2b")
        self.communityRatingEntry.grid(row=1, column=0, padx = (10, 5), pady=(10,10), sticky = "nsew")
        self.communityRatingEntry.insert("0", self.media.rating)

        communityRatingText = ctk.CTkLabel(communityRatingFrame, text=" / 10")
        communityRatingText.grid(row=1, column=1, padx = (5,10) , pady=(10,10), sticky = "nsew")

        ### Runtime (Input) ###
        runtimeFrame = ctk.CTkFrame(leftColumn,corner_radius=6, fg_color="#333333")
        runtimeFrame.grid(row = 2, column = 0, pady=(10,0), padx=10, sticky = "nsew")
        runtimeFrame.grid_columnconfigure(0, weight = 1)
        runtimeFrame.grid_rowconfigure(1, weight = 1)

        runtimeTitle = ctk.CTkLabel(runtimeFrame, corner_radius=6, fg_color="black", text = "Runtime")
        runtimeTitle.grid(row=0, column=0, columnspan = 2, sticky = "ew")
        
        self.runtimeEntry=ctk.CTkEntry(runtimeFrame, fg_color="#2b2b2b")
        self.runtimeEntry.grid(row=1, column=0, padx = (10,5), pady=(10,10), sticky = "nsew")
        self.runtimeEntry.insert("0", self.media.runtime)

        runtimeText = ctk.CTkLabel(runtimeFrame, text="minutes")
        runtimeText.grid(row=1, column=1, padx = (5,10) , pady=(10,10), sticky = "nsew")

        ### Episode Count (Input) ###
        episodeFrame = ctk.CTkFrame(leftColumn, corner_radius=6, fg_color="#333333")
        episodeFrame.grid(row = 2, column = 1, pady=(10,0), padx=10, sticky = "nsew")
        episodeFrame.grid_columnconfigure(0, weight = 1)
        episodeFrame.grid_rowconfigure(1, weight = 1)

        episodeTitle = ctk.CTkLabel(episodeFrame, corner_radius=6, fg_color="black", text = "Episode Count")
        episodeTitle.grid(row=0, column=0, sticky = "ew")
        
        self.episodeEntry=ctk.CTkEntry(episodeFrame, fg_color="#2b2b2b")
        self.episodeEntry.grid(row=1,column=0, padx = 10, pady=(10,10), sticky = "nsew")
        self.episodeEntry.insert("0", self.media.episodeCount)

        ### Media Type (Radio Button) ###
        mediaTypeFrame = ctk.CTkFrame(leftColumn,corner_radius=6, fg_color="#333333")
        mediaTypeFrame.grid(row = 3, column = 0, pady=(10,0), padx=10, sticky = "nsew")
        mediaTypeFrame.grid_columnconfigure(0, weight=1)

        mediaTypeTitle = ctk.CTkLabel(mediaTypeFrame, corner_radius=6, fg_color="black", text = "Media Type")
        mediaTypeTitle.grid(row=0, column=0, sticky = "ew")
        
        mediaTypeListFrame = ctk.CTkFrame(mediaTypeFrame, corner_radius=6, fg_color="#2b2b2b")
        mediaTypeListFrame.grid(row=1, column=0, sticky = "nsew", padx = 10, pady = 10)

        mediaTypeOptions = []
        self.mediaTypeVar = tk.IntVar(value = self.media.mediaType)

        def mediaTypeVarEvent():
            print(f"Setting Media Type as: {Media.MEDIATYPE[self.mediaTypeVar.get()]}")

        for index, mediaType in Media.MEDIATYPE.items():
            mediaTypeOptions.append(ctk.CTkRadioButton(mediaTypeListFrame, text=f"{mediaType}", command=mediaTypeVarEvent, variable = self.mediaTypeVar, value = index))
            mediaTypeOptions[index].grid(row=index,column=0, columnspan = 2, pady=(10,0), padx = 10, sticky = "w")
        
        mediaTypeOptions[-1].grid(row=2,column=0, pady=(10,10), padx = 10, sticky = "w")
        
        ### Media Format (Checklist) ###
        mediaFormatFrame = ctk.CTkFrame(leftColumn, corner_radius=6, fg_color="#333333")
        mediaFormatFrame.grid(row = 4, column = 0, pady=(10,0), padx=10, sticky = "nsew")

        mediaFormatFrame.grid_columnconfigure(0, weight=1)
        mediaFormatFrame.grid_rowconfigure(1, weight=1)

        mediaFormatTitle = ctk.CTkLabel(mediaFormatFrame, text = "Add Formats", corner_radius=6, fg_color="black")
        mediaFormatTitle.grid(row=0, column = 0, pady = (0,10), sticky = "we")
        
        self.mediaformatIncludeCheck = [tk.BooleanVar(value=False) for _ in range(3)]
        
        for item in self.media.mediaFormat:
            self.mediaformatIncludeCheck[item].set(True)

        mediaFormatInclude = []
        mediaFormatColumn = ctk.CTkFrame(mediaFormatFrame, fg_color="#2b2b2b", corner_radius=6)
        mediaFormatColumn.grid(row = 1, column = 0, padx = (10,10), pady = (0,10), sticky = "nswe")

        def formatIncludeEvent(index):
            print(f'Setting status of {Media.MEDIAFORMAT[index]} as: {self.mediaformatIncludeCheck[index].get()}')

        for index, mediaFormat in Media.MEDIAFORMAT.items():
            mediaFormatInclude.append(ctk.CTkCheckBox(mediaFormatColumn, text = f"{mediaFormat}", command = lambda value = index: formatIncludeEvent(value), variable=self.mediaformatIncludeCheck[index], onvalue=True, offvalue=False))
            mediaFormatInclude[index].grid(row = index, column = 0, padx = (10,10), pady = (5,5), sticky = "w")
        
        mediaFormatInclude[0].grid(row = 0, column = 0, padx = (10,10), pady = (10,5), sticky = "w")
        mediaFormatInclude[-1].grid(row = 2, column = 0, padx = (10,10), pady = (5,10), sticky = "w")

        def getPosterImage():
            self.posterImagePath = fd.askopenfilename(
                filetypes=[('JPEG Files', '*.jpeg'), ('JPG Files', '*.jpg'), ('PNG Files', '*.png'), ('All Files', '*.*')]
            )
            if self.posterImagePath:
                with Image.open(self.posterImagePath) as img:
                    aspectRatio = posterHeight / img.height
                    posterImage = ctk.CTkImage(
                        light_image=img.copy(),
                        dark_image=img.copy(),
                        size=(img.width * aspectRatio, posterHeight)
                    )

                self.posterImageLabel = ctk.CTkLabel(posterImageFrame, image=posterImage, text="")
                self.posterImageLabel.grid(row=1, column=0, pady=(0, 10), padx=20, sticky="ew")
                self.update()

        posterImageFrame = ctk.CTkFrame(leftColumn, corner_radius=6, width=300, fg_color="#333333")
        posterImageFrame.grid(row=3, column=1, pady=(10, 0), padx=10, sticky="nsew")
        posterImageFrame.grid_columnconfigure(0, weight=1)

        posterHeight = 105
        self.posterImagePath = f"imgsrc/media/{parseName(self.media.name)}Poster.jpg"
        with Image.open(self.posterImagePath) as img:
            aspectRatio = posterHeight / img.height
            posterImage = ctk.CTkImage(
                light_image=img.copy(),
                dark_image=img.copy(),
                size=(img.width * aspectRatio, posterHeight)
            )

        posterImageButton = ctk.CTkButton(
            posterImageFrame,
            text="Upload Poster Image",
            corner_radius=6,
            command=getPosterImage,
            font=("Ariel", 16, "bold")
        )
        posterImageButton.grid(row=0, column=0, pady=(0, 10), padx=0, sticky="we")

        self.posterImageLabel = ctk.CTkLabel(posterImageFrame, image=posterImage, text="", corner_radius=6)
        self.posterImageLabel.grid(row=1, column=0, pady=(0, 10), padx=20, sticky="nswe")

        ### Cover Image (File Upload) ###
        def getCoverImage():
            self.coverImagePath = fd.askopenfilename(
                filetypes=[('JPEG Files', '*.jpeg'), ('JPG Files', '*.jpg'), ('PNG Files', '*.png'), ('All Files', '*.*')]
            )
            if self.coverImagePath:
                with Image.open(self.coverImagePath) as img:
                    aspectRatio = coverHeight / img.height
                    coverImage = ctk.CTkImage(
                        light_image=img.copy(),
                        dark_image=img.copy(),
                        size=(img.width * aspectRatio, coverHeight)
                    )

                self.coverImageLabel = ctk.CTkLabel(coverImageFrame, image=coverImage, text="")
                self.coverImageLabel.grid(row=1, column=0, pady=(0, 10), padx=20, sticky="ew")
                self.update()

        coverImageFrame = ctk.CTkFrame(leftColumn, corner_radius=6, width=300, fg_color="#333333")
        coverImageFrame.grid(row=4, column=1, pady=(10, 0), padx=10, sticky="nsew")
        coverImageFrame.grid_columnconfigure(0, weight=1)

        coverHeight = 105
        self.coverImagePath = f"imgsrc/media/{parseName(self.media.name)}.jpg"
        with Image.open(self.coverImagePath) as img:
            aspectRatio = coverHeight / img.height
            coverImage = ctk.CTkImage(
                light_image=img.copy(),
                dark_image=img.copy(),
                size=(img.width * aspectRatio, coverHeight)
            )

        coverImageButton = ctk.CTkButton(
            coverImageFrame,
            text="Upload Cover Image",
            corner_radius=6,
            command=getCoverImage,
            font=("Ariel", 16, "bold")
        )
        coverImageButton.grid(row=0, column=0, pady=(0, 10), padx=0, sticky="we")

        self.coverImageLabel = ctk.CTkLabel(coverImageFrame, image=coverImage, text="", corner_radius=6)
        self.coverImageLabel.grid(row=1, column=0, pady=(0, 10), padx=20, sticky="nswe")

        ### Age Rating (Radio Button) ###
        ageClassificationFrame = ctk.CTkFrame(leftColumn,corner_radius=6, width = 300, fg_color="#333333")
        ageClassificationFrame.grid(row = 5, column = 0, pady=10, padx=10, sticky = "nsew")
        ageClassificationFrame.grid_columnconfigure(0, weight=1)
        ageClassificationFrame.grid_rowconfigure(1, weight=1)

        ageClassificationTitle = ctk.CTkLabel(ageClassificationFrame, corner_radius=6, fg_color="black", text = "Select Age Rating", width = 200)
        ageClassificationTitle.grid(row=0, column=0, columnspan = 2, sticky = "ew")
        
        ageClassificationListFrame = ctk.CTkFrame(ageClassificationFrame, corner_radius=6, fg_color="#2b2b2b")
        ageClassificationListFrame.grid(row = 1, column = 0, sticky = "nsew", padx = 10, pady = (10, 10))

        ageClassificationOptions = []
        self.ageClassificationVar = tk.IntVar(value = self.media.ageClassification)

        def ageClassificationVarEvent():
            print(f"Setting Age Rating as: {Media.AGERATING[self.ageClassificationVar.get()]}")

        for index, ageClassification in Media.AGERATING.items():
            ageClassificationOptions.append(ctk.CTkRadioButton(ageClassificationListFrame, text=f"{ageClassification}", command=ageClassificationVarEvent, variable = self.ageClassificationVar, value = index))
            ageClassificationOptions[index].grid(row=index+1,column=0, pady=(10,0), padx = 10, sticky = "w")
        
        ageClassificationOptions[-1].grid(row=5,column=0, pady=(10,10), padx = 10, sticky = "w")

        ### Classification Notes ###
        classNotesFrame = ctk.CTkFrame(leftColumn, corner_radius=6, fg_color="#333333")
        classNotesFrame.grid(row=5, column = 1, sticky = "nsew", padx = 10, pady = 10)
        classNotesFrame.grid_columnconfigure(0, weight = 1)
        classNotesFrame.grid_rowconfigure(1, weight = 1)

        classNotesTitle = ctk.CTkLabel(classNotesFrame, corner_radius=6, fg_color="black", text = "Classification Notes", width = 200)
        classNotesTitle.grid(row=0, column=0, sticky = "ew")
        
        self.classNotesEntry = ctk.CTkTextbox(classNotesFrame, corner_radius=6, fg_color="#2b2b2b", border_width=2, border_color="#565b5e")
        self.classNotesEntry.grid(row = 1, column = 0, padx = 10, pady = (10, 10), sticky = "nsew")
        self.classNotesEntry.insert("0.0",self.media.ageNote)

        #########################################################################
        ### Middle Column
        middleColumn = ctk.CTkFrame(options, corner_radius= 6, fg_color="transparent")
        middleColumn.grid(row=0, column = 1, pady = 10, padx = 10, sticky = "nsew")
        middleColumn.grid_columnconfigure(0, weight=1)
        
        middleColumn.grid_rowconfigure(1, weight = 1, uniform = "maple")
        middleColumn.grid_rowconfigure(2, weight = 1, uniform = "maple")

        ### Tagline (Entry)
        taglineFrame = ctk.CTkFrame(middleColumn, corner_radius=6, fg_color="#333333")
        taglineFrame.grid(row = 0, column = 0, pady = (5,0), padx=10, sticky = "nsew")
        taglineFrame.grid_columnconfigure(0, weight = 1)
        taglineFrame.grid_rowconfigure(1, weight = 1)

        taglineTitle = ctk.CTkLabel(taglineFrame, corner_radius=6, fg_color="black", text = "Tagline")
        taglineTitle.grid(row=0, column=0, sticky = "ew")
        
        self.taglineEntry=ctk.CTkEntry(taglineFrame, fg_color="#2b2b2b")
        self.taglineEntry.grid(row=1,column=0, padx = 10, pady=(10,10), sticky = "nsew")
        self.taglineEntry.insert("0",self.media.tagline)
        
        ### Description (Textbook)
        descriptionFrame = ctk.CTkFrame(middleColumn, corner_radius=6, fg_color="#333333")
        descriptionFrame.grid(row = 1, column = 0, pady = (10,0), padx=10, sticky = "nsew")
        descriptionFrame.grid_columnconfigure(0, weight = 1)
        descriptionFrame.grid_rowconfigure(1, weight = 1)

        descriptionTitle = ctk.CTkLabel(descriptionFrame, corner_radius=6, fg_color="black", text = "Description")
        descriptionTitle.grid(row=0, column=0, sticky = "ew")
        
        self.descriptionEntry=ctk.CTkTextbox(descriptionFrame, fg_color="#2b2b2b", border_width=2, border_color="#565b5e")
        self.descriptionEntry.grid(row=1,column=0, padx = 10, pady=(10,10), sticky = "nsew")
        self.descriptionEntry.insert("0.0", self.media.description)

        ### Viewing Notes (Input)
        noteFrame = ctk.CTkFrame(middleColumn,corner_radius=6, fg_color="#333333")
        noteFrame.grid(row = 2, column = 0, pady=(10,0), padx=10, sticky = "nsew")
        noteFrame.grid_columnconfigure(0, weight = 1)
        noteFrame.grid_rowconfigure(1, weight = 1)

        noteTitle = ctk.CTkLabel(noteFrame, corner_radius=6, fg_color="black", text = "Viewing Notes")
        noteTitle.grid(row=0, column=0, sticky = "ew")
        
        self.noteEntry=ctk.CTkTextbox(noteFrame, fg_color="#2b2b2b",  border_width=2, border_color="#565b5e")
        self.noteEntry.grid(row=1,column=0, padx = 10, pady=(10,10), sticky = "nsew")
        self.noteEntry.insert("0.0", self.media.viewingNote)

        #########################################################################
        ### Right Column
        rightColumn = ctk.CTkFrame(options, corner_radius= 6, fg_color="transparent")
        rightColumn.grid(row=0, column = 2, pady = 10, padx = 10, sticky = "nsew")
        rightColumn.grid_columnconfigure(0, weight=1)

        rightColumn.grid_rowconfigure(1, weight=1)

        ### Genre Row
        genreColumnFrame = ctk.CTkFrame(rightColumn, corner_radius=6, fg_color="#333333")
        genreColumnFrame.grid(row = 0, column = 0, pady=(5,0), padx=10, sticky = "nsew")

        genreColumnFrame.grid_columnconfigure(0, weight=1)
        genreColumnFrame.grid_rowconfigure(1, weight=1)

        genreTitle = ctk.CTkLabel(genreColumnFrame, text = "Add Genres", corner_radius=6, fg_color="black")
        genreTitle.grid(row=0, column = 0, pady = (0,10), sticky = "we")
        
        self.genreIncludeCheck = [tk.BooleanVar(value=False) for _ in range(13)]

        for item in self.media.genre:
            self.genreIncludeCheck[item].set(True)

        genreInclude = []
        genreColumn = ctk.CTkFrame(genreColumnFrame, fg_color="#2b2b2b", corner_radius=6)
        genreColumn.grid(row = 1, column = 0, padx = (10,10), pady = (0,10), sticky = "nswe")

        def genreIncludeEvent(index):
            print(f'Setting status of {Media.GENRE[index]} as: {self.genreIncludeCheck[index].get()}')

        for index, genre in Media.GENRE.items():
            genreInclude.append(ctk.CTkCheckBox(genreColumn, text = f"{genre}", command = lambda value = index: genreIncludeEvent(value), variable=self.genreIncludeCheck[index], onvalue=True, offvalue=False))
            genreInclude[index].grid(row = index, column = 0, padx = (10,10), pady = (10,10), sticky = "w")

        ### Source Textbox
        sourceFrame = ctk.CTkFrame(rightColumn,corner_radius=6, fg_color="#333333")
        sourceFrame.grid(row = 1, column = 0, pady=(10,0), padx=10, sticky = "nsew")
        sourceFrame.grid_columnconfigure(0, weight = 1)
        sourceFrame.grid_rowconfigure(1, weight = 1)

        sourceTitle = ctk.CTkLabel(sourceFrame, corner_radius=6, fg_color="black", text = "Sources")
        sourceTitle.grid(row=0, column=0, sticky = "ew")
        
        self.sourceEntry=ctk.CTkTextbox(sourceFrame, fg_color="#2b2b2b", border_width=2, border_color="#565b5e")
        self.sourceEntry.grid(row=1,column=0, padx = 10, pady=(10,10), sticky = "nsew")

        for item in range(len(self.media.source)):
            self.sourceEntry.insert(f'{item}.0',self.media.source[item])

        #########################################################################
        ### Franchise Frame
        franchiseOptionFrame = ctk.CTkFrame(options, corner_radius=6, fg_color="#333333")
        franchiseOptionFrame.grid(row = 1, column = 0, columnspan = 3, pady=(5,10), padx=20, sticky = "nsew")
        franchiseOptionFrame.grid_columnconfigure(1, weight = 1)

        franchiseTitle = ctk.CTkLabel(franchiseOptionFrame, corner_radius=6, fg_color="black", text = "Add this media to these Franchises")
        franchiseTitle.grid(row=0, column=0, columnspan = 2, sticky = "ew")

        # Add ability to add to Franchises
        self.franchiseChecklist = [tk.BooleanVar(value=False) for _ in range(len(franchiseList))]
        for j in range(len(franchiseList)):
            if franchiseList[j].isInFranchise(self.media):
                self.franchiseChecklist[j].set(True)
        
        self.franchiseOptions = []
        self.franchiseButtons = []

        for i in range(len(franchiseList)):
            self.grid_rowconfigure(i+1, weight=1)
            self.franchiseOptions.append(franchiseListing(franchiseOptionFrame, franchiseList[i]))
            self.franchiseOptions[i].grid(row=i + 1, column = 1, padx=(0,10), pady=(10, 0), sticky = "ew")

            # self.buttons.append(ctk.CTkButton(self, text=f'More Info', width = 120, height = 50, font = ("ArielBold", 18), command = lambda franchiseChoice=franchiseList[i]: master.displayFranchise(franchiseChoice)))
            self.franchiseButtons.append(ctk.CTkCheckBox(franchiseOptionFrame, text=f'', variable = self.franchiseChecklist[i], onvalue=True, offvalue=False))
            self.franchiseButtons[i].grid(row =i+1, column = 0, padx = (20,20), pady = (10,0), sticky = "ew")
        #########################################################################
        self.franchiseOptions[i].grid(row=i + 1, column = 1, padx=(0,10), pady=(10, 10), sticky = "ew")
        self.franchiseButtons[i].grid(row =i+1, column = 0, padx = (30,30), pady = (10,10))

        ### Add Button
        addButton = ctk.CTkButton(self, text= "Update Media", font = ("Ariel", 24, "bold"),  command = self.addEvent, border_spacing=20)
        addButton.grid(row = 2, column = 0, padx = (100,100), pady = (5,10), sticky = "we")

    def addEvent(self):
        noErrors = True
        name = self.nameEntry.get()

        ### Year Check ##
        yearRelease = self.yearEntry.get()
        if len(yearRelease) == 4 and yearRelease.isnumeric():
            yearRelease = int(yearRelease)
            self.yearEntry.configure(text_color = "white")
        else:
            noErrors = False
            self.yearEntry.configure(text_color = "red")

        ### Rating Check ###
        rating = self.communityRatingEntry.get()

        try:
            rating = float(rating)
            if rating > 10 or rating < 0:
                noErrors = False
                self.communityRatingEntry.configure(text_color = "red")
            else:
                self.communityRatingEntry.configure(text_color = "white")
        except ValueError:
            noErrors = False
            self.communityRatingEntry.configure(text_color = "red")

        ### Runtime Check ###
        runtime = self.runtimeEntry.get()
        if not runtime.isnumeric():
            noErrors = False
            self.runtimeEntry.configure(text_color = "red")
        else:
            runtime = int(runtime)
            if runtime <= 0:
                noErrors = False
                self.runtimeEntry.configure(text_color = "red")
            else:
                self.runtimeEntry.configure(text_color = "white")

        ### Media Type Check ###
        mediaType = self.mediaTypeVar.get()
        ageClassification = self.ageClassificationVar.get()
        ageNote = self.classNotesEntry.get("0.0", "end").replace("\n"," ")

        if mediaType == 1:
            episode = self.episodeEntry.get()
            if not episode.isnumeric():
                noErrors = False
                self.episodeEntry.configure(text_color = "red")
            else:
                episode = int(episode)
                if episode < 0:
                    noErrors = False 
                    self.episodeEntry.configure(text_color = "red")
                else:
                    self.episodeEntry.configure(text_color = "white")
        else:
            episode = 1
        
        ### Media Format List Check ###
        mediaFormat = self.mediaformatIncludeCheck
        mediaFormatList = []
        for i in range(len(mediaFormat)):
            if mediaFormat[i].get():
                mediaFormatList.append(i)

        if len(mediaFormatList) != 0:
            mediaFormatList = set(mediaFormatList)
        else:
            noErrors = False

        ### Genre List Check ###
        genre = self.genreIncludeCheck
        genreList = []

        for j in range(len(genre)):
            if genre[j].get():
                genreList.append(j)
        
        if len(genreList) != 0:
            genreList = set(genreList)
        else:
            noErrors = False

        ### Text Input Check ###
        tagline = self.taglineEntry.get()

        description = self.descriptionEntry.get("0.0", "end")
        description.replace("\n\n", "\n")

        viewingNote = self.noteEntry.get("0.0", "end")
        viewingNote.replace("\n\n", "\n")

        source  = self.sourceEntry.get("0.0", "end")
        source = source.split("\n")

        print(f"Is there no errors: {noErrors}")
        print(self.coverImagePath)
        print(self.posterImagePath)

        if noErrors:
            ### Variable Update ###
            self.media.editName(name)
            self.media.editAgeClassification(ageClassification)
            self.media.editYearRelease(yearRelease)
            self.media.editMediaType(mediaType)
            self.media.editRating(rating)
            self.media.editDescription(description[:-1])
            self.media.editRuntime(runtime)
            self.media.editEpisodeCount(episode)
            self.media.editMediaFormat(mediaFormatList)
            self.media.editTagline(tagline)
            self.media.editGenres(genreList)
            self.media.editSource(source[:-1])
            self.media.editViewingNotes(viewingNote[:-1])
            self.media.editAgeNotes(ageNote[:-1])

            # Update File Again
            self.media.writeText()
            if self.posterImagePath != f'imgsrc/media/{parseName(name)}Poster.jpg':
                copyfile(self.posterImagePath, f'imgsrc/media/{parseName(name)}Poster.jpg')
            
            if self.coverImagePath != f'imgsrc/media/{parseName(name)}.jpg':
                copyfile(self.coverImagePath, f'imgsrc/media/{parseName(name)}.jpg')
            fullUpdateMasterMedia()

            ### Update all franchise
            for index in range(len(franchiseList)):
                franchise = franchiseList[index]
                if self.franchiseChecklist[index].get() and (not franchise.isInFranchise(globals()[parseName(name)])):
                    franchise.updateMedia(globals()[parseName(name)])
                    franchise.writeText()
                elif (not self.franchiseChecklist[index].get()) and franchise.isInFranchise(globals()[parseName(name)]):
                    franchise.removeMedia(globals()[parseName(name)])
                    franchise.writeText()
                else:
                    pass

            updateAllFranchise()
            fullUpdateMasterMedia()

            self.master.displayMedia(self.media)
        
        else:
            self.update()

class editFranchiseFrame(ctk.CTkFrame):
    def __init__(self, master, franchise: Franchise):
        super().__init__(master, width = 1600, height = 1000)
        self.grid_columnconfigure(0, weight=1)

        self.grid_rowconfigure(0, weight = 0)
        self.grid_rowconfigure(1, weight = 1)
        self.grid_rowconfigure(2, weight = 0)
        
        #### Title
        newMediaTitle = ctk.CTkLabel(self, text = "Add New Franchise", fg_color="black", corner_radius=6, height = 80, width=1600, font = ("Ariel", 30, "bold"))
        newMediaTitle.grid(row = 0, column = 0, pady=(10,5), padx=10, sticky = "nsew")

        #### Click Options
        options = ctk.CTkFrame(self, corner_radius=6, width=1600, height = 800)
        options.grid(row = 1, column = 0, pady=(5,5), padx=10, sticky = "nsew")

        options.grid_rowconfigure(0, weight = 1)
        options.grid_columnconfigure(0, weight = 0, uniform = "green")
        options.grid_columnconfigure(1, weight = 1)

        ### Option Selector
        #########################################################################
        ## Left Column
        leftColumn = ctk.CTkFrame(options, fg_color = "transparent")
        leftColumn.grid(row=0, column=0, pady=(10,10), padx=10, sticky = "nsew")

        leftColumn.grid_columnconfigure(0, weight=1)
        leftColumn.grid_rowconfigure(2, weight = 1)

        ### Name (Input)
        nameFrame = ctk.CTkFrame(leftColumn, corner_radius=6, fg_color="#333333")
        nameFrame.grid(row = 0, column = 0, columnspan = 2, pady = (0,0), padx=10, sticky = "nsew")
        nameFrame.grid_columnconfigure(0, weight = 1)
        nameFrame.grid_rowconfigure(6, weight = 1)

        nameTitle = ctk.CTkLabel(nameFrame, corner_radius=6, fg_color="black", text = "Name")
        nameTitle.grid(row=0, column=0, sticky = "ew")
        
        self.nameEntry=ctk.CTkEntry(nameFrame, fg_color="#2b2b2b")
        self.nameEntry.grid(row=1,column=0, padx = 10, pady=(10,10), sticky = "nsew")
        
        ### Tagline (Entry)
        taglineFrame = ctk.CTkFrame(leftColumn, corner_radius=6, fg_color="#333333")
        taglineFrame.grid(row = 1, column = 0, pady = (10,0), padx=10, sticky = "nsew")
        taglineFrame.grid_columnconfigure(0, weight = 1)
        taglineFrame.grid_rowconfigure(1, weight = 1)

        taglineTitle = ctk.CTkLabel(taglineFrame, corner_radius=6, fg_color="black", text = "Tagline")
        taglineTitle.grid(row=0, column=0, sticky = "ew")
        
        self.taglineEntry=ctk.CTkEntry(taglineFrame, fg_color="#2b2b2b")
        self.taglineEntry.grid(row=1,column=0, padx = 10, pady=(10,10), sticky = "nsew")
        
        ### Viewing Notes (Input)
        noteFrame = ctk.CTkFrame(leftColumn,corner_radius=6, fg_color="#333333")
        noteFrame.grid(row = 2, column = 0, pady=(10,0), padx=10, sticky = "nsew")
        noteFrame.grid_columnconfigure(0, weight = 1)
        noteFrame.grid_rowconfigure(1, weight = 1)

        noteTitle = ctk.CTkLabel(noteFrame, corner_radius=6, fg_color="black", text = "Viewing Notes")
        noteTitle.grid(row=0, column=0, sticky = "ew")
        
        self.noteEntry=ctk.CTkTextbox(noteFrame, fg_color="#2b2b2b",  border_width=2, border_color="#565b5e")
        self.noteEntry.grid(row=1,column=0, padx = 10, pady=(10,10), sticky = "nsew")

        #########################################################################
        ### Right Column
        rightColumn = ctk.CTkFrame(options, corner_radius= 6, fg_color = "#333333")
        rightColumn.grid(row=0, column = 1, pady = (10,10), padx = 10, sticky = "nsew")
        rightColumn.grid_columnconfigure(0, weight=1)
        rightColumn.grid_rowconfigure(1, weight=1)

        addMediaLabel = ctk.CTkLabel(rightColumn, corner_radius=6, fg_color="black", text = "Add Media From Franchise")
        addMediaLabel.grid(row=0, column=0, sticky = "ew")

        # List of All Media
        mediaCount = len(mediaList)
        self.mediaInclude = [tk.BooleanVar(value=False) for _ in range(mediaCount)]

        mediaColumn = ctk.CTkScrollableFrame(rightColumn, fg_color="#333333", corner_radius=6)
        mediaColumn.grid(row = 1, column = 0, padx = (10,10), pady = (5,10), sticky = "nswe")

        mediaColumn.grid_columnconfigure(0, weight = 1)
        mediaColumn.grid_columnconfigure(1, weight = 1)

        mediaColumn.currentMediaList = []
        mediaColumn.currentMediaChecklist = []

        def mediaIncludeEvent(index):
            print(f'Setting status of {mediaList[index].name} as: {self.mediaIncludeCheck[index].get()}')

        for index in range(mediaCount):
            mediaColumn.grid_rowconfigure(index, weight = 1)
            mediaColumn.currentMediaChecklist.append(ctk.CTkCheckBox(mediaColumn, text = "", command = lambda value = index: mediaIncludeEvent(value), variable=self.mediaInclude[index], onvalue=True, offvalue=False, width = 20))
            mediaColumn.currentMediaChecklist[index].grid(row = index, column = 0, padx = (10,0), pady = (0,10), sticky = "ew")

            mediaColumn.currentMediaList.append(mediaListing(mediaColumn, mediaList[index]))
            mediaColumn.currentMediaList[index].grid(row = index, column = 1, padx = (0,10), pady = (0,10), sticky = "nsew")

        #########################################################################
        ### Add Button
        addButton = ctk.CTkButton(self, text= "Add New Franchise", font = ("Ariel", 24, "bold"),  command = self.addEvent, border_spacing=20)
        addButton.grid(row = 2, column = 0, padx = (100,100), pady = (5,10), sticky = "we")
    
    def addEvent(self):
        noErrors = True
        name = self.nameEntry.get()
        tagline = self.taglineEntry.get()
        note = self.noteEntry.get("0.0","end")
        note = note.replace("\n\n", "\n")

        media = []

        for index in range(len(self.mediaInclude)):
            status = self.mediaInclude[index].get()
            if status:
                media.append(mediaList[index])

        if noErrors:
            globals()[parseName(name)+"Collection"] = Franchise(name, media, note, tagline)
            globals()[parseName(name)+"Collection"].writeText()
            franchiseList.append(globals()[parseName(name)+"Collection"])
            fullUpdateMasterFranchise()

            self.master.displayFranchise(globals()[parseName(name)+"Collection"])

### Delete Object Frame ###
class deleteMediaFrame(ctk.CTkFrame):
    def __init__(self, master, media: Media):
        super().__init__(master,  width = 1600, height = 1000)
        self.media = media
        self.grid_columnconfigure(0, weight = 1, uniform = "Empire")
        self.grid_columnconfigure(1, weight = 1, uniform = "Empire")
        self.grid_columnconfigure(2, weight = 1, uniform = "Empire")
        self.grid_columnconfigure(3, weight = 1, uniform = "Empire")

        self.grid_rowconfigure(0, weight = 0)
        self.grid_rowconfigure(1, weight = 1)

        #### Title
        deleteMediaTitle = ctk.CTkLabel(self, text = f"Are you sure you want to delete {self.media.name} ({self.media.yearRelease})?\nThis is irreversible!!!", fg_color="black", corner_radius=6, height = 80, width=1600, font = ("Ariel", 30, "bold"))
        deleteMediaTitle.grid(row = 0, column = 0, columnspan = 4, pady=(10,5), padx=10, sticky = "nsew")

        # Movie Image
        # Define poster image path
        self.posterImage = f"imgsrc/media/{parseName(self.media.name)}Poster.jpg"
        posterHeight = 480

        # Open poster image once and calculate ratio
        with Image.open(self.posterImage) as poster_img:
            posterRatio = posterHeight / poster_img.height
            posterImage = ctk.CTkImage(
                light_image=poster_img.copy(),
                dark_image=poster_img.copy(),
                size=(poster_img.width * posterRatio, posterHeight)
            )

        # Define content image path
        self.contentImage = f"imgsrc/media/{parseName(self.media.name)}.jpg"

        # Open content image once and calculate ratio
        with Image.open(self.contentImage) as content_img:
            aspectRatio = posterHeight / content_img.height
            contentImage = ctk.CTkImage(
                light_image=content_img.copy(),
                dark_image=content_img.copy(),
                size=(content_img.width * aspectRatio, posterHeight)
        ) 
        
        # Media Images
        imageFrame = ctk.CTkFrame(self,  fg_color="transparent")
        imageFrame.grid(row=1, column = 0, pady=(10,5), padx=10, sticky = "we", columnspan = 4 )
        imageFrame.grid_columnconfigure(0, weight=1)
        imageFrame.grid_columnconfigure(1, weight=1)

        labelPosterImage = ctk.CTkLabel(imageFrame, image=posterImage, text="") # Poster Image
        labelPosterImage.grid(row=0, column = 0, pady=10, padx=10, sticky = "e")

        labelContentImage = ctk.CTkLabel(imageFrame, image=contentImage, text="") # Scenc Image
        labelContentImage.grid(row=0, column = 1, pady=10,padx=10, sticky = "w")

        ### Yes Button
        yesButton = ctk.CTkButton(self, corner_radius=6, text="Yes", command = lambda media = self.media : master.removeMedia(media))
        yesButton.grid(row = 2, column = 1, padx = 30, pady = 10, sticky = "ew")

        ### No Button
        noButton = ctk.CTkButton(self, corner_radius=6, text="No", command = lambda media = self.media : master.displayMedia(media), hover_color="#c33d3b", fg_color="red")
        noButton.grid(row = 2, column = 2, padx = 30, pady = 10, sticky = "ew")

class deleteFranchiseFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, franchise: Franchise):
        super().__init__(master,  width = 1600, height = 1000)
        self.franchise = franchise
        self.grid_columnconfigure(0, weight = 1, uniform = "Empire")
        self.grid_columnconfigure(1, weight = 1, uniform = "Empire")
        self.grid_columnconfigure(2, weight = 1, uniform = "Empire")
        self.grid_columnconfigure(3, weight = 1, uniform = "Empire")

        self.grid_rowconfigure(0, weight = 0)
        self.grid_rowconfigure(2, weight = 1)
        self.grid_rowconfigure(3, weight = 1)

        #### Title
        deleteFranchiseTitle = ctk.CTkLabel(self, text = f"Are you sure you want to delete {self.franchise.name}?\nThis is irreversible!!!", fg_color="black", corner_radius=6, height = 80, width=1600, font = ("Ariel", 30, "bold"))
        deleteFranchiseTitle.grid(row = 0, column = 0, columnspan = 4, pady=(10,5), padx=10, sticky = "nsew")

        # Franchise Media Listing

        # # Movie Image
        # # Define poster image path
        # self.posterImage = f"imgsrc/media/{parseName(self.media.name)}Poster.jpg"
        # posterHeight = 480

        # # Open poster image once and calculate ratio
        # with Image.open(self.posterImage) as poster_img:
        #     posterRatio = posterHeight / poster_img.height
        #     posterImage = ctk.CTkImage(
        #         light_image=poster_img.copy(),
        #         dark_image=poster_img.copy(),
        #         size=(poster_img.width * posterRatio, posterHeight)
        #     )

        # # Define content image path
        # self.contentImage = f"imgsrc/media/{parseName(self.media.name)}.jpg"

        # # Open content image once and calculate ratio
        # with Image.open(self.contentImage) as content_img:
        #     aspectRatio = posterHeight / content_img.height
        #     contentImage = ctk.CTkImage(
        #         light_image=content_img.copy(),
        #         dark_image=content_img.copy(),
        #         size=(content_img.width * aspectRatio, posterHeight)
        # ) 
        
        # # Media Images
        # imageFrame = ctk.CTkFrame(self,  fg_color="transparent")
        # imageFrame.grid(row=1, column = 0, pady=(10,5), padx=10, sticky = "we", columnspan = 4 )
        # imageFrame.grid_columnconfigure(0, weight=1)
        # imageFrame.grid_columnconfigure(1, weight=1)

        # labelPosterImage = ctk.CTkLabel(imageFrame, image=posterImage, text="") # Poster Image
        # labelPosterImage.grid(row=0, column = 0, pady=10, padx=10, sticky = "e")

        # labelContentImage = ctk.CTkLabel(imageFrame, image=contentImage, text="") # Scenc Image
        # labelContentImage.grid(row=0, column = 1, pady=10,padx=10, sticky = "w")

        count = ctk.CTkLabel(self, text = f'This franchise had {self.franchise.count} items in it. They were:', fg_color="#2b2b2b", corner_radius=6, height = 60, width=1400, font = ("ArielBold", 24, "bold"))
        count.grid(row = 1, column = 0, columnspan = 4, pady=10, padx=10, sticky = "nsew")

        media = ctk.CTkFrame(self, width = 1600, fg_color="#565b5e")
        media.grid(row = 2, column = 0, columnspan = 4, pady=10, padx=10, sticky = "nsew")
        media.grid_columnconfigure(0, weight = 1)

        media.options = []
        for i in range(self.franchise.count):
            media.grid_rowconfigure(i, weight = 1)
            media.options.append(mediaListing(media, self.franchise.media[i]))
            media.options[i].grid(row = i, column = 0, padx = 10, pady=(10, 10), sticky = "ew")

        ### Yes Button
        yesButton = ctk.CTkButton(self, corner_radius=6, text="Yes", command = lambda franchise = self.franchise : master.removeFranchise(franchise))
        yesButton.grid(row = 3, column = 1, padx = 30, pady = 10, sticky = "sew")

        ### No Button
        noButton = ctk.CTkButton(self, corner_radius=6, text="No", command = lambda franchise = self.franchise : master.displayFranchise(franchise), hover_color="#c33d3b", fg_color="red")
        noButton.grid(row = 3, column = 2, padx = 30, pady = 10, sticky = "sew")

### New Object Frames ###
### Frames to add new media and franchises ###
class newMediaFrame(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master, width = 1600, height = 1000)
        self.master = master
        self.grid_columnconfigure(0, weight=1)

        self.grid_rowconfigure(0, weight = 0)
        self.grid_rowconfigure(1, weight = 1)
        self.grid_rowconfigure(2, weight = 1)
        self.grid_rowconfigure(3, weight = 0)
        
        #### Title
        newMediaTitle = ctk.CTkLabel(self, text = "Add New Media", fg_color="black", corner_radius=6, height = 80, width=1600, font = ("Ariel", 30, "bold"))
        newMediaTitle.grid(row = 0, column = 0, pady=(10,5), padx=10, sticky = "nsew")

        #### Click Options
        options = ctk.CTkFrame(self, corner_radius=6, width=1600, height = 800)
        options.grid(row = 1, column = 0, pady=(5,5), padx=10, sticky = "nsew")

        options.grid_rowconfigure(0, weight = 1)
        options.grid_columnconfigure(0, weight = 0, uniform = "green")
        options.grid_columnconfigure(1, weight = 1)
        options.grid_columnconfigure(2, weight = 0, uniform = "green")

        ### Option Selector ###
        #########################################################################
        ##### Left Column #####
        leftColumn = ctk.CTkFrame(options, fg_color = "transparent")
        leftColumn.grid(row=0, column=0, pady=(10,0), padx=10, sticky = "nsew")

        leftColumn.grid_columnconfigure(0, weight=1)
        leftColumn.grid_rowconfigure(5, weight = 1)

        ### Name (Input) ###
        nameFrame = ctk.CTkFrame(leftColumn, corner_radius=6, fg_color="#333333")
        nameFrame.grid(row = 0, column = 0, columnspan = 2, pady = (5,0), padx=10, sticky = "nsew")
        nameFrame.grid_columnconfigure(0, weight = 1)
        nameFrame.grid_rowconfigure(6, weight = 1)

        nameTitle = ctk.CTkLabel(nameFrame, corner_radius=6, fg_color="black", text = "Name")
        nameTitle.grid(row=0, column=0, sticky = "ew")
        
        self.nameEntry=ctk.CTkEntry(nameFrame, fg_color="#2b2b2b")
        self.nameEntry.grid(row=1,column=0, padx = 10, pady=(10,10), sticky = "nsew")
        
        ### Year (Input) ###
        yearFrame = ctk.CTkFrame(leftColumn, corner_radius=6, fg_color="#333333")
        yearFrame.grid(row = 1, column = 0, pady = (10,0), padx=10, sticky = "nsew")
        yearFrame.grid_columnconfigure(0, weight = 1)
        yearFrame.grid_rowconfigure(1, weight = 1)

        yearTitle = ctk.CTkLabel(yearFrame, corner_radius=6, fg_color="black", text = "Year of Release")
        yearTitle.grid(row=0, column=0, sticky = "ew")
        
        self.yearEntry=ctk.CTkEntry(yearFrame, fg_color="#2b2b2b")
        self.yearEntry.grid(row=1,column=0, padx = 10, pady=(10,10), sticky = "nsew")
        
        ### Community Rating Filter (Radio Button) ###
        communityRatingFrame = ctk.CTkFrame(leftColumn,corner_radius=6, width = 300, fg_color="#333333")
        communityRatingFrame.grid(row = 1, column = 1, pady=(10,0), padx=10, sticky = "nsew")
        communityRatingFrame.grid_columnconfigure(0, weight=1)

        communityRatingTitle = ctk.CTkLabel(communityRatingFrame, corner_radius=6, fg_color="black", text = "Community Rating")
        communityRatingTitle.grid(row=0, column=0, columnspan = 2, sticky = "ew")
        
        self.communityRatingEntry = ctk.CTkEntry(communityRatingFrame, placeholder_text="", fg_color="#2b2b2b")
        self.communityRatingEntry.grid(row=1, column=0, padx = (10, 5), pady=(10,10), sticky = "nsew")

        communityRatingText = ctk.CTkLabel(communityRatingFrame, text=" / 10")
        communityRatingText.grid(row=1, column=1, padx = (5,10) , pady=(10,10), sticky = "nsew")

        ### Runtime (Input) ###
        runtimeFrame = ctk.CTkFrame(leftColumn,corner_radius=6, fg_color="#333333")
        runtimeFrame.grid(row = 2, column = 0, pady=(10,0), padx=10, sticky = "nsew")
        runtimeFrame.grid_columnconfigure(0, weight = 1)
        runtimeFrame.grid_rowconfigure(1, weight = 1)

        runtimeTitle = ctk.CTkLabel(runtimeFrame, corner_radius=6, fg_color="black", text = "Runtime")
        runtimeTitle.grid(row=0, column=0, columnspan = 2, sticky = "ew")
        
        self.runtimeEntry=ctk.CTkEntry(runtimeFrame, fg_color="#2b2b2b")
        self.runtimeEntry.grid(row=1, column=0, padx = (10,5), pady=(10,10), sticky = "nsew")

        runtimeText = ctk.CTkLabel(runtimeFrame, text="minutes")
        runtimeText.grid(row=1, column=1, padx = (5,10) , pady=(10,10), sticky = "nsew")

        ### Episode Count (Input) ###
        episodeFrame = ctk.CTkFrame(leftColumn, corner_radius=6, fg_color="#333333")
        episodeFrame.grid(row = 2, column = 1, pady=(10,0), padx=10, sticky = "nsew")
        episodeFrame.grid_columnconfigure(0, weight = 1)
        episodeFrame.grid_rowconfigure(1, weight = 1)

        episodeTitle = ctk.CTkLabel(episodeFrame, corner_radius=6, fg_color="black", text = "Episode Count")
        episodeTitle.grid(row=0, column=0, sticky = "ew")
        
        self.episodeEntry=ctk.CTkEntry(episodeFrame, fg_color="#2b2b2b")
        self.episodeEntry.grid(row=1,column=0, padx = 10, pady=(10,10), sticky = "nsew")

        ### Media Type (Radio Button) ###
        mediaTypeFrame = ctk.CTkFrame(leftColumn,corner_radius=6, fg_color="#333333")
        mediaTypeFrame.grid(row = 3, column = 0, pady=(10,0), padx=10, sticky = "nsew")
        mediaTypeFrame.grid_columnconfigure(0, weight=1)

        mediaTypeTitle = ctk.CTkLabel(mediaTypeFrame, corner_radius=6, fg_color="black", text = "Media Type")
        mediaTypeTitle.grid(row=0, column=0, sticky = "ew")
        
        mediaTypeListFrame = ctk.CTkFrame(mediaTypeFrame, corner_radius=6, fg_color="#2b2b2b")
        mediaTypeListFrame.grid(row=1, column=0, sticky = "nsew", padx = 10, pady = 10)

        mediaTypeOptions = []
        self.mediaTypeVar = tk.IntVar(value = 0)

        def mediaTypeVarEvent():
            print(f"Setting Media Type as: {Media.MEDIATYPE[self.mediaTypeVar.get()]}")

        for index, mediaType in Media.MEDIATYPE.items():
            mediaTypeOptions.append(ctk.CTkRadioButton(mediaTypeListFrame, text=f"{mediaType}", command=mediaTypeVarEvent, variable = self.mediaTypeVar, value = index))
            mediaTypeOptions[index].grid(row=index,column=0, columnspan = 2, pady=(10,0), padx = 10, sticky = "w")
        
        mediaTypeOptions[-1].grid(row=2,column=0, pady=(10,10), padx = 10, sticky = "w")
        
        ### Media Format (Checklist) ###
        mediaFormatFrame = ctk.CTkFrame(leftColumn, corner_radius=6, fg_color="#333333")
        mediaFormatFrame.grid(row = 4, column = 0, pady=(10,0), padx=10, sticky = "nsew")

        mediaFormatFrame.grid_columnconfigure(0, weight=1)
        mediaFormatFrame.grid_rowconfigure(1, weight=1)

        mediaFormatTitle = ctk.CTkLabel(mediaFormatFrame, text = "Add Formats", corner_radius=6, fg_color="black")
        mediaFormatTitle.grid(row=0, column = 0, pady = (0,10), sticky = "we")
        
        self.mediaformatIncludeCheck = [tk.BooleanVar(value=False) for _ in range(3)]

        mediaFormatInclude = []
        mediaFormatColumn = ctk.CTkFrame(mediaFormatFrame, fg_color="#2b2b2b", corner_radius=6)
        mediaFormatColumn.grid(row = 1, column = 0, padx = (10,10), pady = (0,10), sticky = "nswe")

        def formatIncludeEvent(index):
            print(f'Setting status of {Media.MEDIAFORMAT[index]} as: {self.mediaformatIncludeCheck[index].get()}')

        for index, mediaFormat in Media.MEDIAFORMAT.items():
            mediaFormatInclude.append(ctk.CTkCheckBox(mediaFormatColumn, text = f"{mediaFormat}", command = lambda value = index: formatIncludeEvent(value), variable=self.mediaformatIncludeCheck[index], onvalue=True, offvalue=False))
            mediaFormatInclude[index].grid(row = index, column = 0, padx = (10,10), pady = (5,5), sticky = "w")
        
        mediaFormatInclude[0].grid(row = 0, column = 0, padx = (10,10), pady = (10,5), sticky = "w")
        mediaFormatInclude[-1].grid(row = 2, column = 0, padx = (10,10), pady = (5,10), sticky = "w")

        ### Poster Image (File Upload) ###
        def getPosterImage():
            self.posterImagePath = fd.askopenfilename(filetypes = [('JPEG Files', '*.jpeg'),('JPG Files', '*.jpg'),('PNG Files', '*.png'),('All Files', '*.*')])
            aspectRatio = posterHeight/Image.open(self.posterImagePath).height
            posterImage = ctk.CTkImage(light_image=Image.open(self.posterImagePath),
                                  dark_image=Image.open(self.posterImagePath),
                                  size=(Image.open(self.posterImagePath).width * aspectRatio, posterHeight))

            self.posterImageLabel = ctk.CTkLabel(posterImageFrame, image=posterImage, text="") # Cover Image
            self.posterImageLabel.grid(row=1, column = 0, pady=(0,10), padx=20, sticky = "ew")
            self.update()

        posterImageFrame = ctk.CTkFrame(leftColumn, corner_radius=6, width = 300, fg_color= "#333333")
        posterImageFrame.grid(row = 3, column = 1, pady=(10,0), padx=10, sticky = "nsew")
        posterImageFrame.grid_columnconfigure(0, weight=1)

        posterHeight = 105
        self.posterImagePath = "imgsrc/util/portrait.jpg"
        aspectRatio = posterHeight/Image.open(self.posterImagePath).height
        posterImage = ctk.CTkImage(light_image=Image.open(self.posterImagePath),
                                  dark_image=Image.open(self.posterImagePath),
                                  size=(Image.open(self.posterImagePath).width * aspectRatio, posterHeight))

        posterImageButton = ctk.CTkButton(posterImageFrame, text = "Upload Poster Image", corner_radius=6, command = getPosterImage, font = ("Ariel", 16 ,"bold"))
        posterImageButton.grid(row=0, column = 0, pady = (0,10), padx = 0, sticky = "we")

        self.posterImageLabel = ctk.CTkLabel(posterImageFrame, image=posterImage, text="", corner_radius=6) # Cover Image
        self.posterImageLabel.grid(row=1, column = 0, pady=(0,10), padx=20, sticky = "nswe")

        ### Cover Image (File Upload) ###
        def getCoverImage():
            self.coverImagePath = fd.askopenfilename(filetypes = [('JPEG Files', '*.jpeg'),('JPG Files', '*.jpg'),('PNG Files', '*.png'),('All Files', '*.*')])
            aspectRatio = coverHeight/Image.open(self.coverImagePath).height
            coverImage = ctk.CTkImage(light_image=Image.open(self.coverImagePath),
                                  dark_image=Image.open(self.coverImagePath),
                                  size=(Image.open(self.coverImagePath).width * aspectRatio, coverHeight))

            self.coverImageLabel = ctk.CTkLabel(coverImageFrame, image=coverImage, text="") # Cover Image
            self.coverImageLabel.grid(row=1, column = 0, pady=(0,10), padx=20, sticky = "ew")
            self.update()

        coverImageFrame = ctk.CTkFrame(leftColumn, corner_radius=6, width = 300, fg_color= "#333333")
        coverImageFrame.grid(row = 4, column = 1, pady=(10,0), padx=10, sticky = "nsew")
        coverImageFrame.grid_columnconfigure(0, weight=1)

        coverHeight = 105
        self.coverImagePath = "imgsrc/util/landscape.jpg"
        aspectRatio = coverHeight/Image.open(self.coverImagePath).height
        coverImage = ctk.CTkImage(light_image=Image.open(self.coverImagePath),
                                  dark_image=Image.open(self.coverImagePath),
                                  size=(Image.open(self.coverImagePath).width * aspectRatio, coverHeight))

        coverImageButton = ctk.CTkButton(coverImageFrame, text = "Upload Cover Image", corner_radius=6, command = getCoverImage, font = ("Ariel", 16 ,"bold"))
        coverImageButton.grid(row=0, column = 0, pady = (0,10), padx = 0, sticky = "we")

        self.coverImageLabel = ctk.CTkLabel(coverImageFrame, image=coverImage, text="", corner_radius=6) # Cover Image
        self.coverImageLabel.grid(row=1, column = 0, pady=(0,10), padx=20, sticky = "nswe")

        ### Age Rating (Radio Button) ###
        ageClassificationFrame = ctk.CTkFrame(leftColumn,corner_radius=6, width = 300, fg_color="#333333")
        ageClassificationFrame.grid(row = 5, column = 0, pady=10, padx=10, sticky = "nsew")
        ageClassificationFrame.grid_columnconfigure(0, weight=1)
        ageClassificationFrame.grid_rowconfigure(1, weight=1)

        ageClassificationTitle = ctk.CTkLabel(ageClassificationFrame, corner_radius=6, fg_color="black", text = "Select Age Rating", width = 200)
        ageClassificationTitle.grid(row=0, column=0, columnspan = 2, sticky = "ew")
        
        ageClassificationListFrame = ctk.CTkFrame(ageClassificationFrame, corner_radius=6, fg_color="#2b2b2b")
        ageClassificationListFrame.grid(row = 1, column = 0, sticky = "nsew", padx = 10, pady = (10, 10))

        ageClassificationOptions = []
        self.ageClassificationVar = tk.IntVar(value = 0)

        def ageClassificationVarEvent():
            print(f"Setting Age Rating as: {Media.AGERATING[self.ageClassificationVar.get()]}")

        for index, ageClassification in Media.AGERATING.items():
            ageClassificationOptions.append(ctk.CTkRadioButton(ageClassificationListFrame, text=f"{ageClassification}", command=ageClassificationVarEvent, variable = self.ageClassificationVar, value = index))
            ageClassificationOptions[index].grid(row=index+1,column=0, pady=(10,0), padx = 10, sticky = "w")
        
        ageClassificationOptions[-1].grid(row=5,column=0, pady=(10,10), padx = 10, sticky = "w")

        ### Classification Notes ###
        classNotesFrame = ctk.CTkFrame(leftColumn, corner_radius=6, fg_color="#333333")
        classNotesFrame.grid(row=5, column = 1, sticky = "nsew", padx = 10, pady = 10)
        classNotesFrame.grid_columnconfigure(0, weight = 1)
        classNotesFrame.grid_rowconfigure(1, weight = 1)

        classNotesTitle = ctk.CTkLabel(classNotesFrame, corner_radius=6, fg_color="black", text = "Classification Notes", width = 200)
        classNotesTitle.grid(row=0, column=0, sticky = "ew")
        
        self.classNotesEntry = ctk.CTkTextbox(classNotesFrame, corner_radius=6, fg_color="#2b2b2b", border_width=2, border_color="#565b5e")
        self.classNotesEntry.grid(row = 1, column = 0, padx = 10, pady = (10, 10), sticky = "nsew")

        #########################################################################
        ### Middle Column
        middleColumn = ctk.CTkFrame(options, corner_radius= 6, fg_color="transparent")
        middleColumn.grid(row=0, column = 1, pady = 10, padx = 10, sticky = "nsew")
        middleColumn.grid_columnconfigure(0, weight=1)
        
        middleColumn.grid_rowconfigure(1, weight = 1, uniform = "maple")
        middleColumn.grid_rowconfigure(2, weight = 1, uniform = "maple")

        ### Tagline (Entry)
        taglineFrame = ctk.CTkFrame(middleColumn, corner_radius=6, fg_color="#333333")
        taglineFrame.grid(row = 0, column = 0, pady = (5,0), padx=10, sticky = "nsew")
        taglineFrame.grid_columnconfigure(0, weight = 1)
        taglineFrame.grid_rowconfigure(1, weight = 1)

        taglineTitle = ctk.CTkLabel(taglineFrame, corner_radius=6, fg_color="black", text = "Tagline")
        taglineTitle.grid(row=0, column=0, sticky = "ew")
        
        self.taglineEntry=ctk.CTkEntry(taglineFrame, fg_color="#2b2b2b")
        self.taglineEntry.grid(row=1,column=0, padx = 10, pady=(10,10), sticky = "nsew")

        ### Description (Textbook)
        descriptionFrame = ctk.CTkFrame(middleColumn, corner_radius=6, fg_color="#333333")
        descriptionFrame.grid(row = 1, column = 0, pady = (10,0), padx=10, sticky = "nsew")
        descriptionFrame.grid_columnconfigure(0, weight = 1)
        descriptionFrame.grid_rowconfigure(1, weight = 1)

        descriptionTitle = ctk.CTkLabel(descriptionFrame, corner_radius=6, fg_color="black", text = "Description")
        descriptionTitle.grid(row=0, column=0, sticky = "ew")
        
        self.descriptionEntry=ctk.CTkTextbox(descriptionFrame, fg_color="#2b2b2b", border_width=2, border_color="#565b5e")
        self.descriptionEntry.grid(row=1,column=0, padx = 10, pady=(10,10), sticky = "nsew")

        ### Viewing Notes (Input)
        noteFrame = ctk.CTkFrame(middleColumn,corner_radius=6, fg_color="#333333")
        noteFrame.grid(row = 2, column = 0, pady=(10,0), padx=10, sticky = "nsew")
        noteFrame.grid_columnconfigure(0, weight = 1)
        noteFrame.grid_rowconfigure(1, weight = 1)

        noteTitle = ctk.CTkLabel(noteFrame, corner_radius=6, fg_color="black", text = "Viewing Notes")
        noteTitle.grid(row=0, column=0, sticky = "ew")
        
        self.noteEntry=ctk.CTkTextbox(noteFrame, fg_color="#2b2b2b",  border_width=2, border_color="#565b5e")
        self.noteEntry.grid(row=1,column=0, padx = 10, pady=(10,10), sticky = "nsew")

        #########################################################################
        ### Right Column
        rightColumn = ctk.CTkFrame(options, corner_radius= 6, fg_color="transparent")
        rightColumn.grid(row=0, column = 2, pady = 10, padx = 10, sticky = "nsew")
        rightColumn.grid_columnconfigure(0, weight=1)

        rightColumn.grid_rowconfigure(1, weight=1)

        ### Genre Row
        genreColumnFrame = ctk.CTkFrame(rightColumn, corner_radius=6, fg_color="#333333")
        genreColumnFrame.grid(row = 0, column = 0, pady=(5,0), padx=10, sticky = "nsew")

        genreColumnFrame.grid_columnconfigure(0, weight=1)
        genreColumnFrame.grid_rowconfigure(1, weight=1)

        genreTitle = ctk.CTkLabel(genreColumnFrame, text = "Add Genres", corner_radius=6, fg_color="black")
        genreTitle.grid(row=0, column = 0, pady = (0,10), sticky = "we")
        
        self.genreIncludeCheck = [tk.BooleanVar(value=False) for _ in range(13)]

        genreInclude = []
        genreColumn = ctk.CTkFrame(genreColumnFrame, fg_color="#2b2b2b", corner_radius=6)
        genreColumn.grid(row = 1, column = 0, padx = (10,10), pady = (0,10), sticky = "nswe")

        def genreIncludeEvent(index):
            print(f'Setting status of {Media.GENRE[index]} as: {self.genreIncludeCheck[index].get()}')

        for index, genre in Media.GENRE.items():
            genreInclude.append(ctk.CTkCheckBox(genreColumn, text = f"{genre}", command = lambda value = index: genreIncludeEvent(value), variable=self.genreIncludeCheck[index], onvalue=True, offvalue=False))
            genreInclude[index].grid(row = index, column = 0, padx = (10,10), pady = (10,10), sticky = "w")

        ### Source Textbox
        sourceFrame = ctk.CTkFrame(rightColumn,corner_radius=6, fg_color="#333333")
        sourceFrame.grid(row = 1, column = 0, pady=(10,0), padx=10, sticky = "nsew")
        sourceFrame.grid_columnconfigure(0, weight = 1)
        sourceFrame.grid_rowconfigure(1, weight = 1)

        sourceTitle = ctk.CTkLabel(sourceFrame, corner_radius=6, fg_color="black", text = "Sources")
        sourceTitle.grid(row=0, column=0, sticky = "ew")
        
        self.sourceEntry=ctk.CTkTextbox(sourceFrame, fg_color="#2b2b2b", border_width=2, border_color="#565b5e")
        self.sourceEntry.grid(row=1,column=0, padx = 20, pady=(10,10), sticky = "nsew")
        #########################################################################
        ### Franchise Frame
        franchiseOptionFrame = ctk.CTkFrame(options, corner_radius=6, fg_color="#333333")
        franchiseOptionFrame.grid(row = 1, column = 0, columnspan = 3, pady=(5,10), padx=20, sticky = "nsew")
        franchiseOptionFrame.grid_columnconfigure(1, weight = 1)

        franchiseTitle = ctk.CTkLabel(franchiseOptionFrame, corner_radius=6, fg_color="black", text = "Add this media to these Franchises")
        franchiseTitle.grid(row=0, column=0, columnspan = 2, sticky = "ew")

        # Add ability to add to Franchises
        self.franchiseChecklist = [tk.BooleanVar(value=False) for _ in range(len(franchiseList))]
        self.franchiseOptions = []
        self.franchiseButtons = []

        for i in range(len(franchiseList)):
            self.grid_rowconfigure(i+1, weight=1)
            self.franchiseOptions.append(franchiseListing(franchiseOptionFrame, franchiseList[i]))
            self.franchiseOptions[i].grid(row=i + 1, column = 1, padx=(0,10), pady=(10, 0), sticky = "ew")

            # self.buttons.append(ctk.CTkButton(self, text=f'More Info', width = 120, height = 50, font = ("ArielBold", 18), command = lambda franchiseChoice=franchiseList[i]: master.displayFranchise(franchiseChoice)))
            self.franchiseButtons.append(ctk.CTkCheckBox(franchiseOptionFrame, text=f'', variable = self.franchiseChecklist[i], onvalue=True, offvalue=False))
            self.franchiseButtons[i].grid(row =i+1, column = 0, padx = (20,20), pady = (10,0), sticky = "ew")
        #########################################################################
        self.franchiseOptions[i].grid(row=i + 1, column = 1, padx=(0,10), pady=(10, 10), sticky = "ew")
        self.franchiseButtons[i].grid(row =i+1, column = 0, padx = (30,30), pady = (10,10))

        ### Add Button
        addButton = ctk.CTkButton(self, text= "Add New Media", font = ("Ariel", 24, "bold"),  command = self.addEvent, border_spacing=20)
        addButton.grid(row = 2, column = 0, padx = (100,100), pady = (5,10), sticky = "we")

    def addEvent(self):
        noErrors = True
        name = self.nameEntry.get()

        ### Year Check ##
        yearRelease = self.yearEntry.get()
        if len(yearRelease) == 4 and yearRelease.isnumeric():
            yearRelease = int(yearRelease)
            self.yearEntry.configure(text_color = "white")
        else:
            noErrors = False
            self.yearEntry.configure(text_color = "red")

        ### Rating Check ###
        rating = self.communityRatingEntry.get()

        try:
            rating = float(rating)
            if rating > 10 or rating < 0:
                noErrors = False
                self.communityRatingEntry.configure(text_color = "red")
            else:
                self.communityRatingEntry.configure(text_color = "white")
        except ValueError:
            noErrors = False
            self.communityRatingEntry.configure(text_color = "red")

        # if (not rating.isdecimal() or not rating.isnumeric()):
        #     rating = float(rating)
        #     if rating > 10 or rating < 0:
        #         noErrors = False
        #         self.communityRatingEntry.configure(text_color = "red")
        #     else:
        #         self.communityRatingEntry.configure(text_color = "white")
        # else:
        #     noErrors = False
        #     self.communityRatingEntry.configure(text_color = "red")

        ### Runtime Check ###
        runtime = self.runtimeEntry.get()
        if not runtime.isnumeric():
            noErrors = False
            self.runtimeEntry.configure(text_color = "red")
        else:
            runtime = int(runtime)
            if runtime <= 0:
                noErrors = False
                self.runtimeEntry.configure(text_color = "red")
            else:
                self.runtimeEntry.configure(text_color = "white")

        ### Media Type Check ###
        mediaType = self.mediaTypeVar.get()
        ageClassification = self.ageClassificationVar.get()
        ageNote = self.classNotesEntry.get("0.0", "end").replace("\n"," ")

        if mediaType == 1:
            episode = self.episodeEntry.get()
            if not episode.isnumeric():
                noErrors = False
                self.episodeEntry.configure(text_color = "red")
            else:
                episode = int(episode)
                if episode < 0:
                    noErrors = False 
                    self.episodeEntry.configure(text_color = "red")
                else:
                    self.episodeEntry.configure(text_color = "white")
        else:
            episode = 1
        
        ### Media Format List Check ###
        mediaFormat = self.mediaformatIncludeCheck
        mediaFormatList = []
        for i in range(len(mediaFormat)):
            if mediaFormat[i].get():
                mediaFormatList.append(i)

        if len(mediaFormatList) != 0:
            mediaFormatList = set(mediaFormatList)
        else:
            noErrors = False

        ### Genre List Check ###
        genre = self.genreIncludeCheck
        genreList = []

        for j in range(len(genre)):
            if genre[j].get():
                genreList.append(j)
        
        if len(genreList) != 0:
            genreList = set(genreList)
        else:
            noErrors = False

        ### Text Input Check ###
        tagline = self.taglineEntry.get()

        description = self.descriptionEntry.get("0.0", "end")
        description.replace("\n\n", "\n")

        viewingNote = self.noteEntry.get("0.0", "end")
        viewingNote.replace("\n\n", "\n")

        source  = self.sourceEntry.get("0.0", "end")
        source = source.split("\n")

        print(f"Is there no errors: {noErrors}")
        print(self.coverImagePath)
        print(self.posterImagePath)

        if noErrors:
            ### Variable Creation ###
            globals()[parseName(name)] = Media(name, ageClassification, yearRelease, mediaType, rating, description, runtime, episode, mediaFormatList, tagline, genreList, source, viewingNote, ageNote)
            globals()[parseName(name)].writeText()
            copyfile(self.posterImagePath, f'imgsrc/media/{parseName(name)}Poster.jpg')
            copyfile(self.coverImagePath, f'imgsrc/media/{parseName(name)}.jpg')
            mediaList.append(globals()[parseName(name)])
            fullUpdateMasterMedia()

            ### Update all franchise
            for index in range(len(franchiseList)):
                franchise = franchiseList[index]
                if self.franchiseChecklist[index].get():
                    franchise.updateMedia(globals()[parseName(name)])
                    franchise.writeText()

            self.master.displayMedia(globals()[parseName(name)])
        
        else:
            self.update()

class newFranchiseFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, width = 1600, height = 1000)
        self.grid_columnconfigure(0, weight=1)

        self.grid_rowconfigure(0, weight = 0)
        self.grid_rowconfigure(1, weight = 1)
        self.grid_rowconfigure(2, weight = 0)
        
        #### Title
        newMediaTitle = ctk.CTkLabel(self, text = "Add New Franchise", fg_color="black", corner_radius=6, height = 80, width=1600, font = ("Ariel", 30, "bold"))
        newMediaTitle.grid(row = 0, column = 0, pady=(10,5), padx=10, sticky = "nsew")

        #### Click Options
        options = ctk.CTkFrame(self, corner_radius=6, width=1600, height = 800)
        options.grid(row = 1, column = 0, pady=(5,5), padx=10, sticky = "nsew")

        options.grid_rowconfigure(0, weight = 1)
        options.grid_columnconfigure(0, weight = 0, uniform = "green")
        options.grid_columnconfigure(1, weight = 1)

        ### Option Selector
        #########################################################################
        ## Left Column
        leftColumn = ctk.CTkFrame(options, fg_color = "transparent")
        leftColumn.grid(row=0, column=0, pady=(10,10), padx=10, sticky = "nsew")

        leftColumn.grid_columnconfigure(0, weight=1)
        leftColumn.grid_rowconfigure(2, weight = 1)

        ### Name (Input)
        nameFrame = ctk.CTkFrame(leftColumn, corner_radius=6, fg_color="#333333")
        nameFrame.grid(row = 0, column = 0, columnspan = 2, pady = (0,0), padx=10, sticky = "nsew")
        nameFrame.grid_columnconfigure(0, weight = 1)
        nameFrame.grid_rowconfigure(6, weight = 1)

        nameTitle = ctk.CTkLabel(nameFrame, corner_radius=6, fg_color="black", text = "Name")
        nameTitle.grid(row=0, column=0, sticky = "ew")
        
        self.nameEntry=ctk.CTkEntry(nameFrame, fg_color="#2b2b2b")
        self.nameEntry.grid(row=1,column=0, padx = 10, pady=(10,10), sticky = "nsew")
        
        ### Tagline (Entry)
        taglineFrame = ctk.CTkFrame(leftColumn, corner_radius=6, fg_color="#333333")
        taglineFrame.grid(row = 1, column = 0, pady = (10,0), padx=10, sticky = "nsew")
        taglineFrame.grid_columnconfigure(0, weight = 1)
        taglineFrame.grid_rowconfigure(1, weight = 1)

        taglineTitle = ctk.CTkLabel(taglineFrame, corner_radius=6, fg_color="black", text = "Tagline")
        taglineTitle.grid(row=0, column=0, sticky = "ew")
        
        self.taglineEntry=ctk.CTkEntry(taglineFrame, fg_color="#2b2b2b")
        self.taglineEntry.grid(row=1,column=0, padx = 10, pady=(10,10), sticky = "nsew")
        
        ### Viewing Notes (Input)
        noteFrame = ctk.CTkFrame(leftColumn,corner_radius=6, fg_color="#333333")
        noteFrame.grid(row = 2, column = 0, pady=(10,0), padx=10, sticky = "nsew")
        noteFrame.grid_columnconfigure(0, weight = 1)
        noteFrame.grid_rowconfigure(1, weight = 1)

        noteTitle = ctk.CTkLabel(noteFrame, corner_radius=6, fg_color="black", text = "Viewing Notes")
        noteTitle.grid(row=0, column=0, sticky = "ew")
        
        self.noteEntry=ctk.CTkTextbox(noteFrame, fg_color="#2b2b2b",  border_width=2, border_color="#565b5e")
        self.noteEntry.grid(row=1,column=0, padx = 10, pady=(10,10), sticky = "nsew")

        #########################################################################
        ### Right Column
        rightColumn = ctk.CTkFrame(options, corner_radius= 6, fg_color = "#333333")
        rightColumn.grid(row=0, column = 1, pady = (10,10), padx = 10, sticky = "nsew")
        rightColumn.grid_columnconfigure(0, weight=1)
        rightColumn.grid_rowconfigure(1, weight=1)

        addMediaLabel = ctk.CTkLabel(rightColumn, corner_radius=6, fg_color="black", text = "Add Media From Franchise")
        addMediaLabel.grid(row=0, column=0, sticky = "ew")

        # List of All Media
        mediaCount = len(mediaList)
        self.mediaInclude = [tk.BooleanVar(value=False) for _ in range(mediaCount)]

        mediaColumn = ctk.CTkScrollableFrame(rightColumn, fg_color="#333333", corner_radius=6)
        mediaColumn.grid(row = 1, column = 0, padx = (10,10), pady = (5,10), sticky = "nswe")

        mediaColumn.grid_columnconfigure(0, weight = 1)
        mediaColumn.grid_columnconfigure(1, weight = 1)

        mediaColumn.currentMediaList = []
        mediaColumn.currentMediaChecklist = []

        def mediaIncludeEvent(index):
            print(f'Setting status of {mediaList[index].name} as: {self.mediaIncludeCheck[index].get()}')

        for index in range(mediaCount):
            mediaColumn.grid_rowconfigure(index, weight = 1)
            mediaColumn.currentMediaChecklist.append(ctk.CTkCheckBox(mediaColumn, text = "", command = lambda value = index: mediaIncludeEvent(value), variable=self.mediaInclude[index], onvalue=True, offvalue=False, width = 20))
            mediaColumn.currentMediaChecklist[index].grid(row = index, column = 0, padx = (10,0), pady = (0,10), sticky = "ew")

            mediaColumn.currentMediaList.append(mediaListing(mediaColumn, mediaList[index]))
            mediaColumn.currentMediaList[index].grid(row = index, column = 1, padx = (0,10), pady = (0,10), sticky = "nsew")

        #########################################################################
        ### Add Button
        addButton = ctk.CTkButton(self, text= "Add New Franchise", font = ("Ariel", 24, "bold"),  command = self.addEvent, border_spacing=20)
        addButton.grid(row = 2, column = 0, padx = (100,100), pady = (5,10), sticky = "we")
    
    def addEvent(self):
        noErrors = True
        name = self.nameEntry.get()
        tagline = self.taglineEntry.get()
        note = self.noteEntry.get("0.0","end")
        note = note.replace("\n\n", "\n")

        media = []

        for index in range(len(self.mediaInclude)):
            status = self.mediaInclude[index].get()
            if status:
                media.append(mediaList[index])

        if noErrors:
            globals()[parseName(name)+"Collection"] = Franchise(name, media, note, tagline)
            globals()[parseName(name)+"Collection"].writeText()
            franchiseList.append(globals()[parseName(name)+"Collection"])
            fullUpdateMasterFranchise()

            self.master.displayFranchise(globals()[parseName(name)+"Collection"])

### List frames ###
### For Media Objects
class mediaListFrame(ctk.CTkFrame):
    def __init__(self, master: mainContentFrame):
        super().__init__(master, width = 1600, height = 1000)
        self.grid_columnconfigure(0, weight=1)

        self.grid_rowconfigure(0, weight = 0)
        self.grid_rowconfigure(1, weight = 0)
        self.grid_rowconfigure(2, weight = 1)

        #### Title
        labelName = ctk.CTkLabel(self, text = "List of All Media", fg_color="black", corner_radius=6, height = 80, width=1600, font = ("Ariel", 30, "bold"))
        labelName.grid(row = 0, column = 0, pady=(10,10), padx=10, sticky = "nsew")

        #### Sorting and Filtering Options
        options = ctk.CTkFrame(self, corner_radius=6, width=1600, height = 500)
        options.grid(row = 1, column = 0, pady=(10,10), padx=10, sticky = "nsew")

        options.grid_columnconfigure(0, weight = 1, uniform = "white")
        options.grid_columnconfigure(1, weight = 1, uniform = "white")
        options.grid_columnconfigure(2, weight = 1, uniform = "white")
        options.grid_columnconfigure(3, weight = 1, uniform = "white")
        options.grid_columnconfigure(4, weight = 1, uniform = "white")
        options.grid_columnconfigure(5, weight = 0)

        options.grid_rowconfigure(0, weight = 0)
        options.grid_rowconfigure(1, weight = 1)

        ######################################################################
        # Sort Bar
        # Sort Frame
        sortFrame = ctk.CTkFrame(options, corner_radius=6, width=300, fg_color = "transparent")
        sortFrame.grid(row = 0, column = 0, pady=(10,10), padx=10, sticky = "nsew")
        sortFrame.grid_columnconfigure(0, weight=1)
        sortFrame.grid_rowconfigure(1, weight =  1)

        ### Sorting Options: Column 0
        sortRadio = ctk.CTkFrame(sortFrame, corner_radius=6, width=300, fg_color = "#333333")
        sortRadio.grid(row = 0, column = 0, pady=0, padx=(0,10), sticky = "nsew")
        sortRadio.grid_columnconfigure(0, weight=1)

        def sortVarEvent():
            print(f"Sort Radio Options updated, now sorting by : {self.sortVar.get()}")
        
        def toggleDirectionEvent():
            if self.toggleDirectionVar.get() == 0:
                print(f"Toggling Direction to Ascend")
            else:
                print(f"Toggling Direction to Descend")

        sortLabel = ctk.CTkLabel(sortRadio, text="Sort Options", corner_radius=6, fg_color="black")
        sortLabel.grid(row=0,column=0, sticky = "we")

        self.sortVar = tk.IntVar(value=0)
        sortName = ctk.CTkRadioButton(sortRadio, text="Name",
                                                    command=sortVarEvent, variable= self.sortVar, value=0)
        sortName.grid(row=1,column=0, pady=(10,0), padx = (10,0), sticky="ew")
        
        sortYear = ctk.CTkRadioButton(sortRadio, text="Year of Release",
                                                    command=sortVarEvent, variable= self.sortVar, value=1)
        sortYear.grid(row=2,column=0, pady=(10,0), padx = (10,0), sticky="ew")
        
        sortRating = ctk.CTkRadioButton(sortRadio, text="Community Rating",
                                                    command=sortVarEvent, variable= self.sortVar, value=2)
        sortRating.grid(row=3,column=0, pady=(10,0), padx = (10,0), sticky="ew")
        
        sortRuntime = ctk.CTkRadioButton(sortRadio, text="Run Time",
                                                    command=sortVarEvent, variable= self.sortVar, value=3)
        sortRuntime.grid(row=4,column=0, pady=(10,10), padx = (10,0), sticky="ew")
        
        #### Sorting Direction
        directionFrame = ctk.CTkFrame(sortFrame, corner_radius=6, width=300, fg_color = "#333333")
        directionFrame.grid(row = 1, column = 0, pady=(10,0), padx=(0,10), sticky = "nsew")
        directionFrame.grid_columnconfigure(0, weight=1)

        ascensionLabel = ctk.CTkLabel(directionFrame, text="Direction of Sort", corner_radius=6, fg_color="black")
        ascensionLabel.grid(row=0,column=0, pady=(0,0), sticky="ew")
        
        self.toggleDirectionVar = tk.BooleanVar(value = False)
        
        toggleAsc = ctk.CTkRadioButton(directionFrame, text = "Ascending", command = toggleDirectionEvent, variable = self.toggleDirectionVar, value = True)
        toggleAsc.grid(row=1,column=0, pady=(10,0), padx = (10,0), sticky="ew")
        toggleDesc = ctk.CTkRadioButton(directionFrame, text = "Descending", command = toggleDirectionEvent, variable = self.toggleDirectionVar, value = False)
        toggleDesc.grid(row=2,column=0, pady=(10,10), padx = (10,0), sticky="ew")

        ### Media Type Filter (Radio Button): Column 1
        filterMediaType = ctk.CTkFrame(options,corner_radius=6, width = 300)
        filterMediaType.grid(row = 0, column = 1, pady=(10,10), padx=10, sticky = "nsew")
        filterMediaType.grid_columnconfigure(0, weight=1)

        filterMediaTypeTitle = ctk.CTkLabel(filterMediaType, corner_radius=6, fg_color="black", text = "Filter by Media Type")
        filterMediaTypeTitle.grid(row=0, column=0, sticky = "ew")
        
        filterMediaTypeOptions = []
        self.mediaTypeVar = tk.IntVar(value = 3)

        def mediaTypeVarEvent():
            print(f"Filtering Media Type by: {Media.MEDIATYPE[self.mediaTypeVar.get()]}")

        for index, mediaType in Media.MEDIATYPE.items():
            filterMediaTypeOptions.append(ctk.CTkRadioButton(filterMediaType, text=f"{mediaType}", command=mediaTypeVarEvent, variable =self.mediaTypeVar, value = index))
            filterMediaTypeOptions[index].grid(row=index+1,column=0, pady=(10,0), padx = 10, sticky = "w")
        
        filterMediaTypeOptions.append(ctk.CTkRadioButton(filterMediaType, text=f"No Filter", command=mediaTypeVarEvent, variable =self.mediaTypeVar, value = 3,  hover_color="#c33d3b", fg_color="red"))
        filterMediaTypeOptions[3].grid(row=3+1,column=0, pady=(10,0), padx = 10, sticky = "w")

        ### Community Rating Filter (Radio Button): Column 2
        filterCommunityRating = ctk.CTkFrame(options,corner_radius=6, width = 300)
        filterCommunityRating.grid(row = 0, column = 2, pady=(10,10), padx=10, sticky = "nsew")
        filterCommunityRating.grid_columnconfigure(0, weight=1)

        filterCommunityRatingTitle = ctk.CTkLabel(filterCommunityRating, corner_radius=6, fg_color="black", text = "Filter by Community Rating")
        filterCommunityRatingTitle.grid(row=0, column=0, sticky = "ew")
        
        filterCommunityRatingOptions = []
        self.communityRatingTypeVar = tk.IntVar(value = 6)

        def communityRatingTypeVarEvent():
            print(f"Filtering Community Rating by: {RATINGS[self.communityRatingTypeVar.get()]}")

        for index, grade in RATINGS.items():
            filterCommunityRatingOptions.append(ctk.CTkRadioButton(filterCommunityRating, text=f"{grade}", command=communityRatingTypeVarEvent, variable = self.communityRatingTypeVar, value = index))
            filterCommunityRatingOptions[index].grid(row=index+1,column=0, pady=(10,0), padx = 10, sticky = "w")

        ### Age Rating Filter (Radio Button)
        filterAgeClassification = ctk.CTkFrame(options,corner_radius=6, width = 300)
        filterAgeClassification.grid(row = 0, column = 3, pady=(10,10), padx=10, sticky = "nsew")
        filterAgeClassification.grid_columnconfigure(0, weight=1)

        filterAgeClassificationTitle = ctk.CTkLabel(filterAgeClassification, corner_radius=6, fg_color="black", text = "Filter by Age Rating", width = 200)
        filterAgeClassificationTitle.grid(row=0, column=0, sticky = "ew")
        
        filterAgeClassificationOptions = []
        self.ageClassificationVar = tk.IntVar(value = 5)

        def ageClassificationVarEvent():
            print(f"Filtering Age Rating by: {Media.AGERATING[self.ageClassificationVar.get()]}")

        for index, ageClassification in Media.AGERATING.items():
            filterAgeClassificationOptions.append(ctk.CTkRadioButton(filterAgeClassification, text=f"{ageClassification}", command=ageClassificationVarEvent, variable = self.ageClassificationVar, value = index))
            filterAgeClassificationOptions[index].grid(row=index+1,column=0, pady=(10,0), padx = 10, sticky = "w")
        
        filterAgeClassificationOptions.append(ctk.CTkRadioButton(filterAgeClassification, text=f"No Filter", command=ageClassificationVarEvent, variable = self.ageClassificationVar, value = 5,  hover_color="#c33d3b", fg_color="red"))
        filterAgeClassificationOptions[5].grid(row=5+1,column=0, pady=(10,0), padx = 10,  sticky = "w")
        
        ### Runtime Filter (Input)
        filterRuntime = ctk.CTkFrame(options,corner_radius=6, fg_color = "transparent")
        filterRuntime.grid(row = 0, column = 4, pady=(10,10), padx=10, sticky = "nsew")
        filterRuntime.grid_columnconfigure(0, weight=1)
        filterRuntime.grid_rowconfigure(0, weight = 1, uniform = "dutch")
        filterRuntime.grid_rowconfigure(1, weight = 1, uniform = "dutch")

        filterRuntimeTitle = ctk.CTkLabel(filterRuntime, corner_radius=6, fg_color="black", text = "Filter by Runtime")
        filterRuntimeTitle.grid(row=0, column=0, sticky = "ew", pady = (0,10))

        # Min Runtime Frame
        minRuntime = ctk.CTkFrame(filterRuntime, fg_color="#333333")
        minRuntime.grid(row=0, column = 0, padx = 0, pady = (0,10), sticky = "nsew")
        minRuntime.grid_columnconfigure(0, weight = 1, uniform="grass")
        minRuntime.grid_rowconfigure(1, weight = 1)

        minRuntimeTitle = ctk.CTkLabel(minRuntime, text = "Minimum Runtime", corner_radius=6, fg_color="black")
        minRuntimeTitle.grid(row=0, column =0, columnspan =2, padx = 0, pady = 0, sticky = "nsew")

        self.minRuntimeEntry = ctk.CTkEntry(minRuntime, corner_radius=6, fg_color="#2b2b2b")
        self.minRuntimeEntry.grid(row=1, column=0, padx = (10,5), pady=(10,10), sticky = "ew")
        self.minRuntimeEntry.insert("0", "0")

        minRuntimeText = ctk.CTkLabel(minRuntime, text="minutes")
        minRuntimeText.grid(row=1, column=1, padx = (5,10) , pady=(10,10), sticky = "nsew")

        # Max Runtime Frame
        maxRuntime = ctk.CTkFrame(filterRuntime, fg_color="#333333")
        maxRuntime.grid(row=1, column = 0, padx = 0, pady = (10,0), sticky = "nsew")
        maxRuntime.grid_columnconfigure(0, weight = 1, uniform="grass")
        maxRuntime.grid_rowconfigure(1, weight = 1)
        
        maxRuntime.grid_columnconfigure(0, weight = 1, uniform="grass")
        maxRuntime.grid_rowconfigure(1, weight = 1)

        maxRuntimeTitle = ctk.CTkLabel(maxRuntime, text = "Maximum Runtime", corner_radius=6, fg_color="black")
        maxRuntimeTitle.grid(row=0, column =0, columnspan = 2, padx = 0, pady = 0, sticky = "nsew")

        self.maxRuntimeEntry = ctk.CTkEntry(maxRuntime, corner_radius=6, fg_color="#2b2b2b")
        self.maxRuntimeEntry.grid(row=1, column=0, padx = (10,5), pady=(10,10), sticky = "ew")
        self.maxRuntimeEntry.insert("0", "100000")

        maxRuntimeText = ctk.CTkLabel(maxRuntime, text="minutes")
        maxRuntimeText.grid(row=1, column=1, padx = (5,10) , pady=(10,10), sticky = "nsew")

        ### Genre Filter
        genreFilter = ctk.CTkFrame(options, corner_radius=6, width = 300)
        genreFilter.grid(row = 0, column = 5, pady=(10,10), padx=10, sticky = "nsew")

        genreFilter.grid_columnconfigure(0, weight=0)
        genreFilter.grid_columnconfigure(1, weight=0)

        genreTitle = ctk.CTkLabel(genreFilter, text = "Choose Genres", corner_radius=6, fg_color="black")
        genreTitle.grid(row=0, column = 0, columnspan = 2, pady = (0,10), sticky = "we")

        genreIncludeLabel = ctk.CTkLabel(genreFilter, text = "Include Genres", corner_radius=6, fg_color="black")
        genreIncludeLabel.grid(row=1, column = 0, padx = (10,10), pady = (0,10), sticky = "we")

        genreRemoveLabel = ctk.CTkLabel(genreFilter, text = "Remove Genres", corner_radius=6, fg_color="black")
        genreRemoveLabel.grid(row=1, column = 1, padx = (10,10), pady = (0,10), sticky = "we")
        
        self.genreIncludeCheck = [tk.BooleanVar(value=False) for _ in range(13)]
        self.genreRemoveCheck = [tk.BooleanVar(value=False) for _ in range(13)]

        genreInclude = []
        genreRemove = []

        includeColumn = ctk.CTkScrollableFrame(genreFilter)
        includeColumn.grid(row = 2, column = 0, padx = (10,10), pady = (0,10), sticky = "we")
        removeColumn = ctk.CTkScrollableFrame(genreFilter)
        removeColumn.grid(row = 2, column = 1, padx = (10,10), pady = (0,10), sticky = "we")

        def genreIncludeEvent(index):
            print(f'Including {Media.GENRE[index]} in filter: {self.genreIncludeCheck[index].get()}')

        def genreRemoveEvent(index):
            print(f'Excluding {Media.GENRE[index]} in filter: {self.genreRemoveCheck[index].get()}')

        for index, genre in Media.GENRE.items():
            genreInclude.append(ctk.CTkCheckBox(includeColumn, text = f"{genre}", command = lambda value = index: genreIncludeEvent(value), variable=self.genreIncludeCheck[index], onvalue=True, offvalue=False))
            genreInclude[index].grid(row = index, column = 0, padx = (10,10), pady = (10,10), sticky = "w")

            genreRemove.append(ctk.CTkCheckBox(removeColumn, text = f"{genre}", command = lambda value = index: genreRemoveEvent(value), variable=self.genreRemoveCheck[index], onvalue=1, offvalue=0, hover_color="#c33d3b", fg_color="red"))
            genreRemove[index].grid(row = index, column = 1, padx = (10,10), pady = (10,10), sticky = "w")

        searchButton = ctk.CTkButton(options, text= "Search", command = self.searchEvent)
        searchButton.grid(row = 1, column = 0, columnspan = 6, padx = (10,10), pady = (10,10), sticky = "ew")

        # Listing
        self.listMedia = ctk.CTkScrollableFrame(self, fg_color = "#333333", corner_radius=6, width=1600)
        self.listMedia.grid(row = 2, column = 0, pady=(10,10), padx = 10, sticky = "nsew")

        self.listMedia.grid_columnconfigure(0, weight=1)
        self.listMedia.grid_columnconfigure(1, weight=0)

        self.listMedia.options = []
        self.listMedia.buttons = []

        for i in range(len(mediaList)):
            self.listMedia.options.append(mediaListing(self.listMedia, mediaList[i]))
            self.listMedia.options[i].grid(row = i, column = 0, padx=10, pady=(10, 10), sticky = "ew")

            # self.listMedia.buttons.append(ctk.CTkButton(self.listMedia, text=f'More Info', width = 120, height = 50, font = ("ArielBold", 18), command = lambda mediaChoice=mediaList[i]: master.displayMedia(mediaChoice)))
            self.listMedia.buttons.append(ctk.CTkButton(self.listMedia, image=infoImage, text=f'', width = 120, height = 50, font = ("ArielBold", 18), command = lambda mediaChoice=mediaList[i]: master.displayMedia(mediaChoice)))
            self.listMedia.buttons[i].grid(row = i, column = 1, padx = (10,10), pady = (10,10))
    
    ### Search Function
    def searchEvent(self):
        error = False
        varSort = (self.sortVar.get(), self.toggleDirectionVar.get())
        varFilt = (self.mediaTypeVar.get(), self.communityRatingTypeVar.get(), self.ageClassificationVar.get(), (self.minRuntimeEntry.get(),self.maxRuntimeEntry.get()), ([x.get() for x in self.genreIncludeCheck], [x.get() for x in self.genreRemoveCheck])) # (Media Type, Rating, Age Rating, Runtime, Genre)


        (minRuntime,maxRuntime) = varFilt[3]

        if (not minRuntime.isnumeric()) and (not maxRuntime.isnumeric()):
            error = True

        else:
            minRuntime = int(minRuntime)
            maxRuntime = int(maxRuntime)
            if maxRuntime < minRuntime:
                error = True

        if error:
            self.minRuntimeEntry.configure(text_color = "red")
            self.maxRuntimeEntry.configure(text_color = "red")
            self.update()

        else:
            print("\n\n\nSearching!!!")

            self.minRuntimeEntry.configure(text_color = "white")
            self.maxRuntimeEntry.configure(text_color = "white")
            self.update()
        
            ## Sorting
            if varSort[0] == 0:
                def localSort(media: Media):
                    return media.name
                processList = sorted(mediaList, key = localSort, reverse = varSort[1])
            elif varSort[0] == 1:
                def localSort(media: Media):
                    return media.yearRelease
                processList = sorted(mediaList, key = localSort, reverse = not varSort[1])
            elif varSort[0] == 2:
                def localSort(media: Media):
                    return media.rating
                processList = sorted(mediaList, key = localSort, reverse = not varSort[1])
            elif varSort[0] == 3:
                def localSort(media: Media):
                    return media.runtime
                processList = sorted(mediaList, key = localSort, reverse = not varSort[1])
            
            ## Filtering
            # Filtering by media type
            mediaType = varFilt[0]
            
            def removeMediaType(x: Media):
                if x.mediaType == mediaType:
                    return True
                else:
                    return False 
            
            if varFilt[0] == 3:
                processList = processList
            else:
                processList = list(filter(removeMediaType, processList))

            # Filtering by Community Rating
            def grade2MinRating(grade: int):
                # RATINGS = {0:"S", 1:"A+ or above", 2:"A or above", 3:"B+ or above", 4: "B or above", 5:"C or above", 6:"D or above"}
                if grade == 0:
                    return 90
                elif grade == 1:
                    return 85
                elif grade == 2:
                    return 80
                elif grade == 3:
                    return 75
                elif grade == 4:
                    return 70
                elif grade == 5:
                    return 60
                else:
                    return 0

            minRating = grade2MinRating(varFilt[1])

            def removeCommunityRating(x: Media):
                if x.rating >= minRating:
                    return True
                else:
                    return False 

            if varFilt[1] == 6:
                processList = processList
            else:
                processList = list(filter(removeCommunityRating, processList))
        
            # Filtering by Age Rating
            ageClassification = varFilt[2]
            
            def removeAgeClassification(x: Media):
                if x.ageClassification == ageClassification:
                    return True
                else:
                    return False 
            
            if varFilt[2] == 5:
                processList = processList
            else:
                processList = list(filter(removeAgeClassification, processList))

            def removeRuntime(x: Media):
                if x.runtime >= minRuntime and x.runtime <= maxRuntime:
                    return True
                else: 
                    return False
            
            if varFilt[3] == 0:
                processList = processList
            else:
                processList = list(filter(removeRuntime, processList))

            # Filter by Genre
            def booleanList2Index(list: list):
                indexArray = []
                for index in range(len(list)):
                    if list[index]:     
                        indexArray.append(index)
                return indexArray

            includedGenres = booleanList2Index(varFilt[4][0])

            for genre in includedGenres:
                print(f'Included Genre: {Media.GENRE[genre]}')
                def checkGenreIncluded(x: Media):
                    if genre in x.genre:
                        # print(f"{x.name} has {Media.GENRE[genre]}")
                        return True
                    else:
                        return False
                processList = list(filter(checkGenreIncluded, processList))
            
            print("\nRemaining Items after Including Genres: ", end="")    
            for item in processList:
                print(f'{item.name}', end=", ")
            print("")

            removedGenres = booleanList2Index(varFilt[4][1])

            for genre in removedGenres:
                print(f'Excluded Genre: {Media.GENRE[genre]}')
                def checkGenreNotIncluded(x: Media):
                    if genre not in x.genre:
                        # print(f"{x.name} does not have {Media.GENRE[genre]}")
                        return True
                    else:
                        return False
                processList = list(filter(checkGenreNotIncluded, processList))

            print("\nRemaining Items after Removing Genres: ", end="")
            for item in processList:
                print(f'{item.name}', end=", ")
            print("\n")

            # Listing
            self.listMedia.destroy()
            self.listMedia.pack_forget()
            self.listMedia.update()

            self.listMedia = ctk.CTkScrollableFrame(self, fg_color="gray30", corner_radius=6, width=1600, height = 1000)
            self.listMedia.grid(row = 2, column = 0, pady=(10,10), padx = 20, sticky = "nsew")

            self.listMedia.grid_columnconfigure(0, weight=1)
            self.listMedia.grid_columnconfigure(1, weight=0)

            self.listMedia.options = []
            self.listMedia.buttons = []

            i = 0
            for item in processList:
                self.listMedia.options.append(mediaListing(self.listMedia, item))
                self.listMedia.options[i].grid(row = i, column = 0, padx=10, pady=(10, 10), sticky = "ew")

                # self.listMedia.buttons.append(ctk.CTkButton(self.listMedia, text=f'More Info', width = 120, height = 50, font = ("ArielBold", 18), command = lambda mediaChoice=item: self.master.displayMedia(mediaChoice)))
                self.listMedia.buttons.append(ctk.CTkButton(self.listMedia, image=infoImage, text=f'', width = 120, height = 80, font = ("ArielBold", 18), command = lambda mediaChoice=mediaList[i]: self.master.displayMedia(mediaChoice)))            
                self.listMedia.buttons[i].grid(row = i, column = 1, padx = (10,10), pady = (10,10), sticky = "news")
                i = i + 1
            
            print("Finished Searching!!!")

class mediaListing(ctk.CTkFrame):
    def __init__(self, master: mediaListFrame, media:Media):
        super().__init__(master, corner_radius=6, height=100, width = 1600)
        self.grid_columnconfigure(0, weight = 0)
        self.grid_columnconfigure(1, weight = 1)
        self.grid_columnconfigure(2, weight = 1, uniform = "november")
        self.grid_columnconfigure(3, weight = 0)
        self.grid_columnconfigure(4, weight = 0)
        self.grid_columnconfigure(5, weight = 0)
        self.grid_columnconfigure(6, weight = 0)
        
        # Initial Data Values
        self.title = f'{media.name} ({media.yearRelease})'
        self.imgPath = f"imgsrc/media/{parseName(media.name)}.jpg"
        self.tagline = media.tagline
        self.mediaType = Media.MEDIATYPE[media.mediaType]
        self.rating = f'{media.rating} ({ratingConversion(media.rating)})'
        
        self.ageClassification = media.ageClassification

        ratingPath = getAgeClassificationImage(self.ageClassification)      
        ratingImage = ctk.CTkImage(light_image=Image.open(ratingPath),dark_image=Image.open(ratingPath), size = (50,50))

        # Widget Creation
        self.title = ctk.CTkLabel(self, text = self.title, font = ("Ariel", 22, 'bold'), width = 200)
        self.title.grid(row = 0, column = 0, padx = (10,10), pady = (10,10), sticky = "w")

        self.ageClassification = ctk.CTkLabel(self, image=ratingImage, text="")
        self.ageClassification.grid(row = 0, column = 1, padx = (10,10), pady = (10,10), sticky = "w")

        self.tagline = ctk.CTkLabel(self, text = self.tagline, font = ("Ariel", 20, 'italic'))
        self.tagline.grid(row = 0, column = 2, padx = (10,10), pady = (10,10), sticky = "w")

        self.mediaType = ctk.CTkLabel(self, text=self.mediaType, font = ("Ariel", 20, "bold"), text_color="#2fa572")
        self.mediaType.grid(row = 0, column = 3, padx = (10,10), pady = (10,10))

        self.rating = ctk.CTkLabel(self, text=f"Rating: {self.rating}", font = ("ArielBold", 20))
        self.rating.grid(row = 0, column = 4, padx = (10,10), pady = (10,10))

        # if not TV, then need to span across two columns
        if Media.MEDIATYPE[media.mediaType] != "TV Series":
            self.episodeCount = ctk.CTkLabel(self, text = f"                              ", font = ("Ariel", 18))
            self.episodeCount.grid(row = 0, column = 5, padx = (10,10), pady = (10,10))

            # self.runtime = ctk.CTkLabel(self, text = f"Runtime: {media.runtime}", font = ("Ariel", 18))
            # self.runtime.grid(row = 0, column = 5, columnspan = 2, padx = (10,10), pady = (10,10))

            self.runtime = ctk.CTkLabel(self, text = f"Runtime: {media.runtime}", font = ("Ariel", 18))
            self.runtime.grid(row = 0, column = 6, padx = (10,10), pady = (10,10))

        # else
        else:
            self.episodeCount = ctk.CTkLabel(self, text = f"Episode Count: {media.episodeCount}", font = ("Ariel", 18))
            self.episodeCount.grid(row = 0, column = 5, padx = (10,10), pady = (10,10))

            self.runtime = ctk.CTkLabel(self, text = f"Runtime: {media.runtime}", font = ("Ariel", 18))
            self.runtime.grid(row = 0, column = 6, padx = (10,10), pady = (10,10))

### For Franchise Objects
class franchiseListFrame(ctk.CTkScrollableFrame):
    def __init__(self, master: mainContentFrame):
        super().__init__(master, width = 1600, height = 1000)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)

        labelname = ctk.CTkLabel(self, text = "List of All Franchise", fg_color="black", corner_radius=6, height = 80, width=1600, font = ("Ariel", 30, "bold"))
        labelname.grid(row = 0, column = 0, columnspan = 2, pady=(10,10), padx=10, sticky = "nsew")

        ## Want to change it so that these are actually independant frames.
        self.options = []
        self.buttons = []
        for i in range(len(franchiseList)):
            self.grid_rowconfigure(i+1, weight=1)
            self.options.append(franchiseListing(self, franchiseList[i]))
            self.options[i].grid(row=i + 1, column = 0, padx=10, pady=(10, 0), sticky = "ew")

            # self.buttons.append(ctk.CTkButton(self, text=f'More Info', width = 120, height = 50, font = ("ArielBold", 18), command = lambda franchiseChoice=franchiseList[i]: master.displayFranchise(franchiseChoice)))
            self.buttons.append(ctk.CTkButton(self, text=f'',image=infoImage, width = 120, height = 50, font = ("ArielBold", 18), command = lambda franchiseChoice=franchiseList[i]: master.displayFranchise(franchiseChoice)))
            self.buttons[i].grid(row =i+1, column = 1, padx = (30,10), pady = (10,10))

class franchiseListing(ctk.CTkFrame):
    def __init__(self, master: franchiseListFrame, franchise:Franchise):
        super().__init__(master, corner_radius=6, height=100, width = 1600)
        self.grid_columnconfigure(0, weight = 0)
        self.grid_columnconfigure(1, weight = 1)
        self.grid_columnconfigure(2, weight = 1)
        self.grid_columnconfigure(3, weight = 0, uniform = "may")
        self.grid_columnconfigure(4, weight = 0, uniform = "may")

        # Initial Data Values
        self.title = f'{franchise.name} ({franchise.earliestMedia()})'
        self.tagline = f'{franchise.tagline}'
        self.count = f'Number of Media: {franchise.count}'
        self.score = "{:#.2f}".format(franchise.aveRating())+f' ({ratingConversion(franchise.aveRating())})'

        # Widget Creation
        self.title = ctk.CTkLabel(self, text = self.title, font = ("Ariel", 22, 'bold'), width = 200)
        self.title.grid(row = 0, column = 0, padx = (10,10), pady = (20,20), sticky = "w")

        self.ageClassification = franchise.maxAgeClassification()
        ratingPath = getAgeClassificationImage(self.ageClassification)      
        ratingImage = ctk.CTkImage(light_image=Image.open(ratingPath),dark_image=Image.open(ratingPath), size = (50,50))

        self.ageClassification = ctk.CTkLabel(self, image=ratingImage, text="")
        self.ageClassification.grid(row = 0, column = 1, padx = (10,10), pady = (10,10), sticky = "w")

        self.tagline = ctk.CTkLabel(self, text = self.tagline, font = ("Ariel", 20, 'italic'))
        self.tagline.grid(row = 0, column = 2, padx = (10,10), pady = (20,20), sticky = "ew")

        self.score = ctk.CTkLabel(self, text = self.score, font = ("Ariel", 20))
        self.score.grid(row = 0, column = 3, padx = (10,10), pady = (20,20), sticky = "we")

        self.count = ctk.CTkLabel(self, text = self.count, font = ("Ariel", 20))
        self.count.grid(row = 0, column = 4, padx = (10,10), pady = (20,20), sticky = "e")

### Random Frame ###
### This should give the user an option to filter by options and then it'll open the randomFrame screen.
class randomFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, width = 1600, height = 1000)
        self.grid_columnconfigure(0, weight=1)

        self.grid_rowconfigure(0, weight = 0)
        self.grid_rowconfigure(1, weight = 0)
        self.grid_rowconfigure(2, weight = 1)
        
        ################################################################################
        #### Title
        labelName = ctk.CTkLabel(self, text = "Random Media Picker", fg_color="black", corner_radius=6, height = 80, width=1600, font = ("Ariel", 30, "bold"))
        labelName.grid(row = 0, column = 0, pady=(10,10), padx=10, sticky = "nsew")

        ################################################################################
        #### Options Filtering
        options = ctk.CTkFrame(self, corner_radius=6, width=1600, height = 800)
        options.grid(row = 1, column = 0, pady=(10,10), padx=10, sticky = "nsew")

        options.grid_columnconfigure(0, weight = 0, uniform = "white")
        options.grid_columnconfigure(1, weight = 0, uniform = "white")
        options.grid_columnconfigure(2, weight = 1)

        options.grid_rowconfigure(0, weight = 1)

        ################## Left Column
        leftColumnFrame = ctk.CTkFrame(options, corner_radius=6, fg_color = "transparent")
        leftColumnFrame.grid(row=0, column = 0, pady = 10, padx = 10, sticky = "nsew")
        leftColumnFrame.grid_rowconfigure(0, weight = 1)
        leftColumnFrame.grid_rowconfigure(1, uniform = "birch")
        leftColumnFrame.grid_rowconfigure(2, uniform = "birch")

        ### Media Type Filter (Radio Button): Top Row
        filterMediaType = ctk.CTkFrame(leftColumnFrame,corner_radius=6, fg_color="#333333")
        filterMediaType.grid(row = 0, column = 0, pady=(0,10), padx=10, sticky = "nsew")
        filterMediaType.grid_columnconfigure(0, weight=1)

        filterMediaTypeTitle = ctk.CTkLabel(filterMediaType, corner_radius=6, fg_color="black", text = "Filter by Media Type")
        filterMediaTypeTitle.grid(row=0, column=0, sticky = "ew")
        
        filterMediaTypeOptions = []
        self.mediaTypeVar = tk.IntVar(value = 3)

        def mediaTypeVarEvent():
            print(f"Filtering Media Type by: {Media.MEDIATYPE[self.mediaTypeVar.get()]}")

        for index, mediaType in Media.MEDIATYPE.items():
            filterMediaTypeOptions.append(ctk.CTkRadioButton(filterMediaType, text=f"{mediaType}", command=mediaTypeVarEvent, variable =self.mediaTypeVar, value = index))
            filterMediaTypeOptions[index].grid(row=index+1,column=0, pady=(10,0), padx = 10, sticky = "w")
        
        filterMediaTypeOptions.append(ctk.CTkRadioButton(filterMediaType, text=f"No Filter", command=mediaTypeVarEvent, variable =self.mediaTypeVar, value = 3,  hover_color="#c33d3b", fg_color="red"))
        filterMediaTypeOptions[2].grid(row=3,column=0, pady=(10,10), padx=10, sticky = "w")

        ### Runtime Filter (Input)
        filterRuntime = ctk.CTkFrame(leftColumnFrame,corner_radius=6)
        filterRuntime.grid(row = 1, column = 0, pady=(10,10), padx=10, sticky = "nsew")
        filterRuntime.grid_columnconfigure(0, weight=1)
        filterRuntime.grid_rowconfigure(0, weight = 1, uniform = "dutch")
        filterRuntime.grid_rowconfigure(1, weight = 1, uniform = "dutch")

        filterRuntimeTitle = ctk.CTkLabel(filterRuntime, corner_radius=6, fg_color="black", text = "Filter by Runtime")
        filterRuntimeTitle.grid(row=0, column=0, sticky = "ew", pady = (0,10))

        # Min Runtime Frame
        minRuntime = ctk.CTkFrame(filterRuntime, fg_color="#333333")
        minRuntime.grid(row=0, column = 0, padx = 0, pady = (0,10), sticky = "nsew")
        minRuntime.grid_columnconfigure(0, weight = 1, uniform="grass")
        minRuntime.grid_rowconfigure(1, weight = 1)

        minRuntimeTitle = ctk.CTkLabel(minRuntime, text = "Minimum Runtime", corner_radius=6, fg_color="black")
        minRuntimeTitle.grid(row=0, column =0, columnspan =2, padx = 0, pady = 0, sticky = "nsew")

        self.minRuntimeEntry = ctk.CTkEntry(minRuntime, corner_radius=6, fg_color="#2b2b2b")
        self.minRuntimeEntry.grid(row=1, column=0, padx = (10,5), pady=(10,10), sticky = "ew")
        self.minRuntimeEntry.insert("0", "0")

        minRuntimeText = ctk.CTkLabel(minRuntime, text="minutes")
        minRuntimeText.grid(row=1, column=1, padx = (5,10) , pady=(10,10), sticky = "nsew")

        # Max Runtime Frame
        maxRuntime = ctk.CTkFrame(filterRuntime, fg_color="#333333")
        maxRuntime.grid(row=1, column = 0, padx = 0, pady = (10,0), sticky = "nsew")
        maxRuntime.grid_columnconfigure(0, weight = 1, uniform="grass")
        maxRuntime.grid_rowconfigure(1, weight = 1)
        
        maxRuntime.grid_columnconfigure(0, weight = 1, uniform="grass")
        maxRuntime.grid_rowconfigure(1, weight = 1)

        maxRuntimeTitle = ctk.CTkLabel(maxRuntime, text = "Maximum Runtime", corner_radius=6, fg_color="black")
        maxRuntimeTitle.grid(row=0, column =0, columnspan = 2, padx = 0, pady = 0, sticky = "nsew")

        self.maxRuntimeEntry = ctk.CTkEntry(maxRuntime, corner_radius=6, fg_color="#2b2b2b")
        self.maxRuntimeEntry.grid(row=1, column=0, padx = (10,5), pady=(10,10), sticky = "ew")
        self.maxRuntimeEntry.insert("0", "100000")

        maxRuntimeText = ctk.CTkLabel(maxRuntime, text="minutes")
        maxRuntimeText.grid(row=1, column=1, padx = (5,10) , pady=(10,10), sticky = "nsew")

        ######### Middle Column
        middleColumnFrame = ctk.CTkFrame(options, corner_radius=6, fg_color="transparent")
        middleColumnFrame.grid(row=0, column = 1, pady = 10, padx = 10, sticky = "nsew")

        ### Community Rating Filter (Radio Button): Column 2
        filterCommunityRating = ctk.CTkFrame(middleColumnFrame,corner_radius=6, width = 300, fg_color="#333333")
        filterCommunityRating.grid(row = 0, column = 0, pady=(0,10), padx=10, sticky = "nsew")
        filterCommunityRating.grid_columnconfigure(0, weight=1)

        filterCommunityRatingTitle = ctk.CTkLabel(filterCommunityRating, corner_radius=6, fg_color="black", text = "Filter by Community Rating")
        filterCommunityRatingTitle.grid(row=0, column=0, sticky = "ew")
        
        filterCommunityRatingOptions = []
        self.communityRatingTypeVar = tk.IntVar(value = 6)

        def communityRatingTypeVarEvent():
            print(f"Filtering Community Rating by: {RATINGS[self.communityRatingTypeVar.get()]}")

        for index, grade in RATINGS.items():
            filterCommunityRatingOptions.append(ctk.CTkRadioButton(filterCommunityRating, text=f"{grade}", command=communityRatingTypeVarEvent, variable = self.communityRatingTypeVar, value = index))
            filterCommunityRatingOptions[index].grid(row=index+1,column=0, pady=(10,0), padx = 10, sticky = "w")

        filterCommunityRatingOptions[-1].grid(row=index+1,column=0, pady=(10,10), padx = 10, sticky = "w")

        ### Age Rating Filter (Radio Button)
        filterAgeClassification = ctk.CTkFrame(middleColumnFrame,corner_radius=6, width = 300, fg_color="#333333")
        filterAgeClassification.grid(row = 1, column = 0, pady=(10,10), padx=10, sticky = "nsew")
        filterAgeClassification.grid_columnconfigure(0, weight=1)

        filterAgeClassificationTitle = ctk.CTkLabel(filterAgeClassification, corner_radius=6, fg_color="black", text = "Filter by Age Rating", width = 200)
        filterAgeClassificationTitle.grid(row=0, column=0, sticky = "ew")
        
        filterAgeClassificationOptions = []
        self.ageClassificationVar = tk.IntVar(value = 5)

        def ageClassificationVarEvent():
            print(f"Filtering Age Rating by: {Media.AGERATING[self.ageClassificationVar.get()]}")

        for index, ageClassification in Media.AGERATING.items():
            filterAgeClassificationOptions.append(ctk.CTkRadioButton(filterAgeClassification, text=f"{ageClassification}", command=ageClassificationVarEvent, variable = self.ageClassificationVar, value = index))
            filterAgeClassificationOptions[index].grid(row=index+1,column=0, pady=(10,0), padx = 10, sticky = "w")
        
        filterAgeClassificationOptions.append(ctk.CTkRadioButton(filterAgeClassification, text=f"No Filter", command=ageClassificationVarEvent, variable = self.ageClassificationVar, value = 5,  hover_color="#c33d3b", fg_color="red"))
        filterAgeClassificationOptions[5].grid(row=5+1,column=0, pady=(10,10), padx=10, sticky = "w")

        ######### Right Column
        ### Genre Filter
        genreFilter = ctk.CTkFrame(options, corner_radius=6, width = 800)
        genreFilter.grid(row = 0, column = 2, pady=(10,10), padx=10, sticky = "nsew")

        genreFilter.grid_columnconfigure(0, weight=1, uniform = "white" )
        genreFilter.grid_columnconfigure(1, weight=1, uniform = "white")
        genreFilter.grid_rowconfigure(2, weight=0)

        genreTitle = ctk.CTkLabel(genreFilter, text = "Choose Genres", corner_radius=6, fg_color="black")
        genreTitle.grid(row=0, column = 0, columnspan = 2, pady = (0,10), sticky = "we")

        genreIncludeLabel = ctk.CTkLabel(genreFilter, text = "Include Genres", corner_radius=6, fg_color="black")
        genreIncludeLabel.grid(row=1, column = 0, padx = (10,10), pady = (0,10), sticky = "we")

        genreRemoveLabel = ctk.CTkLabel(genreFilter, text = "Remove Genres", corner_radius=6, fg_color="black")
        genreRemoveLabel.grid(row=1, column = 1, padx = (10,10), pady = (0,10), sticky = "we")
        
        self.genreIncludeCheck = [tk.BooleanVar(value=False) for _ in range(13)]
        self.genreRemoveCheck = [tk.BooleanVar(value=False) for _ in range(13)]

        genreInclude = []
        genreRemove = []

        includeColumn = ctk.CTkFrame(genreFilter)
        includeColumn.grid(row = 2, column = 0, padx = (10,10), pady = (0,10), sticky = "nswe")
        removeColumn = ctk.CTkFrame(genreFilter)
        removeColumn.grid(row = 2, column = 1, padx = (10,10), pady = (0,10), sticky = "nswe")

        def genreIncludeEvent(index):
            print(f'Including {Media.GENRE[index]} in filter: {self.genreIncludeCheck[index].get()}')

        def genreRemoveEvent(index):
            print(f'Excluding {Media.GENRE[index]} in filter: {self.genreRemoveCheck[index].get()}')

        for index, genre in Media.GENRE.items():
            genreInclude.append(ctk.CTkCheckBox(includeColumn, text = f"{genre}", command = lambda value = index: genreIncludeEvent(value), variable=self.genreIncludeCheck[index], onvalue=True, offvalue=False))
            genreInclude[index].grid(row = index, column = 0, padx = (10,10), pady = (10,10), sticky = "w")

            genreRemove.append(ctk.CTkCheckBox(removeColumn, text = f"{genre}", command = lambda value = index: genreRemoveEvent(value), variable=self.genreRemoveCheck[index], onvalue=1, offvalue=0, hover_color="#c33d3b", fg_color="red"))
            genreRemove[index].grid(row = index, column = 1, padx = (10,10), pady = (10,10), sticky = "w")

        ################################################################################
        #### Search Button
        searchButton = ctk.CTkButton(self, text= "Give me something random!", font = ("Ariel", 24, "bold"),  command = self.randomEvent, border_spacing=20)
        searchButton.grid(row = 2, column = 0, columnspan = 6, padx = (100,100), pady = (0,10), sticky = "we")
    
    def randomEvent(self):
        error = False
        varFilt = (self.mediaTypeVar.get(), self.communityRatingTypeVar.get(), self.ageClassificationVar.get(), (self.minRuntimeEntry.get(),self.maxRuntimeEntry.get()), ([x.get() for x in self.genreIncludeCheck], [x.get() for x in self.genreRemoveCheck])) # (Media Type, Rating, Age Rating, Runtime, Genre)
        (minRuntime,maxRuntime) = varFilt[3]

        if minRuntime.isnumeric() and maxRuntime.isnumeric():
            minRuntime = int(minRuntime)
            maxRuntime = int(maxRuntime)
            if maxRuntime < minRuntime:
                error = True

        else:
            print("not numeric")
            error = True

        print(error)

        if error:
            self.minRuntimeEntry.configure(text_color = "red")
            self.maxRuntimeEntry.configure(text_color = "red")
            self.update()
        else:
            ## Filtering
            # Filtering by media type
            processList = mediaList
            mediaType = varFilt[0]
            
            def removeMediaType(x: Media):
                if x.mediaType == mediaType:
                    return True
                else:
                    return False 
            
            if varFilt[0] == 3:
                processList = processList
            else:
                processList = list(filter(removeMediaType, processList))

            # Filtering by Community Rating
            def grade2MinRating(grade: int):
                # RATINGS = {0:"S", 1:"A+ or above", 2:"A or above", 3:"B+ or above", 4: "B or above", 5:"C or above", 6:"D or above"}
                if grade == 0:
                    return 90
                elif grade == 1:
                    return 85
                elif grade == 2:
                    return 80
                elif grade == 3:
                    return 75
                elif grade == 4:
                    return 70
                elif grade == 5:
                    return 60
                else:
                    return 0

            minRating = grade2MinRating(varFilt[1])

            def removeCommunityRating(x: Media):
                if x.rating >= minRating:
                    return True
                else:
                    return False 

            if varFilt[1] == 6:
                processList = processList
            else:
                processList = list(filter(removeCommunityRating, processList))
        
            # Filtering by Age Rating
            ageClassification = varFilt[2]
            
            def removeAgeClassification(x: Media):
                if x.ageClassification == ageClassification:
                    return True
                else:
                    return False 
            
            if varFilt[2] == 5:
                processList = processList
            else:
                processList = list(filter(removeAgeClassification, processList))

            # Filtering by Runtime
            def removeRuntime(x: Media):
                if x.runtime >= minRuntime and x.runtime <= maxRuntime:
                    return True
                else: 
                    return False
            
            if varFilt[3] == 0:
                processList = processList
            else:
                processList = list(filter(removeRuntime, processList))
            if varFilt[3] == 0:
                processList = processList
            else:
                processList = list(filter(removeRuntime, processList))

            # Filter by Genre
            def booleanList2Index(list: list):
                indexArray = []
                for index in range(len(list)):
                    if list[index]:     
                        indexArray.append(index)
                return indexArray

            includedGenres = booleanList2Index(varFilt[4][0])

            for genre in includedGenres:
                print(f'Included Genre: {Media.GENRE[genre]}')
                def checkGenreIncluded(x: Media):
                    if genre in x.genre:
                        # print(f"{x.name} has {Media.GENRE[genre]}")
                        return True
                    else:
                        return False
                processList = list(filter(checkGenreIncluded, processList))
            
            print("\nRemaining Items after Including Genres: ", end="")    
            for item in processList:
                print(f'{item.name}', end=", ")
            print("")

            removedGenres = booleanList2Index(varFilt[4][1])

            for genre in removedGenres:
                print(f'Excluded Genre: {Media.GENRE[genre]}')
                def checkGenreNotIncluded(x: Media):
                    if genre not in x.genre:
                        # print(f"{x.name} does not have {Media.GENRE[genre]}")
                        return True
                    else:
                        return False
                processList = list(filter(checkGenreNotIncluded, processList))

            print("\nRemaining Items after Removing Genres: ", end="")
            for item in processList:
                print(f'{item.name}', end=", ")
            print("\n")

            processListLength = len(processList)
            if processListLength > 0:
                random.seed(datetime.now().timestamp())
                randomNumber = random.randint(0, processListLength-1)
                randomMedia = processList[randomNumber]
                print(randomMedia.name)

                self.master.displayMedia(randomMedia)

################################################################################
### Read Media Data
def readMasterMedia():
    """Will read the file called masterMedia.txt and create each individual Media file
    """
    globals()["mediaList"] = []
    fMaster = open("masterMedia.txt", "r")
    masterContent = fMaster.read().strip()
    if not masterContent:
        return
    
    mediaNames = masterContent.split("\n")
    fMaster.close()
    
    for media in mediaNames:
        mediaVarName = parseName(media)
        globals()[mediaVarName] = readMediaData(mediaVarName)
        mediaList.append(globals()[mediaVarName])

def readMediaData(fileName: str):
    """ Reads a .txt file from filmData to create an instance of Media

    Args:
        fileName (str): String of the filename used for the media

    Returns:
        Media: Returns instance of class Media
    """
    # Reading file contents
    f = open("filmData/" + fileName + ".txt", "r", encoding="Windows-1252")
    fileContent = f.read()
    att = fileContent.split("\n\n")

    # Modifying attributes to be correct data type
    name = att[0]
    
    ageClassification = int(att[1])
    
    yearRelease = int(att[2])
    
    mediaType = int(att[3]) 
    
    rating = float(att[4])
    
    description = att[5]
    
    runtime = int(att[6])
    
    episodeCount = int(att[7])
    
    mediaFormatElements = att[8].strip("{}").split(", ")
    mediaFormat = set(map(int, mediaFormatElements))

    tagline = att[9]

    genreElements = att[10].strip("{}").split(", ")
    genre = set(map(int, genreElements))

    source = att[11].split(",")

    viewingNote = att[12]

    ageNote = att[13]

    f.close()

    return Media(name, ageClassification, yearRelease, mediaType, rating, description, runtime, episodeCount, mediaFormat, tagline, genre, source, viewingNote, ageNote)

################################################################################
### Read Franchise Data
def readMasterFranchise():
    """Will read the file called masterFranchise.txt and create each individual Franchise file
    """
    # Reading file contents
    globals()["franchiseList"] = []
    fMaster = open("masterFranchise.txt", "r")
    masterContent = fMaster.read().strip()
    if not masterContent:
        return

    franchiseNames = masterContent.split("\n")
    fMaster.close()
    
    for franchise in franchiseNames:
        franchiseVarName = parseName(franchise)
        globals()[franchiseVarName + "Collection"] = readFranchiseData(franchiseVarName)
        franchiseList.append(globals()[franchiseVarName  + "Collection"])

def readFranchiseData(fileName: str):
    """Reads a .txt file from franchiseData to create an instance of Franchise

    Args:
        fileName (str): String of the filename used for the media

    Returns:
        Media: Returns instance of class Franchise
    """
    # Reading file contents
    f = open("franchiseData/" + fileName + ".txt", "r")
    fileContent = f.read()
    att = fileContent.split("\n\n")

    # Creating correct data types for media
    name = att[0]
    name = name

    mediaString = att[1].split(",")
    mediaLst = []
    for item in mediaString:
        if item != "": 
            mediaName = item.strip().strip(":").strip("[]")
            mediaLst.append(globals()[parseName(mediaName)])
    
    viewingNotes = att[2]

    tagLine = att[3]

    f.close()

    return Franchise(name, mediaLst, viewingNotes, tagLine)

################################################################################
### Console List Statements
def printMediaList():
    print("Media List")
    print("=========================================")
    for media in mediaList:
        media.printBasicMedia()
    print("\n")

def printFranchiseList():
    print("Franchise List")
    print("=========================================")
    for franchise in franchiseList:
        print(f"{franchise.name} ({franchise.count})")

################################################################################
def fullUpdateMasterFranchise():
    def nameSort(franchise: Franchise):
        return franchise.name    

    newFranchiseList = sorted(franchiseList, key = nameSort)
    fMaster = open("masterFranchise.txt","w")
    text = ""

    for item in newFranchiseList:
        text += f'{item.name}\n'
    
    text = text[:-1]
    fMaster.write(text)
    fMaster.close()

def fullUpdateMasterMedia():
    def nameSort(media: Media):
        return media.name    

    newMediaList = sorted(mediaList, key = nameSort)
    fMaster = open("masterMedia.txt","w")
    text = ""

    for item in newMediaList:
        text += f'{item.name}\n'
    
    text = text[:-1]
    fMaster.write(text)
    fMaster.close()

def updateAllFranchise():
    for franchise in franchiseList:
        franchise.writeText()

################################################################################
if __name__ == "__main__":
    testRun = False
    ### Master File
    readMasterMedia()
    readMasterFranchise()
    
    if testRun:
        printMediaList()
        printFranchiseList()

    ##### Create App
    app = cardApp()
    # app.bind("<Escape>", lambda x: app.destroy())
    # app.after(0, lambda x: app.state('zoomed'))
    app.mainloop()

    ### Update Files
    updateAllFranchise()
    fullUpdateMasterFranchise()
    fullUpdateMasterMedia()