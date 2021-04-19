# -*- coding: utf-8 -*-
from plone import api
from plone.restapi.interfaces import IExpandableElement
from plone.restapi.services import Service
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


@implementer(IExpandableElement)
@adapter(Interface, Interface)
class RegisterItem(object):

    def __init__(self, context, request):
        self.context = context.aq_explicit
        self.request = request

    def __call__(self, expand=False):
        result = {
            'register_item': {
                '@id': '{}/@register_item'.format(
                    self.context.absolute_url(),
                ),
            },
        }
        if not expand:
            return result

        # === Your custom code comes here ===

        # Example:
        try:
            subjects = self.context.Subject()
        except Exception as e:
            print(e)
            subjects = []
        query = {}
        query['portal_type'] = "Document"
        query['Subject'] = {
            'query': subjects,
            'operator': 'or',
        }
        brains = api.content.find(**query)
        items = []
        for brain in brains:
            # obj = brain.getObject()
            # parent = obj.aq_inner.aq_parent
            items.append({
                'title': brain.Title,
                'description': brain.Description,
                '@id': brain.getURL(),
            })
        result['register_item']['items'] = items
        return result


class RegisterItemGet(Service):

    def reply(self):
        service_factory = RegisterItem(self.context, self.request)
        return service_factory(expand=True)['register_item']