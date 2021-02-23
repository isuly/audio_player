import pyaudio
import wave

import sys, select


class Player:
    def __init__(self):
        self.stream = None

    def play_file(self, fname):
        # create an audio object
        wf = wave.open(fname, 'rb')
        p = pyaudio.PyAudio()
        chunk = 1024

        # open stream based on the wave object which has been input.
        self.stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                             channels=wf.getnchannels(),
                             rate=wf.getframerate(),
                             output=True)

        # read data (based on the chunk size)
        data = wf.readframes(chunk)

        # play stream (looping from beginning of file to the end)
        while len(data) > 0:
            i, o, e = select.select([sys.stdin], [], [], 0)
            if i:
                if sys.stdin.readline().strip() == "stop":
                    break
            # writing to the stream is what *actually* plays the sound.
            self.stream.write(data)
            data = wf.readframes(chunk)

            # cleanup stuff.
        self.stream.close()
        p.terminate()


player = Player()
player.play_file('/home/isuly/Рабочий стол/aa.wav')
