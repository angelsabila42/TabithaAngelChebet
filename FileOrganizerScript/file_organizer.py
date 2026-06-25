# Assignment2: Write a python script that performs file organization of your download folder
from pathlib import Path

class FileOrganizer:
    def __init__(self, target_directory: Path):
        self.target_path = target_directory
        
        self.folder_names = {
            "Audio": {'aif','cda','mid','midi','mp3','mpa','ogg','wav','wma'},
            "Compressed":{'7z','deb','pkg','rar','rpm', 'tar.gz','z', 'zip'},
            'Code':{'js','jsp','html','ipynb','py','java','css'},
            'Documents':{'ppt','pptx','pdf','xls', 'xlsx','doc','docx','txt', 'tex', 'epub'},
            'Images':{'bmp','gif','ico','jpeg','jpg','png','jfif','svg','tif','tiff'},
            'Software':{'apk','bat','bin', 'exe','jar','msi','msix'},
            'Videos':{'3gp','avi','flv','h264','mkv','mov','mp4','mpg','mpeg','wmv'},
            'Others': {'NONE'}
            }
        
        self.extension_map = {
            extension: filetype 
            for filetype, extensions in self.folder_names.items()
            for extension in extensions
            }
        
        self.lowercase_categories = {name.lower() for name in self.folder_names.keys()}
        
    def _setup_directories(self):
        #Building paths and checking existence
        for folder_name in self.folder_names.keys():
            folder_path = self.target_path / folder_name
            folder_path.mkdir(parents=True, exist_ok=True)
            
    def _get_safe_destination(self, destination):
        if not destination.exists():
            return destination
        
        parent_dir = destination.parent
        base_name = destination.stem
        extension = destination.suffix
        
        counter = 1
        
        while True:
            new_destination = parent_dir / f"{base_name}_$counter{extension}"
            if not new_destination.exists():
                return new_destination
            counter += 1
            
    def _get_new_path(self, old_path):
        extension = old_path.suffix[1:].lower()
        
        target_folder = self.extension_map.get(extension, "Others")
        
        final_path = self.target_path / target_folder / old_path.name
        return final_path
    
    def organize(self):
        print(f"Scanning and cleaning: {self.target_path}")
        self._setup_directories()
        
        #Separating files and folders
        onlyfiles = [file for file in self.target_path.iterdir() if file.is_file()]
        onlyfolders = [folder for folder in self.target_path.iterdir() if folder.is_dir()]
        
        #Moving the files
        for file_path in onlyfiles:
            #Calculate the new location using the function
            raw_destination = self._get_new_path(file_path)
            safe_destination = self._get_safe_destination(raw_destination)
            
            #Physically move the file
            file_path.rename(safe_destination)
            print(f"Moved File: {file_path.name} -> {safe_destination.parent.name}")
                    
                    
        #Moving the unknown folders to others
        for folder_path in onlyfolders:
            if folder_path.name.lower() not in self.lowercase_categories:
                destination = self.target_path / "Others" / folder_path.name
                folder_path.rename(destination)
                print(f"Moved Folder: {folder_path.name} -> Others/") 
                
        print("Organization cycle completed cleanly!")
        
if __name__ == "__main__":
    downloads = Path.home() / "Downloads" 
    downloader_cleanup = FileOrganizer(downloads)
    downloader_cleanup.organize()