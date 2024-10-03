from django import forms
from django.core.exceptions import ValidationError


class DNSForm(forms.Form):
    # Input
    domainValue = forms.CharField(label="", max_length=200, initial=None, widget=forms.TextInput(attrs={'placeholder': 'Introduce un dominio'}))

    # Select    
    TYPE_CHOICES =( 
        ("NS", "NS"), 
        ("A", "A"), 
        ("AAAA", "AAAA"),
        ("TXT", "TXT"),
        ("SPF", "SPF"),
        ("MX", "MX"),        
        ("CAA", "CAA"),
        ("CNAME", "CNAME"),        
        ("SRV", "SRV"),
        ("CAA", "CAA"),
        ("SOA", "SOA")
    ) 
    selectDNS = forms.ChoiceField(label="", choices = TYPE_CHOICES, initial = "A")  