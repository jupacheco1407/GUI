from PySide6.QtCore import QThread, Signal
import time

class MaxForceThread(QThread):
    progress_updated = Signal(int)
    calculation_complete = Signal(list)
    
    def __init__(self, trigno_base):
        super().__init__()
        self.trigno_base = trigno_base
        self.running = True
        
    def run(self):
        """Capture data for 5 seconds and find max values"""
        max_values = [0] * len(self.trigno_base.channel_guids)
        start_time = time.time()
        
        # Temporary data handler
        def data_handler(data):
            nonlocal max_values
            for i, channel_data in enumerate(data):
                current_max = max(channel_data) if channel_data else 0
                if current_max > max_values[i]:
                    max_values[i] = current_max
        
        # Register temporary callback
        original_callback = self.trigno_base.collection_data_handler.DataHandler.processData
        self.trigno_base.collection_data_handler.DataHandler.processData = data_handler
        
        # Start collection
        self.trigno_base.Start_Callback(False, False)
        
        # Update progress for 5 seconds
        for second in range(1, 6):
            time.sleep(1)
            self.progress_updated.emit(second)
            if not self.running:
                break
        
        # Stop collection and restore original callback
        self.trigno_base.Stop_Callback()
        self.trigno_base.collection_data_handler.DataHandler.processData = original_callback
        
        # Emit results
        self.calculation_complete.emit(max_values)
    
    def stop(self):
        """Stop the calculation early"""
        self.running = False