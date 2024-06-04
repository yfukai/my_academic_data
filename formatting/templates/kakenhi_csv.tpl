{% for d in data -%}
{%- if "conference" in d.type -%}
{{ d.names|join("、") }}, {{ d.title }}, {{ d.conference.name }}, {{ d.conference.date.begin.strftime('%Y') }}, {{ d.conference.date.end.strftime('%Y') }}, {{ 1 if d.invited else 0 }}, {{ 1 if d.international else 0 }} 
{% endif -%}
{% endfor %}
