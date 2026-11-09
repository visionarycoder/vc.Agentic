# CI/CD Integration Examples for Test Environments

This reference provides concrete examples of integrating test environment deployment into popular CI/CD platforms.

## GitHub Actions

### Multi-Environment Pipeline

```yaml
name: Deploy to Environments

on:
  push:
    branches: [main, staging, develop]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    outputs:
      image-tag: ${{ steps.meta.outputs.tags }}
    steps:
      - uses: actions/checkout@v3

      - name: Build and push Docker image
        uses: docker/build-push-action@v4
        with:
          push: true
          tags: myapp:${{ github.sha }}
          cache-from: type=registry,ref=myapp:latest

  test:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to test environment
        run: |
          kubectl set image deployment/myapp \
            myapp=myapp:${{ github.sha }} \
            --namespace=test

      - name: Run integration tests
        run: npm run test:integration
        env:
          TEST_URL: https://test.myapp.com

      - name: Run smoke tests
        run: |
          curl -f https://test.myapp.com/health || exit 1

  deploy-staging:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment:
      name: staging
      url: https://staging.myapp.com
    steps:
      - name: Deploy to staging
        run: |
          kubectl set image deployment/myapp \
            myapp=myapp:${{ github.sha }} \
            --namespace=staging

      - name: Verify deployment
        run: |
          kubectl rollout status deployment/myapp -n staging
          curl -f https://staging.myapp.com/health

  deploy-production:
    needs: deploy-staging
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://myapp.com
    steps:
      - name: Deploy to production (canary)
        run: |
          # Deploy to 10% of pods first
          kubectl set image deployment/myapp-canary \
            myapp=myapp:${{ github.sha }} \
            --namespace=production

      - name: Monitor canary metrics
        run: |
          # Wait 5 minutes, check error rates
          sleep 300
          ERROR_RATE=$(curl -s https://metrics.myapp.com/api/error-rate)
          if (( $(echo "$ERROR_RATE > 0.01" | bc -l) )); then
            echo "Error rate too high, rolling back"
            kubectl rollout undo deployment/myapp-canary -n production
            exit 1
          fi

      - name: Promote canary to full deployment
        run: |
          kubectl set image deployment/myapp \
            myapp=myapp:${{ github.sha }} \
            --namespace=production
```

Key patterns:
- Build once, deploy the same artifact to all environments
- Progressive deployment: test → staging → production
- Automated smoke tests after each deployment
- Canary deployment with automated rollback on metric degradation

## GitLab CI/CD

### Environment-Specific Deployments

```yaml
stages:
  - build
  - test
  - deploy-staging
  - deploy-production

variables:
  DOCKER_IMAGE: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA

build:
  stage: build
  script:
    - docker build -t $DOCKER_IMAGE .
    - docker push $DOCKER_IMAGE
  only:
    - main
    - staging
    - develop

test:
  stage: test
  image: $DOCKER_IMAGE
  services:
    - postgres:15
  variables:
    DATABASE_URL: postgresql://test:test@postgres:5432/testdb
  script:
    - npm install
    - npm run test
    - npm run test:integration
  coverage: '/Coverage: \d+\.\d+%/'

deploy-staging:
  stage: deploy-staging
  image: alpine:latest
  environment:
    name: staging
    url: https://staging.myapp.com
  before_script:
    - apk add --no-cache openssh
    - eval $(ssh-agent -s)
    - ssh-add <(echo "$SSH_PRIVATE_KEY_STAGING")
  script:
    - ssh deploy@staging.myapp.com "
        docker pull $DOCKER_IMAGE &&
        docker-compose -f docker-compose.staging.yml down &&
        docker-compose -f docker-compose.staging.yml up -d
      "
  only:
    - main

deploy-production:
  stage: deploy-production
  image: alpine:latest
  environment:
    name: production
    url: https://myapp.com
  before_script:
    - apk add --no-cache openssh
    - eval $(ssh-agent -s)
    - ssh-add <(echo "$SSH_PRIVATE_KEY_PROD")
  script:
    - ssh deploy@prod.myapp.com "
        docker pull $DOCKER_IMAGE &&
        docker-compose -f docker-compose.prod.yml up -d --no-deps --build app
      "
  when: manual  # Require manual approval
  only:
    - main
```

## Jenkins Pipeline

```groovy
pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "myapp:${env.BUILD_NUMBER}"
        STAGING_URL = "https://staging.myapp.com"
        PROD_URL = "https://myapp.com"
    }

    stages {
        stage('Build') {
            steps {
                script {
                    docker.build(DOCKER_IMAGE)
                }
            }
        }

        stage('Test') {
            steps {
                sh 'docker-compose -f docker-compose.test.yml up --abort-on-container-exit'
                junit 'test-results/*.xml'
            }
        }

        stage('Deploy to Staging') {
            when {
                branch 'main'
            }
            steps {
                script {
                    // Use Kubernetes plugin
                    kubernetesDeploy(
                        configs: 'k8s/staging/*.yaml',
                        kubeconfigId: 'staging-kubeconfig'
                    )
                }

                // Smoke test
                sh '''
                    for i in {1..10}; do
                        if curl -f ${STAGING_URL}/health; then
                            echo "Staging deployment successful"
                            exit 0
                        fi
                        sleep 10
                    done
                    echo "Staging health check failed"
                    exit 1
                '''
            }
        }

        stage('Approval') {
            when {
                branch 'main'
            }
            steps {
                input message: 'Deploy to production?', ok: 'Deploy'
            }
        }

        stage('Deploy to Production') {
            when {
                branch 'main'
            }
            steps {
                script {
                    kubernetesDeploy(
                        configs: 'k8s/production/*.yaml',
                        kubeconfigId: 'prod-kubeconfig'
                    )
                }

                // Monitor for 5 minutes
                sh '''
                    for i in {1..30}; do
                        ERROR_RATE=$(curl -s ${PROD_URL}/metrics | jq '.error_rate')
                        if (( $(echo "$ERROR_RATE > 0.01" | bc -l) )); then
                            echo "Error rate too high: $ERROR_RATE"
                            kubectl rollout undo deployment/myapp -n production
                            exit 1
                        fi
                        sleep 10
                    done
                '''
            }
        }
    }

    post {
        failure {
            slackSend(
                color: 'danger',
                message: "Deployment failed: ${env.JOB_NAME} ${env.BUILD_NUMBER}"
            )
        }
        success {
            slackSend(
                color: 'good',
                message: "Deployment successful: ${env.JOB_NAME} ${env.BUILD_NUMBER}"
            )
        }
    }
}
```

## CircleCI

```yaml
version: 2.1

executors:
  docker-executor:
    docker:
      - image: cimg/base:stable

jobs:
  build:
    executor: docker-executor
    steps:
      - checkout
      - setup_remote_docker
      - run:
          name: Build Docker image
          command: |
            docker build -t myapp:${CIRCLE_SHA1} .
            docker push myapp:${CIRCLE_SHA1}

  test:
    executor: docker-executor
    steps:
      - checkout
      - run:
          name: Run tests
          command: |
            docker-compose -f docker-compose.test.yml up --abort-on-container-exit
      - store_test_results:
          path: test-results

  deploy-staging:
    executor: docker-executor
    steps:
      - run:
          name: Deploy to staging
          command: |
            kubectl set image deployment/myapp \
              myapp=myapp:${CIRCLE_SHA1} \
              --namespace=staging
            kubectl rollout status deployment/myapp -n staging

  deploy-production:
    executor: docker-executor
    steps:
      - run:
          name: Deploy to production
          command: |
            kubectl set image deployment/myapp \
              myapp=myapp:${CIRCLE_SHA1} \
              --namespace=production

workflows:
  version: 2
  build-test-deploy:
    jobs:
      - build
      - test:
          requires:
            - build
      - deploy-staging:
          requires:
            - test
          filters:
            branches:
              only: main
      - hold-for-approval:
          type: approval
          requires:
            - deploy-staging
      - deploy-production:
          requires:
            - hold-for-approval
```

## Key Patterns Across All Platforms

1. **Build artifact once**: Create container image or package in build stage, reuse across all environments
2. **Progressive deployment**: Automatic promotion through test → staging, manual gate before production
3. **Automated validation**: Health checks and smoke tests after each deployment
4. **Fast feedback**: Pipeline should complete in <30 minutes to encourage frequent deployment
5. **Rollback capability**: Automated rollback on metric degradation or failed health checks
6. **Environment isolation**: Use namespaces, separate credentials, different URLs per environment
7. **Audit trail**: All deployments logged, Git commit linked to deployed version

## Monitoring Integration

Integrate monitoring into deployment pipeline:

```bash
# Post-deployment validation script
#!/bin/bash
set -e

ENV=$1
URL=$2

# Wait for deployment to stabilize
sleep 30

# Check error rate from monitoring system
ERROR_RATE=$(curl -s "https://metrics.example.com/api/v1/query?query=rate(http_errors_total{env='$ENV'}[5m])" | jq -r '.data.result[0].value[1]')

if (( $(echo "$ERROR_RATE > 0.01" | bc -l) )); then
    echo "Error rate too high: $ERROR_RATE"
    exit 1
fi

# Check latency
P95_LATENCY=$(curl -s "https://metrics.example.com/api/v1/query?query=histogram_quantile(0.95,http_request_duration_seconds{env='$ENV'})" | jq -r '.data.result[0].value[1]')

if (( $(echo "$P95_LATENCY > 1.0" | bc -l) )); then
    echo "P95 latency too high: $P95_LATENCY"
    exit 1
fi

echo "Deployment validation passed"
```

Call this script in your CI/CD pipeline after deploying to any environment.
