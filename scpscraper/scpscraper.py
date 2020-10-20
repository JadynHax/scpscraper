import os, shutil, sys, re, urllib.request, pytest
from math import ceil
from bs4 import BeautifulSoup
from typing import Union
from tqdm import tqdm

from scpscraper import gdrive

def get_single_scp(scp_id: str) -> BeautifulSoup:
  """Returns HTML code for the `page-content` div of a given SCP."""
  try:
    # Grab the HTML code.
    r = urllib.request.urlopen(url=f'http://scp-wiki.wikidot.com/scp-{scp_id}')
    
    # Return the organized content for parsing.
    return BeautifulSoup(r, 'lxml')
  
  # Error handling.
  except Exception as e:
#     print(f'\nWARNING: Failed to access SCP Wiki page for SCP-{scp_id}. Error: {e}', file=sys.stderr)
    return

def _get_scp_name(scp_id: int) -> str:
  """Gets the name of an SCP from the SCP Series pages. Internal function, shouldn't need to be called by a user."""
  try:
    # Determine which series the SCP is in.
    if scp_id < 1000:
      url = 'http://scp-wiki.wikidot.com/scp-series'
    elif scp_id % 1000 == 0:
      url = f'http://scp-wiki.wikidot.com/scp-series-{int(scp_id/1000+1)}'
    else:
      url = f'http://scp-wiki.wikidot.com/scp-series-{ceil(scp_id/1000, 0)}'

    # Grab the HTML and parse as needed.
    r = urllib.request.urlopen(url=url)
    try:
      soup = BeautifulSoup(r, 'lxml')
      content = soup.find('div', id='page-content')
      list_elements = content.find_all('li')

      for li in list_elements:
        if re.findall('[0-9]+', li.find_next('a')['href']):
          if int(re.findall('[0-9]+', li.find_next('a')['href'])[0]) == scp_id:
            scp_name = re.split('-', li.get_text())[-1]
            return scp_name.strip(' ')
    
    # Handle 404 errors.
    except urllib.error.HTTPError as e:
      if e.code == 404:
#         print(f'\nWARNING: Unavailable SCP Series for SCP-{scp_id}!', file=sys.stderr)
        return

    # Handle other HTTP errors.
      else:
#         print(f'\nWARNING: Failed to access SCP Series page for SCP-{scp_id}. HTTP Status Code {e.code}. {e.read()}', file=sys.stderr)
        return 
  
  # Even more error handling.
  except Exception as e:
#     print(f'\nWARNING: Failed to access SCP Series page for SCP-{scp_id}. Request Error: {e}', file=sys.stderr)
    return

def parse_scp(soup: BeautifulSoup, scp_id: Union[str, int]) -> dict:
  """Parses the HTML content of a page on the SCP wiki. Internal function, shouldn't need to be called by a user."""
  # Just to get this out of the way...
  if soup is None:
    return None

  # Get rating.
  try:
    rating = soup.find('span', {'class': 'rate-points'}).contents[1].contents[0].replace('+', '')
  
  # Error handling.
  except AttributeError:
    # print(f'No rating found for SCP-{scp_id}!')
    rating = 0

  # Get page-content block.
  content = soup.find('div', id='page-content')
  # print(content)

  # Get main image (if it exists).
  try:
    main_image = content.find('div', {'class': 'scp-image-block'}).contents[0]['src']
  
  # Error handling.
  except AttributeError:
    # print(f'No main_image found for SCP-{scp_id}!')
    main_image = None
  
  # More error handling.
  except KeyError:
    # print(f'No main_image found for SCP-{scp_id}')
    main_image = None

  # Get image caption
  try:
    image_caption = content.find('div', {'class': 'scp-image-block'}).contents[2].contents[1].contents[0]
  
  # Error handling.
  except AttributeError:
    # print(f'No image_caption found for SCP-{scp_id}!')
    image_caption = None
  
  # Even more error handling.
  except KeyError:
    # print(f'No image_caption found for SCP-{scp_id}')
    image_caption = None

  # Get main content
  try:
    # Initial variable definitions.
    mapping = {}
    key = None
    # print(content.find_all('p'))

    # Find all the paragraph elements.
    for item in content.find_all('p'):
      # Grab the paragraph element's first child.
      first_child = item.next
      
      # Use bold portions as keys/identifiers for their sections.
      if first_child.name == 'strong':
        key = first_child.text.rstrip(': ')
        value = first_child.next_sibling.strip(': ')
      
      else:
        # Add subsequent paragraphs to the same section.
        if key is not None:
          value = f'{mapping[key]}\n{item.get_text(strip=True)}'
        
        # Don't if there's no section to add them to.
        else:
          value = None
      
      # Put that all into the value for the key.
      mapping[key] = value
    
    # Remove the sections that didn't have keys.
    try:
      mapping.pop(None)
    
    # Error handling.
    except:
      pass
  
  # Error handling.
  except AttributeError as e:
    # print(f'Can\'t parse content of SCP-{scp_id}! Error: {e}')
    mapping = None

  # Get page info.
  page_info = soup.find('div', id='page-info')
  revision = re.findall('\d+', page_info.next)[0]
  last_updated = page_info.find('span')['class'][1].replace('time_', '')

  # Get tags.
  tags_list = soup.find('div', {'class': 'page-tags'}).find('span')
  tags = [tag.string for tag in tags_list if tag.string != '\n']

  # Get link to the discussion page.
  discussion_link = 'http://www.scpwiki.com' + soup.find('a', id='discuss-button')['href']

  return {
    'id': scp_id,
    'rating': int(rating),
    'image': {
      'src': main_image,
      'caption': image_caption
    },
    'content': mapping,
    'revision': int(revision),
    'last_edited': int(last_updated),
    'tags': tags,
    'discussion': discussion_link
  }

def get_scp(scp_id: Union[str, int]) -> dict:
  """
  Returns a dictionary with as much content as possible regarding the SCP ID.

  Parameters:
    scp_id: ID of the SCP to grab info for. Should be either a string with leading zeroes (ex. 002) or an integer (ex. 2).
  """

  # Make the formatting nice for get_single_scp
  if int(scp_id) < 10:
    scp_id = f'00{scp_id}'
  
  elif int(scp_id) < 100:
    scp_id = f'0{scp_id}'
  
  # Get stuff we need from the page's HTML
  site_content = get_single_scp(str(scp_id))
  parsed_content = parse_scp(site_content, int(scp_id))

  # Get SCP's name and add it to parsed_content.
  if get_scp_name(int(scp_id)) is not None:
    if '[ACCESS DENIED]' not in get_scp_name(int(scp_id)):
      scp_name = get_scp_name(int(scp_id))
      parsed_content['name'] = scp_name
  
  # Don't add the name if there was an error preventing get_scp_name from grabbing it.
  else:
    pass
  
  return parsed_content

def get_scp_name(id: int) -> str:
  """
  Scrapes an SCP's name. Ignores uncreated SCPs. Returns the SCP's name as a string.
  
  Parameters:
    id: The SCP you want to retrieve's object ID.
  """
  try:
    # Redundant, but I can sleep easier since it has that extra layer of fallback.
    if _get_scp_name(id) is not None:
      if "[ACCESS DENIED]" not in _get_scp_name(id):
        return _get_scp_name(id)
  
  # Error handling
  except KeyError as e:
#     print(f"\nWARNING: Failed to scrape SCP-{id}! Error: {e}", file=sys.stderr)
    pass

def scrape_scps(min_skip: int=0, max_skip: int=6000, tags: list=[], ai_dataset: bool=False, copy_to_drive: bool=False) -> None:
  """
  Scrapes as much info on all SCPs from min_skip to max_skip - 1 as possible. Writes this info to different files based on its section.

  Output files:
    scp-descrips.txt, scp-conprocs.txt, scp-titles.txt, and scp-addenda.txt.

  Parameters:
    min_skip: The SCP number to start at. Default: 0
    max_skip: The SCP number to end at plus one. Default: 6000
    tags: The list of tags to grab from. Will ignore SCPs without these tags. An empty list (default) matches all tags.
    ai_dataset: Set to True if data is later going to be used to train an AI. Adds "<|endoftext|>" tokens where necessary to divide the dataset for training. Default: False
    copy_to_drive: Set to True to copy the output files to your Google Drive when done creating them. Requires having your Google Drive mounted (preferably with scpscraper.gdrive.mount()). Default: False
  """
  # Create/clear the files we need for scraping.
  filelist = []
  filelist.append(open('scp-descrips.txt', 'w'))
  filelist.append(open('scp-conprocs.txt', 'w'))
  filelist.append(open('scp-titles.txt', 'w'))
  filelist.append(open('scp-addenda.txt', 'w'))
  for i in range(len(filelist)):
    filelist[i].close()

  # print('Grabbing and writing skip info...\n', flush=True)

  # Initiate loop, create progress bar.
  for i in tqdm(range(min_skip, max_skip), "Fetching skips", total=max_skip, ncols=150, initial=min_skip, unit="skip", file=sys.stdout, bar_format='{desc}... {percentage:3.2f}% |{bar}|  [{remaining} remaining, {rate_fmt}]', smoothing=0.01875):
    # Nice number formatting.
    if i < 10:
      j = f'00{i}'
    elif i < 100:
      j = f'0{i}'
    else:
      j = i
    
    try:
      # Get all the things for the SCP.
      mylist = get_scp(i)
      
      # Tag match checking code
      match = False
      
      if tags:
        for tag in tags:
          if tag in mylist["tags"]:
            match = True
            break
      
      else:
        match = True
      
      # Get the list of keys in the dictionary (so we can search through it later).
      if match:
        keyslist = mylist["content"].keys()

        # Put stuff in a better format for the AI, if we're making a dataset for one
        if ai_dataset:
          for k in keyslist:
            mylist["content"][k] = mylist["content"][k].replace(j, 'XXXX')

        try:
          # Append current SCP's description to the description file.
          with open('scp-descrips.txt', 'a') as out:
            try:
              # Add <|endoftext|> token if it's a dataset for training AI.
              if ai_dataset:
                out.write('Description: {}\n<|endoftext|>'.format(mylist["content"]["Description"].replace(j, 'XXXX')))
              else:
                out.write(f'Description: {mylist["content"]["Description"]}\n')

              out.write('\n')

            # Error handling.
            except Exception as e:
              # print(f'Failed to grab the description of SCP-{j}! Please grab it yourself! Error: {e}')
              pass

          # Append current SCP's conprocs to the conproc file.
          with open('scp-conprocs.txt', 'a') as out:
            try:
              for k in keyslist:
                # Search keys for "Containment", output to conproc file if it matches.
                if "containment" in k.lower():
                  if ai_dataset:
                    out.write('Special Containment Procedures: {}\n<|endoftext|>\n'.format(mylist["content"][k].replace(j, 'XXXX')))
                  else:
                    out.write(f'Special Containment Procedures: {mylist["content"][k]}\n')

                  # Add <|endoftext|> token if it's a dataset for training AI.


                  out.write('\n')

            # Error handling.
            except:
              # print(f'Failed to grab the conprocs of SCP-{j}! It is probably not an article with a standard format! Please grab them yourself!')
              pass

          try:
            # Append current SCP's title to the title file (if we can grab it).
            with open('scp-titles.txt', 'a') as out:
              # Even more redundancy. I know. This is getting ridiculous.
              if mylist["name"] is not None:
                if "[ACCESS DENIED]" not in mylist["name"]:
                  if ai_dataset:
                    out.write(f'SCP-XXXX: {mylist["name"]}\n')
                  else:
                    out.write(f'SCP-{j}: {mylist["name"]}\n')

                # Handle nonexistent SCPs.
                else:
                  # print(f'SCP-{j} doesn\'t exist yet!')
                  pass

              else:
                # print(f'SCP-{j} doesn\'t exist yet!')
                pass

          # Error handling.
          except Exception as e:
            # raise e
            # print(f'Failed to grab the title of SCP-{j}! Please grab it yourself! Error: {e}')
            pass

          # Find and append addenda (if they exist) to the addenda file.
          with open('scp-addenda.txt', 'a') as out:
            try:
              # Define list or dictionary depending on whether or not we need the keys.
              if ai_dataset:
                addendalist = []
              else:
                addendalist = {}

              for k in keyslist:
                # Search keys for "Addendum", add to addendalist if it matches.
                if "addendum" in k.lower():
                  if ai_dataset:
                    addendalist.append(mylist["content"][k])

                  # Do the same thing for non-dataset, also adding the keys.
                  else:
                    addendalist.update({k: mylist["content"][k]})

              # Write addenda to addenda file.
              if ai_dataset:
                for k in addendalist:
                  buffer = k.strip(': ')
                  out.write('Addendum XXXX-XX: {}\n<|endoftext|>\n\n'.format(buffer.replace(j, 'XXXX')))

              # Do the same for non-dataset.
              else:
                for k in addendalist.keys():
                  buffer = f'{k}: {addendalist[k]}'
                  out.write(f'{buffer}\n\n')

            # Error handling.
            except Exception as e:
              # print(f'Failed to grab the addenda of SCP-{j}! Please grab them yourself (if they exist)! Error: {e}')
              pass

        # More error handling.
        except Exception as e:
          # print(f'Failed to write the info for SCP-{j}! Error: {e}')
          pass

    # Wow, just look at all that error handling!
    except Exception as e:
      # print(f'Failed to grab the info for {i}! Error: {e}')
      pass
    # print(mylist)

  filelist_names = [
                    'scp-descrips.txt',
                    'scp-conprocs.txt',
                    'scp-titles.txt',
                    'scp-addenda.txt',
  ]
  for skip_file in filelist_names:
    # Variable definitions.
    lines_seen = set()
    outfile = open(f'{skip_file}.tmp', "w")

    # Remove duplicate lines.
    for line in open(skip_file, 'r'):
      if line not in lines_seen:
        outfile.write(line)
        lines_seen.add(line)
    
    # Close original outfile connection.
    outfile.flush()
    outfile.close()

    # Write changes to original file and delete temporary file.
    with open(f'{skip_file}.tmp', "r") as infile:
      with open(skip_file, 'w') as outfile:
        outfile.write(infile.read())
    os.remove(f'{skip_file}.tmp')
    if copy_to_drive:
      gdrive.copy_to_drive(skip_file)
  # print("Done!")

def scrape_scps_html(min_skip: int=0, max_skip: int=6000, tags: list=[], ai_dataset: bool=False, copy_to_drive: bool=False) -> None:
  """
  Scrapes the html code of SCPs min_skip to max_skip - 1.
  
  Output files:
    scp-html.txt.

  Parameters:
    min_skip: The SCP number to start at. Default: 0
    max_skip: The SCP number to end at plus one. Default: 6000
    tags: The list of tags to grab from. Will ignore SCPs without these tags. An empty list (default) matches all tags.
    ai_dataset: Set to True if data is later going to be used to train an AI. Adds "<|endoftext|>" tokens where necessary to divide the dataset for training. Default: False
    copy_to_drive: Set to True to copy the output files to your Google Drive when done creating them. Requires having your Google Drive mounted (preferably with scpscraper.gdrive.mount()). Default: False
  """
  # Create/reset text file
  with open('scp_html.txt', "w"):
    pass
  
  # Define blank page contents.
  blank_page = '<div style="text-align: center;">\n<h1 id="toc0"><span>This page doesn\'t exist yet!</span></h1>\n</div>\n<hr>\n<div style="background-color: #600; border: solid 1px #600; border-radius: 20px; color: #fff; width: 450px; margin: 0 auto; font-size: 150%; text-align: center; box-shadow: 0 2px 6px rgba(0,0,0,.5), inset 0 1px rgba(255,255,255,.5), inset 0 10px rgba(255,204,204,.5), inset 0 10px 20px rgba(255,204,204,.3), inset 0 -15px 30px rgba(48,0,0,.5); line-height: 100%; padding: 0 10px;">\n<p><strong>Did you get feedback first?</strong></p>\n</div>\n<div style="background-color: #fff0f0; border: solid 1px #600; border-radius: 20px; color: #300; width: 450px; margin: 20px auto 0; text-align: center; box-shadow: 0 2px 6px rgba(0,0,0,.5); padding: 0 10px;">'
  
  for i in tqdm(range(min_skip, max_skip), "Fetching skips", total=max_skip, ncols=150, initial=min_skip, unit="skip", file=sys.stdout, bar_format='{desc}... {percentage:3.2f}% |{bar}|  [{remaining} remaining, {rate_fmt}]', smoothing=0.01875):
    with open('scp-html.txt', "a") as out:
      if i < 10:
        j = f'00{i}'
      elif i < 100:
        j = f'0{i}'
      else:
        j = i
      
      soup = get_single_scp(j)
      
      if soup is not None:
        # Get page tags
        tags_list = soup.find('div', {'class': 'page-tags'}).find('span')
        page_tags = [tag.string for tag in tags_list if tag.string != '\n']

        # Tag match checking code
        match = False

        if tags != []:
          for tag in tags:
            if tag in page_tags:
              match = True
              break
        
        else:
          match = True
        
        if match:
          content = soup.find('div', id='page-content')

          if blank_page not in content:
            if ai_dataset:
              out.write('{}\n\n<|endoftext|>\n\n\n'.format(str(content).replace(j, 'XXXX')))

            else:
              out.write(f'{content}\n\n')

          else:
            # print(f'\nThe page for SCP-{j} is blank!', file=sys.stderr)
            pass
  
  if copy_to_drive:
    gdrive.copy_to_drive('scp-html.txt')
