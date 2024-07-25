import json

import numpy as np
import pandas as pd
import threading as ts
import time

class StatisticClass:
    def __init__(self):
        self.isrunning = False
        self.percent = 0
        self.result=None
        self.totaldata={}
        self.procdf_time=None
        self.date_YMD=None
        self.dates=None
        self.action_buy=None
        self.action_cart=None
        self.action_fav=None
        self.action_pv=None

        
    def verfiylogin(self, username, password):
        filepath = "./用户名密码.csv"
        alldata = pd.read_csv(filepath)
        alldata.iloc[:, 2] = alldata.iloc[:, 2].astype(dtype=np.str_)
        linecount = alldata.shape[0]

        if alldata.loc[(alldata.iloc[:, 2] == password) & (alldata.iloc[:, 1] == username), :].shape[0] != 0:
            return 1
        elif alldata.loc[alldata.iloc[:, 1] == username, :].shape[0] != 0:
            return -1
        return -2
    
    def getopernum(self, filepath):
        reader = pd.read_csv(filepath, iterator=True, header=None)
        
        no = 0
        procdf = None
        count = 0
        chunksize = 10000
        self.isrunning = True
        self.percent = 0

        while self.isrunning:
            try:
                chunk = reader.get_chunk(chunksize)
                chunk.columns = ['user','product','type','act','timestamp']
                count += chunk.shape[0]

                df = chunk
                df = df.loc[:, 'act':'timestamp']
                df = df.groupby(['act']).count().reset_index()

                if no==0:
                    procdf = df
                else:
                    procdf = pd.concat([procdf, df], axis=0, ignore_index=True)

                no +=1
                self.percent = count/2000000*100
                # print(self.percent)
            except StopIteration:
                self.isrunning = False
                break
        #         将原来的索引变为df其中的一列
        procdf = procdf.groupby(['act']).sum().reset_index()
        print('Thread is over')
        self.result=[procdf.iloc[:,0].to_list(),procdf.iloc[:,1].to_list()]
        return count, procdf
    
    def getpercentage(self):
        return self.percent

    #获取点击top前十的商品
    def getTopTen(self, filepath):
        reader = pd.read_csv(filepath, iterator=True, header=None)

        no = 0
        procdf = None
        count = 0
        chunksize = 10000
        self.isrunning = True
        self.percent = 0

        while self.isrunning:
            try:
                chunk = reader.get_chunk(chunksize)
                chunk.columns = ['user', 'product', 'type', 'act', 'timestamp']
                count += chunk.shape[0]

                # 只选择 act 为 'pv' 的记录
                df = chunk[chunk['act'] == 'pv']
                # 分组并计算每个 product 的出现次数
                df_grouped = df.groupby('product')['act'].count().reset_index(name='count')
                df_grouped.columns=['product', 'count']
                if no == 0:
                    procdf = df_grouped
                else:
                    # 合并结果
                    procdf = pd.concat([procdf, df_grouped], axis=0, ignore_index=True)
                    # 按 product 分组并聚合 count 列
                    procdf = procdf.groupby('product')['count'].sum().reset_index()

                no += 1
                self.percent = count / 2000000 * 100
            except StopIteration:
                self.isrunning = False
                break

        # 最终结果按 count 降序排列并取前 10
        procdf = procdf.sort_values(by='count', ascending=False).head(10).reset_index(drop=True)

        print('Thread is over')
        self.result = [procdf['product'].tolist(), procdf['count'].tolist()]
        return count, procdf
    # 统计购买top10的商品
    def getBuyTopTen(self, filepath):
        reader = pd.read_csv(filepath, iterator=True, header=None)

        no = 0
        procdf = None
        count = 0
        chunksize = 10000
        self.isrunning = True
        self.percent = 0

        while self.isrunning:
            try:
                chunk = reader.get_chunk(chunksize)
                chunk.columns = ['user', 'product', 'type', 'act', 'timestamp']
                count += chunk.shape[0]

                # 只选择 act 为 'pv' 的记录
                df = chunk[chunk['act'] == 'buy']
                # 分组并计算每个 product 的出现次数
                df_grouped = df.groupby('product')['act'].count().reset_index(name='count')
                df_grouped.columns = ['product', 'count']
                if no == 0:
                    procdf = df_grouped
                else:
                    # 合并结果
                    procdf = pd.concat([procdf, df_grouped], axis=0, ignore_index=True)
                    # 按 product 分组并聚合 count 列
                    procdf = procdf.groupby('product')['count'].sum().reset_index()

                no += 1
                self.percent = count / 2000000 * 100
            except StopIteration:
                self.isrunning = False
                break

        # 最终结果按 count 降序排列并取前 10
        procdf = procdf.sort_values(by='count', ascending=False).head(10).reset_index(drop=True)

        print('Thread is over')
        self.result = [procdf['product'].tolist(), procdf['count'].tolist()]
        return count, procdf
    #  统计购买前十
    def getGloableData(self,filepath):
        reader = pd.read_csv(filepath, iterator=True, header=None)

        no = 0
        procdf = None
        count = 0
        chunksize = 10000
        self.isrunning = True
        self.percent = 0

        while self.isrunning:
            try:
                chunk = reader.get_chunk(chunksize)
                chunk.columns = ['user', 'product', 'type', 'act', 'timestamp']
                count += chunk.shape[0]

                # 只选择 act 为 'pv' 的记录
                df = chunk[chunk['act'] == 'buy']
                # 分组并计算每个 product 的出现次数
                df_grouped = df.groupby('product')['act'].count().reset_index(name='count')
                df_grouped.columns = ['product', 'count']
                if no == 0:
                    procdf = df_grouped
                else:
                    # 合并结果
                    procdf = pd.concat([procdf, df_grouped], axis=0, ignore_index=True)
                    # 按 product 分组并聚合 count 列
                    procdf = procdf.groupby('product')['count'].sum().reset_index()

                no += 1
                self.percent = count / 2000000 * 100
            except StopIteration:
                self.isrunning = False
                break

        # 最终结果按 count 降序排列并取前 10
        procdf = procdf.sort_values(by='count', ascending=False).head(10).reset_index(drop=True)

        print('Thread is over')
        self.result = [procdf['product'].tolist(), procdf['count'].tolist()]
        return count, procdf
    # 总览计算
    def getTotalData(self, filepath):
        reader = pd.read_csv(filepath, iterator=True, header=None)
        no = 0
        procdf = None
        count = 0
        chunksize = 10000
        self.isrunning = True
        self.percent = 0
        total_data ={}
        # 开始读取
        while self.isrunning:
            try:
                chunk = reader.get_chunk(chunksize)
                chunk.columns = ['user', 'product', 'type', 'act', 'timestamp']
                count += chunk.shape[0]



                if no == 0:
                    procdf = chunk
                else:
                    # 合并结果
                    procdf = pd.concat([procdf, chunk], axis=0, ignore_index=True)


                no += 1
                self.percent = count / 2000000 * 100
            except StopIteration:
                self.isrunning = False

                break




        # 计算不同类型的总数
        total_data['user_total'] = len(procdf['user'].drop_duplicates())
        total_data['product_total'] = len(procdf['product'].drop_duplicates())
        total_data['type_total'] = len(procdf['type'].drop_duplicates())
        total_data['pv_total'] = procdf.loc[procdf["act"] == "pv"].shape[0]
        total_data['buy_total'] = procdf.loc[procdf["act"] == "buy"].shape[0]
        total_data['cart_total'] = procdf.loc[procdf["act"] == "cart"].shape[0]
        total_data['fav_total'] = procdf.loc[procdf["act"] == "fav"].shape[0]

        self.totaldata=total_data
        return self.totaldata

    def gettotal_data(self):
        return  self.totaldata




    def change_df(self):
        df = pd.read_csv("./datas/UserBehavior_small.csv",
                         chunksize=40000)
        no = 1
        outdf = None
        for chunk in df:
            chunk.columns = ['userid', 'productid', 'typeid', 'act', 'timestamp']
            date = pd.to_datetime(chunk["timestamp"], unit='s')
            chunk["date_YMD"] = [str(i).split(" ")[0] for i in date]
            chunk["date_HMS"] = [str(i).split(" ")[1] for i in date]
            chunk["Hour"] = [str(i).split(":")[0] for i in chunk["date_HMS"]]
            if no == 1:
                outdf = chunk
            else:
                outdf = pd.concat([outdf, chunk], axis=0)
            no += 1

        self.procdf_time = outdf
    def getGroupBy_Date_YMD(self, min_date, max_date):


        print(self.procdf_time)
        # 读取
        self.date_YMD = self.procdf_time.loc[
            (self.procdf_time["date_YMD"] >= min_date) & (self.procdf_time["date_YMD"] <= max_date), ["act", "date_YMD"]]
        self.dates = self.date_YMD.groupby("date_YMD").count().index.to_list()


    def getGroupBy(self,save_colunms):
        if save_colunms == "date_YMD":
            self.action_buy = self.date_YMD.loc[self.date_YMD["act"] == "buy",["act",save_colunms]].groupby(save_colunms).count()["act"].to_list()
            self.action_cart = self.date_YMD.loc[self.date_YMD["act"] == "cart",["act",save_colunms]].groupby(save_colunms).count()["act"].to_list()
            self.action_fav = self.date_YMD.loc[self.date_YMD["act"] == "fav",["act",save_colunms]].groupby(save_colunms).count()["act"].to_list()
            self.action_pv = self.date_YMD.loc[self.date_YMD["act"] == "pv",["act",save_colunms]].groupby(save_colunms).count()["act"].to_list()
        else:
            self.action_buy = self.procdf_time.loc[self.procdf_time["act"] == "buy",["act",save_colunms]].groupby(save_colunms).count()["act"].to_list()
            self.action_cart = self.procdf_time.loc[self.procdf_time["act"] == "cart",["act",save_colunms]].groupby(save_colunms).count()["act"].to_list()
            self.action_fav = self.procdf_time.loc[self.procdf_time["act"] == "fav",["act",save_colunms]].groupby(save_colunms).count()["act"].to_list()
            self.action_pv = self.procdf_time.loc[self.procdf_time["act"] == "pv",["act",save_colunms]].groupby(save_colunms).count()["act"].to_list()
































inst = StatisticClass()
inst.change_df()
# 多线程调用行为统计
def running_act_count():
    # macos
    # ret=inst.getopernum("/Users/wzf/Resilio Sync/BigData/可视化/flask_example/flask_example/datas/UserBehavior_small.csv")
    # window
    ret=inst.getopernum("./datas/UserBehavior_small.csv")
    print("=====")
    print(ret)


# 调用pv行为统计top10
def running_pv_top():
    # macos
    # count,ret=inst.getTopTen("/Users/wzf/Resilio Sync/BigData/可视化/flask_example/flask_example/datas/UserBehavior_small.csv")
    # window
    ret=inst.getTopTen("./datas/UserBehavior_small.csv")
    # print("=====")

    # print(ret)
    # print(getdata())


# 调用buy行为统计top10
def running_buy_top():
    # macos
    # count,ret=inst.getBuyTopTen("/Users/wzf/Resilio Sync/BigData/可视化/flask_example/flask_example/datas/UserBehavior_small.csv")
    # window
    ret=inst.getBuyTopTen("./datas/UserBehavior_small.csv")
    # print("=====")
    #
    # print(ret)
    # print(getdata())

# 时间计算方法
def time_work():
    inst.getGroupBy_Date_YMD("2017-11-25","2017-12-03")
    inst.getGroupBy("date_YMD")
    data=json.dumps({
        "Dates": inst.dates,
        "daily_Buy": inst.action_buy,
        "daily_Cart": inst.action_cart,
        "daily_Fav": inst.action_fav,
        "daily_Pv": inst.action_pv
    })
    inst.getGroupBy("Hour")
    data1 = json.dumps({
        "Hours": [i for i in range(0, 24)],
        "Hour_Buy": inst.action_buy,
        "Hour_Cart": inst.action_cart,
        "Hour_Fav": inst.action_fav,
        "Hour_Pv": inst.action_pv
    })
    return data,data1



def running_getTotalData():
    inst.getTotalData("./datas/UserBehavior_small.csv")



def checkStatus():
    return  inst.isrunning,inst.getpercentage()

def getdata():
    inst.isrunning=False
    inst.percent=0

    return inst.result


def get_totaldata():
    inst.isrunning = False
    inst.percent = 0
    ret=inst.gettotal_data()
    print(ret)
    return ret



# threadrun = ts.Thread(target=running_getTotalData())
# threadrun.start()
# time.sleep(0.2)
# while inst.isrunning is True:
#     print("percentage: " + str(int(inst.getpercentage())) + "%")
#     time.sleep(0.1)

