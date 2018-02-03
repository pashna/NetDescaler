import os
import pandas as pd
import numpy as np
from pandas import Grouper
import re
import matplotlib.pyplot as plt
from matplotlib import interactive
interactive(True)


class ResultAnalyzer:
    def read_df(self, path):

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

        self.df = df

    def __aggregate(self, df, freq, scale=1.):
        freq_int = int(re.search(r'\d+', freq).group())
        freq_dim = freq.replace(str(freq_int), "")

        new_freq = str(int(freq_int / scale)) + freq_dim
        df = df.groupby(Grouper(key='date', freq=new_freq))['size'].sum()
        df = df.fillna(0)
        df = pd.DataFrame(df)

        df['diff'] = np.arange(0, len(df))
        df['diff'] *= freq_int

        return df

    def filter_ip(self, df, ip_srcs=[], ip_dsts=[]):
        if len(ip_srcs):
            df = df[df.ip_src.isin(ip_srcs)]
        if len(ip_dsts):
            df = df[df.ip_dst.isin(ip_dsts)]

        return df

    def calc_xy(self, freq='500ms', ip_srcs=[], ip_dsts=[], scale=1.):

        df_exp = self.filter_ip(self.df, ip_srcs, ip_dsts)
        df_exp = self.__aggregate(df_exp, freq, scale)

        x = df_exp['diff'].values.astype(float) / 1000.
        y = df_exp['size'].values.astype(float) / (1024*1024)
        return x, y

    def get_src_ip(self, ip_dsts=[]):

        if len(ip_dsts) > 0:
            dst_df_ip = self.df[self.df['ip_dst'].isin(ip_dsts)]
            return sorted(list(dst_df_ip['ip_src'].unique()))
        else:
            return sorted(list(self.df['ip_src'].unique()))

    def get_dst_ip(self, ip_srcs=[]):

        if len(ip_srcs) > 0:
            src_df_ip = self.df[self.df['ip_src'].isin(ip_srcs)]
            return list(src_df_ip['ip_dst'].unique())
        else:
            return list(self.df['ip_dst'].unique())
