from utilities import *

def flood(color_of_tile, flooded_list, screen_size):

    def search(tile):
        if color_of_tile[tile]==color_of_tile[flooded_list[0]]:
            if tile in flooded_list:
                pass
            else:
                 flooded_set.add(tile)
                 flooded_list.append(tile)

    for tile in flooded_list:
        if in_bounds(up(tile), screen_size):
            search(up(tile))
        if in_bounds(down(tile), screen_size):
            search(down(tile))
        if in_bounds(left(tile), screen_size):
            search(left(tile))
        if in_bounds(right(tile), screen_size):
            search(right(tile))
    
