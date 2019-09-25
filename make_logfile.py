import os
import datetime

def get_log():
    
    max_files = 0

    #path to log file directory
    path = os.environ.get('logpath')
    os.chdir(path)
    files = sorted(os.listdir(path), key=os.path.getctime) 
    number_files = len(files)

    if number_files >= max_files :
        n_to_delete = max_files - number_files + 1
        oldest = files[0:n_to_delete]
        for old_file in oldest :
            os.remove(old_file)

    now = datetime.datetime.now()
    f_log_name = path + 'log_'+now.strftime('%Y-%m-%d_%H,%M')+'.txt'
    f_log = open(f_log_name,'w')
    return f_log
