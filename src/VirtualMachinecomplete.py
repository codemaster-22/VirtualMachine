#!/usr/bin/env python
# coding: utf-8

# In[1]:
import sys
def memory(i):
    a=[]
    if i[1]=='pointer':
        a.append('@3')
        a.append('D=A')
    elif i[1]=='temp':
        a.append('@5')
        a.append('D=A')
    else:
        if i[1]=='argument':
            a.append('@ARG')
        elif i[1]=='local':
            a.append('@LCL')
        elif i[1]=='this':
            a.append('@THIS')
        elif i[1]=='that':
            a.append('@THAT') 
        a.append('D=M')
    a.append('@'+i[2])
    if i[1]=='static':
        a=['@'+z+'.'+i[2]]
    return a    


# In[7]:


def pushfunc(i):
    a=[]
    if(i[1]=='constant'):
        a.append('@'+i[2])
        a.append('D=A')
    else:
        a=memory(i)
        if(i[1]!='static'):
            a.append('A=A+D')
        a.append('D=M')
    a.append('@SP')
    a.append('A=M')
    a.append('M=D')
    a.append('@SP')
    a.append('M=M+1')
    return a


# In[8]:


def popfunc(i):
    a=memory(i)
    if(i[1]!='static'):
        a.append('D=A+D')
    else:
        a.append('D=A')
    a.append('@R13')
    a.append('M=D')
    a.append('@SP')
    a.append('AM=M-1')
    a.append('D=M')
    a.append('@R13')
    a.append('A=M')
    a.append('M=D')
    return a


# In[9]:


def popfunc2():
    a=[]
    a.append('@SP')
    a.append('AM=M-1')
    a.append('D=M')
    return a
def pushfunc2(n):
    a=[]
    if(n!=0):
        a.append('D=M')
    a.append('@SP')
    a.append('AM=M+1')
    a.append('A=A-1')
    a.append('M=D')
    return a


# In[10]:


def arthimetic(i):
    a=[]
    a.append('@SP')
    a.append('AM=M-1')
    a.append('D=M')
    a.append('A=A-1')
    return a


# In[11]:


def functioncall(i):
    a=[]
    a.append('@SP')
    a.append('D=M')
    a.append('@LCL')
    a.append('M=D')
    a.append('@'+i[2])
    a.append('D=A')
    a.append('('+i[1]+'.loop)')
    a.append('@'+i[1]+'.end')
    a.append('D;JEQ')
    a.append('@SP')
    a.append('AM=M+1')
    a.append('A=A-1')
    a.append('M=0')
    a.append('D=D-1')
    a.append('@'+i[1]+'.loop')
    a.append('0;JMP')
    a.append('('+i[1]+'.end)')
    return a


# In[12]:


def returnr14():
    a=[]
    a+=['@R14','AM=M-1','D=M']
    return a


# In[13]:


def call(i):
    a=[]
    global x
    a+=['@'+i[1]+'_'+str(x),'D=A']
    a+=pushfunc2(0)
    a.append('@LCL')
    a+=pushfunc2(1)
    a.append('@ARG')
    a+=pushfunc2(1)
    a.append('@THIS')
    a+=pushfunc2(1)
    a.append('@THAT')
    a+=pushfunc2(1)
    a+=['@SP','D=M','@5','D=D-A','@'+i[2],'D=D-A','@ARG','M=D','@'+i[1],'0;JMP','('+i[1]+'_'+str(x)+')']
    x+=1
    return a 


# In[14]:


def returncall(i):
    a=[]
    a+=['@LCL','D=M','@R14','M=D','@5','D=D-A','A=D','D=M','@R13','M=D']
    a+=popfunc2()
    a+=['@ARG','A=M','M=D','D=A+1','@SP','M=D']
    a+=returnr14()
    a+=['@THAT','M=D']
    a+=returnr14()
    a+=['@THIS','M=D']
    a+=returnr14()
    a+=['@ARG','M=D']
    a+=returnr14()
    a+=['@LCL','M=D','@R13','A=M','0;JMP']
    return a


# In[15]:
def main():
	count =int(sys.argv[1])
	files=[]
	for i in range(count):
        files.append(sys.argv[2+i])
    for file in files:
	    with open(file) as myfile:
	      contents=myfile.readlines()
        file=file[:-3]
	    z=file[::-1]
        i=z.find('/')
        z=z[:i]
        z=z[::-1]
		x=0
		for i in range(len(contents)):
		    s="//"
		    if s in contents[i]:
		        j=contents[i].find(s)
		        contents[i]=contents[i][:j]
		    if '\n' in contents[i]:
		        j=contents[i].find('\n')
		        contents[i]=contents[i][:j]
		    contents[i]=contents[i].split()
	    while [] in contents:
	      contents.remove([])
		final=[]
		for i in contents:
		    if('push'== i[0]):
		        final+=pushfunc(i)
		        continue
		    if('pop'==i[0]):
		        final+=popfunc(i)
		        continue
		    if('label'==i[0]):
		        final+=['('+i[1]+')']
		        continue
		    if('goto'==i[0]):
		        final+=['@'+i[1],'0;JMP']
		        continue
		    if('if-goto'==i[0]):
		        final+=popfunc2()
		        final+=['@'+i[1],'D;JNE']
		        continue
		    if('function'==i[0]):
		        final+=['('+i[1]+')']
		        final+=functioncall(i)
		        continue
		    if('call'==i[0]):
		        final+=call(i)
		        continue
		    if('return'==i[0]):
		        final+=returncall(i)
		        continue
		    else:
		        if('not'==i[0]):
		            final+=['@SP','A=M-1','M=!M']
		            continue
		        elif('neg'==i[0]):
		            final+=['@SP','A=M-1','M=-M']
		            continue
		        final+=arthimetic(i)
		        if('add'==i[0]):
		            final+=['M=M+D']
		        elif('sub'==i[0]):
		            final+=['M=M-D']
		        elif('and'==i[0]):
		            final+=['M=M&D']
		        elif('or'==i[0]):
		            final+=['M=M|D']
		        else:
		            a=['D=M-D','M=-1']
		            global x
		            a.append('@label_'+str(x))
		            if('gt'==i[0]):
		                a.append('D;JGT')
		            elif('lt'==i[0]):
		                a.append('D;JLT')
		            else:
		                a.append('D;JEQ')
		            a.append('@SP')
		            a.append('A=M-1')
		            a.append('M=0')
		            a.append('('+'label_'+str(x)+')')
		            x+=1
		            final+=a
        with open(file+'.asm',mode='w') as myfile:
              myfile.write('\n'.join(final)+'\n')

# In[16]:
if __name__ == "__main__":
    main()


