python
from humanizer import humanize, HumanizeRequest

request = HumanizeRequest(
    text="It is important to note that the system leverages cutting-edge technology.",
    naturalness_target=70
)

response = humanize(request)
print(response.revised_text)