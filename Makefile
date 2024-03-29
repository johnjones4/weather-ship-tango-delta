PROJECT=$(shell basename $(shell pwd))
TAG=ghcr.io/johnjones4/${PROJECT}
VERSION=$(shell date +%s)

.PHONY: ui

info:
	echo ${PROJECT} ${VERSION}

container:
	docker build -t ${TAG} ./server
	docker push ${TAG}:latest
	docker image rm ${TAG}:latest

ui:
	cd ui && npm install
	cd ui && npm run build
	tar zcvf ui.tar.gz ./ui/build
	git tag ${VERSION}
	git push origin ${VERSION}
	gh release create ${VERSION} ui.tar.gz --generate-notes

ci: container ui
