You are an AI extracting intent.

Missions:
{% for mission in aikb.mission_catalog %}
- {{ mission.mission_name }}
{% endfor %}

User said: {{ user_input }}
Language: {{ language }}
