from django import template
import women.views as views

register = template.Library()  #Необходим для создания тегов

@register.simple_tag(name='getcats')
def get_categories():
    return views.cats_db


@register.inclusion_tag('women/list_categories.html') #Тег будет передавать сформированную html страницу women/list_categories.html
def show_categories(cat_selected=0):
    cats = views.cats_db
    return {"cats": cats, 'cat_selected':cat_selected}