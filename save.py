import json
import uuid

class SaveEditor:
    def __init__(self, savePath):
        self.data = {}
        self.item_num = 0
        self.avatar_prepend = ''
        self.cur_item = []
        with open(savePath, encoding="utf8") as f:
            self.data = json.load(f)
        for k in self.data:
            if 'avatar' in str(k).lower():
                self.avatar_prepend = k.split(sep='.')[0]
                break
        for k in self.data:
            if '.itemList.id.' in k:
                self.cur_item.append(int(k.split(sep='.')[-1]))
            elif "itemList.Num" in k:
                self.item_num = self.data[k]
    
    def gen_item(self,itemID,itemCount):

        itemUUIDKey = "{avatarPrepend}.itemList.UUID.{itemCount}".format(avatarPrepend = self.avatar_prepend, itemCount = self.item_num)
        itemIDKey = "{avatarPrepend}.itemList.id.{itemCount}".format(avatarPrepend = self.avatar_prepend, itemCount = self.item_num)
        itemCountKey = "{avatarPrepend}.itemList.count.{itemCount}".format(avatarPrepend = self.avatar_prepend, itemCount = self.item_num)
        itemIndexKey = "{avatarPrepend}.itemList.index.{itemCount}".format(avatarPrepend = self.avatar_prepend, itemCount = self.item_num)
        itemSeidKey = "{avatarPrepend}.itemList.Seid.{itemCount}".format(avatarPrepend = self.avatar_prepend, itemCount = self.item_num)
        itemDict = {
            itemUUIDKey:str(uuid.uuid4().hex),
            itemIDKey:itemID,
            itemCountKey:itemCount,
            itemIndexKey:0,
            itemSeidKey:{},
        }
        return itemDict
    
    def add_item(self,itemID,itemCount=10,tempIndex=21):
        '''tempIndex is to maintain json order'''
        itemDict = self.gen_item(itemID,itemCount)
        #remove last tempIndex items 
        tempData = dict(list(self.data.items())[-tempIndex:])
        self.data = dict(list(self.data.items())[:-tempIndex])
        #add item
        for k,v in itemDict.items():
            self.data[k]=v
        self.item_num += 1
        #add back last tempIndex items
        for k,v in tempData.items():
            self.data[k]=v
        #update itemnum
        itemNumKey = "{avatarPrepend}.itemList.Num".format(avatarPrepend = self.avatar_prepend)
        self.data[itemNumKey] = self.item_num


    def output(self,path):
        with open(path,"w", encoding="utf8") as f:
            json.dump(self.data,f)