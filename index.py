from multiprocessing import Lock, Process, Queue, current_process
import time
import queue # imported for using queue.Empty exception
from datetime import datetime, timedelta


from post_parser import grab_posts


def get_dates_array(date_from, date_to, date_range_days):
    dates = []

    date_from_dt = datetime.strptime(date_from, '%Y-%m-%d')
    date_to_dt = datetime.strptime(date_to, '%Y-%m-%d')

    days_range = range(int((date_to_dt - date_from_dt).days))

    for dr in days_range:
        dates.append([date_from_dt, date_from_dt + timedelta(days=date_range_days)])
        date_from_dt = date_from_dt + timedelta(days=date_range_days)

    return dates


def do_task(tasks_to_accomplish, tasks_that_are_done):
    while True:
        try:
            '''
                try to get task from the queue. get_nowait() function will 
                raise queue.Empty exception if the queue is empty. 
                queue(False) function would do the same task also.
            '''
            task = tasks_to_accomplish.get_nowait()
        except queue.Empty:
            print('queue is empty')
            break
        else:
            '''
                if no exception has been raised, add the task completion 
                message to task_that_are_done queue
            '''
            print(task)
            try:
                grab_posts(task[0], task[1])
            except Exception as e:
                print(e.__repr__())
                # break
            tasks_that_are_done.put(str(task) + ' is done by ' + current_process().name)
            time.sleep(5.5)
    return True


def main(tasks_list, processes_num):
    # number_of_task = 10
    number_of_task = len(tasks_list)
    # number_of_processes = 3
    number_of_processes = processes_num
    tasks_to_accomplish = Queue()
    tasks_that_are_done = Queue()
    processes = []

    for i in range(number_of_task):
        # tasks_to_accomplish.put("Task no " + str(i))
        tasks_to_accomplish.put(tasks_list[i])

    # creating processes
    for w in range(number_of_processes):
        p = Process(target=do_task, args=(tasks_to_accomplish, tasks_that_are_done))
        processes.append(p)
        p.start()

    # completing process
    for p in processes:
        p.join()

    # print the output
    while not tasks_that_are_done.empty():
        print(tasks_that_are_done.get())

    return True


date_start = '2020-01-20'
date_end = '2020-02-01'
date_range_days = 1
workers_max_count = 1



# grab_posts()

if __name__ == "__main__":
    # grab_posts()
    posts_dates = get_dates_array(date_start, date_end, date_range_days)
    print(posts_dates)
    print(len(posts_dates))

    main(posts_dates, workers_max_count)

    # tasks_queue = Queue()


    # print(type(posts_dates[0][0]))
    # print(type(date_start))
    #
    # if type(date_start) is str:
    #     print('string')
    # else:
    #     print('not string')