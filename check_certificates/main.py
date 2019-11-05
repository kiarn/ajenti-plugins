from jadi import component

from aj.auth import PermissionProvider
from aj.plugins.core.api.sidebar import SidebarItemProvider


@component(SidebarItemProvider)
class ItemProvider(SidebarItemProvider):
    def __init__(self, context):
        self.context = context

    def provide(self):
        return [
            {
                'attach': 'category:devicemanagement',
                'id': 'sync',
                'name': _('Check certificates'),
                'icon': 'fas fa-certificate',
                'url': '/view/lm/certificates',
                'children': [],
            }
        ]


@component(PermissionProvider)
class Permissions(PermissionProvider):
    def provide(self):
        return [
            {
                'id': 'lm:settings',
                'name': _('Check certificates'),
                'default': False,
            },
        ]
