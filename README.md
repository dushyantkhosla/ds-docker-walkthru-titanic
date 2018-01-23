# Data Science on Docker // A step-by-step guide

### Download the Docker Image

`docker pull eadlab/ds-docker-walkthru-titanic`

### Run the Container for the first time

```
docker run -it -v (pwd):/home \
                  -p 8080:8080 \
                  -p 5000:5000 \
                  -e GIT_USER_NAME="Dushyant Khosla" \
                  -e GIT_USER_MAIL="dushyant.khosla@yahoo.com" \
                  eadlab/ds-docker-walkthru-titanic
```
- Remember to substitute your own and email for mine. 😏

### Restart a Container

- Changes made to a container (say a `conda install`) are persisted locally.
- `docker run` creates a new container, but if you want to go back into a container you exited, use `docker attach`

```
docker ps -a
docker start <container-id>
docker attach <container-id>
```

- Resume working!


### Project Structure

- Start developing your code in Jupyter, saved under `notebooks/`
    - Follow the `OSEMN` model, (Create a notebook each for **O**btaining, **S**crubbing, **Evxploring, **M**odeling and i**N**terpreting)
- Raw data goes under `data/raw/` and is **immutable**
- Move completed code under `src/`
- Keep tests in `src/tests/`
- Check out *Cookiecutter Data Science* for more detail
