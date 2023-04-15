from genericpath import isfile
import os
from traffic_filter import conversation_stat
import shutil

def create_dataset(root):
    pathlist = os.listdir(root)

    ignore_path = ['tsne','csv']
    for i in ignore_path:
        if i in pathlist:
            pathlist.remove(i)

    pathlist = [i for i in pathlist if os.path.isdir(os.path.join(root,i))]
    for date_path in pathlist:
        for id_path in os.listdir(os.path.join(root,date_path)):
            id, bv= id_path.split('_')
            pcap_path = os.path.join(root,date_path,id_path,bv+'.pcap')
            if os.path.isfile(pcap_path):
                conversation_stat(pcap_path)

                csv_src_path = os.path.join(root,date_path,id_path,bv+'.csv')
                root_csv = os.path.join(root,'csv')
                if not os.path.isdir(root_csv):
                    os.makedirs(root_csv)
                csv_dst_path = os.path.join(root_csv,bv+"_"+date_path+'.csv')
                if os.path.isfile(csv_src_path):
                    shutil.copy(csv_src_path,csv_dst_path)
            
            


create_dataset('D:\\result_bak')