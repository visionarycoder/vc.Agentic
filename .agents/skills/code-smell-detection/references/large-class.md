---
title: Large Class Smell Reference
doc_type: reference
status: active
last_updated: 2026-09-21
parent_skill: code-smell-detection
---

# Large Class Smell

## Description

Class grows until it carries too many responsibilities, members, and public entry points.

## Detection Signals

- Class >500 lines
- Class >10 public methods
- Fields cluster into separate responsibility groups
- Methods touch different subsets of fields

## Why This Is Problematic

- Responsibility boundaries blur
- Small changes trigger broad regression risk
- Tests grow large and slow
- Reuse drops because consumers pull in unrelated behavior

## Remediation

Use **Extract Class** or **Extract Subclass**.

```csharp
// ❌ BEFORE: One class owns authentication, profile updates, and reporting
public sealed class UserManager
{
    private readonly IUserRepository _users;
    private readonly IPasswordHasher _passwordHasher;
    private readonly IReportWriter _reportWriter;

    public Task<bool> ValidateCredentialsAsync(string email, string password) => throw new NotImplementedException();
    public Task ResetPasswordAsync(Guid userId) => throw new NotImplementedException();
    public Task ChangePasswordAsync(Guid userId, string currentPassword, string newPassword) => throw new NotImplementedException();
    public Task UpdateDisplayNameAsync(Guid userId, string displayName) => throw new NotImplementedException();
    public Task UpdateTimezoneAsync(Guid userId, string timezone) => throw new NotImplementedException();
    public Task UpdateNotificationPreferenceAsync(Guid userId, bool enabled) => throw new NotImplementedException();
    public Task<string> ExportActivityReportAsync(Guid userId) => throw new NotImplementedException();
    public Task<string> ExportBillingReportAsync(Guid userId) => throw new NotImplementedException();
    public Task<string> ExportUsageReportAsync(Guid userId) => throw new NotImplementedException();
    public Task LockUserAsync(Guid userId) => throw new NotImplementedException();
    public Task UnlockUserAsync(Guid userId) => throw new NotImplementedException();
}

// ✅ AFTER: Focused classes own focused responsibilities
public sealed class UserAuthenticationService
{
    private readonly IUserRepository _users;
    private readonly IPasswordHasher _passwordHasher;

    public Task<bool> ValidateCredentialsAsync(string email, string password) => throw new NotImplementedException();
    public Task ResetPasswordAsync(Guid userId) => throw new NotImplementedException();
    public Task ChangePasswordAsync(Guid userId, string currentPassword, string newPassword) => throw new NotImplementedException();
    public Task LockUserAsync(Guid userId) => throw new NotImplementedException();
    public Task UnlockUserAsync(Guid userId) => throw new NotImplementedException();
}

public sealed class UserProfileService
{
    private readonly IUserRepository _users;

    public Task UpdateDisplayNameAsync(Guid userId, string displayName) => throw new NotImplementedException();
    public Task UpdateTimezoneAsync(Guid userId, string timezone) => throw new NotImplementedException();
    public Task UpdateNotificationPreferenceAsync(Guid userId, bool enabled) => throw new NotImplementedException();
}

public sealed class UserReportService
{
    private readonly IUserRepository _users;
    private readonly IReportWriter _reportWriter;

    public Task<string> ExportActivityReportAsync(Guid userId) => throw new NotImplementedException();
    public Task<string> ExportBillingReportAsync(Guid userId) => throw new NotImplementedException();
    public Task<string> ExportUsageReportAsync(Guid userId) => throw new NotImplementedException();
}
```

## Verification

Test: Measure line count, public method count, and responsibility clusters before and after extraction.
Pass: Each extracted class owns one responsibility area. Public API size drops per class. Tests pass.

## Reference

[Large Class - Refactoring Guru](https://refactoring.guru/smells/large-class)
