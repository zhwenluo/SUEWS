__author__ = 'Fredrik Lindberg'

# This class will be used to plot output result from Suews

import numpy as np
import matplotlib.pylab as plt
import matplotlib.dates as dt
import datetime

def leap_year(yy):
    if (yy % 4) == 0:
        if (yy % 100) == 0:
            if (yy % 400) == 0:
                leapyear = 1
            else:
                leapyear = 0
        else:
            leapyear = 1
    else:
        leapyear = 0

    return leapyear


def make_dectime(dataout):
    datenum_yy = np.zeros(dataout.shape[0])
    for i in range(0, dataout.shape[0]): # making date number
        datenum_yy[i] = dt.date2num(dt.datetime.datetime(int(dataout[i, 0]), 1, 1))

    dectime = datenum_yy + dataout[:, 4]

    return dectime

class SuewsPlotting:
    def __init__(self):
        pass

    def plotbasic(self, dataout, datain):

        dectime = make_dectime(dataout)
        dates = dt.num2date(dectime)

        plt.figure(1, figsize=(15, 7), facecolor='white')
        ax1 = plt.subplot(3, 1, 1)
        ax1.plot(dates, dataout[:, 5], 'r', label='$K_{down}$')
        ax1.plot(dates, dataout[:, 6], 'g', label='$K_{up}$')
        ax1.plot(dates, dataout[:, 7], 'b', label='$L_{down}$')
        ax1.plot(dates, dataout[:, 8], 'c', label='$L_{up}$')
        ax1.plot(dates, dataout[:, 10], 'k', label='$Q*$')
        ax1.set_ylim([-100, 1000])
        ax1.set_ylabel('$W$'' ''$m ^{-2}$', fontsize=14)
        pos1 = ax1.get_position()
        pos2 = [pos1.x0 - 0.07, pos1.y0 + 0.05, pos1.width * 1.05, pos1.height * 1.1]
        ax1.set_position(pos2)
        plt.legend(bbox_to_anchor=(1.13, 1.08))

        ax2 = plt.subplot(3, 1, 2, sharex=ax1)
        ax2.plot(dates, dataout[:, 13],'k', label='$Q_S$')
        ax2.set_ylabel('$W$'' ''$m ^{-2}$', fontsize=14)
        ax2.plot(dates, dataout[:, 14],'c', label='$Q_F$')
        ax2.plot(dates, dataout[:, 15],'r', label='$Q_H$')
        ax2.plot(dates, dataout[:, 16],'b', label='$Q_E$')
        ax2.set_ylim([-100, 400])
        pos1 = ax2.get_position()
        pos2 = [pos1.x0 - 0.07, pos1.y0 + 0.01, pos1.width * 1.05, pos1.height * 1.1]
        ax2.set_position(pos2)
        plt.legend(bbox_to_anchor=(1.13, 1.0))

        ax3 = plt.subplot(3, 1, 3, sharex=ax1)
        ax4 = ax3.twinx()
        ax3.plot(dates, dataout[:, 57], 'g-', label='$LAI$')
        ax4.bar(dectime, datain[:, 13], width=0.0, edgecolor='b' , label='$Precip$')
        ax4.plot(dectime, dataout[:, 43], 'k', label='$SMD$')
        ax3.set_xlabel('Time', fontsize=14)
        ax3.set_ylabel('$LAI$'' ''$f_{vegetation}$', color='g', fontsize=14)
        ax4.set_ylabel('$mm$', color='b', fontsize=14)
        ax3.set_xlim([min(dectime), max(dectime)])
        pos1 = ax3.get_position()
        pos2 = [pos1.x0 - 0.07, pos1.y0 - 0.02, pos1.width * 1.05, pos1.height * 1.1]
        ax3.set_position(pos2)
        ax4.set_position(pos2)
        plt.legend(bbox_to_anchor=(1.16, 1.0))


    def plotmonthlystatistics(self, dataout, datain):

        dectime = make_dectime(dataout)
        dates = dt.num2date(dectime)
        month = np.zeros(datain.shape[0])
        day = np.zeros((datain.shape[0]))
        hour = np.zeros((datain.shape[0]))
        for i in range(0, datain.shape[0]):
            month[i] = dates[i].month
            day[i] = dates[i].day
            hour[i] = dates[i].hour

        pltmonth = np.zeros(int(month.max() - month.min() + 1))
        Qh = np.zeros(int(month.max() - month.min() + 1))
        Qe = np.zeros(int(month.max() - month.min() + 1))
        Qs = np.zeros(int(month.max() - month.min() + 1))
        Qf = np.zeros(int(month.max() - month.min() + 1))
        Qstar = np.zeros(int(month.max() - month.min() + 1))
        precip = np.zeros(int(month.max() - month.min() + 1))
        wu = np.zeros(int(month.max() - month.min() + 1))
        st = np.zeros(int(month.max() - month.min() + 1))
        evap = np.zeros(int(month.max() - month.min() + 1))
        drain = np.zeros(int(month.max() - month.min() + 1))

        for i in range(int(month.min()), int(month.max() + 1)):
            pltmonth[i - 1] = i
            Qh[i - 1] = np.mean(dataout[month == i, 15])
            Qe[i - 1] = np.mean(dataout[month == i, 16])
            Qs[i - 1] = np.mean(dataout[month == i, 13])
            Qf[i - 1] = np.mean(dataout[month == i, 14])
            Qstar[i - 1] = np.mean(dataout[month == i, 10])

            precip[i - 1] = np.sum(dataout[month == i, 17])
            wu[i - 1] = np.sum(dataout[month == i, 18])  #Ie  # exteranl wu
            st[i - 1] = np.sum(dataout[month == i, 23])  # storage
            evap[i - 1] = np.sum(dataout[month == i, 19])
            drain[i - 1] = np.sum(dataout[month == i, 25]) # runoff

        plt.figure(2, figsize=(15, 7), facecolor='white')
        ax1 = plt.subplot(1, 2, 1)
        ax1.plot(pltmonth, Qstar, 'ro-', label='$Q*$')
        ax1.plot(pltmonth, -Qh, 'ro-', label='$Q_H$')
        ax1.plot(pltmonth, -Qe, 'bo-', label='$Q_E$')
        ax1.plot(pltmonth, -Qs, 'ko-', label='$\Delta Q_S$')
        ax1.plot(pltmonth, Qf, 'co-', label='$Q_F$')
        ax1.plot(pltmonth, Qf * 0, 'k')
        ax1.set_xlim([1, 12])
        ax1.set_xlabel('$Month$', fontsize=14)
        ax1.set_ylabel('$W$'' ''$m ^{-2}$', fontsize=14)
        plt.title('Monthly  partition of the surface energy balance')
        pos1 = ax1.get_position()
        pos2 = [pos1.x0 - 0.06, pos1.y0 + 0.00, pos1.width * 1.00, pos1.height * 1.0]
        ax1.set_position(pos2)
        plt.legend(bbox_to_anchor=(1.25, 1.0))

        ax3 = plt.subplot(1, 2, 2, sharex=ax1)
        ax3.plot(pltmonth, wu, 'go-', label='$W-use$')
        ax3.plot(pltmonth, -st, 'ro-', label='$Storage$')
        ax3.plot(pltmonth, -evap, 'bo-', label='$E$')
        ax3.plot(pltmonth, -drain, 'ko-', label='$Runoff$')
        ax3.bar(pltmonth, precip, width=0.5, edgecolor='b', align='center', label='$Precip$')
        ax3.set_xlabel('$Month$', fontsize=14)
        ax3.set_ylabel('$mm$', fontsize=14)
        ax3.set_xlim([1, 12])
        ax3.set_xticks(pltmonth)
        plt.title('Monthly water balance')
        pos1 = ax3.get_position()
        pos2 = [pos1.x0 - 0.01, pos1.y0 - 0.00, pos1.width * 1.00, pos1.height * 1.0]
        ax3.set_position(pos2)
        ax3.set_position(pos2)
        plt.legend(bbox_to_anchor=(1.3, 1.0))




