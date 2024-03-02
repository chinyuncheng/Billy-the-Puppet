"""
MIT License

Copyright (c) 2024-present chinyuncheng

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os

def create_folder(path: str, folder_name: str) -> str:
    """
    Create a new folder for the specific path
    """
    new_folder_path = os.path.join(path, folder_name)
    os.makedirs(new_folder_path, exist_ok=True)
    return new_folder_path

def get_files(folder_path, file_extension: str = None) -> list[str]:
    """
    Get all files with the specific file extension
    """
    data = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file_extension and os.path.basename(file).find(file_extension) == -1:
                continue
            file_path = os.path.join(root, file)
            data.append(file_path)
    return data
