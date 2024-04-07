{% extends "mail_templated/base.tpl" %}

{% block subject %}
Account activation
{% endblock %}
{% block html %}
<a href="http://127.0.0.1:8001/accounts/api/v1/activation/confirm/{{token}}">http://127.0.0.1:8001/accounts/api/v1/activation/confirm/{{token}}</a>
{% endblock %}