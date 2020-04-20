from aip import AipSpeech
import socket
import sys
import wave
import re
import pyaudio
import os
import ffmpeg

""" 你的 APPID AK SK """
APP_ID = '19440847'
API_KEY = 'vZVpPOyd1qELSvTKFqzmgBoa'
SECRET_KEY = 'oGLRZUXdPgUcbK84CXDdeL4Uu9VDl1h3'
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

#录音
def record():
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 2
        RATE = 16000
        RECORD_SECONDS = 2  #录音文件时长
        WAVE_OUTPUT_FILENAME = "Oldboy.wav"

        p = pyaudio.PyAudio()

        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        print("开始录音,请说话......")

        frames = []

        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                data = stream.read(CHUNK)
                frames.append(data)

        print("录音结束!")

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

#wav格式转pcm格式
def wav_to_pcm(wav_file):
    pcm_file = "%s.pcm" %(wav_file.split(".")[0])
    os.system("C:/ffmpeg/ffmpeg-20200415-51db0a4-win64-static/bin/ffmpeg -y  -i %s  -acodec pcm_s16le -f s16le -ac 1 -ar 16000 %s"%(wav_file,pcm_file))

    return pcm_file

#语音识别
def cognitive():
        pcm_file =wav_to_pcm("Oldboy.wav")

        def get_file_content(filePath):
                with open(filePath, 'rb') as fp:
                        return fp.read()

# 识别本地文件
        result = client.asr(get_file_content(pcm_file), 'wav', 16000, {
                'dev_pid': 1537,
                'rate':16000,
                'format':'pcm',
                'cuid': '80-FA-5B-3D-C6-33',
                })
        print('result>>>>>',result)
        if result['err_no'] == 0:
                return result['result'][0]
        return ''

def action(Str):
        command = ''

        if re.search('前',Str) !=None or re.search('钱',Str) !=None or re.search('直',Str) !=None:
                command = 'chassis speed x 0.3 y 0 z 0'
        if re.search('后',Str) !=None or re.search('退',Str) !=None or re.search('倒',Str) !=None:
                command = 'chassis speed x -0.3 y 0 z 0'
        if re.search('左',Str) !=None or re.search('做',Str) !=None:
                command = 'chassis speed x 0 y -0.3 z 0'
        if re.search('右',Str) !=None or re.search('又',Str) !=None or re.search('由',Str) !=None:
                command = 'chassis speed x 0 y 0.3 z 0'
        if re.search('停',Str) !=None or re.search('听',Str)  !=None or re.search('站',Str) !=None or re.search('不',Str) !=None:
                command = 'chassis speed x 0 y 0 z 0'
        if re.search('旋转',Str) !=None or re.search('打转',Str) !=None or re.search('形状',Str) !=None:
                command = 'chassis speed x 0 y 0 z 60'
        if re.search('抬高',Str) !=None or re.search('抬头',Str) !=None:
                command = 'gimbal move p 20'
        if re.search('低头',Str) !=None or re.search('下看',Str) !=None:
                command = 'gimbal move p -20'
        if re.search('云台左转',Str) !=None  or re.search('平台左转',Str) !=None:
                command = 'gimbal move y -40'
        if re.search('云台右转',Str) !=None or re.search('云台又转',Str) !=None or re.search('云台由转',Str) !=None or re.search('平台右转',Str) !=None:
                command = 'gimbal move y 40'
        if re.search('回中',Str) !=None :
                command = 'gimbal recenter'
        if re.search('射击',Str) !=None or re.search('设计',Str) !=None or re.search('涉及',Str) !=None:
                command = 'blaster fire'
        if re.search('自由',Str) !=None : #将运行模式改为自由模式
                command = 'robot mode free'
        if re.search('声音',Str) !=None :
                command = 'sound event applause on'
        if re.search('关闭',Str) !=None :
                command = 'quit'
        if command !='':
                print("command inner>>>>",command)
                s.send(command.encode('utf-8'))
                try:
                        buf = s.recv(1024)
                        print(buf.decode('utf-8'))
                       
                except socket.error as e:
                        print("Error receiving:",e)
        if command =="quit":
                sys.exit(0)


def connect():
# 机器人 IP 地址根据实际 IP 进行修改
        host = "192.168.43.125"
        port = 40923
        address = (host,int(port))
        address = (host,int(port))

        # 与机器人控制命令端口建立 TCP 连接
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        print("Connecting...")

        s.connect(address)

        print("Connected!")
        return s

s = connect()
s.send("command".encode('utf-8'))
# buf = s.recv(1024)

# print(buf.decode('utf-8'))
while(True):
        record()
        result = cognitive()
        action(result)


s.shutdown(socket.SHUT_WR)