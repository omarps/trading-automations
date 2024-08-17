from abc import ABC, abstractmethod


class RenamerStrategy(ABC):

    def __init__(self):
        self.section_name = None
        self.folder_name = None
        self.pattern = None
        self.new_filename = None

    @abstractmethod
    def rename(self, original_filepath, root, file, idx):
        if file.startswith("."):
            return None # ignore .DS_Store files

        pass
