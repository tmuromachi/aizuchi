import simpleaudio


class BackChannel:
    def __init__(self, bc_timing):
        self.wav_obj = simpleaudio.WaveObject.from_wave_file("../data/dog.wav")

        self.silent_flag = 0  # 0:無音, 1:音声検知時, 2:音声検知&無音開始時
        self.silent_count = 0
        self.bc_timing = bc_timing

    def update(self, f0):
        """
        F0を受け取り、相槌可能か判定
        :param f0:
        :return:
        """
        if (self.silent_flag == 0) & (f0 > 0):
            self.silent_flag = 1
            self.silent_count = 0
        elif ((self.silent_flag == 1) & (f0 == 0)) or self.silent_flag == 2:
            self.silent_flag = 2
            self.silent_count += 1

        if self.silent_count >= self.bc_timing:
            self.silent_flag = 0
            self.silent_count = 0
            self.play_aizuchi()
            print("相槌！")

    def play_aizuchi(self):
        # 相槌
        play_obj = self.wav_obj.play()
        play_obj.wait_done()
