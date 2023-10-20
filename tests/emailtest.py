import requests


def send_simple_message(htm):
    return requests.post(
        "https://api.eu.mailgun.net/v3/ameasere.com/messages",
        auth=("api", "<key>"),
        data={"from": "Polaris <noreply@ameasere.com>",
              "to": ["leigh@ameasere.com"],
              "subject": "Hello",
              "html": htm})


with open('emailtest_assets/index.html', 'r') as f:
    html = f.read()

# Replace all sections in this HTML with the correct values
html = html.replace('{{first_line}}', 'This is a test email.')
html = html.replace('{{second_line}}', 'You don\'t need to do anything!')
html = html.replace('{{button_text}}', 'Our Website')
html = html.replace('{{button_href}}', 'https://ameasere.com/polaris-fd5354')
print(send_simple_message(html).text)
