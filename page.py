from justpy import QuasarPage
import os


class MyPage(QuasarPage):

    """
    QuasarPage modified to incorporate custom actions upon closing window:
    switching off sound and deleting reports.
    """

    def __init__(self, sound, **kwargs):
        super().__init__(**kwargs)
        self.sound = sound
        self.reports = []

    async def on_disconnect(self, websocket=None):
        if self.delete_flag:
            self.sound.stop()
            for filename in self.reports:
                os.remove(os.path.realpath(filename))
            self.delete_components()
            self.remove_page()
