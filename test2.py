

import os
from subprocess import Popen, PIPE

if os.name == 'nt':
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
    from comtypes import CLSCTX_ALL
    from ctypes import POINTER, cast

    def volume():
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        if volume.GetMute() == 1:
            volume.SetMute(0, None)
        volume.SetMasterVolumeLevel(volume.GetVolumeRange()[1], None)

    def volumedown():
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMasterVolumeLevel(volume.GetVolumeRange()[0], None)
else:
    def volume(value):
        try:
            card = Popen(["amixer", "-D", "pulse", "sset",
                         "Master", str(value) + "%"], stdout=PIPE)
            print(card)
            out = card .communicate()
            print(out)
        except:
            # Alternative, this as the second
            #   because this gave me an installation error with Pop OS 21.10
            try:
                import alsaaudio as audio
            except:
                os.system("python3 -m pip install pyalsaaudio")
            mixer = audio.Mixer('Headphone', cardindex=1)
            mixer.setvolume(int(value))

volume(50)
