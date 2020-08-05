from converter import Converter
conv = Converter()

info = conv.probe('/home/dashere/SQLconvert-2020-06-11_16.18.20')

convert = conv.convert('/home/dashere/SQLconvert-2020-06-11_16.18.20', '/home/dashere/SQLconvert.mp4', {
    'format': 'mp4',
    'audio': {
        'codec': 'aac',
        'samplerate': 11025,
        'channels': 2
    },
    'video': {
        'codec': 'hevc',
        'width': 720,
        'height': 400,
        'fps': 25
    }})

for timecode in convert:
    print(f'\rConverting ({timecode:.2f}) ...')