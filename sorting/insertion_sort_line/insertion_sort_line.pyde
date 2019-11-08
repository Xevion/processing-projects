def setup():

def draw():
    if unsorted:
        get = unsorted.pop(0)
        for index, num in enumerate(sorted):
            if sorted[index] < sorted[index + 1] and sorted[index + 1] >= get:
                sorted.append(
