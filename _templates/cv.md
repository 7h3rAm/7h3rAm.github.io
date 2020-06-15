CV
==
date: 15/Jun/2020
summary: curriculum vitae for Ankur Tyagi
tags: cv

# Ankur Tyagi
* {{ datadict.metadata.address.street_apt|md2html }}
* {{ datadict.metadata.address.city_state|md2html }}
* {{ datadict.metadata.phone|md2html }}
* {{ datadict.metadata.email|md2html }}
* {{ datadict.metadata.urls.linkedin|md2html }}
* {{ datadict.metadata.urls.twitter|md2html }}
* {{ datadict.metadata.urls.github|md2html }}
* {{ datadict.metadata.urls.blog|md2html }}


## 📋 Experience

## 🔬 Research
### 📜 Patents
{% for patent in datadict.metadata.research.patents %}
{% if patent.url is not none %}
* `{{ patent.date }}`: {{ patent.name }} (<a href="{{ patent.url }}" target="_blank">{{ patent.id }}</a>)
{% else %}
* `{{ patent.date }}`: {{ patent.name }} (<code>{{ patent.id }}</code>)
{% endif %}
{% endfor %}

## 🎙️ Talks/Papers/Demos
{% for talk in datadict.metadata.research.talks %}
### {{ talk.name }}
{{ talk.description }}  
{% for conference in talk.conferences %}
* `{{ conference.date }}`: <a href="{{ conference.url }}" target="_blank">{{ conference.name }}</a>
{% endfor %}
{% endfor %}

## 📰 Media
{% for article in datadict.metadata.research.media %}
* `{{ article.date }}`: {{ article.name }} (<a href="{{ article.url }}" target="_blank">{{ article.publication }}</a>)
{% endfor %}

## 📈 Academics
### 📈 University
### 📈 Certifications
