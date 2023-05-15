from menus.base import Menu, NavigationNode
from menus.menu_pool import menu_pool
from django.utils.translation import gettext_lazy as _

class DefaultMenu(Menu):

    def get_nodes(self, request):
        nodes = []
        n = NavigationNode(_('Inicio'), "/", 1)
        n2 = NavigationNode(_('Hallazgos'), "/hallazgos/", 2)
        n3 = NavigationNode(_('Noticias'), "/noticias/", 3)
        n4 = NavigationNode(_('Metodología'), "/metodologia/", 4)
        nodes.append(n)
        nodes.append(n2)
        nodes.append(n3)
        nodes.append(n4)
        return nodes

menu_pool.register_menu(DefaultMenu)
