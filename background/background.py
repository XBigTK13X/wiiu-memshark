import threading
import queue
import time
import types

def schedule(task):	
	def send_message(self, message):
		self.get_queue().put(message)
	
	def set_queue(self, queue):
		self.queue = queue
	
	def get_queue(self):
		return self.queue

	task.send_message = types.MethodType(send_message, task)
	task.set_queue = types.MethodType(set_queue, task)
	task.get_queue = types.MethodType(get_queue, task)

	task.set_queue(queue.Queue())

	def background():
		running = True
		while running:
			task.background()
			item = None
			try:
				item = task.get_queue().get(timeout=1)
			except Exception:
				swallow = True
			if item != None:
				if item == "kill_thread":
					running = False
				else:								
					task.handle_message(item)
	task.thread = threading.Thread(target=background)
	task.thread.daemon = True
	task.thread.start()