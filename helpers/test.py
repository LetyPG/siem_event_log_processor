import unittest
import os  
import shutil
from helpers.data_generator import generate_test_data_with_edge_cases



class TestEventSiemLogProcessor(unittest.TestCase):
   
    def setUp(self):                        
        self.test_dir = "test_data"             
        os.makedirs(self.test_dir, exist_ok=True)  
        self.test_file_path = os.path.join(self.test_dir, "test_events.txt")
    
        # Generate test data with edge cases using Faker
        self.sample_data = generate_test_data_with_edge_cases()
        
        with open(self.test_file_path, "w") as f:  
            f.write(self.sample_data)

    def tearDown(self):                         
        if os.path.exists(self.test_dir):       
            shutil.rmtree(self.test_dir) 

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)