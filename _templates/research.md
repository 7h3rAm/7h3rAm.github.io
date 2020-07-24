# 🔬 Research <a name="top"></a>
## 📜 Patents<a href="#top"> ↟ </a>
{% for patent in datadict.metadata.research.patents %}
{% if patent.url is not none %}

  * `{{ patent.date }}`: {{ patent.name }} ([{{ patent.id }}]({{ patent.url }}))

{% else %}

  * `{{ patent.date }}`: {{ patent.name }} (`{{ patent.id }}`)

{% endif %}
{% endfor %}

## 🎙️ Talks/Papers/Demos<a href="#top"> ↟ </a>
{% for talk in datadict.metadata.research.talks %}
### {{ talk.name }}
{{ talk.description }}<br/>
{% for conference in talk.conferences %}

  * `{{ conference.date }}`: [{{ conference.name }}]({{ conference.url }})

{% endfor %}
{% endfor %}

# 📰 Media<a href="#top"> ↟ </a>
{% for article in datadict.metadata.research.media %}

  * `{{ article.date }}`: {{ article.name }} ([{{ article.publication }}]({{ article.url }}))

{% endfor %}
