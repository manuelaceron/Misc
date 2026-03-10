""" 

Async IO

Concurrent code with aync.io syntax


1. Synchronous code: one thing after another, sequential
2. Concurrent code: not faster, not waiting something is finished, but take many tasks and process them in the back?
 - single threaded
 - coopartate multitasking
 - for CPU bounded heavy computations -> use processes

Event loop:?

"""

""" 
synchronous library cant work with event loop, they dont have await

await key word: 
 - stop their execution and start later (these objects implements __await__ method under the hood).
 - telling the event loop to stop execution of current function, and yield control back to the event loop and then run another task,
  and it will stay suspended until this awaitable completes

Python async.io has 3 types of awaitable objects:

1. Coroutines: functions whose execution we can pause. Defined with async keyword.
 - Desegned to work in EVENT LOOP.
 - 2 important parts:
  - coroutine function
  - coroutine object: awaitable returned calling that function
2. Tasks: wrappers around coroutines that are scheduled on the event loop, can be executed independently
 - its how we actually run coroutines concurrently
3. Futures: low-level objects representing eventual results (like promises in javascript), usually dont use futures directly, async io uses it under the hood.
    - has status, can be cancelled, ca be finished


Important things for real world projects:
For concurrency, first see if there are async libraries that replace my sync code, otherwise:
 1. Use threads to wrap sync code
 2. or use processes to wrap sync code

IO Bound:
 - We wait external things to be done, eg. web requests, database access, file access...
 - We can optimize this with async or threads

CPU Bound:
 - Computation, processing
 - We can use multiple processes than async or threads
 
I can use a profiler to determine where my script is taking more resources (IO Bound or CPU bound)
"""

import asyncio
import time

async def async_function(test_param: str, time: int = 1) -> str:
    print("Start doing something....", flush=True)
    
    # the wait will suspend this task/function until the process next to it
    # in this case, sleep, finishes...
    await asyncio.sleep(time)
    
    # time.sleep() dows not support await, makes code run sequentially
    # it does not suspennd the function but block it, then, no other taks can run menawhile
    # time.sleep() is an example of any other syncrhonous code, for example web requests
    # for that case we'd need asynchronous request library
    # another alternative is to use the synchronous fucntion and pass it to threads.... see normal_sync_fcn...>
    
    print(f"Process {test_param} finished")
    return f"Async result: {test_param}"


def normal_sync_fcn(param):
    print(f"Do something with {param}...", flush=True)
    time.sleep(param)
    print(f"Done with {param}", flush=True)
    return f"Result of {param}"
    
    
    
    
    
# define an async function
async def main():
    
    """ COROUTINE """
    print("EXAMPLE COROUTINE")
    #Create coroutine object
    coroutine_obj = async_function("TEST")
    print(coroutine_obj)
    
    # Here it runs the function
    # Both scheduled in the event loop and run to completion at the same time
    coroutine_result = await coroutine_obj
    print(coroutine_result)
    
    """ TASK """
    print("EXAMPLE TASK")
    # task scheduled to the event loop to run whenever it gets a chance
    # the task will keep track whether the coroutine finished, raised error, cancelled
    # tasks are future under the hood
    # tasks are scheduled in the event loop and sit there without run, until the event loop gets control
    # we can queue up many tasks and the event loop will run them when its ready
    task = asyncio.create_task(async_function("TEST"))
    print(task)
    
    # await the task: the await scheduled the task in the event loop and run to completion
    # the await suspends this main coroutine, until the process in task finishes...
    task_result = await task
    print(task_result)
    
    
    """ Example 1 """
    print("EXAMPLE 1: using many coroutines")
    # this example has same behaviour as synchronous code, there is not concurrency... first coroutine 1, then coroutine 2
    # because the coroutine is created, but is the await that schdules and runs until completion
    task1 = async_function("TEST1")
    print(task1)
    task_result1 = await task1
    print(task_result1)
    
    task2 = async_function("TEST2")
    print(task2)
    task_result2 = await task2
    print(task_result2)
    
    """ Example 2 """
    print("EXAMPLE 2: using many tasks")
    
    # the task schedulles a coroutine on the event loop
    # Here both tasks run "same time" without the first one finishes
    task1 = asyncio.create_task(async_function("TEST1", 2))
    task2 = asyncio.create_task(async_function("TEST2", 1))
    task_result1 = await task1
    print(task_result1)
    task_result2 = await task2
    print(task_result2)
    
    """ Example 3 """
    print("EXAMPLE 3: using many tasks")
    
    task1 = asyncio.create_task(async_function("TEST1", 2))
    task2 = asyncio.create_task(async_function("TEST2", 1))
    task_result2 = await task2
    print(task_result2)
    task_result1 = await task1
    print(task_result1)
    
    """ Example 4 """
    print("EXAMPLE 4: run threads/processes")
    
    # we have syncrhnonous code and want to run it async
    # wrap it!
    
    # In case we want threads (IO Bound)
    print("example with threads")
    task1 = asyncio.create_task(asyncio.to_thread(normal_sync_fcn,1))
    task2 = asyncio.create_task(asyncio.to_thread(normal_sync_fcn,2))
    
    result1 = await task1
    print("Thread 1 fully completed.")
    task_result2 = await task2
    print("Thread 1 fully completed.")
    
    # In case we want processes (for CPU bound)
    from concurrent.futures import ProcessPoolExecutor
    print("example with processes")
    loop = asyncio.get_running_loop()
    
    with ProcessPoolExecutor() as executor:
        task1 = loop.run_in_executor(executor, normal_sync_fcn, 1)
        task2 = loop.run_in_executor(executor, normal_sync_fcn, 2)
        
        result1 = await task1
        print("Process 1 fully completed")
        result2 = await task2
        print("Process 2 fully completed")
    
    
    """ Example 5 """
    print("Example 5: Tasks groups and taks gather")
    
    # Gather taks:
    # if one fails, shows exception and continue with others
    tasks = [asyncio.create_task(async_function(i)) for i in range(1,3)]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    print(f"Taks results: {results}")
    
    # Task group:
    # with first failure, it cancelled all other tasks
    # we use this when we want all our tasks to run succesfully! eg. calling a bunch or web requests
    async with asyncio.TaskGroup() as tg:
        results = [tg.create_task(async_function(i)) for i in range(1,3)]
        # all tasks are awaited when the contect manager exists
    print(f"Task group results: {[result.result() for result in results]}")
    

if __name__ == "__main__":
    asyncio.run(main())