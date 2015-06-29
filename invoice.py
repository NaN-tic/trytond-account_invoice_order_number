# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta
from trytond.pyson import Eval

__all__ = ['Invoice', 'Party']
__metaclass__ = PoolMeta


class Invoice:
    __name__ = 'account.invoice'

    number_order = fields.Char('Order Number', states={
            'readonly': Eval('state') != 'draft',
            'required': (Eval('state').in(['posted', 'paid']) &
                Eval('requires_order_number')),
            },
        depends=['state', 'requires_order_number'])
    requires_order_number = fields.Function(fields.Boolean(
            'Requires Order Number'),
        'get_requires_order_number', searcher='search_requires_order_number')

    def get_requires_order_number(self, name):
        return self.party.requires_order_number

    @classmethod
    def search_requires_order_number(cls, name, clause):
        return [('party.requires_order_number',) + tuple(clause[1:])]


class Party:
    __name__ = 'party.party'

    requires_order_number = fields.Boolean('Requires order number')
