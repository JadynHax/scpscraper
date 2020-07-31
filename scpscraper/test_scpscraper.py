import pytest, scpscraper

def test_get_name():
  name_list = [None, 'classification [Blocked]', 'The "Living" Room', 'Biological Motherboard', 'The 12 Rusty Keys and the Door', 'Skeleton Key', 'Fountain of Youth', 'Abdominal Planet', 'Zombie Plague', 'Red Ice', 'Collars of Control', 'Sentient Civil War Memorial Statue', 'A Bad Composition', 'Blue Lady Cigarettes', 'The Concrete Man', 'Pipe Nightmare', 'Organism', 'Shadow Person', 'Super Ball', 'The Monster Pot', 'Unseen Mold', 'Skin Wyrm', 'The Morgue', 'Black Shuck', 'Game Show of Death', 'Worn Wardrobe', 'Afterschool Retention', 'The Vermin God', 'Knowledge', 'Daughter of Shadows', 'The Homunculus', 'What is Love?', "Brothers' Bride", 'The Missing Number', 'Obsidian Ritual Knife', 'Possessive Mask', 'The Reincarnation Pilgrimage of the Yazidi (Kiras Guhorîn)', 'Dwarf Star', 'The Everything Tree', 'Proboscis Engineers', "Evolution's Child", 'Broadcasting Patient', 'A Formerly Winged Horse', 'The Beatle', 'Fission Cannon', 'Atmospheric Converter', '"Predatory" Holly Bush', 'Microbial Mutagen', 'The Cursed SCP Number', 'Plague Doctor', 'To The Cleverest', 'Japanese Obstetrical Model', 'Traveling Train', 'Young Girl', 'Water Nymph', '[unknown]', 'A Beautiful Person', 'The Daily Grind', 'Heart of Darkness', 'Radioactive Mineral', 'Infernal Occult Skeleton', 'Auditory Mind Control', '"Quantum" Computer', '"The World\'s Best TothBrush"', 'Flawed von Neumann Structure', 'Destroyed Organic Catalyst', "Eric's Toy", "The Artist's Pen", 'The Wire Figure', 'Second Chance', 'Iron Wings', 'Degenerative Metamorphic Entity', 'The Foot of the Bed', '"Cain"', 'Quantum Woodlouse', 'Corrosive Snail', '"Able"', 'Rot Skull', 'Guilt', 'Old AI', 'Dark Form', 'Spontaneous Combustion Virus', '"Fernand" the Cannibal', 'An Abandoned Row Home', 'Static Tower', "drawn ''Cassy''", 'The Office of Dr. [REDACTED]', 'The Stairwell', 'The Lizard King', 'Tophet', "Apocorubik's Cube", 'Nostalgia', '"The Best of The 5th Dimension"', 'Red Sea Object', 'Miniature Event Horizon', 'Gun', 'The "Shy Guy"', 'Old Fairgrounds', 'Surgeon Crabs', 'The Portrait']
  
  for i in range(100):
    assert scpscraper.get_scp_name(i) == name_list[i], 'get_scp_name() is not working properly!'

def test_scrape_scps():
  scpscraper.scrape_scps(0, 50)
  
  filelist = [
                    'scp-descrips.txt',
                    'scp-conprocs.txt',
                    'scp-titles.txt',
  ]
  
  for test_file in filelist:
    with open(test_file, 'r') as in_text:
      assert in_text.read() != '', f'scrape_scps() is not working properly! {test_file} is empty!'

def test_scps_html():
  scpscraper.scrape_scps_html(0, 50)
  
  with open('scp-html.txt', 'r') as in_text:
    assert in_text.read() != '', f'scrape_scps() is not working properly! scp-html is empty!'
