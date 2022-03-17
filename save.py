import json
from re import I
import uuid
from collections import defaultdict


class SaveEditor:
    def __init__(self, savePath):
        '''
        self.cur_item is stored as d[item_id] : [(item_position,item_count),...]
        '''
        self.data = {}
        self.item_num = 0
        self.avatar_prepend = ''
        self.cur_item = defaultdict(list)
        self.eq_item =[]
        with open(savePath, encoding="utf8") as f:
            self.data = json.load(f)
        for k in self.data:
            if 'avatar' in str(k).lower():
                self.avatar_prepend = k.split(sep='.')[0]
                break
        for k,v in self.data.items():
            if '.itemList.Seid.' in k and len(v)>0:
                self.eq_item.append(int(k.split(sep='.')[-1]))
            elif '.itemList.id.' in k:
                cur_id = int(k.split(sep='.')[-1])
                itemCountKey = "{ap}.itemList.count.{ic}".format(ap = self.avatar_prepend, ic = cur_id)
                itemCount = self.data[itemCountKey]
                self.cur_item[v].append((cur_id,itemCount))
            elif "itemList.Num" in k:
                self.item_num = self.data[k]
    
    def prep_item(self,itemID,itemCount,avatarPrepend,itemNum,itemIndex=0,itemSeid={}):
        #setting key
        itemUUIDKey = "{ap}.itemList.UUID.{ic}".format(ap = avatarPrepend, ic = itemNum)
        itemIDKey = "{ap}.itemList.id.{ic}".format(ap = avatarPrepend, ic = itemNum)
        itemCountKey = "{ap}.itemList.count.{ic}".format(ap = avatarPrepend, ic = itemNum)
        itemIndexKey = "{ap}.itemList.index.{ic}".format(ap = avatarPrepend, ic = itemNum)
        itemSeidKey = "{ap}.itemList.Seid.{ic}".format(ap = avatarPrepend, ic = itemNum)
        itemDict = {
            itemUUIDKey:str(uuid.uuid4().hex),
            itemIDKey:itemID,
            itemCountKey:itemCount,
            itemIndexKey:itemIndex,
            itemSeidKey:itemSeid,
        }
        return itemDict


    def new_item(self,itemId,itemCount,tempIndex=21):
        '''tempIndex is to maintain json order'''
        #remove last tempIndex items 
        tempData = dict(list(self.data.items())[-tempIndex:])
        self.data = dict(list(self.data.items())[:-tempIndex])
        #add item
        itemDict = self.prep_item(itemId,itemCount,self.avatar_prepend,self.item_num)
        for k,v in itemDict.items():
            self.data[k]=v
        #add back last tempIndex items
        for k,v in tempData.items():
            self.data[k]=v
        #update itemnum
        self.item_num += 1
        itemNumKey = "{avatarPrepend}.itemList.Num".format(avatarPrepend = self.avatar_prepend)
        self.data[itemNumKey] = self.item_num

    def update_item(self,itemId,itemCount):
        '''update the first instance of the item it finds'''
        position = self.cur_item[itemId][0][0]
        curCount = self.cur_item[itemId][0][1]
        itemCountKey = "{ap}.itemList.count.{ic}".format(ap = self.avatar_prepend, ic = position)
        self.data[itemCountKey] = curCount+itemCount

    #cant add equipment , not sure how to add proper SeId
    def Add_Item(self,itemId,itemCount=10):
        if itemId not in self.eq_item:
            if itemId in self.cur_item:
                self.update_item(itemId,itemCount)
            else:
                self.new_item(itemId,itemCount)
        else:
            print(itemId+" not added as it is a equipment item")

    def output(self,path):
        with open(path,"w", encoding="utf8") as f:
            json.dump(self.data,f)