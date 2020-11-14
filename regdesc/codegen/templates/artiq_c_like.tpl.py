from artiq.language.core import portable
from artiq.language.types import TInt32
from numpy import int32

{% for reg in registers %}
{% for field in reg.fields %}
@portable
def {{ device|upper }}_{{ reg.name|upper }}_{{ field.name|upper }}_GET(reg: TInt32) -> TInt32:
    return int32((reg >> {{ field.shift }}) & {{ "0x{:X}".format(field.mask) }})

@portable
def {{ device|upper }}_{{ reg.name|upper }}_{{ field.name|upper }}(x: TInt32) -> TInt32:
    return int32((x & {{ "0x{:X}".format(field.mask) }}) << {{ field.shift }})

@portable
def {{ device|upper }}_{{ reg.name|upper }}_{{ field.name|upper }}_UPDATE(reg: TInt32, x: TInt32) -> TInt32:
    return int32((reg & ~({{ "0x{:X}".format(field.mask) }} << {{ field.shift }})) | ((x & {{ "0x{:X}".format(field.mask) }}) << {{ field.shift }}))
{% endfor %}
{% endfor %}
