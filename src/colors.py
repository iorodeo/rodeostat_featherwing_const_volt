import collections

# Create color pallete
color_to_rgb = collections.OrderedDict([ 
    ('black'  , 0x000000), 
    ('white'  , 0xffffff), 
    ('red'    , 0xff0000),
    ('green'  , 0x00ff00),
    ('blue'   , 0x0000ff),
    ('gray'   , 0x999999),
    ('yellow' , 0xffff00),
    ('orange' , 0xffac1c),
    ])
color_to_index = {k:i for (i,k) in enumerate(color_to_rgb)}
num_color = len(color_to_rgb)
