# CHECK24 GenDev Messenger Challenge
Welcome to my submission for the 4th round of the GenDev Scholarship! 🚀 I'm excited to present my implementation of the CHECK24 Messenger Challenge, building a seamless chat experience for service providers and customers.

## Overview
This messenger application allows users to communicate seamlessly after a service provider sends a quote. The challenge involves creating both the backend and frontend components, providing a robust and enjoyable user experience.

## Stack
Backend: Pythons FastAPI with PostgresDB for data persistence.
Frontend: React.js (Vite) for a responsive and dynamic UI.

## This are the minimal functional requirements I have implemented:
✅ Chat view: the same conversation should be viewable from both perspectives: customer and service provider (they should each have their own site/route, so that hypothetically a service provider on one device is able to chat with the customer on the other device)

✅ Overview over all chats: think about implementing simple(!) chat overviews for both perspectives to click into chats, too.

✅ Persistance: chats are mutable, so they should be persisted in a database/store of your choice and accessible via an unique identifier

✅ Scrolling pagination: the customer/service provider should be able to scroll through a chat (and its history) with a hypothetical length of 10000s of messages per chat (think about Pagination)

✅ Image and PDF attachments: The customer/service provider should be able to send messages with optional attachments like pictures or documents (PDF)

✅ Masking of sensible information: Any contactable data (phone, email, URL) within all messages should be masked as long as the conversation status is "quoted"

✅ Show sent message in chat without refreshing: Messages should appear within the chat as they were sent (without refreshing the page)

✅ Hide message field if rejected state: If a conversation status is "rejected" the message input field should disappear and actions should not be possible any longer

✅ Request customer reviews: Within the chat the service provider should be able to request a review from the customer once they've worked together (feature explicitly explained within our provided datasets)

✅ A quick screencast 🎥 of your final working app within your GitHub repository (+ optional a link to a live version to check out or an explanation how to start your app on our machines, see "How do I hand in my project?")

## The other ideas:
✅ Unread banner behaviour (highly appreciated)

✅ An extendable/generic message API format (consider whether your API design is also suitable for new product requirements e.g. new message types)

✅ Thumbnail processing (to improve UX)

✅ Live-Updates (Socket/Polling/...) - (in my case SSE)

❌ Start the conversation at the scroll offset of the first unread message

✅ Dockerize your system so that anyone can run it on their machine

✅ OpenAPI for backend <-> frontend communication (+ code generation)

## Other implemented ideas:
✅ OAuth2-Integration

📚 Message Reactions

📚 User Search with Keywords from all users

✅ Paginated Chat view

(📚) On Database Level: Support for Thread Messages

### Explanation
✅ Implemented in Client and Server

📚 Only implemented in Server

❌ Not implemented

## How to Run Locally

### Via docker-compose
You can run the application via docker-compose. 
Therefore, you need access to the docker image of the server and client on ghcr.io.
```
docker login ghcr.io
```
Navigate to the project directory and export the following environment variables:
```
export POSTGRES_PASSWORD=...
export SECRET_KEY=...
export TOKEN_EXPIRE_MINUTES
```
After that you can run:
```
docker-compose up
```

### For development
Clone the repository.
Navigate to the project directory.

#### For the server

❗️ Do this first if you do not have generated the client

Navigate to '/server' and export/put the following env variable in an .env file:
```
DATABASE_HOSTNAME=localhost
DATABASE_PORT=5432
DATABASE_PASSWORD=...
DATABASE_NAME=gendev_db
DATABASE_USERNAME=postgres
SECRET_KEY=...
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1000
```
If you have no running db you could also export the following env variable:
```
export SKIP_DB_CONNECTION=True
```
Afterwards, run the following command to generate the client:
```
python extract-openapi.py app.main:app
```
Before installing the requirements, think about creating a virtual environment.
```
python -m venv venv
```
Activate the virtual environment. Afterwards, install the requirements and run the server.
```
pip install -r requirements.txt
```
```
uvicorn app.main:app --reload --host 0.0.0.0
```

#### For the client

Navigate to '/client' and put the following env variable in an .env file:
```
VITE_PROXY_API_URL=http://0.0.0.0:8000
```
Afterwards, install the requirements and run the server.
```
yarn install
```
```
yarn run generateAPI
```
```
yarn run dev
```

## Demo
Short drafts and a demo video can be found under my [nextcloud](https://nextcloud.sokutan.de/s/CCeWBg8jtNqiDJf).

## Questions?
For any questions or clarifications, feel free to reach out to [s.okutan@tum.de](s.okutan@tum.de).

Thank you for the opportunity, and I look forward to your feedback! 😊
