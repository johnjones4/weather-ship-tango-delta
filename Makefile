PROJECT=$(shell basename $(shell pwd) | awk '{print tolower($0)}')
TAG=ghcr.io/johnjones4/${PROJECT}
VERSION=$(shell date +%s)

info:
	echo ${PROJECT} ${VERSION}

container:
	docker build -t ${TAG} ./server
	docker push ${TAG}:latest
	docker image rm ${TAG}:latest

ui:
	cd ui && npm install
	cd ui && npm build
	tar zcvf ui.tar.gz ./ui/build
	git tag ${VERSION}
	git push origin ${VERSION}
	gh release create ${VERSION} ui.tar.gz

ci: container ui
