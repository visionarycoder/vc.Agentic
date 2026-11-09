# Infrastructure as Code Patterns for Test Environments

This reference covers specific IaC patterns and tooling choices for managing test environment infrastructure.

## Tool Selection: Terraform vs Pulumi vs CloudFormation

**Terraform** — Multi-cloud, declarative HCL syntax, largest ecosystem of providers. Best for: teams managing infrastructure across multiple cloud providers, organizations with existing Terraform expertise, need for extensive community modules.

**Pulumi** — Multi-cloud, uses real programming languages (Python, TypeScript, Go), enables unit testing infrastructure code. Best for: development teams that prefer familiar languages over DSLs, need for complex logic and conditionals, organizations wanting to test infrastructure code like application code.

**CloudFormation** — AWS-native, deep AWS integration, no separate state management. Best for: AWS-only infrastructure, teams wanting to avoid external dependencies, need for AWS-specific features not yet in Terraform.

Recent 2026 benchmarks show Terraform and Pulumi have comparable deployment performance (avg 45-60s for typical multi-tier apps), while CloudFormation averages 120s+ due to internal orchestration overhead.

## Environment Parameterization Pattern

Avoid duplicating IaC code per environment. Instead, use a single template with environment-specific variables:

```python
# Pulumi example - Python
import pulumi
import pulumi_aws as aws

config = pulumi.Config()
env = pulumi.get_stack()  # 'dev', 'staging', 'prod'

# Environment-specific sizing
instance_sizes = {
    'dev': 't3.small',
    'staging': 't3.medium',
    'prod': 't3.xlarge'
}

app_server = aws.ec2.Instance('app-server',
    instance_type=instance_sizes[env],
    ami=config.require('ami_id'),
    tags={'Environment': env}
)
```

This pattern ensures environment parity (same infrastructure shape) while allowing practical differences (resource sizing, replica counts).

## State Management

Terraform and Pulumi maintain state files tracking what infrastructure exists. Critical practices:

- **Remote state storage**: Store state in S3/GCS/Azure Blob, never in Git
- **State locking**: Use DynamoDB/Consul to prevent concurrent modifications
- **Separate state per environment**: Staging and production should have independent state files to prevent accidental cross-environment changes
- **Backup state regularly**: State corruption can make infrastructure unmanageable

## Module Organization

```
infrastructure/
├── modules/
│   ├── networking/      # VPC, subnets, security groups
│   ├── compute/         # EC2, ECS, Lambda
│   ├── data/            # RDS, DynamoDB, S3
│   └── monitoring/      # CloudWatch, Datadog integration
├── environments/
│   ├── dev/
│   │   ├── main.tf
│   │   └── variables.tfvars
│   ├── staging/
│   │   ├── main.tf
│   │   └── variables.tfvars
│   └── prod/
│       ├── main.tf
│       └── variables.tfvars
└── README.md
```

Modules contain reusable infrastructure patterns. Environment directories instantiate those modules with environment-specific values.

## Secrets and Sensitive Configuration

Never hardcode secrets in IaC. Use secrets managers:

```hcl
# Terraform - reference existing secret
data "aws_secretsmanager_secret_version" "db_password" {
  secret_id = "staging/database/password"
}

resource "aws_db_instance" "main" {
  password = data.aws_secretsmanager_secret_version.db_password.secret_string
  # ... other config
}
```

Secrets should be created and rotated outside IaC (manual or separate automation), then referenced by IaC.

## Drift Detection and Remediation

Infrastructure drift occurs when manual changes bypass IaC. Detect with:

```bash
# Terraform
terraform plan -detailed-exitcode
# Exit code 2 means drift detected

# Pulumi
pulumi preview --diff
```

Run drift detection daily via CI/CD. When detected:
1. Investigate why manual change was made
2. Update IaC to reflect desired state
3. Apply IaC to reconcile

Never ignore drift — it compounds and eventually makes IaC unreliable.

## Testing Infrastructure Code

Pulumi enables unit testing infrastructure logic:

```python
import unittest
import pulumi

class TestInfrastructure(unittest.TestCase):
    @pulumi.runtime.test
    def test_instance_type_correct(self):
        def check_instance(args):
            urn, instance_type = args
            self.assertEqual(instance_type, 't3.medium')

        return pulumi.Output.all(app_server.urn, app_server.instance_type).apply(check_instance)
```

For Terraform, use tools like Terratest (Go) to deploy to temporary environments and validate:

```go
func TestStagingEnvironment(t *testing.T) {
    terraformOptions := &terraform.Options{
        TerraformDir: "../environments/staging",
    }
    defer terraform.Destroy(t, terraformOptions)
    terraform.InitAndApply(t, terraformOptions)

    instanceID := terraform.Output(t, terraformOptions, "instance_id")
    aws.GetEc2InstanceIds(t, region)  // Verify instance exists
}
```

## GitOps Pattern

Store IaC in Git. Use CI/CD to automatically apply changes:

1. Developer opens PR with infrastructure change
2. CI runs `terraform plan` or `pulumi preview`, posts diff as PR comment
3. Team reviews infrastructure change alongside code review
4. On merge, CD pipeline runs `terraform apply` or `pulumi up`
5. Infrastructure change is deployed, Git commit is source of truth

This creates an audit trail and prevents manual infrastructure changes.

## Handling Database Migrations

Database schema changes are the riskiest part of deployment. Pattern:

1. **Backward-compatible migrations first**: Add new columns/tables without removing old ones
2. **Deploy application code that uses both old and new schema**
3. **Migrate data** from old to new structure
4. **Deploy application code that uses only new schema**
5. **Remove old schema** in a later migration

Never bundle schema removal with schema addition in the same deployment.

For test environments, maintain migration scripts in version control and run them automatically as part of environment provisioning:

```yaml
# GitHub Actions example
- name: Run database migrations
  run: |
    export DATABASE_URL=${{ secrets.STAGING_DB_URL }}
    npm run migrate
```

## Environment-as-a-Service (EaaS)

Modern pattern: Developers request environments via API/CLI, infrastructure is provisioned automatically.

```bash
# Example CLI workflow
$ envctl create --template web-app --branch feature-123
Provisioning environment feature-123...
Environment ready: https://feature-123.staging.example.com
Database: feature-123-db.internal

# Automatic teardown after 7 days or on branch merge
```

Implement with: Kubernetes namespaces + Helm charts, or cloud-native solutions like AWS App Runner, Google Cloud Run.

Benefits: Eliminates environment contention, ensures clean state per test, reduces costs (ephemeral environments are short-lived).

## Multi-Region Considerations

If production is multi-region, staging should be too (at least 2 regions). Test:
- Cross-region data replication
- Failover procedures
- Region-specific configuration

Use IaC to define regions as a list variable:

```hcl
variable "regions" {
  type    = list(string)
  default = ["us-east-1", "eu-west-1"]
}

resource "aws_instance" "app" {
  for_each      = toset(var.regions)
  provider      = aws[each.value]
  instance_type = var.instance_type
  # ... other config
}
```

This ensures regional infrastructure stays in sync.
