from __future__ import division
import time

FPS = 60
SECS_PER_FRAME = 60.0 / FPS

def main():
    
    
    done = False

    while(not done):

        start_time = time.time()

        # Input

        # Update
        time.sleep(1)
        sleep_time = max(start_time + SECS_PER_FRAME - time.time(), 0)

        # Render
        print round(sleep_time * 1000.0, 5)

        # Time
        
        time.sleep(sleep_time)

        

if __name__ == "__main__":
  try:
    main()
  except KeyboardInterrupt:
    pass