from libs.progress import ProgressBar
import time

total_time = 5
iterations = 10

def test_popup():
    with ProgressBar(message="Calculating", progress_name="items") as p:
        for i in range(iterations):
            p.progress()
            time.sleep(total_time / iterations)
     
def test_popup_iterator():
    for i in ProgressBar(range(iterations), message="Evaluating", progress_name="batches"):
        time.sleep(total_time / iterations)
        
#test_popup_iterator()
test_popup()
