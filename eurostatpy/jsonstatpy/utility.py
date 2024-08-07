def lst2html(lst):
    html = "<table>"
    for r in lst:
        html += "<tr>"
        for c in r:
            html += "<td>{}</td>".format(c)
        html += "</tr>"
    html += "</table>"
    return html
