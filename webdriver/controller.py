import os
import threading
import time
from queue import PriorityQueue, Empty  # Use queue instead of asyncio
from typing import Any, Dict, Optional

from PyQt5.QtCore import pyqtSignal, QObject
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By


class WebDriverControllerSignals(QObject):
    status_update = pyqtSignal(str)


class WebDriverController:
    def __init__(self, idle_timeout=300):  # 300 seconds = 5 minutes
        self.signals = WebDriverControllerSignals()
        self.driver: Optional[webdriver.Firefox] = None
        self.driver_lock = threading.Lock()
        self.task_queue = PriorityQueue()  # Use queue.PriorityQueue
        self.stop_event = threading.Event()
        self.worker_thread = threading.Thread(target=self._process_tasks, daemon=True)
        self.driver_path = os.path.join(os.path.dirname(__file__), "geckodriver.exe")
        self.idle_timeout = idle_timeout
        self.last_used_time = time.time()  # Track the last activity timestamp
        self.worker_thread.start()

    def start_driver(self):
        """Start the WebDriver instance."""
        with self.driver_lock:
            if self.driver is None:
                if not os.path.exists(self.driver_path):
                    print()
                    self.signals.status_update.emit(f"Geckodriver not found at {self.driver_path}")
                    return
                    # raise FileNotFoundError(f"Geckodriver not found at {self.driver_path}")
                self.signals.status_update.emit("Webdriver Starting.")
                self.driver = webdriver.Firefox(service=Service(self.driver_path))
                self.signals.status_update.emit("Webdriver Running.")

        print("WebDriver started.")

    def stop_driver(self):
        """Stop the WebDriver instance."""
        with self.driver_lock:
            if self.driver is not None:
                self.driver.quit()
                self.driver = None
        print("WebDriver stopped.")

    def add_task(self, task: Dict[str, Any], priority: int = 1):
        """Add a task to the task queue."""
        print('YOOOOOOOOO  add_task')
        self.task_queue.put(priority, task)  # No need to await

    def _process_tasks(self):
        """Process tasks from the queue."""
        while not self.stop_event.is_set():
            try:
                priority, task = self.task_queue.get(timeout=1)  # Timeout avoids blocking on empty queue
                self._execute_task(task)
                self.last_used_time = time.time()
            except Empty:
                current_time = time.time()
                if self.driver and current_time - self.last_used_time > self.idle_timeout:
                    self.signals.status_update.emit("Webdriver was shut down.\nReason: Webdriver has been inactive for 5 minutes.")
                    self.stop_driver()
                time.sleep(1)
            except Exception as e:
                print(f"Task processing error: {e}")

    def _execute_task(self, task: Dict[str, Any]):
        """Execute a single task."""
        if not self.driver:
            print("Driver not initialized. Task skipped.")
            self.start_driver()
        self.last_used_time = time.time()
        action_type = task.get("type")
        if action_type == "navigate":
            self._navigate(task)
        elif action_type == "click":
            self._click(task)
        elif action_type == "write":
            self._type(task)
        elif action_type == "wait":
            self._wait(task)
        else:
            print(f"Unknown action type: {action_type}")

    def _navigate(self, action: Dict[str, Any]):
        """Navigate to a URL."""
        url = action.get("url")
        if url:
            self.driver.get(url)
            print(f"Navigated to {url}")

    def _click(self, action: Dict[str, Any]):
        """Click an element."""
        selector = action.get("selector")
        by = action.get("by", "css")
        if selector:
            try:
                element = self.driver.find_element(self._get_by(by), selector)
                element.click()
                print(f"I clicked element: {selector}")
            except Exception as e:
                print(f"Failed to find element {selector}: {e}")

    def _type(self, action: Dict[str, Any]):
        """Type text into an element."""
        selector = action.get("selector")
        text = action.get("text")
        by = action.get("by", "css")
        if selector and text is not None:
            try:
                element = self.driver.find_element(self._get_by(by), selector)
                element.send_keys(text)
                print(f"I typed: {text} into element: {selector}")
            except Exception as e:
                print(f"Failed to find element {selector}: {e}")

    def _wait(self, action: Dict[str, Any]):
        """Wait for a certain amount of time."""
        duration = action.get("duration", 1)
        import time
        time.sleep(duration)
        print(f"Waited for {duration} seconds")

    @staticmethod
    def _get_by(by: str) -> By:
        """Convert a string to a Selenium By object."""
        by_mapping = {
            "css": By.CSS_SELECTOR,
            "id": By.ID,
            "xpath": By.XPATH,
            "name": By.NAME,
            "tag": By.TAG_NAME,
            "class": By.CLASS_NAME,
            "link_text": By.LINK_TEXT,
            "partial_link_text": By.PARTIAL_LINK_TEXT,
        }
        return by_mapping.get(by.lower(), By.CSS_SELECTOR)  # Default to CSS_SELECTOR

    def shutdown(self):
        """Gracefully shut down the controller."""
        self.stop_event.set()
        self.worker_thread.join()
        self.stop_driver()
        print("Controller shut down.")


# # Example Usage:
# if __name__ == "__main__":
#     controller = WebDriverController()
#     controller.start_driver()
#
#     # Add tasks
#     controller.add_task({"type": "navigate", "url": "https://example.com"})
#     controller.add_task({"type": "wait", "duration": 2})
#     controller.add_task({"type": "click", "selector": "a.some-link", "by": "css"})
#     controller.add_task({"type": "type", "selector": "#search", "text": "Selenium", "by": "id"})
#
#     import time
#     time.sleep(5)  # Let tasks process
#     controller.shutdown()
