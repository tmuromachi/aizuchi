import time
import datetime
import mic_f0
import backchannel


def main():
    mic = mic_f0.MicF0()
    bc = backchannel.BackChannel(BC_TIMING)

    while True:
        f0 = mic.update()
        print(datetime.datetime.now(), "F0:", f0)
        time.sleep(0.01)
        bc.update(f0)


if __name__ == "__main__":
    BC_TIMING = 30   # 相槌の無音区間待機時間(25->0.25s)
    main()
