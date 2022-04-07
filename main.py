import justpy as jp
from soundgen import SoundGen
import dbcommands as dbc
import numpy as np
from page import MyPage
from certificate import Certificate


class MainPage:
    """
    Simple interface for generating sound, adjusting its frequency with a slider
    and selecting hearing range of the user. With the obtained data,
    the program calculates statistics (compares current user's frequency range to
    existing database) and creates a pdf "certificate" of hearing range.
    """

    path = "/"

    @classmethod
    def serve(cls, req):

        # sine wave generator
        sound = SoundGen(440, 0.15)

        freq_dict = cls.gen_freq_dict()

        wp = MyPage(sound=sound, title="Good Time Institute", favicon="icon.jpg", tailwind=True)

        body = jp.Div(a=wp, style="background-color: #C1FFD7; width: 100%;")

        main_div = jp.Div(a=body, classes="py-10 m-auto text-center lg:w-1/2 md:w-3/4 sm:w-3/4 lg:text-base md:text-lg sm:text-lg")

        jp.Div(a=main_div, text="Hearing frequency range test",
               style="font-family: Helvetica; font-size: 2em; font-weight: bold; padding: 0 0 20px;")
        jp.Div(a=main_div, text="Instructions:",
               style="font-family: Helvetica; font-size: 1em; font-weight: bold; padding-bottom: 4px;")
        jp.Div(a=main_div, text="Use headphones for best results. "
                                "Press \"Start\" to activate sound "
                                "and use the slider to adjust frequency.\n"
                                "When you reach one of the boundaries, press the corresponding button "
                                "to mark the frequency.\n"
                                "Once you have both boundaries, click \"Submit\" to see "
                                "your statistics (compared to previous users) and obtain a certificate.",
               style="font-family: Helvetica; font-size: 1em; padding-bottom: 10px")

        sound_div = jp.Div(a=main_div,
                           style="padding-top: 10px; padding-bottom: 10px; padding-right: 10px; padding-left: 10px; ")

        button = jp.QButton(a=sound_div, text="Start", style="background-color: #FCFFA6;",
                            click=cls.play_sound)

        jp.Div(a=sound_div, text="Volume",
               style="margin-top: 20px; margin-bottom: 25px; font-weight: bold;")

        vol_slider = jp.QSlider(a=sound_div,
                                style="color: #BAA8EF; margin-top: 12px;",
                                label=True, label_always=True,
                                min=1, max=9, step=1, value=4)
        vol_slider.on("change", cls.set_vol)

        jp.Div(a=sound_div, text="Frequency",
               style="margin-top: 20px; margin-bottom: 25px; font-weight: bold;")

        freq_slider = jp.QSlider(a=sound_div,
                                 label=True, label_always=True,
                                 style="color: #BAA8EF; margin-top: 12px;",
                                 min=1, max=len(freq_dict.keys()), step=1, value=85, freq_dict=freq_dict)
        freq_slider.label_value = f"{freq_dict[freq_slider.value]} Hz"
        freq_slider.on("change", cls.set_freq)

        input_div = jp.Div(a=main_div, style="margin-top: 5px; margin-bottom: 5px; "
                                             "display: grid; grid-template-columns: auto auto; ")

        output_div = jp.Div(a=main_div, style="margin-top: 5px; margin-bottom: 0px; "
                                              "display: grid; grid-template-columns: auto auto; "
                                              "height: 50px;")

        low_out = jp.Div(a=output_div, text="",
                         style="margin-right: 30px; margin-left: 10px; margin-top: 5px; text-align: left; "
                               "font-size: 1.5em; font-family: Helvetica; ")

        high_out = jp.Div(a=output_div, text="",
                          style="margin-left: 30px; margin-right: 10px; margin-top: 5px; text-align: right; "
                                "font-size: 1.5em; font-family: Helvetica; ")

        low_button = jp.QButton(a=input_div, text="Mark lower bound",
                                style="background-color: #FCFFA6; margin-right: 100px;",
                                out=low_out,
                                click=cls.get_freq)

        high_button = jp.QButton(a=input_div, text="Mark upper bound",
                                 style="background-color: #FCFFA6; margin-left: 100px;",
                                 out=high_out,
                                 click=cls.get_freq)

        submit_div = jp.Div(a=main_div)

        results_div = jp.Div(a=main_div,
                             style="margin-top: 10px; margin-bottom: 10px; height: 120px; padding: 5px;")

        line1 = jp.Div(a=results_div, text="")
        line2 = jp.Div(a=results_div, text="")
        line3 = jp.Div(a=results_div, text="Your statistics will appear here.",
                       style="margin-top: 10px; margin-bottom: 10px;")
        line4 = jp.Div(a=results_div, text="")
        line5 = jp.Div(a=results_div, text="")

        submit_button = jp.QButton(a=submit_div, text="Submit", low=low_out, high=high_out,
                                   style="background-color: #FCFFA6; width: 30%;",
                                   click=cls.submit, results=[line1, line2, line3, line4, line5],
                                   report=None)

        report_div = jp.Div(a=main_div,
                            style="display: grid; grid-template-columns: auto auto; "
                                  "width: 80%; "
                                  "margin-left: auto; margin-right: auto;")

        report_name = jp.QInput(a=report_div, placeholder="Your name",
                                style="background-color: white; font-family: Helvetica; font-size: 1.5em; "
                                      "padding-left: 10px; padding-right: 10px; ")

        report_button = jp.QButton(a=report_div, text="Generate certificate",
                                   style="background-color: #FCFFA6; ",
                                   disable=False, click=cls.get_certificate,
                                   low=low_out, high=high_out, report_name=report_name)

        submit_button.report = report_button

        return wp

    @staticmethod
    def play_sound(widget, msg):
        """
        Toggle sound on or off
        """
        if widget.text == "Start":
            widget.text = "Stop"
            widget.a.a.a.a.sound.play()
        else:
            widget.text = "Start"
            widget.a.a.a.a.sound.stop()

    @staticmethod
    def set_freq(widget, msg):
        """
        Adjust frequency based on slider setting
        """
        f = int(widget.freq_dict[widget.value])
        widget.a.a.a.a.sound.set_frequency(f)
        widget.label_value = f"{f} Hz"

    @staticmethod
    def set_vol(widget, msg):
        """
        Adjust volume based on slider setting
        """
        v = float(widget.value) * 0.03
        widget.a.a.a.a.sound.set_volume(v)

    @staticmethod
    def get_freq(widget, msg):
        """
        Extract current frequency and post it to label under buttons
        """
        f = int(round(widget.a.a.a.a.sound.freq))
        widget.out.text = f"{f} Hz"

    @staticmethod
    def submit(widget, msg):
        """
        Submit results for current user to the database and compares them against the data
        """
        if widget.low.text and widget.high.text:
            low = int(widget.low.text.split()[0])
            high = int(widget.high.text.split()[0])
            hrange = high - low
            dbc.insert_record(low, high, hrange)
            records = dbc.select_specific_columns("low", "high", "range")
            records = np.array(records)
            s1 = f"Your lower bound is ranked {(low > records[:,0]).sum() + 1}th lowest."
            s2 = f"Your upper bound is ranked {(high < records[:,1]).sum() + 1}th highest."
            s3 = f"Your hearing range is ranked {(hrange < records[:, 2]).sum() + 1}th broadest."
            s4 = f"Results from {records.shape[0]} submissions in the database."
            s5 = "Form is disabled. Reload the page to make a new test and submission."
            s = [s1, s2, s3, s4, s5]
            for i, j in zip(s, widget.results):
                j.text = i
                j.style = "font-family: Helvetica; "
            widget.disable = True
            widget.report.disable = False

    @staticmethod
    def get_certificate(widget, msg):
        """
        Generate report based on user results
        """
        report = Certificate(widget.report_name.value,
                             widget.low.text,
                             widget.high.text)
        widget.report_name.value = ""
        report.generate()
        widget.a.a.a.a.reports.append(report.filename)

    @staticmethod
    def gen_freq_dict():
        """
        Generate dictionary with values for frequency slider and their corresponding actual frequency values
        :return dict:
        """
        y = list(range(10, 50, 1)) + list(range(50, 100, 5)) \
            + list(range(100, 1000, 10)) + list(range(1000, 5000, 100)) \
            + list(range(5000, 10000, 250)) + list(range(10000, 20500, 500))
        d = {i + 1: j for i, j in enumerate(y)}
        return d


if __name__ == "__main__":
    jp.Route(MainPage.path, MainPage.serve)
    jp.justpy()
