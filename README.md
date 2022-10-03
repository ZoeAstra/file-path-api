# file-path-api

The file-path-api RESTful API can be started by calling `.\run.ps1` in a Windows PowerShell environment, or `bash run.sh` in a Mac/Linux environment. The script takes an absolute path as an argument, builds a docker image, and passes the path (or the default "testdir" included in the project, if no other path is specified) along to docker compose to use as a bind mount.

This API is documented in the Swagger/OpenAPI 3.0.3 format, located in the `apidocs.yml` file in the root directory. The YAML file has also been converted to JSON, and served up as a Swagger UI static webpage, which can be found at [http://localhost:5000/static/index.html](http://localhost:5000/static/index.html) when the website is running.

Some of the tests are kind of wonky. Comparing the results is hard when sometimes the order of the result changes, as well as for some reason it refusing to properly do POSTs, PUTs, and DELETEs. All methods work perfectly in postman, so it must be something in the tests. If I were willing to spend more time on this, I'd find a more robust/easier way of testing API results. 

Since it may help, I did include an export of my postman tests for this project, `file-path-api.postman_collection.json`, in the root directory of this project.

I probably spent longer than I should have on this, about 8 hours, though a fair bit of that was due to my unfamiliarity with creating APIs in Flask, several confusing bugs, as well as being a bit (or a lot) of a perfectionist.
