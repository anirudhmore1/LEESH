#!/usr/bin/env python
# coding: utf-8

# In[37]:


import requests
r = requests.get('http://127.0.0.1:8000/gpsdatas/')
r.text


# In[28]:

r = requests.patch('http://127.0.0.1:8000/gpsdatas/max_testing/', data = {'deviceid':'max_testing', 'taskid':'sar_put2','gpsdata':'{"stamp":4,"lat":-80,"log":38}'})
r.text

# In[38]:


r = requests.put('http://127.0.0.1:8000/gpsupdatedataapiview/max_testing/update', data = {'deviceid':'max_testing', 'taskid':'sar_put','gpsdata':'{"stamp":4,"lat":-80,"log":38}'})
r.text


# In[ ]:
