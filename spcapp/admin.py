from django.contrib import admin
from .models import Clients
from .models import Dict
from .models import Works
from .models import Month

# при такой регистрации моделей, в списке объектов модели отображается только то, что описано в модели 
# в функции __str__
admin.site.register(Clients)
admin.site.register(Dict)
admin.site.register(Works)
admin.site.register(Month)

