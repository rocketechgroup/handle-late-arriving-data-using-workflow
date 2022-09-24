# Handle Late Arriving data using workflow
Sometimes, there are delays in data pipelines which means we may not have the latest information to trigger downstream systems.
Cloud Workflow can be effective in handling those use cases and this repo has an example shows how. 

## Set up the workflow
### Set environment variables
```
export PROJECT_ID=<replace with your gcp project id>
export SA_NAME_WORKFLOW=workflow-demo
export SA_NAME_FUNC=cloud-function-demo
```

### Create service account
```
gcloud iam service-accounts create ${SA_NAME_WORKFLOW}
gcloud iam service-accounts create ${SA_NAME_FUNC}
```


### Assign permissions
> Note that for production, don't set cloud function invoker at project level but on the specific function instead or the workflow can invoke all functions in that project
1) Add permissions for workflow sa
```
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
   --member "serviceAccount:${SA_NAME_WORKFLOW}@${PROJECT_ID}.iam.gserviceaccount.com" \
   --role "roles/logging.logWriter"

gcloud projects add-iam-policy-binding ${PROJECT_ID} \
   --member "serviceAccount:${SA_NAME_WORKFLOW}@${PROJECT_ID}.iam.gserviceaccount.com" \
   --role "roles/cloudfunctions.invoker"
```
2) Add permissions for cloud functions sa
```
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
   --member "serviceAccount:${SA_NAME_FUNC}@${PROJECT_ID}.iam.gserviceaccount.com" \
   --role "roles/datastore.viewer"
```

### Deploy cloud functions
Customer Check
```
gcloud functions deploy customer_check \
    --runtime python38 \
    --trigger-http \
    --entry-point customer_check \
    --source cloud_functions/customer_check \
    --region europe-west2 \
    --security-level secure-always \
    --run-service-account ${SA_NAME_FUNC}
```

### Deploy the Workflow
```
gcloud workflows deploy workflow \
    --location=europe-west2 \
    --source=workflow.yaml \
    --service-account=${SA_NAME_WORKFLOW}@${PROJECT_ID}.iam.gserviceaccount.com
```