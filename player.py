import pyaudio
import select
import sys
import wave


class Player:
    def __init__(self):
        self.stream = None

    def play_file(self, fname):
        wf = wave.open(fname, 'rb')
        p = pyaudio.PyAudio()
        chunk = 1024

        self.stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                             channels=wf.getnchannels(),
                             rate=wf.getframerate(),
                             output=True)
        data = wf.readframes(chunk)

        run = True
        while True:
            i, o, e = select.select([sys.stdin], [], [], 0)
            if i:
                command = sys.stdin.readline().strip()
                if command == "run":
                    run = True
                elif command == "pause":
                    run = False
                elif command == "stop":
                    break
            if run and len(data) > 0:
                self.stream.write(data)
                data = wf.readframes(chunk)

        self.stream.close()
        p.terminate()


player = Player()
player.play_file('/home/isuly/Рабочий стол/aa.wav')
