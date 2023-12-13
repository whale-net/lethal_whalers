wget -O openapi_2.json https://thunderstore.io/api/docs/?format=openapi

docker run --rm -v $PWD:/local openapitools/openapi-generator-cli generate -i /local/openapi_2.json -g python -o /local/out/python_client

# validate passes
docker run --rm -v $PWD:/local openapitools/openapi-generator-cli validate -i /local/openapi_2.json

# only models, runs on unmodified
docker run --rm -v $PWD:/local openapitools/openapi-generator-cli generate -i /local/openapi_2.json -g python -o /local/out/python_client --global-property models




# wget https://repo1.maven.org/maven2/org/openapitools/openapi-generator-cli/6.6.0/openapi-generator-cli-6.6.0.jar -O openapi-generator-cli.jar

# mkdir -p ~/bin/openapitools
# curl https://raw.githubusercontent.com/OpenAPITools/openapi-generator/master/bin/utils/openapi-generator-cli.sh > ~/bin/openapitools/openapi-generator-cli
# chmod u+x ~/bin/openapitools/openapi-generator-cli
# export PATH=$PATH:~/bin/openapitools/

# curl -X 'POST' \
#   'https://converter.swagger.io/api/convert' \
#   -H 'accept: application/json' \
#   -H 'Content-Type: application/json' \
#   -d @openapi_2.json \
#   > openapi_3.json

# openapi-python-client generate --path ./openapi_3.json

# for now remove
rm openapi_2.json # openapi_3.json
