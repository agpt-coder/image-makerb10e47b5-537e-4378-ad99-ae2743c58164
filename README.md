---
date: 2024-04-12T15:15:38.083957
author: AutoGPT <info@agpt.co>
---

# image maker

Based on the information gathered, your task involves creating images from input text utilizing advancements in AI technology. Specifically, you'll be leveraging the capabilities of sophisticated text-to-image AI models like DALL·E 2 by OpenAI, Google's Imagen, Midjourney, and Stable Diffusion by Stability AI. These models are distinguished by their ability to generate high-resolution images accurately reflecting the nuances of given textual descriptions. They offer improved fidelity, customization options, and accessibility compared to earlier models, enabling the creation of detailed and creative images based on specific themes, styles, or subjects of interest expressed in text. This project would involve integrating one or more of these AI technologies to develop a system that interprets textual inputs and produces corresponding images, capturing the specified details, themes, and styles as closely as possible.

## What you'll need to run this
* An unzipper (usually shipped with your OS)
* A text editor
* A terminal
* Docker
  > Docker is only needed to run a Postgres database. If you want to connect to your own
  > Postgres instance, you may not have to follow the steps below to the letter.


## How to run 'image maker'

1. Unpack the ZIP file containing this package

2. Adjust the values in `.env` as you see fit.

3. Open a terminal in the folder containing this README and run the following commands:

    1. `poetry install` - install dependencies for the app

    2. `docker-compose up -d` - start the postgres database

    3. `prisma generate` - generate the database client for the app

    4. `prisma db push` - set up the database schema, creating the necessary tables etc.

4. Run `uvicorn project.server:app --reload` to start the app

## How to deploy on your own GCP account
1. Set up a GCP account
2. Create secrets: GCP_EMAIL (service account email), GCP_CREDENTIALS (service account key), GCP_PROJECT, GCP_APPLICATION (app name)
3. Ensure service account has following permissions: 
    Cloud Build Editor
    Cloud Build Service Account
    Cloud Run Developer
    Service Account User
    Service Usage Consumer
    Storage Object Viewer
4. Remove on: workflow, uncomment on: push (lines 2-6)
5. Push to master branch to trigger workflow
