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

def copy(path: str):
  """
  Copies a file or directory to your Google Drive.
  """
  _is_mounted()
  
  if os.path.exists(path):
    if os.path.isfile(path):
      shutil.copyfile(path, "/content/drive/My Drive/{}".format(path)

    elif os.path.isdir(path):
      shutil.copytree(path, "/content/drive/My Drive/{}".format(path)

    else:
      raise PathNotRecognizedError("Path {} is not a file or a directory!".format(path))
  
  else:
    raise PathNotExistsError("Path {} does not exist!".format(path)
