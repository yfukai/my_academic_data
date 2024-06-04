{% for d in data -%}
{%- if "conference" in d.type -%}
{%- if d.international -%}
{{ d.names|join(", ") }}, {{ d.title }}, {{ d.conference.name }}, {{ d.conference.place[1] }}, {{ d.conference.place[2] }}, {{ d.conference.date.begin.strftime('(%b. %Y)') }} 
{% else -%}
{{ d.names|join(", ") }}, {{ d.title }}, {{ d.conference.name }}, {{ d.conference.place_ja[1] }}, {{ d.conference.date.begin.strftime('%Y年%-m月') }} 
{% endif -%}
{% endif -%}
{% endfor %}
