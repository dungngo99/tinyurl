DOCKER_REGISTRY=654654166580.dkr.ecr.us-east-1.amazonaws.com

mongo=mongo
shortenurl_backend=shortenurl-backend
nginx=nginx

region=us-east-1
account=654654166580

mongo_repo=${DOCKER_REGISTRY}/${mongo}
echo ${mongo_repo}
shortenurl_backend_repo=${DOCKER_REGISTRY}/${shortenurl_backend}
echo ${shortenurl_backend_repo}
nginx_repo=${DOCKER_REGISTRY}/${nginx}
echo ${nginx_repo}

mongo_image_id=$1
echo ${mongo_image_id}
shortenurl_image_id=$2
echo ${shortenurl_image_id}
nginx_image_id=$3
echo ${nginx_image_id}

aws ecr get-login-password --region ${region} | docker login --username AWS --password-stdin ${account}.dkr.ecr.${region}.amazonaws.com

aws ecr create-repository --repository-name ${mongo} --region ${region}
aws ecr create-repository --repository-name ${shortenurl_backend} --region ${region}
aws ecr create-repository --repository-name ${nginx} --region ${region}

docker tag ${mongo_image_id} ${mongo_repo}
docker tag ${shortenurl_image_id} ${shortenurl_backend_repo}
docker tag ${nginx_image_id} ${nginx_repo}

docker push ${mongo_repo}
docker push ${shortenurl_backend_repo}
docker push ${nginx_repo}

# aws ecr delete-repository --repository-name ${mongo} --region ${region} --force
# aws ecr delete-repository --repository-name ${shortenurl_backend} --region ${region} --force
# aws ecr delete-repository --repository-name ${nginx} --region ${region} --force