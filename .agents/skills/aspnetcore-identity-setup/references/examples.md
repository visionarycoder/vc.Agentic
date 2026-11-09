---
title: ASP.NET Core Identity Code Examples
description: Detailed code examples for Identity setup, configuration, and modern C# patterns.
doc_type: reference
status: active
last_updated: 2026-08-22
target_audience: ai
complexity: high
estimated_tokens: 600
parent_skill: aspnetcore-identity-setup
tags:
  - aspnetcore
  - identity
  - examples
  - csharp
---

# ASP.NET Core Identity Code Examples

Detailed code samples for ASP.NET Core Identity setup patterns.

## Primary Constructor with UserManager

```csharp
// Service using UserManager with dependency injection via primary constructor
public class AccountService(
    UserManager<ApplicationUser> userManager,
    SignInManager<ApplicationUser> signInManager,
    ILogger<AccountService> logger)
{
    public async ValueTask<IdentityResult> RegisterAsync(
        string email,
        string password,
        string displayName,
        CancellationToken ct)
    {
        var user = new ApplicationUser
        {
            UserName = email,
            Email = email,
            DisplayName = displayName,
            EmailConfirmed = false
        };

        var result = await userManager.CreateAsync(user, password);
        if (result.Succeeded)
        {
            logger.LogInformation("User {Email} registered successfully", email);
            var token = await userManager.GenerateEmailConfirmationTokenAsync(user);
            // Send confirmation email
        }
        else
        {
            logger.LogWarning("Registration failed for {Email}", email);
        }

        return result;
    }
}
```

## File-Scoped Identity Policy Configuration

```csharp
// Hide internal policy setup in file scope
file static class IdentityPolicies
{
    internal static void ConfigurePasswordPolicy(IdentityOptions options)
    {
        options.Password.RequiredLength = 12;
        options.Password.RequireDigit = true;
        options.Password.RequireLowercase = true;
        options.Password.RequireUppercase = true;
        options.Password.RequireNonAlphanumeric = true;
    }

    internal static void ConfigureLockoutPolicy(IdentityOptions options)
    {
        options.Lockout.DefaultLockoutTimeSpan = TimeSpan.FromMinutes(15);
        options.Lockout.MaxFailedAccessAttempts = 5;
        options.Lockout.AllowedForNewUsers = true;
    }
}
```

## Collection Expressions for Authorization Policies

```csharp
// Use collection expressions for policy rule definitions
var policies = new[]
{
    ("Admin", new[] { "admin-role" }),
    ("Editor", new[] { "editor-role", "publish-claim" }),
    ("Viewer", new[] { "viewer-role" })
};

foreach (var (name, requiredRoles) in policies)
{
    builder.Services.AddAuthorizationBuilder()
        .AddPolicy(name, policy =>
        {
            foreach (var role in requiredRoles)
            {
                policy.RequireRole(role);
            }
        });
}
```

## Custom User Model

```csharp
public class ApplicationUser : IdentityUser
{
    [MaxLength(100)]
    public required string DisplayName { get; set; }

    public DateTime CreatedAt { get; init; } = DateTime.UtcNow;

    public bool IsActive { get; set; } = true;
}
```

## DbContext Configuration

```csharp
public class ApplicationDbContext(DbContextOptions<ApplicationDbContext> options)
    : IdentityDbContext<ApplicationUser>(options)
{
    protected override void OnModelCreating(ModelBuilder builder)
    {
        base.OnModelCreating(builder);

        // Customize Identity table names
        builder.Entity<ApplicationUser>().ToTable("Users");
        builder.Entity<IdentityRole>().ToTable("Roles");
        builder.Entity<IdentityUserRole<string>>().ToTable("UserRoles");
        builder.Entity<IdentityUserClaim<string>>().ToTable("UserClaims");
        builder.Entity<IdentityUserLogin<string>>().ToTable("UserLogins");
        builder.Entity<IdentityRoleClaim<string>>().ToTable("RoleClaims");
        builder.Entity<IdentityUserToken<string>>().ToTable("UserTokens");
    }
}
```

## Program.cs Setup

```csharp
var builder = WebApplication.CreateBuilder(args);

// Add DbContext
builder.Services.AddDbContext<ApplicationDbContext>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("DefaultConnection")));

// Add Identity with custom options
builder.Services.AddIdentity<ApplicationUser, IdentityRole>(options =>
{
    // Password policy
    options.Password.RequiredLength = 12;
    options.Password.RequireDigit = true;
    options.Password.RequireUppercase = true;
    options.Password.RequireNonAlphanumeric = true;

    // Lockout policy
    options.Lockout.DefaultLockoutTimeSpan = TimeSpan.FromMinutes(15);
    options.Lockout.MaxFailedAccessAttempts = 5;
    options.Lockout.AllowedForNewUsers = true;

    // User policy
    options.User.RequireUniqueEmail = true;
    options.SignIn.RequireConfirmedEmail = true;
})
.AddEntityFrameworkStores<ApplicationDbContext>()
.AddDefaultTokenProviders();

var app = builder.Build();

// Middleware order is critical
app.UseAuthentication();  // Must come before UseAuthorization
app.UseAuthorization();

app.MapControllers();
app.Run();
```
