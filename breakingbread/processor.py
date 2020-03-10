# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 00:22:01 2020

@author: anjali
"""

from breakingbread.models import *

def cuisine_list(request):
    cuisine_list=[];
    #retrieving the cuisine list
    cuisines = Cuisine.objects.all();
    for cuisine in cuisines:
        cuisine_list.append(cuisine[0])
    return {"cuisine":cuisine_list}