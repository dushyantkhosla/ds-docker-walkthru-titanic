# Data Science on Docker // A step-by-step guide

### Download the Docker Image

`docker pull eadlab/ds-docker-walkthru-titanic`

### Run the Container

```
docker run -it -v (pwd):/home \
                  -p 8080:8080 \
                  -p 5000:5000 \
                  -e GIT_USER_NAME="Dushyant Khosla" \
                  -e GIT_USER_MAIL="dushyant.khosla@yahoo.com" \
                  eadlab/ds-docker-walkthru-titanic
```

- Remember to substitute your own and email for mine. 😏
- Remember to `git push` the changes that you make.

### Project Structure

- Start developing your code in Jupyter, saved under `notebooks/`
    - Follow the `OSEMN` model, (Create a notebook each for **O**btaining, **S**crubbing, **Evxploring, **M**odeling and i**N**terpreting) 
- Raw data goes under `data/raw/` and is **immutable**
- Move completed code under `src/`
- Keep tests in `src/tests/`
- Check out *Cookiecutter Data Science* for more detail
