import gc

def show_memory():
    print("Free memory: {} bytes".format(gc.mem_free()))
    print('Allocated memory: {} bytes'.format(gc.mem_alloc()))    

x = [n for n in range(10000)]
y = [n for n in range(10000)]
show_memory()

gc.collect()
show_memory()

