
# SCP Scraper
A small Python library designed for scraping data from the SCP wiki. Made with AI training (namely NLP models) and dataset collection (for things like categorization of SCPs for external projects) in mind, and has arguments to allow for ease of use in those applications.

Below you will find installation instructions, examples of how to use this library, and the ways in which you can utilize it. I hope you find this as useful as I have!

## Sample Code

### Installation
`scpscraper` can be installed via `pip install`. Here's the command I recommend using, so you consistently have the latest version.
```
pip3 install --upgrade scpscraper
```

### The Basics
#### Importing the Library
```py
# Before we begin, we obviously have to import scpscraper.
import scpscraper
```

#### Grabbing an SCP's Name
```py
# Let's use 3001 (Red Reality) as an example.
name = scpscraper.get_scp_name(3001)

print(name) # Outputs "Red Reality"
```

#### Grabbing as many details as possible about an SCP
```py
# Again using 3001 as an example
info = scpscraper.get_scp(3001)

print(info) # Outputs a dictionary with the
# name, object id, rating, page content by section, etc.
```

### The Fun Stuff
#### Grabbing an SCP's `page-content` div HTML
For reference, the `page-content` div contains what the user actually wrote, without all the extra Wikidot external stuff.
```py
# Once again, 3001 is the example
scp = scpscraper.get_single_scp(3001)

# Grab the page-content div specifically
content = scp.find_all('div', id='page-content')

print(content) # Outputs "<div id="page-content"> ... </div>"
```

#### Scraping HTML or information from *multiple* SCPs
```py
# Grab info on SCPs 000-099
scpscraper.scrape_scps(0, 100)

# Same as above, but only grabbing Keter-class SCPs
scpscraper.scrape_scps(0, 100, tags=['keter'])

# Grab 000-099 in a format that can be used to train AI
scpscraper.scrape_scps(0, 100, ai_dataset=True)

# Grab 000-099 and copy them to your Google Drive afterwards
# NOTE: this can only be used when running on Google Colaboratory
scpscraper.scrape_scps(0, 100, copy_to_drive=True)
```
```py
# Scrape the page-content div's HTML from SCP-000 to SCP-099
# Only including this as the example, but scrape_scps_
scpscraper.scrape_scps_html(0, 100)
```

## Planned Updates
Potential updates in the future to make scraping data from any website easy/viable, allowing for easy mass collection of data.

## Link to GitHub Repo
https://github.com/JaonHax/scpscraper/
<!--stackedit_data:
eyJoaXN0b3J5IjpbLTExODA0NjQ3MTYsODY3NDgzODM5XX0=
-->