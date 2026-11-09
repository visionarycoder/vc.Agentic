---
metadata-version: "1.0.0"
title: "EF Core ORM Project"
description: "Preserve scoped source guidance for efcore-orm-project."
document-type: "reference"
repository: "vc.Agentic"
language: "Standard Technical English"
updated: "2026-11-08"
---

# EF Core ORM Project

Scaffold Entity Framework Core ORM projects following the Vertical Slice Design (VBD) pattern with clean separation of entities, configurations, and context.

## Project Structure

```
<ProjectName>.Data/
  Entities/
    Customer.cs
    Order.cs
    OrderItem.cs
  Configurations/
    CustomerConfiguration.cs
    OrderConfiguration.cs
    OrderItemConfiguration.cs
  <DatabaseName>Context.cs
  <ProjectName>.Data.csproj
```

**Naming:** Context class is `<DatabaseName>Context` (e.g., `SalesContext`, `InventoryContext`) derived from `DbContext`.

## Entity Organization

**Location:** `Entities/` subfolder

Entities are clean domain models without EF-specific attributes:

```csharp
public class Order
{
    public int Id { get; set; }
    public string OrderNumber { get; set; }
    public DateTime OrderDate { get; set; }
    public decimal TotalAmount { get; set; }
    public int CustomerId { get; set; }

    // Navigation properties
    public Customer Customer { get; set; }
    public ICollection<OrderItem> OrderItems { get; set; }
}
```

**Why clean entities:** Separates domain concerns from persistence. Entities focus on business logic; configuration handles database mapping.

## Configuration Organization

**Location:** `Configurations/` subfolder

Each entity gets one configuration class implementing `IEntityTypeConfiguration<TEntity>`:

```csharp
public class OrderConfiguration : IEntityTypeConfiguration<Order>
{
    public void Configure(EntityTypeBuilder<Order> builder)
    {
        builder.ToTable("Orders", schema: "sales");

        builder.HasKey(o => o.Id);
        builder.Property(o => o.Id).UseIdentityColumn();

        builder.Property(o => o.OrderNumber)
            .IsRequired()
            .HasMaxLength(20);

        builder.Property(o => o.TotalAmount)
            .HasPrecision(18, 2)
            .IsRequired();

        builder.HasOne(o => o.Customer)
            .WithMany(c => c.Orders)
            .HasForeignKey(o => o.CustomerId)
            .OnDelete(DeleteBehavior.Restrict);
    }
}
```

**Key patterns:**
- Explicit table names and schemas
- Always specify decimal precision (default varies by provider)
- Configure relationships from one side only (avoid duplicate configuration)
- Explicit delete behavior (`Restrict` or `Cascade` - never rely on defaults)
- Use `IsRequired()` for non-nullable columns
- Set `HasMaxLength()` for string columns to avoid `nvarchar(max)`

## DbContext Structure

**Location:** Root of ORM project

```csharp
public class SalesContext : DbContext
{
    public SalesContext(DbContextOptions<SalesContext> options)
        : base(options)
    {
    }

    public DbSet<Customer> Customers { get; set; }
    public DbSet<Order> Orders { get; set; }
    public DbSet<OrderItem> OrderItems { get; set; }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);

        // Apply all configurations from assembly
        modelBuilder.ApplyConfigurationsFromAssembly(typeof(SalesContext).Assembly);
    }
}
```

**Why `ApplyConfigurationsFromAssembly`:** Automatically discovers and applies all `IEntityTypeConfiguration<T>` classes. No manual registration needed when adding new entities.

## Service Registration

In the consuming service or API project:

```csharp
// Program.cs or Startup.cs
builder.Services.AddDbContext<SalesContext>(options =>
    options.UseSqlServer(
        builder.Configuration.GetConnectionString("SalesDatabase")));
```

**Lifetime:** `AddDbContext` registers with `Scoped` lifetime by default - one instance per request. This is correct for web applications.

## Injecting DbContext into Services

```csharp
public class OrderService
{
    private readonly SalesContext _context;

    public OrderService(SalesContext context)
    {
        _context = context;
    }

    public async Task<Order> GetOrderAsync(int id)
    {
        return await _context.Orders
            .Include(o => o.OrderItems)
            .FirstOrDefaultAsync(o => o.Id == id);
    }
}
```

**Service lifetime:** Services consuming DbContext should be `Scoped` or `Transient`, never `Singleton`. Singleton services cannot inject scoped dependencies.

**For background services or long-lived contexts:** Use `IDbContextFactory<TContext>`:

```csharp
// Registration
builder.Services.AddDbContextFactory<SalesContext>(options =>
    options.UseSqlServer(connectionString));

// Usage in background service
public class OrderProcessor : BackgroundService
{
    private readonly IDbContextFactory<SalesContext> _contextFactory;

    public OrderProcessor(IDbContextFactory<SalesContext> contextFactory)
    {
        _contextFactory = contextFactory;
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        while (!stoppingToken.IsCancellationRequested)
        {
            await using var context = await _contextFactory.CreateDbContextAsync(stoppingToken);
            // Process orders with this context
            await Task.Delay(TimeSpan.FromMinutes(5), stoppingToken);
        }
    }
}
```

## Key Configuration Patterns

### Composite Keys

```csharp
builder.HasKey(oi => new { oi.OrderId, oi.ProductId });
```

### Indexes

```csharp
builder.HasIndex(o => o.OrderNumber).IsUnique();
builder.HasIndex(o => new { o.CustomerId, o.OrderDate });
```

### Value Conversions

```csharp
builder.Property(o => o.Status)
    .HasConversion<string>()
    .HasMaxLength(30);
```

### Shadow Properties

```csharp
builder.Property<DateTime>("CreatedAt")
    .HasDefaultValueSql("GETUTCDATE()");
```

### Owned Types

```csharp
builder.OwnsOne(o => o.ShippingAddress, a =>
{
    a.Property(x => x.Street).HasColumnName("ShippingStreet").HasMaxLength(200);
    a.Property(x => x.City).HasColumnName("ShippingCity").HasMaxLength(100);
});
```

### Global Query Filters

```csharp
builder.HasQueryFilter(o => !o.IsDeleted);
```

## Performance Essentials

**Read-only queries:** Use `AsNoTracking()` when not modifying entities:

```csharp
var orders = await _context.Orders
    .AsNoTracking()
    .Where(o => o.CustomerId == customerId)
    .ToListAsync();
```

**N+1 prevention:** Use `Include()` for related data:

```csharp
var order = await _context.Orders
    .Include(o => o.OrderItems)
    .Include(o => o.Customer)
    .FirstOrDefaultAsync(o => o.Id == id);
```

**Split queries** for multiple collections to avoid cartesian explosion:

```csharp
var order = await _context.Orders
    .Include(o => o.OrderItems)
    .Include(o => o.Payments)
    .AsSplitQuery()
    .FirstOrDefaultAsync(o => o.Id == id);
```

## Migration Workflow

Migrations belong in the ORM project:

```bash
# Add migration
dotnet ef migrations add InitialCreate --project <ProjectName>.Data

# Update database
dotnet ef database update --project <ProjectName>.Data
```

**Startup project:** If migrations are run from a different project (e.g., API), specify both:

```bash
dotnet ef migrations add InitialCreate \
  --project <ProjectName>.Data \
  --startup-project <ProjectName>.Api
```

## Common Pitfalls

**Decimal precision:** Always specify `HasPrecision(18, 2)` - defaults vary by provider and cause silent truncation.

**Delete behavior:** Explicitly set `OnDelete(DeleteBehavior.Restrict)` or `DeleteBehavior.Cascade` - provider defaults differ.

**Relationship configuration:** Configure each relationship from one side only. Configuring both ends causes conflicts.

**String lengths:** Always set `HasMaxLength()` - default is `nvarchar(max)` which prevents indexing.

**Change tracking:** Don't forget `AsNoTracking()` for read-only queries - change tracking has memory overhead.

**Concurrent access:** DbContext is not thread-safe. Never share instances across threads or store in Singleton services.

## VBD Integration

When following Vertical Slice Design patterns referenced in the user's request:

- ORM project is a separate class library
- Service projects inject the DbContext via constructor
- Each feature/slice can have its own query methods but shares the same context
- Repository pattern is optional - direct DbContext injection is often cleaner
- Keep business logic in services, not in configuration classes
