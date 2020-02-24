#!/usr/bin/env python
# coding: utf-8

# In[23]:

import sys
def main():
    count=int(sys.argv[1])
    for i in range(count):
       files.append(sys.argv[2+i])
    destfile=files[-1]
    files.pop()
    contents=['@256\n','D=A\n','@ARG\n','M=D\n','@261\n','D=A\n','@SP\n','M=D\n']
    for file in files:
        with open(file) as myfile:
        	contents+=myfile.readlines()   
    with open(destfile,mode='w') as myfile:
    	destfile.write(' '.join(contents))

if __name__ == "__main__":
    main()

# In[ ]:




