# JWST Hack

This is a personal project that is intended to simplify the process of getting
interesting images from JWST data.

---

## Goals

The main goals of the project are:

- Gain experience in working with FastAPI and pydantic
- Gain experience in image processing
- Have fun trying to create some interesting images from scientific data
- Provide a fun API for people to quickly find interesting images from JWST.

---

## Getting started

To run the project for development it is fairly simple.

### Apple Silicon macOS

If you use Apple Silicon and conda as your dependency management tool follow these instructions

1. Create a new environment, for example: `conda create python=3.10`
2. Ensure that you have the conda forge channel available/default
3. Install the conda requirements `conda install --file requirements.conda.txt`
4. Install the pip requirements `pip install -r requirements.pip.txt`
5. Run the server `uvicorn app.main:app --reload`

### Everyone else

For anyone else use these instructions. Please note that these are not tested and will likely only work on
some linux based systems. If you find they are wrong and send corrections I will update this section.

1. Create a new environment, for example `python3 -m venv <name-of-virtualenv>`
2. Activate environment `<name-of-virtualenv>/bin/activate`
3. Install the requirements `pip install -r requirements.txt`
4. Run the server `uvicorn app.main:app --reload`
