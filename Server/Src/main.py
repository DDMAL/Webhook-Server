from flask import Flask, request
import requests
import datetime
import os

app = Flask(__name__)

slackbot_webhook = os.getenv('SLACKBOT_WEBHOOK')

@app.route("/dockerhub-webhook", methods=["POST"])
def hello_world():
    payload = request.json
    print ("Payload")
    print (payload)
    print (f"Headers: {request.headers}")
    compound_docker_tag = payload["push_data"]["tag"]
    repo_name = payload["repository"]["repo_name"]
    repo_url = payload["repository"]["repo_url"]
    timestamp = payload["push_data"]["pushed_at"]

    # Convert unix time to datetime
    datetime_obj = datetime.datetime.fromtimestamp(timestamp)
    formatted_datetime = datetime_obj.isoformat()

    # rodan-status-${SOURCE_BRANCH}-${DOCKER_TAG}
    build_repo_name, status, source_branch, docker_tag = compound_docker_tag.split("-")

    if status == "fail":
        status = f":red_circle: {status}"
    else:
        status = f":large_green_circle: {status}"

	# Post to slack bot
    post_url = slackbot_webhook
    header_text = f"A GitHub activity triggers Docker Hub's auto-build for https://hub.docker.com/r/ddmal/{build_repo_name}"
    if docker_tag == "this":
        docker_tag = "(A pull request)"
    post_json = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": header_text
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Repo Name:*\n{build_repo_name}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Docker Tag:*\n{docker_tag}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Timestamp:*\n{formatted_datetime}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Branch*:\n{source_branch}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Status*:\n{status}"
                    }
                ]
            }
        ]
    }
    requests.post(post_url, json=post_json)
    return "<p>Reach /webhook: Hello!</p>"

@app.route("/")
def mam():
    return "<p>Reach /: ROOT!</p>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
