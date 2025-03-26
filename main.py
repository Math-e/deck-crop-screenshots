import os
# The decky plugin module is located at decky-loader/plugin
# For easy intellisense checkout the decky-loader code repo
# and add the `decky-loader/plugin/imports` path to `python.analysis.extraPaths` in `.vscode/settings.json`
import decky
import asyncio
#from PIL import Image
from pathlib import Path

class Plugin:

    _id_map = {}
    _id_map_frontend = {}
    _trunc_id_map = {}
    _screenshots_dir = None
    _rescuer_task = None
    _current_app_name = "Unknown"
    _rescued = False

    # for grabbing just-captured screenshots
    async def screenshot_rescuer(self):
        png_path = "/tmp/gamescope.raw_encoded.png"
        raw_path = "/tmp/gamescope.raw"
        decky_plugin.logger.info("Rescuer started")
        while True:
            try:
                if os.path.exists(png_path):
                    dt = time.time() - os.path.getmtime(png_path)
                    if dt > 2:
                        path = (
                            Plugin._dump_folder
                            / Plugin._current_app_name.replace(":", " ")
                            / (str(int(time.time())) + ".png")
                        )
                        #path.parent.mkdir(parents=True, exist_ok=True)
                        #shutil.copy(png_path, path)
                        #shutil.copy(png_path, self._dump_folder / "most_recent.jpg")
                        os.unlink(png_path)
                        os.unlink(raw_path)
                        decky_plugin.logger.info(
                            f"Rescued screenshot for {Plugin._current_app_name}"
                        )
                        Plugin._rescued = True
            except Exception:
                decky_plugin.logger.exception("watchdog")
            await asyncio.sleep(0.5)


    def get_app_name(self, app_id):
        if app_id in self._id_map_frontend:
            return self._id_map_frontend[app_id]
        if app_id in self._id_map:
            return self._id_map[app_id]
        # At this point we probably have a non-steam app, where the ID in the screenshot is sent back wrong
        if app_id in self._trunc_id_map:
            return self._trunc_id_map[app_id]
        for _id, name in self._id_map_frontend.items():
            if bin(_id).endswith(bin(app_id)[2:]):
                self._trunc_id_map[app_id] = name
                decky_plugin.logger.info(f"Found name of {app_id} to be {name}")
                return name
    
    async def set_id_map_frontend(self, allapps):
        self._id_map_frontend = {a[0]: a[1] for a in allapps}
        decky_plugin.logger.info("Set frontend id map")

    def defaultScreenshotDir(self):
        userdataDir = Path.home() / '.local/share/Steam/userdata/'
        # avoid the user #0
        steamUsers = list(userdataDir.rglob(r'[^0{1}]'))
        # this function assumes the lower Steam user ID. Another one can be set below
        userIndex = 0
        gamesDir = Path(Path(steamUsers[userIndex]), '760/remote/screenshots/')

        return gamesDir

    def imageCrop(self, imgPath: Path):
        if imgPath.is_file() and imgPath.name.endswith(('.jpg', '.png')):
            img = Image.open(imgPath)

            # check if it is in Deck resolution
            if img.size == (1280, 800):
                decky.logger.info("Cropping %s"%imgPath.name)
                # 1280x720 = (0,40,1280,760)
                croppedImg = img.crop((0,40,1280,760))
                # overwrites original image
                croppedImg.save(imgPath)
            
            else: decky.logger.info("%s is not a native Deck screenshot."%imgPath.absolute)
        else: decky.logger.info("%s is not a valid image file"%imgPath.absolute)

    async def cropGameDir(self, gameId):
        gameDir = Path(self.screenshotsDir, gameId)
        files = target.iterdir()
        for file in files:
            self.imageCrop(file)
        
    def cropTest(self) -> bool:
        file = Path(self.defaultScreenshotDir, ('760/remote/1680000/screenshots/20250214223034_1.jpg'))
        #self.imageCrop(file)
        decky.logger.info('Cropped ', file)
        return True
               
    # A normal method. It can be called from the TypeScript side using @decky/api.
    async def add(self, left: int, right: int) -> int:
        decky.logger.info("Adding %s and %s"%(left, right))
        return left + right

    async def long_running(self):
        await asyncio.sleep(15)
        # Passing through a bunch of random data, just as an example
        await decky.emit("timer_event", "Hello from the backend!", True, 2)

    # Asyncio-compatible long-running code, executed in a task when the plugin is loaded
    async def _main(self):
        self.loop = asyncio.get_event_loop()
        decky.logger.info("Hello World from _main!")

    # Function called first during the unload process, utilize this to handle your plugin being stopped, but not
    # completely removed
    async def _unload(self):
        decky.logger.info("Goodnight World!")
        pass

    # Function called after `_unload` during uninstall, utilize this to clean up processes and other remnants of your
    # plugin that may remain on the system
    async def _uninstall(self):
        decky.logger.info("Goodbye World!")
        pass

    async def start_timer(self):
        self.loop.create_task(self.long_running())

    # Migrations that should be performed before entering `_main()`.
    async def _migration(self):
        decky.logger.info("Migrating")
        # Here's a migration example for logs:
        # - `~/.config/decky-template/template.log` will be migrated to `decky.decky_LOG_DIR/template.log`
        decky.migrate_logs(os.path.join(decky.DECKY_USER_HOME,
                                               ".config", "decky-template", "template.log"))
        # Here's a migration example for settings:
        # - `~/homebrew/settings/template.json` is migrated to `decky.decky_SETTINGS_DIR/template.json`
        # - `~/.config/decky-template/` all files and directories under this root are migrated to `decky.decky_SETTINGS_DIR/`
        decky.migrate_settings(
            os.path.join(decky.DECKY_HOME, "settings", "template.json"),
            os.path.join(decky.DECKY_USER_HOME, ".config", "decky-template"))
        # Here's a migration example for runtime data:
        # - `~/homebrew/template/` all files and directories under this root are migrated to `decky.decky_RUNTIME_DIR/`
        # - `~/.local/share/decky-template/` all files and directories under this root are migrated to `decky.decky_RUNTIME_DIR/`
        decky.migrate_runtime(
            os.path.join(decky.DECKY_HOME, "template"),
            os.path.join(decky.DECKY_USER_HOME, ".local", "share", "decky-template"))
