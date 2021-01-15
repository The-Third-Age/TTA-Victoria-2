# from PIL import Image
#
# terrain_colors = set()
# counts_lotr = {}
# dir = "../../../../Program Files (x86)/Steam/steamapps/common/Victoria 2/mod/LOTR/map/terrain.bmp"
# terrain = Image.open(dir)
# im = terrain.load()
# for row in range(5616):
#     for col in range(2160):
#         pixel = im[row, col]
#         if pixel in counts_lotr:
#             counts_lotr[pixel] = counts_lotr[pixel] + 1
#         else:
#             counts_lotr[pixel] = 1
#         terrain_colors.add(pixel)
# list_terrain_colors = list(terrain_colors)
# list_terrain_colors.sort()
# print(list_terrain_colors)
# print(counts_lotr)