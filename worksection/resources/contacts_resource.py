from __future__ import annotations

from typing import Any, Dict, List

from worksection.resource import Resource
from worksection.models.contact import Contact
from worksection.models.contact_group import ContactGroup


class ContactsResource(Resource):
    def list(self) -> List[Contact]:
        return [Contact.from_dict(i) for i in self._call_action('get_contacts')]

    def create(self, email: str, name: str, params: Dict[str, Any] = {}) -> Contact:
        """Optional params: title, group, phone, phone2, phone3, phone4, address, address2"""
        return Contact.from_dict(self._call_action_one('add_contact', {'email': email, 'name': name, **params}))

    def groups(self) -> List[ContactGroup]:
        return [ContactGroup.from_dict(i) for i in self._call_action('get_contact_groups')]

    def create_group(self, title: str) -> ContactGroup:
        return ContactGroup.from_dict(self._call_action_one('add_contact_group', {'title': title}))