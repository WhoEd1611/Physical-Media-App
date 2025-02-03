### This file is designed to hold the classes and the functions used for interacting with files
from os.path import isfile

### Media Code
# Media Class
class Media:
    # Global Access Variables
    AGERATING = {0: "G", 1: "PG", 2: "M", 3: "MA15+", 4: "R18"}
    MEDIATYPE = {0: "Movie", 1: "TV Series", 2: "OVA"}
    MEDIAFORMAT = {0: "DVD", 1: "Blu-Ray", 2: "4K"}
    GENRE = {0: "Anime", 1: "Action", 2: "Adventure", 3: "Animation", 4: "Comedy", 5: "Drama", 6: "Fantasy", 7: "Horror", 8: "Mecha", 9: "Romance", 10: "Science Fiction", 11: "Sport", 12: "Supernatural"}

    def __init__(self, name, ageClassification: int, yearRelease: int, mediaType: int, rating: float, description: str, runtime: int, episodeCount: int = 1, mediaFormat: set = {1}, tagline: str = "", genre: set = {}, source: str = [], viewingNote: str = "", ageNote: str = ""):
        """
        Args:
            name (str): Name of Media
            ageClassification (str): Age classification. Must be one of {0: G, 1: PG, 2: M, 3: MA15+, 4: R18}
            yearRelease (int): Year of release
            mediaType (int): Type of Media. Must be one of {0: Movie, 1: TV, 2: OVA}
            rating (int): Community rating
            description (str): Description of Media
            runtime (int): Runtime of Media in minutes
            episodeCount (int): Amount of episodes. Defaults to 1
            mediaFormat (set, optional): Format of Media. Set contains variables from 0-2, where {0: DVD, 1: Blu-Ray, 2: 4K}. Defaults to {1}.
            tagline (str, optional): Tagline of Media. Defaults to "".
            genre (set, optional): Set of genres. Defaults to []. Can include: {0: Anime, 1: Action, 2: Adventure, 3: Animation, 4: Comedy, 5: Drama, 6: Fantasy, 7: Horror, 8: Mecha, 9: Romance, 10: Science Fiction, 11: Sport, 12: Supernatural}
            source (list, optional): List of things to watch on it. For example, if held across two Blu-ray sets, put titles of both in a List.
        """
        self.name = name
        self.ageClassification = ageClassification
        self.yearRelease = yearRelease
        self.mediaType = mediaType
        self.rating = rating
        self.description = description
        self.runtime = runtime
        self.episodeCount = episodeCount
        self.mediaFormat = mediaFormat
        self.tagline = tagline
        self.genre = genre
        self.source = source
        self.viewingNote = viewingNote
        self.ageNote = ageNote

    def __rep__(self):
        return f"{self.name} ({self.yearRelease})"

    def editName(self, newName: str):
        self.name = newName

    def editAgeClassification(self, newAge: int):
        self.ageClassification = newAge
    
    def editYearRelease(self, newYear: int):
        self.yearRelease = newYear

    def editMediaType(self, newMediaType: int):
        self.mediaType = newMediaType
    
    def editRating(self, newRating: float):
        self.rating = newRating
    
    def editDescription(self, newDescription: str):
        self.description = newDescription
    
    def editRuntime(self, newRuntime: int):
        self.runtime = newRuntime
    
    def editEpisodeCount(self, newEpisodeCount: int):
        self.episodeCount = newEpisodeCount
    
    def editMediaFormat(self, newFormatSet: set):
        self.mediaFormat = newFormatSet
    
    def editTagline(self, newTagline: str):
        self.tagline = newTagline
    
    def editGenres(self, newGenre: set):
        self.genre = newGenre
    
    def editSource(self, newSource: list):
        self.source = newSource
    
    def editViewingNotes(self, newNote: str):
        self.viewingNote = newNote
    
    def editAgeNotes(self, newNote: str):
        self.ageNote = newNote

    def parseName(self):
        """Will return media title without any space or colons

        Returns:
            name (str): Parsed media title
        """
        name = self.name
        name = name.replace(" ", "")
        name = name.strip(":")
        name = name.strip("+")
        return name

    def attributeValues(self):
        """Return dictionary of attributes

        Returns:
            dict: Dictionary of attributes
        """
        return self.__dict__.items()

    def writeText(self):
        """Writes the class to a text file
        """
        # Check if there is existing text file with name
        name = self.parseName()
        path = "filmData/" + name
        
        if isfile(path + ".txt"):
            # If file exists
            # Open File
            f = open(path + ".txt", "w")
            
            # Specified desire format for text here!
            mediaDict = self.attributeValues()
            text = ""

            for key, value in mediaDict:
                if key == "source":
                    sourceText = ""
                    for source in value:
                        sourceText += source
                        sourceText += ","
                    text = text + sourceText + "\n\n"

                else:
                    text = text + str(value) + "\n\n"
            
            # Close File
            f.write(text)
            f.close()
        
        else:
            # If file exists
            # Open File
            f = open(path + ".txt", "w")
            
            # Specified desire format for text here!
            mediaDict = self.attributeValues()
            text = ""

            for key, value in mediaDict:
                if key == "source":
                    sourceText = ""
                    for source in value:
                        sourceText += source
                        sourceText += ","
                    text = text + sourceText + "\n\n"

                else:
                    text = text + str(value) + "\n\n"
            
            # Close File
            f.write(text)
            f.close()

    def printDetailMedia(self):
        attributeDict = self.attributeValues()
        for key, value in attributeDict:
            
            if key != "episodeCount":
                print(f'{key}: ', end = "")
            else:
                if self.__dict__["mediaType"] == 1:
                    print(f'{key}: {value}')
            
            if key not in ["ageClassification", "mediaType", "mediaFormat", "genre", "episodeCount"]:
                print(f'{value}\n')
            else:
                match key:
                    case "ageClassification":
                        print(f'{self.AGERATING[value]}\n')
                    case "mediaType":
                        print(f'{self.MEDIATYPE[value]}\n')
                    case "mediaFormat":
                        text = ""
                        for item in value:
                            text = text + str(self.MEDIAFORMAT[int(item)]) + ", "
                        text += "\n"
                        print(text)
                    case "genre":
                        text = ""
                        for item in value:
                            text = text + str(self.GENRE[int(item)]) + ", "
                        text += "\n"
                        print(text)
                    case "episodeCount":
                        pass
        print(".....................................................................\n")

### Franchise Code
# Franchise Class
class Franchise:
    def __init__(self, name: str, media: list = [], viewingNotes: str = "", tagline: str = ""):
        self.name = name
        self.media = media
        self.count = len(media)
        self.viewingNotes = viewingNotes
        self.tagline = tagline

    def updateMedia(self, newMedia: Media):
        #1. Check if newMedia is already in there
        if newMedia not in self.media:
            #2. Append if not in self.media
            self.media.append(newMedia)
        self.count += 1

    def removeMedia(self, removedMedia: Media):
        try: 
            self.media.remove(removedMedia)
            self.count -= 1
        except ValueError:
            print(f"{removedMedia.name} not in {self.name}")

    def editName(self, newName: str):
        self.name = newName
    
    def editViewingNotes(self, newNotes: str):
        self.viewingNotes = newNotes

    def editTagline(self, newTagline: str):
        self.tagline = newTagline

    def parseName(self):
        """Will return franchise title without any space or colons

        Returns:
            name (str): Parsed franchise title
        """
        name = self.name
        name = name.replace("Collection", "")
        name = name.strip()
        name = name.strip(":")
        return name

    def printListMedia(self):
        print("List of media in franchise:", end = " ")
        for media in self.media:
            mediaName = media.name
            mediaYear = media.yearRelease
            print(f'{mediaName} ({mediaYear})', end = ", ") 
        print("\n................................................................................")

    def printFranchise(self):
        print(f'{self.name} Collection\nCount: {self.count}')
        self.printListMedia()
    
    def writeText(self):
        name = self.parseName()
        path = "franchiseData/" + name

        media = self.media
        media = sorted(media, key = lambda item: item.yearRelease)
        
        if isfile(path + ".txt"):
            # If file exists
            # Open File
            f = open(path + ".txt", "w")

            # Specified desire format for text here!
            text = ""
            text += str(self.name)
            text += "\n\n"

            for item in media:
                text += str(item.name)
                text += ","
            
            text += "\n\n"

            text += self.viewingNotes

            text += "\n\n"
            text += self.tagline

            # Close File
            f.write(text)
            f.close()
        
        else:
            # If file does not exist.
            # Create File
            f = open(path + ".txt", "a")

            # Specified desire format for text here!
            text = ""
            text += str(self.name)
            text += "\n\n"
            
            for item in self.media:
                text += str(item.name)
                text += ","

            text += "\n\n"

            text += self.viewingNotes

            text += "\n\n"
            text += self.tagline

            # Close File
            f.write(text)
            f.close()
    
    def earliestMedia(self):
        # minYear = 1000000
        # for item in self.media:
        #     if item.yearRelease < minYear:
        #         minYear = item.yearRelease
        
        minYear = min(item.yearRelease for item in self.media)

        return minYear
    
    def maxAgeClassification(self):
        # maxAge = 0
        # for item in self.media:
        #     if item.ageClassification > maxAge:
        #         maxAge = item.ageClassification
        
        maxAge = min(item.ageClassification for item in self.media)

        return maxAge
    
    def aveRating(self):
        # maxRating = 0
        # for item in self.media:

        maxRating = sum(item.rating for item in self.media)/len(self.media)

        return maxRating

    def isInFranchise(self, media: Media):
        return media in self.media

if __name__ == "__main__":
    # ## Media Tests
    # # Testing file creation
    # Akira = Media("Akira", 2, 1988, 0, 8.16, "Neo-Tokyo, 2019. The city is being rebuilt post World War III. Kaneda and Tetsuo, two high school drop outs, stumble on a secret, government project to development new weapons - telekinetic humans. Tetsuo learns of the existence of his ‘peer’, Akira, the project’s most powerful subject and determines to challenge them…", 124, 1, {0,1}, "Neo-Tokyo is about to EXPLODE!", {0, 10, 7}, ["Akira"], "", "High Level Violence")
    # Akira.printDetailMedia()
    # Akira.writeText()

    # ### Franchise Tests
    # # Testing file creation
    # AkiraCollection = Franchise("Akira", [Akira], "HelloWorld", "Something Something Dark Side")
    # AkiraCollection.printFranchise()
    # AkiraCollection.writeText()
    # del AkiraCollection
    pass