import gc

print("Free memory: {} bytes".format(gc.mem_free()))
print('Allocated memory: {} bytes'.format(gc.mem_alloc()))

