
run-megalinter:
	@docker run --rm --name megalint -v $(shell pwd):/tmp/lint busybox rm -rf /tmp/lint/megalinter-reports
	@docker run --rm --name megalint -v $(shell pwd):/tmp/lint -e MARKDOWN_SUMMARY_REPORTER=true oxsecurity/megalinter:v8
