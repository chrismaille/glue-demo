# External variables and his default values
ENVIRONMENT		?= "demo"
S3_BUCKET		?= "etl-artifacts-glue-"$(ENVIRONMENT)
STACK_NAME		?= "etl-demo-"$(ENVIRONMENT)
AWS_PROFILE		?= "default"
AWS_REGION		?= "us-east-1"
PACKAGE_FILE	:= ./packaged.yaml

.PHONY: show_config
# Show configuration used in SAM operations
show_config:
	@echo "ENVIRONMENT: $(ENVIRONMENT)"
	@echo "PACKAGE_TMPL: $(PACKAGE_FILE)"
	@echo "S3_BUCKET: $(S3_BUCKET)"
	@echo "STACK_NAME: $(STACK_NAME)"
	@echo "AWS_PROFILE: $(AWS_PROFILE)"
	@echo "AWS_REGION: $(AWS_REGION)"

.PHONY: package
package: show_config
	@aws --profile $(AWS_PROFILE) s3api create-bucket --bucket $(S3_BUCKET)
	@aws --profile $(AWS_PROFILE) s3api put-object \
		--bucket $(S3_BUCKET) \
		--key microservices_etl.py \
		--body ./glue_scripts/microservices_etl.py
	@aws cloudformation package \
		--template-file glue_cloudformation.yml \
		--s3-bucket $(S3_BUCKET) \
		--output-template-file $(PACKAGE_FILE)

.PHONY: install
install:
	@poetry install

.PHONY: deploy
deploy: package
	@aws cloudformation deploy \
		--stack-name $(STACK_NAME) \
		--template-file $(PACKAGE_FILE) \
		--capabilities CAPABILITY_IAM

.PHONY: remove
remove:
	@aws cloudformation delete-stack \
		--stack-name $(STACK_NAME)
	@aws --profile $(AWS_PROFILE) s3 rb s3://$(S3_BUCKET) --force
	@aws --profile $(AWS_PROFILE) s3 rb s3://microservices-parket-glue-demo --force
