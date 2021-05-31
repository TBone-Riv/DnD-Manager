from django import template

register = template.Library()


@register.filter(name='add_title')
def add_class(field, title):
    return field.as_widget(attrs={'placeholder': title})


@register.filter(name='add_class')
def add_title(field, class_attr):
    css_class = field.field.widget.attrs.get('class', '')
    css_class = f"{css_class} {class_attr}" if css_class else class_attr
    field.field.widget.attrs['class'] = css_class
    return field.as_widget(attrs={'class': css_class})
