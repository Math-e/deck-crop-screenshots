from PIL import Image
from pathlib import Path

class DeckCrop:

    def defaultScreenshotDir(self):
        userdataDir = Path(Path.home(), '.local/share/Steam/userdata/')
        # avoid the user #0
        steamUsers = list(userdataDir.rglob(r'[^0{1}]'))
        # this function assumes the lower Steam user ID. Another one can be set below
        userIndex = 0
        gamesDir = Path(Path(steamUsers[userIndex]), '760/remote/screenshots')

        return gamesDir

    def imageCrop(self, imgPath: Path):
        if imgPath.is_file() and imgPath.name.endswith(('.jpg', '.png')):
            img = Image.open(imgPath)

            # check if it is in Deck resolution
            if img.size == (1280, 800):
                print("Cropping ", imgPath.name)
                # 1280x720 = (0,40,1280,760)
                croppedImg = img.crop((0,40,1280,760))
                # overwrites original image
                croppedImg.save(imgPath)
            
            else: print("Image is not a native Deck screenshot.")
        else: print("Not a valid image file")

    def cropGameDir(gameId):
        gameDir = Path(self.screenshotsDir, gameId)
        files = target.iterdir()
        for file in files:
            self.imageCrop(file)


    def cropAllGames(self, target: Path = None):
        games = self.screenshotsDir.iterdir()
        for game in games:
            if game.is_dir():
                self.cropGameDir(game.name)
        
    def cropTest(self):
        file = Path(self.defaultScreenshotDir, ('760/remote/1680000/screenshots/20250214223034_1.jpg'))


    def __main__(self, screenshotsDir: Path = None):
        self.screenshotsDir = screenshotsDir or self.defaultScreenshotDir()
               