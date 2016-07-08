from threading import Semaphore

class Lightswitch:
  def __init__(self):
    self.counter = 0
    self.mutex = Semaphore(1)

  def lock(self, sem):
    self.mutex.acquire()
    self.counter += 1
    if self.counter == 1:
        sem.acquire()
    self.mutex.release()

  def unlock(self, sem):
    self.mutex.acquire()
    self.counter -= 1
    if self.counter == 0:
      sem.release()
    self.mutex.release()
    
"""
No-starve readers-writers

### Init
readSwitch = Lightswitch()
roomEmpty = Semaphore(1)
turnstile = Semaphore(1)

### Writer
turnstile.wait()
roomEmpty.wait()
# Critical section for writers
turnstile.signal()
roomEmpty.signal()

### Reader
turnstile.wait()
turnstile.signal()

readSwitch.lock(roomEmpty)
# Read processing
readSwitch.unlock(roomEmpty)

If a writer is waiting on roomEmpty, it will hold the turnstile mutex,
so no incoming readers can pass the turnstile. Therefore, all the
remaining readers will lightswitch-unlock roomEmpty, allowing the
writer to progress.
"""
