```
#!/usr/bin/env python3
import thread
from time import ctime, sleep,time

def job1():
    print("job1 start:\n",time())
    sleep(2)
    print("job1 end:\n",time())

def job2():
    print("job2 start:\n",time())
    sleep(4)
    print("job2 end:\n",time())

def main():
    print("main1 start:\n",time())
    thread.start_new_thread(job1,())
    thread.start_new_thread(job2,())
    sleep(3)
    print("main1 end:\n",time())
    
if __name__ == "__main__":
    main()
```

