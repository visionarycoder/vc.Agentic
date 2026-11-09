# Generator Catalog

Complete reference of 100+ specialized Roslyn generators organized by domain.

## Service Boundary Generators

**ServiceBoundaryGenerator** — Reads a decorated class or JSON file and emits the full VBD project set for one service boundary.

**BoundaryContractGenerator** — Generates the service's public contract (interfaces + DTOs) with zero external dependencies.

**BoundaryTopologyGenerator** — Emits the service's internal component topology (Manager, Access, Engine) with correct dependency wiring.

**ContractProjectGenerator** — Creates the Contract project structure with interfaces, DTOs, and project file.

**ServiceProjectGenerator** — Creates the Service implementation project with Engines and dependency registration.

**AccessProjectGenerator** — Generates Access components for persistence, external APIs, or infrastructure dependencies.

**ManagerProjectGenerator** — Emits Manager classes that orchestrate Engines and handle cross-Engine workflows.

**EngineProjectGenerator** — Generates Engines that implement volatility-isolated business logic.

**EmulatorProjectGenerator** — Creates an emulator project for offline testing with deterministic behavior.

**SimulatorProjectGenerator** — Creates a simulator project for behavior modeling and scenario testing.

**TestProjectGenerator** — Emits the test project with regression harnesses and boundary contract tests.

## Cross-Boundary Safety Generators

**BoundaryIsolationAnalyzer** — Ensures no cross-service references violate VBD (must go through contracts only).

**ContractVersioningGenerator** — Emits versioned contracts to prevent coupling and enable independent deployment.

**BoundaryProxyGenerator** — Generates client proxies that depend only on contracts, never implementations.

**CrossBoundaryCallAnalyzer** — Detects and flags direct implementation references across boundaries.

## Domain Modeling Generators

**ValueObjectGenerator** — Emits immutable value objects with structural equality, validation, and operators.

**EntityModelGenerator** — Generates domain entities with backing fields, change tracking, and encapsulation.

**AggregateRootGenerator** — Produces aggregate roots with event application scaffolding and invariant enforcement.

**DomainEventGenerator** — Creates domain event classes and dispatch helpers for event-driven architectures.

**SpecificationPatternGenerator** — Generates specification classes from LINQ expressions for reusable query logic.

**UnionTypeGenerator** — Emits discriminated unions with exhaustive matching and type-safe access.

## Data & Persistence Generators

**EfModelGenerator** — Generates EF Core model configurations from attributes or conventions.

**EfDbContextGenerator** — Builds DbContext partials with typed DbSets, conventions, and interceptors.

**SqlQueryGenerator** — Emits parameterized SQL command builders from annotated methods.

**RepositoryGenerator** — Creates repository implementations from interface definitions with CRUD operations.

**DapperMappingGenerator** — Generates Dapper row-mappers and custom type handlers.

**MigrationScriptGenerator** — Produces SQL migration scripts from annotated schema changes.

## API & Web Generators

**MinimalApiEndpointGenerator** — Generates minimal API endpoints from annotated handler classes.

**ControllerScaffoldingGenerator** — Emits ASP.NET Core controllers from domain service interfaces.

**OpenApiContractGenerator** — Produces OpenAPI schemas from annotated DTOs with examples and descriptions.

**HttpClientFactoryGenerator** — Generates typed HttpClient wrappers using IHttpClientFactory.

**ApiClientProxyGenerator** — Builds strongly-typed REST client proxies from interface definitions.

**RouteMapGenerator** — Generates route constants and maps for ASP.NET Core routing.

## Messaging & Integration Generators

**MessageContractGenerator** — Emits immutable message contracts for queues and buses with versioning.

**MessageDispatcherGenerator** — Generates lightweight in-process dispatchers without MediatR dependency.

**MessagePipelineGenerator** — Produces request/response pipelines with compile-time wiring.

**KafkaProducerGenerator** — Generates typed Kafka producers and serializers.

**KafkaConsumerGenerator** — Builds consumer handlers with topic routing and error handling.

**EventBusRegistrationGenerator** — Auto-registers event handlers into DI container.

**GrpcClientGenerator** — Generates gRPC client wrappers with retry policies and deadlines.

**PubSubTopicGenerator** — Produces typed topic names and routing constants.

## Vue.js Generators

**VueComponentGenerator** — Generates Vue SFC components from annotated C# view models with props and emits.

**VueRouteGenerator** — Emits Vue Router route definitions from backend endpoint metadata.

**VueStoreGenerator** — Produces Pinia stores from domain models with actions and getters.

**VueFormGenerator** — Generates Vue forms with validation from DTOs and data annotations.

**VueApiClientGenerator** — Builds Axios-based typed API clients from C# interfaces.

## Angular Generators

**AngularComponentGenerator** — Generates Angular components from annotated C# view models.

**AngularServiceGenerator** — Emits Angular services from backend API interfaces with HttpClient.

**AngularModuleGenerator** — Produces Angular modules from feature definitions with routing and declarations.

**AngularRoutingGenerator** — Generates Angular routing tables from endpoint metadata.

**AngularFormGenerator** — Builds reactive forms from DTOs with validation metadata.

## MAUI Generators

**MauiPageGenerator** — Generates MAUI XAML pages from annotated view models with bindings.

**MauiViewModelGenerator** — Emits INotifyPropertyChanged view models with property change notifications.

**MauiNavigationGenerator** — Produces navigation maps and route constants for Shell navigation.

## WPF Generators

**WpfViewGenerator** — Generates WPF XAML views from annotated models with data templates.

**WpfViewModelGenerator** — Emits MVVM view models with INotifyPropertyChanged and validation.

**WpfCommandGenerator** — Produces ICommand implementations from method signatures with CanExecute logic.

## WinUI Generators

**WinUiPageGenerator** — Generates WinUI XAML pages from annotated view models.

**WinUiViewModelGenerator** — Emits MVVM view models with bindings and notifications.

**WinUiNavigationGenerator** — Produces navigation maps and page registrations.

## Azure Bicep Generators

**BicepStorageGenerator** — Generates Bicep modules for Azure Storage accounts with containers and queues.

**BicepKeyVaultGenerator** — Emits Bicep templates for Azure Key Vault instances with secrets and access policies.

**BicepAppServiceGenerator** — Produces Bicep scripts for App Service plans and apps with configuration.

**BicepSqlServerGenerator** — Generates Bicep modules for Azure SQL servers and databases.

**BicepCosmosGenerator** — Emits Bicep templates for Cosmos DB accounts and containers.

**BicepFunctionAppGenerator** — Produces Bicep modules for Azure Functions with triggers and bindings.

**BicepContainerRegistryGenerator** — Generates Bicep scripts for ACR registries.

**BicepVirtualNetworkGenerator** — Emits Bicep templates for VNets, subnets, and NSGs.

**BicepServiceBusGenerator** — Produces Bicep modules for Service Bus namespaces, queues, and topics.

**BicepEventGridGenerator** — Generates Bicep templates for Event Grid topics and subscriptions.

## Regression & Testing Generators

**RegressionCallGraphGenerator** — Generates call graphs for cross-service invocation tracking.

**RegressionTestCaseGenerator** — Emits regression test cases for service boundary interactions.

**ServiceContractReplayGenerator** — Produces replayable test harnesses for recorded API calls.

**BoundaryMockGenerator** — Generates mocks for external service boundaries with deterministic behavior.

**CrossServiceScenarioGenerator** — Builds multi-service regression scenarios from endpoint metadata.

**StatefulRegressionGenerator** — Emits state-based regression tests for workflows and aggregates.

## CLI (Spectre.Console) Generators

**CliMenuGenerator** — Generates Spectre.Console menu hierarchies from annotated classes.

**CliCommandGenerator** — Emits Spectre.Console commands from method signatures with argument parsing.

**CliPromptGenerator** — Produces typed prompts and input validators.

**CliThemeGenerator** — Generates Spectre.Console themes and styling definitions.

**CliWizardGenerator** — Builds multi-step CLI wizards from workflow definitions.

## Configuration & DI Generators

**DependencyGraphGenerator** — Emits compile-time DI graphs ensuring all services are resolvable.

**ServiceRegistrationGenerator** — Auto-registers interfaces and implementations into Microsoft.Extensions.DependencyInjection.

**OptionsBindingGenerator** — Generates strongly-typed configuration binding code for IOptions<T>.

**FeatureFlagGenerator** — Produces typed feature-flag accessors from appsettings.json.

**HostedServiceGenerator** — Creates IHostedService scaffolding from annotated classes.

**AppSettingsClassGenerator** — Generates strongly-typed settings classes from JSON.

**EnvironmentVariableGenerator** — Emits typed accessors for environment variables.

**ConnectionStringGenerator** — Produces typed connection string accessors.

**SecretsAccessorGenerator** — Generates typed secret accessors for KeyVault.

## Cross-Cutting Concern Generators

**LoggingSourceGenerator** — Emits high-performance LoggerMessage-based logging methods.

**TelemetryGenerator** — Generates OpenTelemetry spans and metrics wrappers.

**CachingDecoratorGenerator** — Builds caching decorators for service interfaces.

**RetryPolicyGenerator** — Produces Polly retry/wait policies from attributes.

**ValidationGenerator** — Generates validation logic from data annotations.

**AuditTrailGenerator** — Emits audit event classes and persistence helpers.

## Serialization Generators

**JsonSerializerContextGenerator** — Generates System.Text.Json source-gen contexts.

**XmlContractGenerator** — Emits XML serialization contracts from annotated classes.

**BinarySerializerGenerator** — Produces high-performance binary serializers.

**CsvMappingGenerator** — Generates CSV row mappers and schema definitions.

## Developer Experience Generators

**BoilerplateReductionGenerator** — Eliminates repetitive patterns via attribute-driven scaffolding.

**CommandHandlerGenerator** — Generates CQRS command handlers without MediatR.

**QueryHandlerGenerator** — Emits CQRS query handlers with typed responses.

**RequestResponseGenerator** — Produces request/response classes for custom pipelines.

**NotificationGenerator** — Generates lightweight in-process notifications.

**PipelineInterceptorGenerator** — Generates request/response interceptors for custom pipelines.
