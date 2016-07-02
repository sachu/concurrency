# python2.7
# in python3, we have asyncio.Semaphore
from threading import Semaphore, Thread
import time, random

class Barrier:
  def __init__(self, n):
    self.n = n
    self.count = 0
    self.mutex = Semaphore(1)
    self.turnstile = Semaphore(0)
    self.turnstile2 = Semaphore(0)

  def phase1(self):
    self.mutex.acquire()
    self.count += 1
    if self.count == self.n:
        # all n threads have reached the barrier
        for _ in xrange(self.n): self.turnstile.release()
    self.mutex.release()
    self.turnstile.acquire()

  def phase2(self):
    self.mutex.acquire()
    self.count -= 1
    if self.count == 0:
      for _ in xrange(self.n): self.turnstile2.release()
    self.mutex.release()
    self.turnstile2.acquire()

  def wait(self):
    self.phase1()
    self.phase2()

def test():
  b1 = Barrier(1)
  b1.wait()
  print 'passed Barrier(1)'

  b2 = Barrier(3)
  def worker(i):
    print 'started Thread %d' % i
    time.sleep(random.randint(1, 10))
    b2.wait()

  threads = t1, t2, t3 = \
      Thread(target=worker, args=(1,)), Thread(target=worker, args=(2,)), \
      Thread(target=worker, args=(3,))
  for t_ in threads:
    t_.start()
  for t_ in threads:
    t_.join()

  print 'passed Barrier(3)'
    

if __name__ == '__main__':
  test()
