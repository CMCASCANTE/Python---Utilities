from django import forms
from django.core.exceptions import ValidationError


##############################################
# Formulario para la función de buscador DNS #
##############################################
class DNSForm(forms.Form):
    # Input
    domainValue = forms.CharField(label="", max_length=200, required=False, initial=None, widget=forms.TextInput(attrs={'placeholder': 'Introduce un dominio'}))

    # Select    
    TYPE_CHOICES =( 
        ("ALL", "ALL"), 
        ("NS", "NS"), 
        ("A", "A"), 
        ("AAAA", "AAAA"),
        ("TXT", "TXT"),
        ("SPF", "SPF"),
        ("MX", "MX"),                
        ("CNAME", "CNAME"),        
        ("SRV", "SRV"),
        ("CAA", "CAA"),
        ("SOA", "SOA")
    ) 
    selectDNS = forms.ChoiceField(label="", choices = TYPE_CHOICES, initial = "A")  

    # Select    
    NAMESERVER_CHOICES =(          
        ("8.8.8.8", "Google"),
        ("1.0.0.1", "Cloudflare"),
         ("208.67.222.222", "OpenDNS"),
          ("9.9.9.9", "Quad9")    
    ) 
    nameServer = forms.ChoiceField(label="", choices = NAMESERVER_CHOICES, initial = "8.8.8.8")  

    # Añadimos un valor al atributo clase para darle CSS
    nameServer.widget.attrs['class'] = "nameServerInput"

######################################################
# Formulario para la función de Testeador de Puertos #
######################################################
class PortForm(forms.Form):
    # Input
    ipValue = forms.GenericIPAddressField(label="", protocol="IPv4", max_length=15, required=False, initial=None, widget=forms.TextInput(attrs={'placeholder': 'IP'}))
    portValue = forms.CharField(label="", initial=None, max_length=5, required=False, widget=forms.TextInput(attrs={'placeholder': 'Puerto', 'class': 'number'}))
    #portValue = forms.DecimalField(label="", min_value=1, max_value=65535, decimal_places=0, initial=None, widget=forms.NumberInput(attrs={'placeholder': 'Puerto'}))

#################################################
# Formularios para la función de Peticiones API #
#################################################
class ApiForm(forms.Form):
    # Input
    urlValue = forms.CharField(label="", max_length=2000, required=False, initial=None, widget=forms.TextInput(attrs={'placeholder': 'API Endpoint', 'autocomplete': "off"}))
    
    # Select    
    TYPE_CHOICES =( 
        ("GET", "GET"), 
        ("POST", "POST")        
    ) 
    apiRequestType = forms.ChoiceField(label="", choices = TYPE_CHOICES, initial = "GET", widget=forms.Select(attrs={'disabled': ''}))  

class ApiFormAuth(forms.Form):
    # Select    
    TYPE_CHOICES =( 
        ("None", "None"), 
        ("Basic", "Basic"), 
        ("Token", "Token")        
    ) 
    apiAuthType = forms.ChoiceField(label="Auth Type", choices = TYPE_CHOICES, initial = "", widget=forms.Select(attrs={'onchange':'authHidden(this)'}))  

class ApiFormAuthBasic(forms.Form):
    # Auth
    basicUser = forms.CharField(label="", max_length=200, required=False, initial=None, widget=forms.TextInput(attrs={'placeholder': 'User', 'autocomplete': "off"}))
    basicPass = forms.CharField(label="", max_length=200, required=False, initial=None, widget=forms.PasswordInput(attrs={'placeholder': 'Pass', 'autocomplete': "off"}))
    
class ApiFormAuthToken(forms.Form):
    # Auth
    tokenKey = forms.CharField(label="", max_length=200, required=False, initial=None, widget=forms.TextInput(attrs={'placeholder': 'Key', 'autocomplete': "off"}))
    tokenValue = forms.CharField(label="", max_length=20000, required=False, initial=None, widget=forms.TextInput(attrs={'placeholder': 'Token', 'autocomplete': "off"}))