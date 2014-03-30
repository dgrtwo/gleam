import ast

from wtforms.fields import Field


def slider_widget(field, ul_class='', **kwargs):
    """widget for rendering a SliderField"""
    # THE BELOW IS JUST AN EXAMPLE, NOTHING TO DO WITH SLIDER
    kwargs.setdefault('type', 'checkbox')
    field_id = kwargs.pop('id', field.id)
    html = [u'<ul %s>' % html_params(id=field_id, class_=ul_class)]
    for value, label, checked in field.iter_choices():
        choice_id = u'%s-%s' % (field_id, value)
        options = dict(kwargs, name=field.name, value=value, id=choice_id)
        if checked:
            options['checked'] = 'checked'
        html.append(u'<li><input %s /> ' % html_options(**options))
        html.append(u'<label %s>%s</label></li>')
    html.append(u'</ul>')
    return u''.join(html)


class SliderField(Field):
    widget = slider_widget

    def __init__(self, id, min, max, value):
        self.id = id
        self.min = min
        self.max = max
        self.value = value

    def _value(self):
        return self.data

    def process_formdata(self, input):
        self.data = ast.literal_eval(input[0])
