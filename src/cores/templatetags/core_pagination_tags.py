from django import template

register = template.Library()

DOT = '...'


@register.simple_tag
def get_page_range(cl):
    """
    Generates the series of links to the pages in a paginated list.
    """
    paginator, page_num = cl.paginator, cl.page.number

    ON_EACH_SIDE = 3
    ON_ENDS = 2

    # If there are 10 or fewer pages, display links to every page.
    # Otherwise, do some fancy
    if paginator.num_pages <= 9:
        page_range = paginator.page_range
    else:
        # Insert "smart" pagination links, so that there are always ON_ENDS
        # links at either end of the list of pages, and there are always
        # ON_EACH_SIDE links at either end of the "current page" link.
        page_range = []

        if page_num > (ON_EACH_SIDE + ON_ENDS) + 1:
            page_range.extend(range(1, ON_EACH_SIDE))
            page_range.append(DOT)
            page_range.extend(range(page_num - ON_EACH_SIDE, page_num + 1))
        else:
            page_range.extend(range(1, page_num + 1))

        if page_num < (paginator.num_pages - ON_EACH_SIDE - ON_ENDS - 1) + 1:
            page_range.extend(range(page_num + 1, page_num + ON_EACH_SIDE + 1))
            page_range.append(DOT)
            page_range.extend(range(paginator.num_pages - ON_ENDS + 1, paginator.num_pages + 1))
        else:
            page_range.extend(range(page_num + 1, paginator.num_pages + 1))

    return page_range


@register.filter
def in_list(value, the_list):
    value = str(value)
    return value in the_list.split(',')
