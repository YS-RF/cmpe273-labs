import asyncio
from pathlib import Path

array_of_opened_file = []
tdarr = [[0]*10 for i in range(10)]
folder_name = Path("input/")
final_output =  open(folder_name/"big_file.txt","w+")

def merge_sort (A):
    merge_sort2(A,0,len(A)-1)

def merge_sort2(A,first,last):
    if first < last:
        middle = (first + last )//2
        merge_sort2(A,first,middle)
        merge_sort2(A,middle+1,last)
        merge (A,first,middle,last)

def merge (A,first,middle,last):
    L = A [first:middle+1]
    R = A [middle+1:last+1]

    L.append(9999)
    R.append(9999)

    i=j=0
    for k in range (first,last+1):
        if L[i]<=R[j]:
            A[k] = L[i]
            i+=1
        else:
            A[k] = R[j]
            j+=1


def sort_ten_files():
    for i in range (1,11):
        filename_unsort = "unsorted_" + str(i) + ".txt"
        filename_sorted = "sorted_" + str(i) + ".txt"

        data_folder = Path("input/")
        file_to_open = data_folder / filename_unsort

        with open(file_to_open,'r') as f:
            array = []

            while True:  
                line = f.readline() 
                if not line: 
                    break
                array.append(int(line.strip()))
            #await here
            merge_sort(array)

            with open (data_folder / filename_sorted,"w+") as g:
                #await here
                for s in array:
                    g.write(str(s)+"\n")

sort_ten_files()

# define tdarr
for i in range (1,11):

    file_name = "sorted_" + str(i) + ".txt"
    file_to_open = folder_name / file_name

    array_of_opened_file.append(open(file_to_open))

    for index in range (10):
        nextint = array_of_opened_file[i-1].readline()
        tdarr[i-1][index] = int(nextint.strip())
# find local min and location

def find_local_min (tdarr):
    localmin = 10000
    location = 0
    for i in range (10):
        while not tdarr[i]:
            i +=1
            if i >=10:
                return [localmin,location]


        if tdarr[i][0]<localmin:
            localmin = tdarr[i][0]
            location = i

    return [localmin,location]


async def find_minimum(myQueue):
    for _ in range (1000):
        temp_local_min = find_local_min(tdarr)
        if temp_local_min is None:
            continue
        await myQueue.put(temp_local_min)
        del tdarr [temp_local_min[1]][0]

async def bring_data_in(myQueue):
    for _ in range (1000):  
        item = await myQueue.get()
        if item is None:
            break
        final_output.write(str(item[0])+"\n")

        nextnum = array_of_opened_file[item[1]].readline().strip()
        if nextnum == '':
            continue
        tdarr[item[1]].append(int(nextnum))

loop = asyncio.get_event_loop()
myQueue = asyncio.Queue(loop=loop, maxsize=5)



try:
    loop.run_until_complete(asyncio.gather(find_minimum(myQueue), bring_data_in (myQueue)))
finally:
    loop.close()

for anything in array_of_opened_file:
    anything.close()