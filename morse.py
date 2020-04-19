import numpy as np
import simpleaudio as sa
import random
import time

class morse:
    def __init__(self):
        self.morse_code = { 'A':'.-', 'B':'-...', 'C':'-.-.', 'D':'-..', 'E':'.',
                    'F':'..-.', 'G':'--.', 'H':'....', 'I':'..', 'J':'.---',
                    'K':'-.-', 'L':'.-..', 'M':'--', 'N':'-.','O':'---',
                    'P':'.--.', 'Q':'--.-', 'R':'.-.', 'S':'...', 'T':'-',
                    'U':'..-', 'V':'...-', 'W':'.--', 'X':'-..-', 'Y':'-.--',
                    'Z':'--..', '.':'.-.-.-', ',':'--..--', ' ':'|'
                    }
        self.words_list = self.garb_practice_words_frm_file()
        self._call_play_by_export = False

        
    def garb_practice_words_frm_file(self):
        words_list = []
        with open('1000_words.txt', 'r') as words_file:
            for line in words_file:
                words_list.append(line.strip())
        return words_list


    def get_rand_word(self):
        word = self.words_list[random.randint(0, len(self.words_list))]
        return word


    def __construct_sound__(self, seconds, freq):
        t_bit = np.linspace(0, seconds, int(seconds * self._fs_), False)
        self.t = np.append(self.t, t_bit)
        self.note = np.append(self.note, np.sin(freq * t_bit * 2 * np.pi))


    def play_morse_code(self, _word_, frequency=450, wpm=20, export=False, ):
        self._fs_ = 44100  # 44100 samples per second
        self.t = np.asarray([])
        self.note = np.asarray([])
        duration = 60 / (wpm * 50)

        for char in _word_:
            if char.upper() in self.morse_code.keys():
                # print(morse_code[char.upper()], end=' ')
                for code in self.morse_code[char.upper()]:
                    if code == '.':
                        self.__construct_sound__(duration, frequency)
                        self.__construct_sound__(duration, 0)
                    if code == '-':
                        self.__construct_sound__(duration*3, frequency)
                        self.__construct_sound__(duration, 0)
                    if code == '|':
                        self.__construct_sound__(duration*2, 0)
                self.__construct_sound__(duration*2, 0)

        if self._call_play_by_export == False:
            audio = self.note * (2**15 - 1) / np.max(np.abs(self.note))
            audio = audio.astype(np.int16)
            play_obj = sa.play_buffer(audio, 1, 2, self._fs_)
            play_obj.wait_done()
        else:
            self._call_play_by_export = False
            return self.note

        if export == True:         
            import wavio
            wavio.write("output.wav", self.note, self._fs_, sampwidth=2)

    
    def export_morse_audio(self, _word_, file_name='morse_audio.wav', frequency=450, wpm=20):
        import wavio
        self._call_play_by_export = True
        wave = self.play_morse_code(_word_, frequency, wpm)
        wavio.write(file_name, wave, self._fs_, sampwidth=2)


class quiz(morse):
    def __init__(self):
        super().__init__()
    

    def start(self, N=1):
        for i in range(N):
            self.word = self.get_rand_word()
            self.retry()
            if i != N-1:
                print('Next\n')
            
    def retry(self):
            print('Guess the word')
            time.sleep(0.5)
            self.play_morse_code(self.word, frequency=400, wpm=12)
            in_word = input()
            if in_word == '?':
                print(self.word)
                return
            elif in_word == '-exit-':
                exit()
            else:
                if self.word.upper() == in_word.upper():
                    print('Correct')
                    return
                else:
                    print('Retry')
                    self.retry()


def main():
    # m = morse()
    # word = m.get_rand_word()
    # print(word)
    # m.play_morse_code(word, frequency=400, wpm=15)
    # m.export_morse_audio(word)
    q = quiz()
    q.start(5)


if __name__ == "__main__":
    main()