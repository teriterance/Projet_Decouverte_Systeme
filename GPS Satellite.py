import numpy as np
import matplotlib.pyplot as plt

f = open("tramesGPSREF", "r+")
k = f.readlines()
k2=[]
for i in k:
    i2 = i.split(',')
    if i2[0]=='$GPGSV':
        k2.append(i2)


GPSe=[]
GPSa=[]
GPSa_rad = []

ax = plt.subplot(111, polar=True)
ax.set_theta_zero_location('N')
ax.set_theta_direction(-1)
ax.set_rmax(90)
ax.grid(True)

for k in range(100):
    GPSei = []
    GPSai = []
    GPSai_rad = []
    for i in k2:
        if len(i)>17:
            if int(i[4]) == k:
                GPSei.append(i[5])
                GPSai.append(i[6])
                if len(GPSei)>2:
                    if GPSei[-1]==GPSei[-2] and GPSai[-1]==GPSai[-2]:
                        GPSei.pop(-1),GPSai.pop(-1)
            if int(i[8]) == k:
                GPSei.append(i[9])
                GPSai.append(i[10])
                if len(GPSei)>2:
                    if GPSei[-1]==GPSei[-2] and GPSai[-1]==GPSai[-2]:
                        GPSei.pop(-1),GPSai.pop(-1)
            if int(i[12]) == k:
                GPSei.append(i[13])
                GPSai.append(i[14])
                if len(GPSei)>2:
                    if GPSei[-1]==GPSei[-2] and GPSai[-1]==GPSai[-2]:
                        GPSei.pop(-1),GPSai.pop(-1)
            if int(i[16]) == k:
                GPSei.append(i[17])
                GPSai.append(i[18])
                if len(GPSei)>2:
                    if GPSei[-1]==GPSei[-2] and GPSai[-1]==GPSai[-2]:
                        GPSei.pop(-1),GPSai.pop(-1)
        elif len(i)>13:
            if int(i[4]) == k:
                GPSei.append(i[5])
                GPSai.append(i[6])
                if len(GPSei)>2:
                    if GPSei[-1]==GPSei[-2] and GPSai[-1]==GPSai[-2]:
                        GPSei.pop(-1),GPSai.pop(-1)
            if int(i[8]) == k:
                GPSei.append(i[9])
                GPSai.append(i[10])
                if len(GPSei)>2:
                    if GPSei[-1]==GPSei[-2] and GPSai[-1]==GPSai[-2]:
                        GPSei.pop(-1),GPSai.pop(-1)
            if int(i[12]) == k:
                GPSei.append(i[13])
                GPSai.append(i[14])
                if len(GPSei)>2:
                    if GPSei[-1]==GPSei[-2] and GPSai[-1]==GPSai[-2]:
                        GPSei.pop(-1),GPSai.pop(-1)
        elif len(i) > 9:
            if int(i[4]) == k:
                GPSei.append(i[5])
                GPSai.append(i[6])
                if len(GPSei)>2:
                    if GPSei[-1]==GPSei[-2] and GPSai[-1]==GPSai[-2]:
                        GPSei.pop(-1),GPSai.pop(-1)
            if int(i[8]) == k:
                GPSei.append(i[9])
                GPSai.append(i[10])
                if len(GPSei)>2:
                    if GPSei[-1]==GPSei[-2] and GPSai[-1]==GPSai[-2]:
                        GPSei.pop(-1),GPSai.pop(-1)
        else:
            if int(i[4]) == k:
                GPSei.append(i[5])
                GPSai.append(i[6])
                if len(GPSei)>2:
                    if GPSei[-1]==GPSei[-2] and GPSai[-1]==GPSai[-2]:
                        GPSei.pop(-1),GPSai.pop(-1)
    for i in GPSai:
        GPSai_rad.append(float(i) * np.pi / 180.0)
    if len(GPSei)>0:
        print(k,GPSei, GPSai)
        ax.scatter(GPSai_rad, GPSei, s=10, label=str(k))

plt.savefig("test3.png")
plt.show()
