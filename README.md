# Webhook explorer

This is a simple project aimed to listen to any incoming request on any path and display out all info about them. This has been incredibly useful
for me to see what requests do other services and apis send back.

# Without setting up

The site [webhook-explorer.mlexps.com](https://webhook-explorer.mlexps.com) is free to use for the general public. Just configure the callback to
be something like `webhook-explorer.mlexps.com/some/path`, then go to the main page to see the list of recent requests.

# Setting up

Setting up is quite easy with docker compose. Just run `./deploy_prod`. This will use a pre-built image and start the server up at port 9015. For
development, run `./deploy_dev` instead. This will mount the /code folder, so that all file changes on the host will be reflected within the container
immediately, without having to rebuild the image.

