import os

dirName = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'vo_hero/'))
for item in os.listdir(dirName):
    if '.DS_Store' in item:
        os.remove(dirName+'/'+item)
    #new = item.replace(item, item+' - Default')
    #os.rename(dirName + '/' + item, dirName + '/' + new)
