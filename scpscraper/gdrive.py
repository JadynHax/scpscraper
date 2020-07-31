import os, shutil, sys

# Check if user is using Google Colaboratory (and if so, we can do fancier things...)
try:
  from google.colab import drive
except:
  pass

# Custom error definitions
class DriveNotMountedError(Exception):
  pass

class PathNotRecognizedError(Exception):
  pass

class PathNotExistsError(Exception):
  pass

class NoColaboratoryVMError(Exception):
  pass

# Special Google Colaboratory functions
def mount():
  """
  Mounts your Google Drive to the Colaboratory VM.
  """
  if 'google.colab' in sys.modules:
    drive.mount('/content/drive')
  else:
    raise NoColaboratoryVMError("You must be in Google Colaboratory to run any Google Drive related functions!")

def _is_mounted():
  if os.path.isdir('/content/drive'):
    return
  else:
    raise DriveNotMountedError("You must first mount your Google Drive using scpscraper.gdrive.mount()!")

def copy(path):
  """
  Copies a file or directory to your Google Drive.
  """
  _is_mounted()
  
  if os.path.exists(path):
    if os.path.isfile(path):
      shutil.copyfile(path, f"/content/drive/My Drive/{path}")

    elif os.path.isdir(path):
      shutil.copytree(path, f"/content/drive/My Drive/{path}")

    else:
      raise PathNotRecognizedError(f"Path {path} is not a file or a directory!")
  
  else:
    raise PathNotExistsError(f"Path {path} does not exist!")
