import os
import pandas as pd
import numpy as np
from pandas import Grouper
import re
import matplotlib.pyplot as plt
from matplotlib import interactive
interactive(True)


class ResultAnalyzer:

    def __init__(self, pathes, freq, ip_srcs=[], ip_dsts=[]):
        """
        :param pathes:[str, ]
        :param freq: str, in pandas format, for ex '500ms'
        """

        self.__pathes = pathes
        self.__freq = freq
        self.__freq_int = int(re.search(r'\d+', freq).group())
        self.__ip_srcs = ip_srcs
        self.__ip_dsts = ip_dsts


    def __read_df(self, path):

        df = pd.read_csv(path, sep='\t', header=None, engine='python')

        df.rename(columns={
            1: 'date',
            2: 'ip_src',
            3: 'ip_dst',
            4: 'size'
        }, inplace=True)

        df.dropna(inplace=True)

        df['date'] = pd.to_datetime(df['date'])
        df.index = df['date']

        del df[0]
        del df[5]

        return df

    def __aggregate(self, df):
        df = df.groupby(Grouper(key='date', freq=self.__freq))['size'].sum()
        df = df.fillna(0)
        df = pd.DataFrame(df)

        df['diff'] = np.arange(0, len(df))
        df['diff'] *= self.__freq_int

        return df

    def filter_ip(self, df):
        if len(self.__ip_srcs):
            df = df[df.ip_src.isin(self.__ip_srcs)]
        if len(self.__ip_dsts):
            df = df[df.ip_src.isin(self.__ip_dsts)]

        return df

    def plot(self):
        df = None
        for path in self.__pathes:
            df_exp = self.__read_df(path)
            self.filter_ip(df)
            df_exp = self.__aggregate(df_exp)
            if df is None:
                df = df_exp
            else:
                df['size'] += df_exp['size']

        df['size'] /= len(self.__pathes)
        df['size'].plot()
        input('press return to continue')

ra = ResultAnalyzer(['/home/pkochetk/images/data/MSU/capture/exp_1/0_1/date__12_16_18_13mb_50.csv'], '500ms')
ra.plot()