import numpy as np
from abc import ABC, abstractmethod


class FileManager:
    @classmethod
    def save_array(cls, file_path, array):
        try:
            np.save(file_path, array)
            print(f"Array saved successfully to {file_path}")
        except Exception as e:
            print(f"Error saving array: {e}")

    @classmethod
    def load_array(cls, file_path):
        try:
            loaded_array = np.load(file_path)
            print(f"Array loaded successfully from {file_path}")
            return loaded_array
        except Exception as e:
            print(f"Error loading array: {e}")
            return np.array([])

    @classmethod
    def display_array(cls, array):
        print(array)
