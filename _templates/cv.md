# Ankur Tyagi

```{{ datadict.metadata.cv.contact|md2html }}```
<br/><br/>

## Introduction
{{ datadict.metadata.cv.intro }}<br/>

{% for domain in datadict.metadata.cv.domains %}

* {{ domain }}

{% endfor %}

## Specialties
{% for specialty in datadict.metadata.cv.specialties %}

* {{ specialty }}

{% endfor %}

## Experience</h2>
{% for job in datadict.metadata.jobs %}
### {{ job.title }} @ {{ job.employer }}
`{{ job.years }} ({{ job.duration }})`
<br/><br/>
{% for desc in job.description %}
{% if desc and desc != "" %}

  * {{ desc }}

{% endif %}
{% endfor %}
{% endfor %}

## Research</h2>
### Patents
{% for patent in datadict.metadata.research.patents %}
{% if patent.url is not none %}

* `{{ patent.date }}`: {{ patent.name }} ([{{ patent.id }}]({{ patent.url }}))

{% else %}

* `{{ patent.date }}`: {{ patent.name }} (`{{ patent.id }}`)

{% endif %}
{% endfor %}

### Talks/Papers/Demos
{% for talk in datadict.metadata.research.talks %}
{{ loop.index }}. {{ talk.name }}
<br/>
{% for conference in talk.conferences %}

* `{{ conference.date }}`: [{{ conference.name }}]({{ conference.url }})

{% endfor %}
{% endfor %}

### Media
{% for article in datadict.metadata.research.media %}

* `{{ article.date }}`: {{ article.name }} ([{{ article.publication }}]({{ article.url }}))

{% endfor %}

## Academics</h2>
### University
{% for acad in datadict.metadata.academics %}

* `{{ acad.date }}`: {{ acad.course }} @ {{ acad.institute }}

{% endfor %}

### Certifications
{% for cert in datadict.metadata.certifications %}

* `{{ cert.date }}`: {{ cert.name }} @ {{ cert.institute }} (`ID: {{ cert.id }}`)

{% endfor %}
