from django import template
import women.views as views
from women.models import Category, TagPost

register = template.Library()  #Необходим для создания тегов

#@register.simple_tag(name='getcats')       Это все использовалось когда мы взаимодействовали с catd_db во вкладке views, но потом сделали свою DB посредством ORM
#def get_categories():
#    return views.cats_db


@register.inclusion_tag('women/list_categories.html') #Тег будет передавать сформированную html страницу women/list_categories.html
def show_categories(cat_selected=0):
    cats = Category.objects.all()
    return {"cats": cats, 'cat_selected':cat_selected}

@register.inclusion_tag('women/list_tags.html') #Тег будет передавать сформированную html страницу women/list_categories.html
def show_all_tags():
    return {"tags": TagPost.objects.all()}