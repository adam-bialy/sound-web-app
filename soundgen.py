from pysinewave import SineWave


class SoundGen(SineWave):

    def __init__(self, freq, vol):
        super().__init__(pitch=9, pitch_per_second=10000, decibels=-30, decibels_per_second=10000)
        self.set_frequency(freq)
        self.set_volume(vol)
        self.volume = self.sinewave_generator.amplitude
        self.freq = self.sinewave_generator.frequency

    def set_frequency(self, freq):
        self.freq = freq
        self.sinewave_generator.set_frequency(self.freq)

    def set_volume(self, volume):
        self.volume = volume
        self.sinewave_generator.set_amplitude(self.volume)


if __name__ == "__main__":
    sine = SoundGen(440)
    sine.play()
    while True:
        user_input = input("Enter a new frequency (integer) or \"q\" to exit: ")
        if user_input.lower() == "q":
            sine.stop()
            break
        else:
            try:
                sine.set_frequency(float(user_input))
            except ValueError:
                continue
