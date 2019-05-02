""" Author: Philipp Steinrötter (steinroe) """

import subprocess
import os
import time

def build_query(filters=None, orderby=None, asc=True, skip=None, top=None) -> str:
    """Builds query string
    
    Keyword Arguments:
        filters {list} -- The filters must be provided as a list of strings, e.q. ["name eq 'my-name'", "id eq '111'"]. (default: {None})
        orderby {str} -- The attribute to order by. (default: {None})
        asc {bool} -- Only considered if orderby is not none. Defines if the values should be ordered ascending or descending. (default: {True})
        skip {int} -- This parameter specifies the number of items in the queried collection which will be skipped and therefore included in the result set. (default: {None})
        top {int} -- This parameter restricts the maximum number of items which will be returned by the request. [description] (default: {None})
    
    Returns:
        str -- Query string
    """
    query_string='?'
    if filters is not None and len(filters) > 0:
        query_string += 'filter='
        for idx, filter_query in enumerate(filters):
            query_string += filter_query
            if idx < len(filters) - 1:
                query_string += ' and '
    if orderby is not None:
        if len(query_string) is not 1:
            query_string += '&'
        query_string += 'orderby=' + orderby
        if asc is True:
            query_string += ' asc'
        else:
            query_string += ' desc'
    if skip is not None:
        if len(query_string) is not 1:
            query_string += '&'
        query_string += 'skip=' + skip
    if top is not None:
        if len(query_string) is not 1:
            query_string += '&'
        query_string += 'top=' + top
    
    if query_string != '?':
        return query_string
    else:
        return None


def current_milli_time():
    return int(round(time.time() * 1000))
