# flango!

Do you like the niceties of Flask, but have to use Django for some reason? Are you a lunatic?

If you answered yes twice, this library is for you!


# Quickstart

Install package.

```bash
pip install flango
```

Create Flango app, add it to your urls.

```python
# urls.py
from flango import Flango

app = Flango(__name__)

@app.route('/<int:pk>')
def index(pk):
    from django.contrib.auth.models import User
    return User.objects.get(pk=pk).first_name

urlpatterns = app.urlpatterns
```


# Benefits

- Access current request anywhere
 
    ```python
    from django import forms
    from flango import request
 
    class MyForm(forms.Form):
       def save(self):
           instance = super(MyForm, self).save(commit=False)
           instance.user = request.user
           instance.save()
           return instance
    ```


- Declare your routes alongside your views
 
    ```python
    from flango import render_template
    from myapp import app
 
    @app.route('/about')
    def about():
       return render_template('about.html')
    ```


- Typed variable parts
 
    ```python
    from flango import render_template
    from myapp import app
 
    @app.route('/map/<float:lat>/<float:long>')
    def map(lat, long):
       assert isinstance(lat, float)
       assert isinstance(long, float)
       return render_template('map.html', lat=lat, long=long)
    ```


- Return response content, status code, and headers directly from views
 
    ```python
    from myapp import app
 
    @app.route('/ok')
    def ok():
       return 'ok'
 
    @app.route('/idk')
    def idk():
       return 'idk', 404
 
    @app.route('/wat')
    def wat():
       return 'wat', 400, {'Content-Type': 'text/wat'}
    ```


- Save precious PEP-8 space when building URLs
 
    ```python
    from django.db import models
    from flango import url_for
    
    class MyModel(models.Model):
       def get_invitation_link(self, friend_name):
           return url_for('my-model-invite', id=self.id, friend_name=friend_name)
    ```


# Using `flango.request` with regular Django views

Flango wraps your view functions in order to provide the `request` object elsewhere. This means that when a your code which accesses `flango.request` is called from a regular Django view, it will fail.

To fix this, add Flango's `global_request_middleware` to your `settings.MIDDLEWARE`:
```python
# settings.py
MIDDLEWARE = (
    'flango.global_request_middleware',
    # ...
)
```

For best results, place it first in the list. This will allow you to use `flango.request` even in other middlewares.
