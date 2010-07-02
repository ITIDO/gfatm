#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

from django import forms
from releasemanager.models import *
import datetime

class JarjadForm(forms.ModelForm):
    jad_file_upload = forms.FileField()    
    jar_file_upload = forms.FileField()
    class Meta:
        model = Jarjad
        exclude = ('jar_file', 'jad_file','uploaded_by','is_release', 'version')
           
        
class BuildForm(forms.ModelForm):
    
    register_forms = forms.BooleanField(required=False, help_text="Do a best effort registration of forms on HQ")
        
    class Meta:
        model = Build
        exclude = ('domain', 'is_release', 'created_at', 'jar_file', 'jad_file', 'zip_file', 'description')


class ResourceSetForm(forms.ModelForm):
    # name = forms.SlugField()

    class Meta:
        model = ResourceSet
        exclude = ('domain', 'is_release', 'created_at')


