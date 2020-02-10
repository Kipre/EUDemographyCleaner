import sys
import datetime

class ReasonableCallback(tf.keras.callbacks.Callback):
  """Stop overflowing your output with the standard tf bullshit"""

  def __init__(self):
    super(ReasonableCallback, self).__init__()

  def on_train_begin(self, logs=None):
    self.starting_time = datetime.datetime.now()
    self.secs_to_finish = '----' 

  def on_epoch_start(self, epoch, logs=None):
    self.print_progress(epoch=epoch, logs=logs)

  def on_epoch_end(self, epoch, logs=None):
    self.secs_to_finish = str(round(self.estimate_time_to_finish(epoch), 3))
    self.print_progress(epoch=epoch, logs=logs)

  def on_batch_start(self, batch, logs=None):
    self.print_progress(batch=batch, logs=logs)

  def on_train_end(self, logs=None):
    self.print_progress(logs=logs, finished=True)

  def print_progress(self, batch=0, epoch=0, logs=None, finished=False):
    line = "Epoch " + str(epoch) + "/" + str(self.params['epochs']) +\
           f" Secs to finish: {self.secs_to_finish} " +\
           f"{self.batch_bar(batch)} "
    if logs:
        line += f"Loss {logs['loss']}"
    if finished:
      line = f"Epoch {epoch}/{self.params['epochs']}"
    sys.stdout.write("\r" + line)
    sys.stdout.flush()

  def estimate_time_to_finish(self, epoch):
    already_running_for = (datetime.datetime.now() - self.starting_time).total_seconds()
    return (already_running_for/max(epoch, 1))*(self.params['epochs']-epoch)

  def batch_bar(self, batch):
    done = 20/((self.params['steps']-batch)/max(batch, 1) + 1)
    to_be_done = 20 - done
    return "#"*int(done) + "_"*int(to_be_done)